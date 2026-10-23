#!/usr/bin/env python3
"""Validate the fluent2-web skill folder.

Checks (standard library only, no network access):
  * SKILL.md has YAML frontmatter with `name` and `description`; the name equals the folder name
    and the description is at most 1024 characters.
  * SKILL.md is shorter than 500 lines.
  * Every references/*.md file named in SKILL.md exists.
  * Every local Markdown link in every .md file resolves (files and, for .md targets, anchors).
  * Every reference-style link `[text][label]` has a definition in the same file.
  * Reference files longer than 300 lines have a table of contents near the top.
  * evals/evals.json is valid JSON in the expected shape.

Exit code 0 when everything passes, 1 when any error is found. Warnings do not fail the run.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "fluent2-web"
SKILL_NAME = "fluent2-web"
MAX_SKILL_LINES = 500
MAX_DESCRIPTION_CHARS = 1024
TOC_THRESHOLD_LINES = 300

INLINE_LINK = re.compile(r"(?<!\!)\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFERENCE_USE = re.compile(r"\[(?P<text>[^\]]+)\]\[(?P<label>[^\]]+)\]")
REFERENCE_DEF = re.compile(r"^\s{0,3}\[(?P<label>[^\]]+)\]:\s*(?P<target>\S+)", re.MULTILINE)
REFERENCE_PATH = re.compile(r"references/[A-Za-z0-9_.-]+\.md")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
CODE_FENCE = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """Remove fenced and inline code so that brackets in code are not read as links."""
    without_fences = CODE_FENCE.sub("", text)
    return INLINE_CODE.sub("", without_fences)


def github_slug(heading: str) -> str:
    """Approximate GitHub's heading anchor algorithm."""
    heading = re.sub(r"`", "", heading.strip().lower())
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return heading.replace(" ", "-")


def anchors_of(path: Path) -> set[str]:
    text = CODE_FENCE.sub("", path.read_text(encoding="utf-8"))
    seen: dict[str, int] = {}
    anchors: set[str] = set()
    for match in HEADING.finditer(text):
        slug = github_slug(match.group(2))
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def is_external(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)) or target.startswith("//")


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        return None, text
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, text[match.end():]


def check_skill_md(errors: list[str]) -> str:
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"missing file: {skill_md.relative_to(REPO_ROOT)}")
        return ""
    text = skill_md.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(text)
    if frontmatter is None:
        errors.append("SKILL.md: frontmatter block (--- ... ---) not found")
    else:
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if not name:
            errors.append("SKILL.md: frontmatter field 'name' is missing")
        elif name != SKILL_DIR.name:
            errors.append(f"SKILL.md: name '{name}' does not equal folder name '{SKILL_DIR.name}'")
        if name and name != SKILL_NAME:
            errors.append(f"SKILL.md: name '{name}' should be '{SKILL_NAME}'")
        if not description:
            errors.append("SKILL.md: frontmatter field 'description' is missing")
        elif len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"SKILL.md: description has {len(description)} characters, limit is {MAX_DESCRIPTION_CHARS}"
            )
    line_count = len(text.splitlines())
    if line_count >= MAX_SKILL_LINES:
        errors.append(f"SKILL.md: {line_count} lines, must be under {MAX_SKILL_LINES}")
    for ref in sorted(set(REFERENCE_PATH.findall(text))):
        if not (SKILL_DIR / ref).is_file():
            errors.append(f"SKILL.md: referenced file does not exist: {ref}")
    return text


def check_links(path: Path, errors: list[str], warnings: list[str]) -> None:
    raw = path.read_text(encoding="utf-8")
    text = strip_code(raw)
    rel = path.relative_to(REPO_ROOT).as_posix()

    definitions = {m.group("label").lower(): m.group("target") for m in REFERENCE_DEF.finditer(raw)}
    used_labels: set[str] = set()

    for match in REFERENCE_USE.finditer(text):
        label = match.group("label").lower()
        used_labels.add(label)
        if label not in definitions:
            errors.append(f"{rel}: reference link [{match.group('text')}][{match.group('label')}] has no definition")
    for label in sorted(set(definitions) - used_labels):
        warnings.append(f"{rel}: link definition [{label}] is never used")

    targets = [(m.group("target"), "inline") for m in INLINE_LINK.finditer(text)]
    targets += [(target, "definition") for target in definitions.values()]
    for target, kind in targets:
        if is_external(target):
            continue
        file_part, _, anchor = target.partition("#")
        if not file_part:
            if anchor and anchor not in anchors_of(path):
                errors.append(f"{rel}: anchor #{anchor} not found ({kind} link)")
            continue
        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            errors.append(f"{rel}: local link does not resolve: {target} ({kind} link)")
        elif anchor and resolved.suffix == ".md" and anchor not in anchors_of(resolved):
            errors.append(f"{rel}: anchor #{anchor} not found in {file_part}")


def check_toc(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if len(text.splitlines()) <= TOC_THRESHOLD_LINES:
        return
    head = "\n".join(text.splitlines()[:40])
    if not re.search(r"^#{2,3}\s+Contents\s*$", head, re.MULTILINE):
        errors.append(f"{path.relative_to(REPO_ROOT).as_posix()}: over {TOC_THRESHOLD_LINES} lines but no 'Contents' section near the top")


def check_evals(errors: list[str]) -> None:
    evals_path = SKILL_DIR / "evals" / "evals.json"
    if not evals_path.is_file():
        errors.append("missing file: fluent2-web/evals/evals.json")
        return
    try:
        data = json.loads(evals_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"evals.json: invalid JSON: {exc}")
        return
    if data.get("skill_name") != SKILL_NAME:
        errors.append(f"evals.json: skill_name must be '{SKILL_NAME}'")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals.json: 'evals' must be a non-empty list")
        return
    seen_ids: set[int] = set()
    for item in evals:
        for key in ("id", "prompt", "expected_output", "files"):
            if key not in item:
                errors.append(f"evals.json: eval is missing '{key}': {item.get('id', '?')}")
        if item.get("id") in seen_ids:
            errors.append(f"evals.json: duplicate id {item.get('id')}")
        seen_ids.add(item.get("id"))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not SKILL_DIR.is_dir():
        print(f"ERROR: skill folder not found: {SKILL_DIR}")
        return 1

    check_skill_md(errors)

    markdown_files = sorted(
        path
        for path in REPO_ROOT.rglob("*.md")
        if not any(part in {".git", "node_modules"} or part.endswith("-workspace") for part in path.parts)
    )
    for path in markdown_files:
        check_links(path, errors, warnings)
    for path in sorted((SKILL_DIR / "references").glob("*.md")):
        check_toc(path, errors)

    check_evals(errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    checked = len(markdown_files)
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s), {checked} markdown file(s) checked")
        return 1
    print(f"OK: {checked} markdown file(s) checked, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
