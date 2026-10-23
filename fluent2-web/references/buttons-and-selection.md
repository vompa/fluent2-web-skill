# Buttons, links and selection controls

Read this file when you style or review buttons, split buttons, menu buttons, toggle buttons, links, checkboxes, radio buttons, switches or sliders on the web: which type to use, how many primaries, size and spacing defaults, labels, keyboard behavior, states and the HTML that makes them accessible. Values tagged Fluent default give way to the project's brief or tokens; see `foundations.md`.

Two audiences use this file. **Path A** projects use Fluent UI React v9 (`Button`, `ToggleButton`, `SplitButton`, `MenuButton`, `CompoundButton`, `Link`, `Checkbox`, `Radio`, `RadioGroup`, `Switch`, `Slider`, wrapped in `Field` where there is a label). **Path B** projects have their own React, HTML and CSS components and borrow Fluent's values and behavior. A rule says which path it addresses when they differ. Tags: **Fluent default** (from Fluent guidance or source), **Derived** (a recommendation on Fluent principles and web standards), **(derived, not verified)**.

## Contents

1. [Buttons](#1-buttons)
2. [Links](#2-links)
3. [Checkbox](#3-checkbox)
4. [Radio buttons](#4-radio-buttons)
5. [Switch](#5-switch)
6. [Slider](#6-slider)
7. [Which selection control](#7-which-selection-control)
8. [Checklists](#8-checklists)
9. [Sources](#9-sources)

## 1. Buttons

Types (Fluent, Path A prop `appearance`): `secondary` (the default: surface plus border), `primary` (brand filled, transparent border), `outline`, `subtle` (no surface), `transparent`; `shape` rounded, square, circular; variants `SplitButton`, `MenuButton` (arrow), `CompoundButton` (title plus description), `ToggleButton` (on/off). Map your project's names onto these once, for example "ghost" to subtle. Path B: one `<button>` element with a class per appearance; do not build buttons from `<div>` or `<a>` without `href`. ([Button][f2-button], [Button source][gh-button])

Markup rules (Derived from the HTML standard):

- Use a real `<button>`. It brings focus, Enter and Space activation and the right role for free. A `<div role="button">` needs `tabindex="0"`, Enter and Space handlers and a disabled state you write yourself.
- `type="button"` on every button that is not the form's submit button. The default type inside a `<form>` is `submit`, so an unmarked button submits the form (and an unmarked button is the Enter target if it comes first). Fluent's `Button` sets `type="button"` itself unless it renders an `<a>` (verified in `useButton.ts`); own components must do the same. ([MDN button][mdn-button])
- The accessible name is the visible text. If the visible label and `aria-label` differ, the label must contain the visible text (WCAG 2.5.3 label in name).
- Icon-only buttons have no text, so they need a name: `aria-label="Delete"` (or visually hidden text) and a tooltip with the same words. Path A: `<Tooltip content="Delete" relationship="label"><Button icon={<DeleteRegular />} /></Tooltip>`; `relationship="label"` makes the tooltip the accessible name, `description` adds a description. The icon itself is `aria-hidden`. ([Tooltip][f2-tooltip])

Hierarchy and placement:

- One primary button per layout. If more than two buttons share the same importance, make all of them neutral. Because two primaries tell the user nothing about what is expected. ([Button][f2-button])
- Many secondary actions: use outline, subtle or transparent variants. Place the primary at the top or left (right in right-to-left layouts; use logical CSS such as `margin-inline-start` and `flex-direction` so `dir="rtl"` works). ([Button][f2-button])
- WinUI: show one or two buttons at once; for more actions prefer a selection control plus one command button. ([WinUI buttons][wl-buttons])
- Dialog order (WinUI): the primary action ("do it") on the left, a second "do it" in the middle, the safe action (close, cancel) at the far right. With several decision buttons the order is affirm, negative, cancel. A lone button sits at the right in a dialog, at the left on a page, and at the right inside a container such as a toast, flyout or list row. A project may keep its own order in form footers and still follow WinUI in confirmation dialogs; record it. The DOM order is the tab order, so write the buttons in the order you want them focused, not only the order you want them drawn (do not reorder visually with `order` or `flex-direction: row-reverse` without checking Tab). ([WinUI buttons][wl-buttons], [WinUI dialogs][wl-dialogs], [WCAG 2.4.3][wcag-243])

Sizes (Fluent default, source, verified): medium padding 5/12, min width 96, text 14/20 Semibold, border 1, radius 4, icon 20 with 6 spacing; small padding 3/8, min width 64, 12/16 Regular; large padding 8/16, 16/22 Semibold, icon 24 (the icon variants use a slightly smaller vertical padding to keep the height); icon-only squares 24, 32, 40. WinUI: min width 120 for short text, at most about 26 characters of text. A dense brief may use a single 32 px height and 16 px icons; if you do, keep one height for buttons and fields and note it. ([Button source][gh-button], [WinUI buttons][wl-buttons])

Target size: WCAG 2.2 (success criterion 2.5.8, level AA) asks for a pointer target of at least 24 by 24 CSS px, or enough space around smaller ones. Fluent's small icon-only button is exactly 24 and its default height is 32, so Fluent defaults pass; a custom 20 px icon button does not. For touch layouts aim for 44 (the AAA criterion 2.5.5 and platform guidance). Check with the computed bounding box, not the icon size. Derived. ([WCAG 2.5.8][wcag-258])

Labels:

- Use a verb in the active voice, sentence case, no final punctuation. Creating: "New" plus the object ("New item"); in a menu the button says "New" and the entries name the object. Adding existing things: "Add" plus the type. Multi-step: "Next" and "Back". ([Button][f2-button])
- Finishing: "Done" for plain confirmation, "Finish" when a selection is applied by the button, "Close" for informational notices and in error messages (not "OK"), "Got it" for important notices, "Hide" for permanent dismissal. "Cancel" discards changes; "Close" changes nothing; do not pair a close "x" with a "Close" button. ([Button][f2-button])
- In dialogs the button text answers the title question concretely: "Delete" and "Cancel" for "Delete this file?", not "Yes" and "No". ([Button][f2-button], [Dialog][f2-dialog])
- Saving: ideally automatic; otherwise "Save" with feedback by toast or message bar. ([Button][f2-button])
- Keep text short; if a label exceeds about 26 characters, stack the buttons or wrap. ([WinUI buttons][wl-buttons])

States and motion:

- States: rest, hover (one step stronger), pressed (two steps), focus, disabled; Fluent animates only color, border and background for 100 ms (`durationFaster`) with the easy-ease curve `cubic-bezier(0.33,0,0.67,1)`, no scale, and `0.01ms` under `prefers-reduced-motion: reduce` (verified). A press scale (0.97 in 100 ms) is an optional brand touch; remove it under reduced motion. Focus is drawn on `:focus-visible` only: an inner 1 px ring in `colorStrokeFocus2` plus a transparent 2 px outline for forced colors (verified); use `:focus-visible`, not `:focus`, so mouse clicks do not leave a ring. ([Button source][gh-button], [MDN :focus-visible][mdn-focusvisible])
- Disabled versus `aria-disabled`: a native `disabled` button leaves the tab order, gets no mouse events (so no tooltip and no hover explanation in most browsers) and is announced as unavailable. When the button must explain itself, keep it focusable: Path A `disabledFocusable` renders `aria-disabled="true"`, keeps the button in the tab order and blocks Enter, Space and click (verified in `useARIAButtonProps.ts`); Path B sets `aria-disabled="true"` and ignores activation in the handler (and styles it like disabled). A tooltip then says why and, if possible, when it becomes available ("Available once a name is entered"). Keep the click target inert, not hidden. Use plain `disabled` when the reason is obvious and no help is needed. Submit buttons that are disabled until the form is valid hide the reason from keyboard users; prefer an enabled button that shows the errors on click (Derived). ([Button][f2-button], [Tooltip][f2-tooltip], [MDN aria-disabled][mdn-ariadisabled])
- Toggle button: rest is off, selected is on; Path A `ToggleButton` with `checked`, which exposes `aria-pressed`; Path B `<button aria-pressed="true|false">`. Show the state by text or an icon as well as color (for example a check mark at the start). The label stays the same when the state changes ("Bold", not "Bold on"), or the name and `aria-pressed` contradict each other. ([Button][f2-button], [MDN aria-pressed][mdn-ariapressed])
- Split button: the main action is the label, further actions are in the menu and do not repeat the main one. Path A `SplitButton` with a `menuButton` slot; Path B two adjacent buttons, the second with `aria-haspopup="menu"`, `aria-expanded` and the name "More options for Save". Inner corners are 0 where the halves meet. On touch both halves open the menu (WinUI). `MenuButton` shows only the menu and carries the same `aria-haspopup` and `aria-expanded`. ([Button][f2-button], [WinUI buttons][wl-buttons], [MDN aria-expanded][mdn-ariaexpanded])
- Keyboard: Enter and Space activate a native button (Enter on keydown, Space on keyup); Tab order follows the DOM; show shortcuts in the tooltip and expose them with `aria-keyshortcuts`. A shortcut must not fire while the user types in a field. ([WinUI keyboard][wl-keyboard], [WinUI tooltips][wl-tooltips], [MDN aria-keyshortcuts][mdn-keyshortcuts])
- Busy state: while an action runs, keep the button focusable with `aria-disabled="true"` and `aria-busy="true"` and ignore further clicks, instead of removing the focus target (Derived). Announce completion through a live region or message bar.
- Contrast: text 4.5:1 and icons 3:1 in every state (WCAG 1.4.3 and 1.4.11); the border has no requirement when the fill carries the identity; disabled is exempt. Check text on a gradient primary at both ends. ([Button][f2-button], [WCAG 1.4.11][wcag-1411])

## 2. Links

- Types: standard (brand color, most accessible), subtle, inverted, on-brand. Path A `Link` has `appearance="default" | "subtle"`, `inline` (always underlined, for links inside running text), `disabled` and `disabledFocusable`. Underline on hover and pressed; focus draws a double underline (verified in the Link source). Keep at least two visual cues that it is interactive (color plus underline): inside a paragraph a link that differs only by color fails WCAG 1.4.1 unless it has 3:1 contrast against the surrounding text and a non-color cue on hover and focus. ([Link][f2-link], [Link source][gh-link], [WCAG 1.4.1][wcag-141])
- Link text works without context: never "click here", no bare "Learn more" without a subject, no raw URL. If the visual text must be short, add context with `aria-label` that starts with the visible text, or visually hidden text. Announce when a link opens a new window or tab ("opens in a new tab", also in the name or description) and add `rel="noopener"` with `target="_blank"` (modern browsers imply it, keep it for older ones). ([Link][f2-link], [WCAG 2.4.4][wcag-244])
- Use a link for navigation, a button for an action. Because assistive technology announces them differently, and a link supports "open in new tab", copy address and middle click, which a button does not. `<a href>` needs a real `href`; an `<a>` without one has no link role and no focus. Path A `Link` renders `<a>` when `href` is set and `<button>` otherwise (verified), so passing no `href` gives a button that looks like a link. ([Link][f2-link], [HTML anchor][mdn-anchor])
- A button styled as a link keeps the behavior and semantics of a button (it activates with Space as well and does not navigate); use it for in-page actions, such as "Show more", and give it a verb. In a single-page app, route changes still use `<a href>` with the router's link component, so the address is real. Derived.
- A skip link ("Skip to content") is an `<a href="#main">` that appears on focus; see `accessibility.md`.

## 3. Checkbox

- Size and parts (Fluent default, verified): box 16 (`size="large"`: 20), radius 2 (`borderRadiusSmall`; `shape="circular"` gives a round box), border in the accessible neutral stroke (`colorNeutralStrokeAccessible`), checked fills with the brand compound background and an inverted check, mixed shows a dash, hover darkens the border, disabled dims border and mark. The click target is the box plus 8 px each side (a hidden `<input type="checkbox">` of box width + 16 stretched over the box, verified), so the target is 32 px wide in the medium size; make the whole row clickable including the label (a `<label>` around or `for` the input). Label to the right with a small gap, 14/20 (`labelPosition="before"` puts it on the left). ([Checkbox source][gh-checkbox])
- Path B markup: a real `<input type="checkbox">` visually restyled (hide the native control with `appearance: none` or draw the box with a sibling and `:checked` plus `:focus-visible`), never a `<div>` with a click handler. Keep the native input in the DOM and focusable; `opacity: 0` over the box with the same size keeps hit-testing and the accessible state. Derived from the HTML standard.
- A checkbox does not apply a change immediately; it records a choice that is submitted. Use it for single yes/no or for a group of at most about seven options. Space toggles it, Enter does not (in a form Enter submits). ([Checkbox][f2-checkbox], [WinUI checkboxes][wl-checkbox])
- Parent checkbox with child items: the mixed state is set by code only, never by the user directly; children are indented (WinUI example 24). Text at most two lines. Do not place two groups side by side; give each group a group label with `<fieldset><legend>` (or `role="group"` and `aria-labelledby`). Path A: `checked="mixed"` (verified: Fluent sets the input's `indeterminate` property); Path B: set `input.indeterminate = true` from script, since there is no HTML attribute for it, and it is exposed as `aria-checked="mixed"`. When the user clicks a mixed parent, define the result (usually "check all"). ([Checkbox][f2-checkbox], [WinUI checkboxes][wl-checkbox], [MDN indeterminate][mdn-indeterminate])
- Phrase the label as the statement the check makes true, and avoid negations: "Notify guests by email", not "Do not send email". Because a ticked negative is a double negative. ([Checkbox][f2-checkbox])
- A "select all" box over a list uses the mixed state for partial selection. Name it ("Select all rows"), and update a live region when the count changes if rows are many. Derived.

## 4. Radio buttons

- Circle 16 with a hit area of 32 like the checkbox (verified); exactly one option; preselect the most sensible one and place it first; vertical layout preferred (`layout="vertical"`, also `horizontal` and `horizontal-stacked` in Path A); about five options at most (WinUI: more than eight belongs in a combobox or select); offer "None" where it makes sense. Path A: `RadioGroup` (renders `role="radiogroup"` with a shared generated `name`, and `required` is passed to each radio, verified) containing `Radio value label`, inside a `Field label="..."` for the group heading. Path B: native `<input type="radio" name="x">` elements in a `<fieldset><legend>`; the shared `name` is what creates the group. ([Radio group][f2-radiogroup], [Radio source][gh-radio], [WinUI radio buttons][wl-radio])
- Labels are short, wrap rather than truncate, sentence case, no final punctuation; the group heading has no colon. Longer explanations go into a subtitle (full sentences) linked with `aria-describedby`, or an info label. ([Radio group][f2-radiogroup])
- Keyboard: native radio groups give you the whole model for free. Tab lands on the selected radio, or on the first if none is selected, so the group is one tab stop; arrow keys move focus and check the next radio ("selection follows focus"); Space checks the focused radio if it is not checked. Screen readers announce name, role, state and position ("2 of 4"). Differences from WinUI: browsers wrap at the ends (the Down arrow on the last option goes to the first, which the ARIA radio group pattern also describes) and there is no Ctrl+Arrow "focus without selecting". Accept the web behavior; do not fight it. ([MDN radio][mdn-radio], [APG radio group][apg-radio], [WinUI radio buttons][wl-radio], [WinUI keyboard][wl-keyboard])
- Path B with custom radios (`role="radio"` on a `<div>`): you must implement the roving tab stop (`tabindex="0"` on the checked item, `-1` on the others), arrow keys that move and check, and `aria-checked`; avoid this unless the native input cannot be styled to fit, which it almost always can. Derived from the APG.
- Radios in a group must not be disabled one by one in a way that leaves the group without a tab stop; a disabled selected radio is skipped by Tab, so check that the group stays reachable. Derived (test it).

## 5. Switch

- Track 40 x 20, thumb 18 with a 2 px gap (`size="small"`: 32 x 16, thumb 14), pill radius, 200 ms (`durationNormal`) easy-ease transition of the thumb; on state brand fill and white thumb (Fluent default, verified). The hit area is the track plus 8 px each side. ([Switch source][gh-switch])
- Markup: Path A `Switch label="..."` renders `<input type="checkbox" role="switch">` (verified); Path B the same: a native checkbox with `role="switch"` and `checked` as the state, plus a label. Do not use `aria-checked` on a native input (the checked state already maps); `aria-checked` is for non-native `role="switch"` elements. Space toggles. The accessible name is the label; the on or off words ("On", "Off") are optional visual text and do not replace it. Derived from the ARIA switch role. ([MDN switch][mdn-switch], [APG switch][apg-switch])
- A switch acts immediately. For settings that need a Save or Apply step, use a checkbox. Because users expect a switch to take effect when flipped. If the change is a network call, show the pending state (`aria-busy`) and undo the switch when it fails, and say so in a message. ([Switch][f2-switch], [WinUI toggles][wl-toggles])
- Label: one or two words, a noun (or a verb in its positive state), never "turn on/off", never a question. Place it above or beside the switch, close to it (`labelPosition="above" | "before" | "after"` in Path A). Extra explanation goes into a tooltip or a description linked with `aria-describedby`. WinUI: replace the default On/Off text only when needed, with one word. ([Switch][f2-switch], [WinUI toggles][wl-toggles])
- Under `prefers-reduced-motion: reduce` the thumb moves without transition. Derived.
- Switch versus checkbox: a switch is an action ("online booking active"), a checkbox is a state to be submitted. ([WinUI toggles][wl-toggles])

## 6. Slider

- For approximate or relative values, not for exact input: money, durations and quantities use a field. Needs a label (can be visually hidden), min and max named, value shown in a tooltip or text beside it, at least four distinct values (otherwise radio buttons). Keep the thumb size constant. ([Slider][f2-slider], [WinUI slider][wl-slider])
- Markup: Path A `Slider min max step value onChange vertical size` renders a hidden native `<input type="range">` over the custom rail and thumb (verified in `useSlider.ts`) and sets `aria-orientation`. Path B: use the native `<input type="range">` and style it with `::-webkit-slider-thumb` and `::-moz-range-thumb`, or the same overlay trick; a custom `role="slider"` element needs `aria-valuemin`, `aria-valuemax`, `aria-valuenow`, `aria-valuetext`, `tabindex="0"` and the Arrow, Home, End and Page keys. The native range input supports all of these. Provide `aria-valuetext` when the number needs a unit ("30 minutes"). Derived from the APG. ([MDN range][mdn-range], [APG slider][apg-slider])
- Keys on the native range: Left and Down decrease, Right and Up increase by `step`, Page keys by a larger amount, Home and End jump to the bounds; there is no wrap. A slider is one tab stop. Dragging needs an alternative that is not dragging (WCAG 2.5.7): the keys count, so keep the focus ring visible on the thumb. ([WCAG 2.5.7][wcag-257])
- Skip it entirely when the product has no relative values.

## 7. Which selection control

| Situation | Control (Path A name) |
| --- | --- |
| One yes/no choice that is submitted | Checkbox (`Checkbox`) |
| A setting that applies instantly | Switch (`Switch`) |
| One of 2 to about 5 options | Radio buttons (`RadioGroup`, `Radio`) |
| One of up to about 8 to 12 options | Native select or combobox (`Select`, `Dropdown`; see `inputs.md`) |
| One of very many | Combobox with type-ahead filter (`Combobox`) |
| Several of up to about 7 | Checkboxes |
| Several of many | Tag picker or multi-select list (`TagPicker`, `Dropdown multiselect`; see `inputs.md`) |
| Approximate value on a range | Slider (`Slider`) |
| Exact number | Number or money field (`SpinButton`, `Input`; see `inputs.md`) |

Counts differ between sources (Fluent radio about 5, WinUI combo box from 9, WinUI radio over 8); a project may fix its own thresholds, and then they win. ([Select][f2-select], [Radio group][f2-radiogroup], [WinUI combo box][wl-combobox])

## 8. Checklists

Each item names how to check it. Tools: **React Testing Library with user-event** (`await user.tab()`, `await user.keyboard(' ')`, `getByRole('button', { name })`, jest-dom `toBeDisabled`, `toHaveAttribute('aria-pressed', 'true')`); **Playwright** (real keyboard, `toHaveScreenshot` in light and dark, `page.emulateMedia({ reducedMotion: 'reduce' })`); **axe-core** (names, roles, contrast). jsdom does not match `:focus-visible` reliably and has no layout, so ring, size and animation checks run in Playwright. ([user-event][tl-userevent], [Playwright emulateMedia][pw-media], [Playwright accessibility][pw-a11y], [axe-core][axe])

### Button

- [ ] Exactly one primary per view or footer (search the JSX for `appearance="primary"` or the primary class per view).
- [ ] Label is a verb phrase, sentence case, no trailing period; no "OK", "Yes" or "No" in dialogs (grep the copy files).
- [ ] Every button in a form that should not submit has `type="button"` (grep for `<button` without `type`, or ESLint `react/button-has-type`).
- [ ] Every state is drawn and reviewed in light and dark (Playwright screenshots): rest, hover, pressed, focus-visible, disabled.
- [ ] Disabled buttons that are not self-explanatory use `disabledFocusable` or `aria-disabled` and have a tooltip with the reason (RTL: tab to it, assert focus, `aria-disabled`, and the tooltip text).
- [ ] Icon-only buttons have an accessible name and a tooltip (`getByRole('button', { name: 'Delete' })` succeeds; axe `button-name`).
- [ ] The target is at least 24 by 24 CSS px (Playwright `boundingBox()`).
- [ ] Press scale and color transitions are about zero when reduced motion is on (Playwright, computed `transition-duration`).
- [ ] Shortcuts appear in tooltips and in `aria-keyshortcuts`, and do not fire inside text fields (test).
- [ ] Toggle buttons expose `aria-pressed` and keep a constant name (RTL).
- [ ] Tab order follows reading order, including when the layout reorders buttons visually (Playwright: press Tab through the footer and record the order).

### Link

- [ ] Navigation uses `<a href>`, actions use `<button>` (grep for `<a` without `href` and for `onClick` on anchors).
- [ ] Link text has meaning out of context and names a new tab; axe `link-name` passes.
- [ ] Links in running text have a non-color cue (screenshot) and 3:1 against surrounding text.

### Checkbox, radio, switch, slider

- [ ] The whole row, label included, is clickable (RTL: `user.click(getByText('Label'))` toggles the input).
- [ ] Border contrast is 3:1 in rest state (script on computed colors).
- [ ] Labels are positive statements; "select all" shows the mixed state for partial selection (`indeterminate` or `aria-checked="mixed"`, test).
- [ ] Radio group: one tab stop, arrows move and check, the group has a name through `legend` or `aria-labelledby` (RTL: `user.tab()` once then `user.keyboard('{ArrowDown}')`; axe `radiogroup`).
- [ ] Switches exist only on views without a save button (review); a switch is `role="switch"` with a name (`getByRole('switch', { name })`).
- [ ] The switch transition is 200 ms and disabled by reduced motion (Playwright).
- [ ] Sliders have a name, a visible value, `aria-valuetext` when the unit matters, and work with the arrow keys (RTL or Playwright).

## 9. Sources

[f2-button]: https://fluent2.microsoft.design/components/web/react/core/button/usage
[f2-link]: https://fluent2.microsoft.design/components/web/react/core/link/usage
[f2-dialog]: https://fluent2.microsoft.design/components/web/react/core/dialog/usage
[f2-tooltip]: https://fluent2.microsoft.design/components/web/react/core/tooltip/usage
[f2-checkbox]: https://fluent2.microsoft.design/components/web/react/core/checkbox/usage
[f2-radiogroup]: https://fluent2.microsoft.design/components/web/react/core/radiogroup/usage
[f2-switch]: https://fluent2.microsoft.design/components/web/react/core/switch/usage
[f2-slider]: https://fluent2.microsoft.design/components/web/react/core/slider/usage
[f2-select]: https://fluent2.microsoft.design/components/web/react/core/select/usage
[wl-buttons]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/buttons
[wl-dialogs]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs
[wl-keyboard]: https://learn.microsoft.com/en-us/windows/apps/develop/input/keyboard-interactions
[wl-tooltips]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/tooltips
[wl-checkbox]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/checkbox
[wl-radio]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/radio-button
[wl-toggles]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/toggles
[wl-slider]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/slider
[wl-combobox]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/combo-box
[gh-button]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-button/library/src/components/Button/useButtonStyles.styles.ts
[gh-link]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-link/library/src/components/Link/useLinkStyles.styles.ts
[gh-checkbox]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-checkbox/library/src/components/Checkbox/useCheckboxStyles.styles.ts
[gh-radio]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-radio/library/src/components/Radio/useRadioStyles.styles.ts
[gh-switch]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-switch/library/src/components/Switch/useSwitchStyles.styles.ts
[mdn-button]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button
[mdn-anchor]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a
[mdn-focusvisible]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
[mdn-ariadisabled]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-disabled
[mdn-ariapressed]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-pressed
[mdn-ariaexpanded]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-expanded
[mdn-keyshortcuts]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-keyshortcuts
[mdn-indeterminate]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/checkbox#indeterminate_state_checkboxes
[mdn-radio]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/radio
[mdn-switch]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/switch_role
[mdn-range]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range
[apg-radio]: https://www.w3.org/WAI/ARIA/apg/patterns/radio/
[apg-switch]: https://www.w3.org/WAI/ARIA/apg/patterns/switch/
[apg-slider]: https://www.w3.org/WAI/ARIA/apg/patterns/slider/
[wcag-141]: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
[wcag-1411]: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
[wcag-243]: https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
[wcag-244]: https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html
[wcag-257]: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html
[wcag-258]: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
[tl-userevent]: https://testing-library.com/docs/user-event/intro
[pw-media]: https://playwright.dev/docs/api/class-page#page-emulate-media
[pw-a11y]: https://playwright.dev/docs/accessibility-testing
[axe]: https://github.com/dequelabs/axe-core
