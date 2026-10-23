---
name: fluent2-web
description: Fluent 2 design rules, component behavior and review checklists for web apps (React, TSX, HTML, CSS, design tokens; Fluent UI React v9 or your own components). Use this skill whenever a task touches a web UI - building, styling or reviewing text, number, money, time, date, search, combo box and tag-picker fields, buttons, checkboxes, switches, tabs, menus, tooltips, dialogs, drawers, popovers, message bars, toasts and progress; keyboard handling (Tab, Enter, Esc, arrows, F6), focus-visible and states (hover, pressed, disabled, invalid); spacing, typography, color and contrast, motion and prefers-reduced-motion; forced colors and screen readers (ARIA names, roles, live regions); UI copy and error messages; AI suggestion panels, drafts and agent actions with correct AI labeling; and Testing Library, Playwright and axe tests of these. Trigger even if the user never says Fluent or design system. Not for Avalonia, WPF, WinUI or MAUI work.
---

# Fluent 2 for the web

This skill turns Microsoft's Fluent 2 guidance (design system, Fluent UI React v9 source and documentation) into rules, numbers, checklists and test patterns for web apps. It is an independent, paraphrased summary with a source link on each rule. It does not replace the project's own design brief. Examples target React 19 with TypeScript, plain CSS or Fluent UI React v9; [fluent-ui-react-notes.md](references/fluent-ui-react-notes.md) lists the Fluent UI React v8 to v9 names, changed behavior and pitfalls.

The skill serves two kinds of project: those built on Fluent UI React v9 (`@fluentui/react-components`), and those with their own React, HTML and CSS components that borrow Fluent's values and behavior. Each reference says which path a statement applies to when they differ.

## The one rule that comes first

If the project has a design brief, a token file (`index.css`, `tokens.css`, a theme object) or an established style, its values win over every Fluent value in this skill. Fluent supplies the behavior and the fallback numbers. When the project deliberately differs from Fluent, record the deviation with its reason in the project (template in [foundations.md](references/foundations.md), section 11), so later edits do not undo it and reviewers can tell "differs on purpose" from "differs by mistake".

Values carry a tag: **Fluent default** (from Fluent guidance or source; starting point only), **Derived** (a recommendation built on Fluent principles or a web standard; Microsoft does not state it) and **(derived, not verified)** (derived and unconfirmed; check before relying on it). Parser rules for time, date, number and money fields are Derived; Fluent defines the principles, not the masks.

## How to work

1. **Find the project's own truth first.** Look for a design brief (`design.md`, `DESIGN.md`, `docs/design*`), a token file or `:root` custom properties, a `FluentProvider` theme, `index.css`, a component folder and existing tests. Note heights, radii, colors, font and any recorded deviations. Extend what exists; do not start a second style system.
2. **Identify the component or topic and open the matching reference file** (table below). Read only what the task needs.
3. **Implement or fix** using the project's tokens. Prefer native platform features (`<dialog>`, the Popover API, `<input>` types, `<details>`) over re-implementations unless the reference says why not. Use Fluent defaults only where the project is silent, and say which origin a number has when you report it.
4. **Walk the checklist** at the end of the reference section. Every checklist item names how to verify it: a test, a screenshot, an axe run or a search in the code. Do the check, do not just tick the box.
5. **Test the behavior**, not only the look: keyboard paths, focus, parsers, states, names and roles. Patterns for Testing Library, Playwright and axe are in [web-mapping.md](references/web-mapping.md). State what you did not verify.
6. **Report briefly:** what changed, which rule it follows, which checks ran, which were not possible, and any new deviation to record.

When reviewing existing UI, report findings as a table with columns Finding, Rule (reference file and section), Fix, and mark each as "differs from Fluent, recorded" (fine), "differs from Fluent, not recorded" (decide and record) or "violates a rule" (fix).

## Where to look

- Read [foundations.md](references/foundations.md) when the task involves spacing, grid, type ramp, colors, contrast, shadows, motion durations and curves, radius, tokens, light and dark themes, breakpoints, recording deviations.
- Read [inputs.md](references/inputs.md) when the task involves any input: text, multi-line, search, number, money, time, date, combo box, select, tag picker; field anatomy; states; Tab, click, Esc, Enter and arrow behavior; parsers; native input types versus text fields.
- Read [buttons-and-selection.md](references/buttons-and-selection.md) when the task involves buttons, split buttons, links, checkbox, radio, switch, slider; choosing a selection control; target sizes.
- Read [navigation.md](references/navigation.md) when the task involves tabs (also icon-only), navigation pane, breadcrumb, menus and context menus, toolbar and overflow, tooltips, shortcut lists.
- Read [dialogs-and-messages.md](references/dialogs-and-messages.md) when the task involves dialogs, drawers, popovers, message bars, toasts, progress, spinners, skeletons; choosing the right surface; native `<dialog>` and the Popover API.
- Read [data-display.md](references/data-display.md) when the task involves lists, tables, data grids, cards, avatars, badges, accordions, dividers, images.
- Read [content-design.md](references/content-design.md) when the task involves labels, titles, button text, error text, empty states, tooltip text, number and date formats.
- Read [accessibility.md](references/accessibility.md) when the task involves keyboard model, focus order and restoration, landmarks and F6 regions, skip links, shortcuts, screen readers and accessible names (axe scan), contrast, forced colors, reduced motion, text scaling, WCAG 2.2 checks.
- Read [responsible-ai.md](references/responsible-ai.md) when the task involves AI output, drafts, assistants, agents, disclosure, consent, feedback, review scoring.
- Read [web-mapping.md](references/web-mapping.md) when the task involves writing CSS or TSX for states and precedence (cascade layers, specificity), tokens as custom properties or `@fluentui/tokens`, the field underline, transitions and the reduced-motion override, behaviors (roving tabindex, toolbar overflow, tooltip defaults, F6 regions, shortcut registry), typed fields with parsers, focus code and tab order walks, ARIA names and live regions, and tests with Testing Library, Playwright and axe and their limits.
- Read [fluent-ui-react-notes.md](references/fluent-ui-react-notes.md) when code written for Fluent UI React v8 does not compile or behave in v9, a Griffel style does not apply, a dialog or popover misbehaves in the top layer, or you want the list of known pitfalls.

Most UI tasks need two or three of these. A new input component, for example, needs [inputs.md](references/inputs.md), [accessibility.md](references/accessibility.md) and [web-mapping.md](references/web-mapping.md).

## Rules at a glance

Foundations (details in [foundations.md](references/foundations.md))

- Use a 4 px grid with 2, 6 and 10 as nudges. A single grid keeps rhythm predictable.
- Type: nothing under 12 px Regular or 14 px Semibold; sentence case; no bold or italic as the only meaning carrier. Use `rem` so the page reflows at 200 percent zoom.
- Contrast: 4.5:1 for text, 3:1 for large text, icons and field borders; measure per state and theme. Fluent's own neutral stroke is about 1.5:1 on light and relies on a darker bottom edge, so do not assume a border token passes.
- Color comes from tokens (custom properties or `@fluentui/tokens`), never hex, named colors or inline shadow colors in components. Hard-coded colors break dark and forced-colors modes.
- Motion explains state changes: hover and color about 100 ms, enter about 200 ms, exit shorter; transitions touch color, opacity and transform only; `prefers-reduced-motion` and an in-app setting zero everything, and a test proves it on every page.

Inputs (details in [inputs.md](references/inputs.md))

- Every input sits in a field with a `<label for>` above, optional help, and error under it, all wired with `aria-describedby`; the error names the problem and the way out. Placeholders are examples, never labels, because they vanish on input.
- Tab into a text field puts the caret at the end (the browser default); Tab into time, date, number, money and search fields selects all, because those are replaced, not edited.
- Typing is filtered, commit happens on Enter or blur: parse, validate, write the display format back. Never overwrite or clear invalid input silently, and never reformat while typing. After a failed commit the component must not keep the old value unnoticed.
- Esc ladder: close the open listbox, then restore the changed field, then close the dialog. Native `<dialog>` and the Popover API handle Esc themselves, so the field layer must stop propagation when it consumed the key. Enter commits the field and submits the form in single-line fields only.
- Money uses a decimal string or integer minor units, never a float; `type="number"` is wrong for money (use `inputmode="decimal"`); rejects extra fraction digits instead of rounding; an empty field is not zero.
- Dependent fields (end after start) recompute after commit, not during typing.

Controls (details in [buttons-and-selection.md](references/buttons-and-selection.md), [navigation.md](references/navigation.md), [dialogs-and-messages.md](references/dialogs-and-messages.md), [data-display.md](references/data-display.md))

- One primary button per layout; labels are verbs; confirmation buttons answer the dialog title ("Delete", "Cancel"), never "OK" or "Yes". Buttons inside forms declare `type="button"` unless they submit.
- Icon-only controls have an accessible name and a tooltip that also shows on focus; the `title` attribute alone is not a tooltip. Disabled controls that must explain themselves use `aria-disabled` so they stay focusable.
- Radio groups are one tab stop with arrows that move and select (native radios do this). Switches act instantly; a form with a Save button uses checkboxes.
- Tab strips and toolbars never wrap; the overflow goes into a menu that the keyboard reaches. Tabs follow the ARIA tabs pattern with a roving tabindex.
- Dialogs use `<dialog>` with `showModal()` or Fluent UI `Dialog`: background inert, initial focus never on a destructive action, Esc cancels, focus returns to the invoker on close.
- Field problems stay at the field, persistent conditions go into a message bar (`role="status"` or `role="alert"`), short confirmations into a toast, decisions before data loss into an alert dialog.
- A clickable card is a link or a button, not a `div` with `onClick`. Tables use `<th scope>` and `aria-sort`.

Content (details in [content-design.md](references/content-design.md))

- Say what failed, why, and offer two ways forward; no technical detail in the main text. Avoid direction words ("above") and "click here". One term per concept.
- Format numbers, dates and amounts through `Intl` with the project's locale rules, not English habits.

Accessibility (details in [accessibility.md](references/accessibility.md))

- WCAG 2.2 AA is the bar, including target size (24 by 24 CSS px minimum), focus not obscured, dragging alternatives and redundant entry.
- The keyboard is a first-class path: tab order equals DOM order (CSS `order` and grid placement do not change it, so check the DOM with a tab walk test), groups are one tab stop, landmarks and F6 switch regions, shortcuts appear in tooltips and `aria-keyshortcuts`.
- Every element has an accessible name; run axe over every route as the role that sees the most pages; fields expose required, help and error; messages use live regions (assertive for errors).
- Verify with a screen reader pass (NVDA or Narrator with Chrome or Edge) and record it; do not rely on axe alone.

AI features (details in [responsible-ai.md](references/responsible-ai.md))

- Every AI output carries a visible AI mark and the approved disclaimer; drafts are never sent without a review step; side effects can be declined and undone; each AI function has its own off switch; failures offer a way without AI; anything that prepares or proposes without being asked is an agent.

## Fluent default values at a glance

These are fallbacks. The project's tokens win. Values come from the Fluent UI React v9 token and component source; the reference files name the file for each value.

| Item | Fluent default |
| --- | --- |
| Grid | 4 px; nudges 2, 6, 10 |
| Field and button height | 32 (small 24, large 40) |
| Control radius | 4 (`borderRadiusMedium`); overlays 8 (`borderRadiusXLarge`); cards 4 to 8 |
| Stroke | 1 px border (`strokeWidthThin`); 2 px focus ring or underline (`strokeWidthThick`) |
| Body text | 14/20 Regular (`fontSizeBase300`, `lineHeightBase300`); caption 12/16; subtitle 20/28 Semibold |
| Font | Segoe UI Variable, Segoe UI, system-ui, sans-serif (`fontFamilyBase`) |
| Hover or color transition | 100 ms (`durationFaster`), curve `0.33, 0, 0.67, 1` (`curveEasyEase`) |
| Enter or exit curves | `0, 0, 0, 1` (`curveDecelerateMax`) and `1, 0, 1, 1` (`curveAccelerateMax`) |
| Input underline | grows 200 ms on focus, leaves 50 ms |
| Tooltip | delay 250 ms, max width 240, gap 4, 12/16 text |
| Menu item | min height 32, width 138 to 300, shadow 16 |
| Dialog | padding 24, width up to 600, shadow 64 |
| Toast | 7 s without action, at most 4 stacked, 16 px apart, shadow 8 |
| Message bar | min height 36, radius 4, icon 20 |
| Progress bar | 2 px (large 4); show only for operations over 1 s |
| Contrast | text 4.5:1, large text and non-text 3:1 |
| Target size | 24 by 24 CSS px minimum (WCAG 2.5.8), 32 px Fluent control height |

## Limits and honesty

- Fluent 2 pages were read through summaries; numbers are most reliable where the Fluent UI React source states the same value. The reference files say where a value is derived or unverified.
- Not covered or not verified: visual comparison against rendered Fluent UI React components, Mica or Acrylic materials, Fluent UI React Native, Web Components (`@fluentui/web-components`), right-to-left layouts, printing, the Microsoft Writing Style Guide in full, Segoe Fluent Icons licensing.
- Examples target React 19, TypeScript, Vite, Testing Library, Playwright and axe-core; adapt names for other frameworks. Fluent UI React v9 names and props change between minor versions; confirm each against the installed version with the type definitions in `node_modules/@fluentui/react-components`.
- jsdom has no layout and no CSS transitions, so sizes, overflow, motion and focus rings need Playwright; Playwright is not a screen reader, so name and role checks via axe do not replace a screen reader pass.
- Fluent is a Microsoft design system; this skill is an independent summary and is not affiliated with or endorsed by Microsoft.
