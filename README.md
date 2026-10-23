# fluent2-web

Based on Microsoft's **[Fluent 2 design system](https://fluent2.microsoft.design/)**, the design language behind Windows, Microsoft 365 and Teams, and on the open source [Fluent UI React v9](https://react.fluentui.dev/) components.

A skill for Claude Code and Claude.ai that teaches Claude to build and review web UIs the way Fluent 2 describes them: component behavior, states, keyboard handling, accessibility (WCAG 2.2 AA), content design, motion, and responsible AI patterns, with checklists you can verify and test patterns for Testing Library, Playwright and axe.

It is the web sibling of [fluent2-avalonia-skill](https://github.com/vompa/fluent2-avalonia-skill), derived from the same rules. It serves two kinds of project: apps built on Fluent UI React v9 (`@fluentui/react-components`), and apps with their own React, HTML and CSS components that borrow Fluent's values and behavior. Typical triggers: "build a time field", "review my input styles", "add an AI draft panel", "why can't I tab through this form".

The skill never replaces your own design brief. If a project has a brief or tokens, those values win; Fluent values are the fallback, and deliberate deviations are recorded with a reason.

The skill is Markdown only: it runs no code, sends nothing and fetches nothing. See [PRIVACY.md](PRIVACY.md).

## Install

**With the `skills` CLI** (works for Claude Code and other agents):

```bash
npx skills add vompa/fluent2-web-skill --skill fluent2-web
```

Add `-g` to install it for all your projects instead of the current one.

**As a Claude Code plugin** (this repository is also a plugin marketplace):

```bash
claude plugin marketplace add vompa/fluent2-web-skill
claude plugin install fluent2-web@vompa-web-skills
```

Inside a session, `/plugin marketplace add vompa/fluent2-web-skill` and `/plugin install fluent2-web@vompa-web-skills` do the same. The skill then runs as `/fluent2-web:fluent2-web` and triggers on its own when a task matches its description.

**By hand:** copy the folder `fluent2-web/` into `.claude/skills/` inside your project (shared with the team through the repository) or into `~/.claude/skills/` (available in all your projects).

```bash
cp -r fluent2-web ~/.claude/skills/
```

**For Claude.ai**, zip the folder as a `.skill` package (the archive root contains the `fluent2-web/` folder) and upload it in the skills settings. Packaging details follow Anthropic's skill documentation.

## Structure

```text
.claude-plugin/
  plugin.json                 Claude Code plugin manifest (points at fluent2-web/)
  marketplace.json            marketplace entry so the repository can be added with one command
fluent2-web/
  SKILL.md                    entry point: when it applies, how to work, rules at a glance
  references/
    foundations.md            layout, type, color, elevation, motion, shape, tokens, themes, deviations
    inputs.md                 field anatomy, states, behavior matrix, native input types, parsers
    buttons-and-selection.md  buttons, links, checkbox, radio, switch, slider, target sizes
    navigation.md             tabs, navigation pane, breadcrumb, menus, toolbar overflow, tooltips
    dialogs-and-messages.md   dialog and drawer, popover, message bar, toast, progress
    data-display.md           lists, tables and data grids, cards, avatars, badges, accordions
    content-design.md         UI text, error messages, formats
    accessibility.md          WCAG 2.2, keyboard, focus, landmarks, screen readers, contrast, motion
    responsible-ai.md         AI disclosure, control, agents, review rubric
    web-mapping.md            Fluent concepts as CSS, TSX, tokens, behaviors and tests
    fluent-ui-react-notes.md  Fluent UI React v8 to v9 names, changed behavior, pitfalls
  evals/evals.json            three realistic test prompts
scripts/validate.py           structure and link checks for contributors (standard library only)
```

Claude reads `SKILL.md` first and opens a reference file only when the task needs it.

## Check

```bash
python scripts/validate.py
```

The script checks the frontmatter, the `SKILL.md` length, that referenced files exist, that local Markdown links and anchors resolve, and that `evals/evals.json` is well formed. It makes no network requests. The same check runs in GitHub Actions on every push.

## Sources and relationship to Microsoft

The content is an independent, paraphrased summary built from public sources: the [Fluent 2 design system](https://fluent2.microsoft.design), the [Fluent UI React v9 documentation](https://react.fluentui.dev/) and the open source [Fluent UI](https://github.com/microsoft/fluentui) repository (token and component source), plus the web standards the rules rest on: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), the [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) and [MDN](https://developer.mozilla.org/). Each rule links to its source in the reference file where it appears.

This project is not affiliated with or endorsed by Microsoft. Fluent, Segoe, Windows and Microsoft 365 are trademarks of Microsoft Corporation. Microsoft texts are paraphrased, not copied. Values marked "Derived" are recommendations of this skill, not Microsoft rules, and values marked "derived, not verified" were not checked against a running app or a source.

## License

MIT, see [LICENSE](LICENSE).
