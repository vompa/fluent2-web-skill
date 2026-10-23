# Inputs: fields, states, keyboard behavior, parsers

Read this file when you build, style or review any input on the web: text, multi-line text, search, number, money, time, date, select, combobox, tag picker. It holds the field anatomy, the state model, a behavior matrix for Tab, click, typing, arrows, Enter, Esc and blur, parser examples and a checklist per field type.

Fluent 2 specifies the anatomy, states, labels, help and error text, and the behavior of the spin button, combobox and tag picker. It does not specify masks or parsers for times, dates, numbers and money. Those parts are marked **Derived** below: a recommended pattern built from Fluent's principles and from web standards, not a Microsoft rule. If the project brief or token file defines field widths, heights or behavior, the brief wins (`foundations.md`).

Two audiences use this file, and a statement says which one it addresses when they differ:

- **Path A, Fluent UI React v9** (`@fluentui/react-components`): you get `Field`, `Input`, `Textarea`, `SearchBox`, `SpinButton`, `Select`, `Combobox`, `Dropdown`, `TagPicker` with Fluent's markup, tokens and keyboard handling. Your job is to wire them correctly and add what Fluent leaves out (parsers, commit rules).
- **Path B, own React, HTML and CSS components** that borrow Fluent's values and behavior: you build the markup yourself, so the HTML and ARIA parts below are your responsibility. The Fluent source numbers are your fallback tokens.

## Contents

1. [Field anatomy](#1-field-anatomy)
2. [States](#2-states)
3. [Behavior matrix](#3-behavior-matrix)
4. [The commit pipeline](#4-the-commit-pipeline)
5. [Single-line text](#5-single-line-text)
6. [Multi-line text](#6-multi-line-text)
7. [Search field](#7-search-field)
8. [Number field](#8-number-field)
9. [Money field](#9-money-field)
10. [Time field](#10-time-field)
11. [Date field](#11-date-field)
12. [Choice fields: select, combobox, list](#12-choice-fields-select-combobox-list)
13. [Multi-select and tag picker](#13-multi-select-and-tag-picker)
14. [Checklists](#14-checklists)
15. [Sources](#15-sources)

## 1. Field anatomy

| Part | Rule | Source |
| --- | --- | --- |
| Field | A field is label + input + optional info button + help text + validation message. Path A: wrap every control in `Field` (`label`, `hint`, `validationMessage`, `validationState`, `required`, `orientation`, `size`); it generates the ids and links them (verified in source: `htmlFor` on the label, `aria-describedby` listing the validation message id first, then the hint id, `aria-invalid` for the error state). Path B: build one reusable component that does the same, so name, help and error are bound to the input and not repeated as loose text per screen (Derived). | [Field][f2-field], [Field source][gh-field], [useFieldControlProps][gh-fieldcontrol] |
| Label | A real `<label for="id">` (or wrapping the control), never a `<div>` or a placeholder. Above the input by default, for quick scanning; to the left (`orientation="horizontal"`: label column 33 percent) only when space is tight and fields are alike. A short noun phrase, not a sentence or an instruction, sentence case, no trailing colon, no end punctuation. Wrap long labels; do not truncate them. 14/20 Regular (Fluent default; the `large` Field size uses 16/22 Semibold). A click on the label focuses the input, which also enlarges the target. | [Label][f2-label], [Label source][gh-label], [HTML label][mdn-label] |
| Required | Mark required fields with an asterisk next to the label and expose "required" to assistive technology. Fluent's asterisk is `aria-hidden` and red (`colorPaletteRedForeground3`, 4 px left padding), so the semantics must sit on the control: `Field required` sets the native `required` on `input`, `select` and `textarea` and `aria-required` on other controls (verified). Path B: set `required` on native controls and `aria-required="true"` on ARIA widgets; hide the visual asterisk with `aria-hidden="true"`. If every field is required, one general note before the form is enough; a two-field sign-in needs none. The save button may stay disabled until required fields are filled; a disabled submit button hides the reason, so say what is missing in a hint or let the click show the errors (Derived). A project may keep the asterisk neutral to avoid clashing with the error color (recorded deviation). Native `required` triggers the browser's own bubbles on submit; use `noValidate` on the form when the app shows its own messages, so there is one validation channel (Derived). | [Field][f2-field], [Label source][gh-label], [WCAG 3.3.2][wcag-332], [MDN required][mdn-required] |
| Help text | Under the field, explains values or format. 12/16 in the third text tone (`colorNeutralForeground3`), 2 px below the field (Fluent default, verified in the Field source). Link it with `aria-describedby`. Fluent writes fragments without a final period and full sentences with one; stay consistent per project. | [Field][f2-field], [Field source][gh-field] |
| Error text | Short and helpful; shows the way forward. Icon 12 px, danger color (`colorPaletteRedForeground1`), 2 px below the field (Fluent default). In Fluent the message has `role="alert"` for error and warning (verified), so it is announced when it appears. Color alone is not enough: the state is color plus icon plus text (WCAG 1.4.1). Fluent's Field shows help and validation separately, both under the control. A compact form may let the error replace the help line to avoid layout jumps (Derived); either way keep the error visible and never only in a tooltip. | [Field][f2-field], [Field source][gh-field], [WCAG 1.4.1][wcag-141], [Responsible AI][f2-rai] |
| Error wiring | Set `aria-invalid="true"` on the control and put the message id in `aria-describedby`. Prefer `aria-describedby` over `aria-errormessage`: Fluent does so, and support for `aria-errormessage` in assistive technology has been uneven (derived, not verified for current versions; test with the screen readers you target). | [useFieldControlProps][gh-fieldcontrol], [MDN aria-invalid][mdn-ariainvalid], [MDN aria-errormessage][mdn-errormessage] |
| Placeholder | A brief hint or a format example, no final period. Never a replacement for the label: it disappears on typing, which burdens people with cognitive impairments, and it is not a reliable accessible name. Fluent default color `colorNeutralForeground4` (`#707070` in the light theme), with `opacity: 1` to undo the browser default; measure the effective contrast (section 2). | [Input][f2-input], [Input source][gh-input], [WCAG 3.3.2][wcag-332] |
| Width | Roughly the expected input length. Slightly wider than the longest expected value; if that is very wide, split into two fields. Set `maxlength` and tell the user when the limit is reached. Document the limit per field (for example name 80, phone 30, email 254). | [Input][f2-input], [WinUI text box][wl-textbox] |
| Size | Fluent default (source): heights 24, 32, 40 (small, medium, large), radius 4 (`borderRadiusMedium`), horizontal padding 8, 12, 18, icons 16, 20, 24, text 12/16, 14/20, 16/22. A desktop or dense brief may use another height; keep one height for all controls on a page. | [Input source][gh-input] |
| Autofill and purpose | Set `autocomplete` tokens on personal data (`name`, `given-name`, `family-name`, `email`, `tel`, `street-address`, `postal-code`, `one-time-code`); `autocomplete="off"` on amounts, quantities, codes and search. WCAG 1.3.5 asks for the input purpose on fields that collect user data. Derived from the standard. | [WCAG 1.3.5][wcag-135], [MDN autocomplete][mdn-autocomplete] |
| Virtual keyboard | `inputmode` (`numeric`, `decimal`, `tel`, `email`, `search`) selects the on-screen keyboard and validates nothing; `enterkeyhint` (`next`, `done`, `go`, `search`, `send`) labels the Enter key. Validation stays in your code. Derived. | [MDN inputmode][mdn-inputmode], [MDN enterkeyhint][mdn-enterkeyhint] |

### Markup for path B

```html
<div class="field">
  <label for="start">Start time <span aria-hidden="true">*</span></label>
  <input id="start" name="start" type="text" inputmode="numeric" autocomplete="off"
         required aria-describedby="start-error start-hint" aria-invalid="true" />
  <div id="start-hint" class="field-hint">For example 09:30</div>
  <div id="start-error" class="field-error" role="alert">
    <svg aria-hidden="true">...</svg> The time is between 00:00 and 23:59.
  </div>
</div>
```

Render `aria-invalid` and the error element only while the value is invalid. Keep the order `error hint` in `aria-describedby`, as Fluent does, so the problem is read first.

### The Fluent field underline (path B)

The focus indicator of an input is not an outline. A 2 px brand line (`colorCompoundBrandStroke`) sits on the bottom edge and grows from the middle: it is a `::after` of the wrapper, scaled with `transform` (cheap, no layout). Source values: in 200 ms (`durationNormal`, decelerate curve `cubic-bezier(0,0,0,1)`), out in 50 ms (`durationUltraFast`), and `0.01ms` when `prefers-reduced-motion: reduce` is set. Fluent also adds a transparent 2 px outline on `:focus-within` so that Windows high-contrast mode (forced colors) still draws a visible border.

```css
.input-wrap { position: relative; border: 1px solid var(--stroke1); border-bottom-color: var(--stroke-accessible);
              border-radius: 4px; min-height: 32px; }
.input-wrap::after { content: ""; position: absolute; inset: auto -1px -1px -1px; height: 4px;
  border-bottom: 2px solid var(--brand-stroke); border-radius: 0 0 4px 4px;
  clip-path: inset(calc(100% - 2px) 0 0 0);
  transform: scaleX(0); transition: transform 50ms cubic-bezier(1,0,1,1); }
.input-wrap:focus-within::after { transform: scaleX(1); transition: transform 200ms cubic-bezier(0,0,0,1); }
.input-wrap:focus-within { outline: 2px solid transparent; }
@media (prefers-reduced-motion: reduce) { .input-wrap::after { transition-duration: 0.01ms; } }
```

The inner `<input>` has `outline: none` only because the wrapper shows the focus state; if your input has no wrapper, keep a `:focus-visible` outline (WCAG 2.4.7, and 2.4.11 that the focused field is not covered by sticky headers). Derived from the Fluent source plus the standard.

## 2. States

Fluent distinguishes seven states, each driven by its own tokens. The first five appear in most briefs; add selected and error.

| State | Fluent behavior | Note |
| --- | --- | --- |
| Rest | Surface 1, 1 px border (`colorNeutralStroke1`), bottom edge darker (`colorNeutralStrokeAccessible`). | See `foundations.md` on contrast. |
| Hover | Border and bottom edge one step darker (`...Hover` tokens); no shadow. | A disabled control does not react. Fluent shows `cursor: not-allowed`; a project may keep the default cursor. |
| Pressed | Bottom edge darker still (`...Pressed`), via `:active` and `:focus-within`. | |
| Keyboard focus | Input: 2 px brand underline that grows in 200 ms and leaves in 50 ms (see above). Button: border plus an inner 1 px ring in the focus color (`colorStrokeFocus2`) and a transparent 2 px outline for forced colors; it appears on `:focus-visible` only. Link: double underline. | Text inputs match `:focus-visible` after a mouse click as well, because the browser always shows focus for controls that take text. That is the right behavior for inputs. |
| Disabled | Dedicated disabled colors, exempt from contrast rules; the focus underline is removed. Label, help text and existing error text stay readable; only the input looks disabled. The tooltip should say why and, if possible, how to enable it. | A uniform 0.5 opacity is a valid shortcut; do not dim the label and help text with it. Native `disabled` removes the control from the tab order and from form submission; `readonly` keeps both. |
| Selected | Tab text and underline in brand color; tag or chip filled with brand background 2 and brand border; row with brand background 2. | |
| Error | Border in the danger color (`colorPaletteRedBorder2`) except while the field has focus; message under the field. Fields also support warning (dark orange) and success (green). | A warning such as "a record with this name exists" fits a field better than a blocking error. |

Sources: [Button source][gh-button], [Input source][gh-input], [Field source][gh-field], [Link source][gh-link], [Button][f2-button], [Field][f2-field], [Label][f2-label].

Placeholder contrast: measure the effective contrast, not the token. The 4.95:1 of `#707070` on white holds for the full-strength color. Browsers style `::placeholder` themselves (Firefox applies a reduced opacity), and a design system may lower the opacity again. Set both `color` and `opacity: 1` on `::placeholder` as Fluent does, then compute the ratio from the final computed color against the field surface per theme and per state (disabled is exempt), and fail the field when it is under 4.5:1 (WCAG 1.4.3). Derived. ([WCAG 1.4.3][wcag-143])

Border contrast: WCAG 1.4.11 asks 3:1 for the visual information that identifies a control. Fluent's own field border is about 1.5:1 and relies on the darker bottom edge; do not assume the border token passes, compute it. Derived. ([WCAG 1.4.11][wcag-1411])

Decision point, error border on focus: Fluent draws the danger border except while the field has focus (the CSS selector is `:not(:focus-within)`, verified), where the border turns neutral and the brand underline takes over; the message under the field stays. A project may keep the danger border while the field is focused, so a user who is correcting the value still sees which field is wrong. Both are valid; record the choice (`foundations.md`) and cover the focused-with-error state in a screenshot and a test. Derived.

## 3. Behavior matrix

This matrix is the heart of consistent keyboard behavior. Rows are events, columns are field types. Text input always has priority over other keys: Space types a space in a field, it does not "press" anything. ([WinUI keyboard][wl-keyboard])

| Event | Text | Number / money | Time | Date | Choice |
| --- | --- | --- | --- | --- | --- |
| Focus by Tab | Caret at end, nothing selected (edit); native default selects all | Select all (replace) | Select all | Select all | Focus ring on the trigger |
| Focus by click | Caret at click point | Caret at click point | Caret at click point | Caret; click on the calendar icon opens the picker | Opens the list (Fluent Dropdown, Combobox: click on the arrow) |
| Typing | Any character | Digits, decimal and group separator, minus only if negative is allowed | Digits, colon, dot, comma | Digits, dot, slash, hyphen | Combobox filters; Select and Dropdown jump to the matching item |
| Up / Down | Nothing | Step | Minute step | Day | Moves highlight (opens when closed) |
| Page Up / Down | Nothing | Large step | Hour | Month | Moves the highlight by a page (Fluent: 10 options) |
| Home / End | Line start / end | Minimum / maximum, if set | As number | Nothing | First / last item (open) |
| Enter | Submits the form (implicit submission, single line) | Commits the value, then submits | As number | As number | Selects, closes |
| Esc | Restores the last committed value if changed; otherwise lets the surface above handle it | As text | As text | As text | Closes the list, no change |
| Blur | Checks length and required | Parses, formats, writes display format | Parses, writes `HH:mm` | Parses, writes display format | Commits selection |
| Error | Danger border, message and icon at the field | As text | As text | As text | As text |
| Submit with errors | Focus moves to the first invalid field | As text | As text | As text | As text |
| After first error | Re-validate while typing; error clears as soon as the value is valid | As text | As text | As text | - |

All rows are **Derived** from WinUI text-box, number-box and keyboard guidance, from Fluent's spin-button and combobox logic ([WinUI text box][wl-textbox], [WinUI number box][wl-numberbox], [WinUI keyboard][wl-keyboard], [Spin button source][gh-spinbuttonlogic], [Key actions source][gh-keyactions]) and from the HTML and ARIA standards, except where a later section cites a Fluent rule directly. Two sources disagree on where focus goes after a failed submit: Fluent's message bar guidance gives the bar focus, a form-level rule often prefers the first invalid field. Pick one per project and write it down. ([Message bar][f2-messagebar])

### Enter and implicit submission

A single-line `<input>` inside a `<form>` submits the form on Enter. The browser clicks the form's default button, which is the first submit button in tree order; if that button is disabled, nothing happens. A form without any submit button submits on Enter only when it has exactly one field that blocks implicit submission (a plain text field). In a `<textarea>` Enter inserts a line break. Consequences: give the form one real `<button type="submit">` and make every other button `type="button"`; do not emulate Enter with a key handler where `onSubmit` does the job; set `enterkeyhint` so the mobile key matches the action. ([HTML spec][html-implicit])

Two web-only traps: during IME composition (Japanese, Chinese, Korean input) Enter and Esc belong to the composition, so ignore them while `event.isComposing` is true; and a controlled React input must commit the typed text before `onSubmit` reads it (see section 4). Derived.

### The Esc ladder on the web

From innermost to outermost (Derived): first Esc closes an open listbox or popup; second Esc restores a changed field to its last committed value; the next Esc closes the dialog or form. Esc cancels only transient surfaces, never page navigation. ([WinUI keyboard][wl-keyboard], [APG combobox][apg-combobox])

The platform adds its own Esc handlers, which you must keep out of the ladder's way:

- A modal `<dialog>` (opened with `showModal()`) closes on Esc and fires a `cancel` event. A popover (the Popover API, `popover` attribute) with `auto` state closes on Esc as light dismiss. Both listen at the document level, so an Esc that closes your listbox may also close the dialog around it unless you stop it. ([MDN dialog][mdn-dialog], [MDN Popover API][mdn-popover])
- Fluent's combobox and dropdown call `stopPropagation()` on the Esc that closes their listbox "to avoid dismissing any parent popups" (verified in `useTriggerSlot.ts`). Do the same in path B for every widget that owns a popup, and call `preventDefault()` on that keydown too.
- For the second rung (restore the field), handle Esc on the input: if the draft differs from the committed value, restore it and stop the event; if not, let it pass. The Fluent `SpinButton` does this: Esc discards the typed text and shows the last value again (verified).
- If you cannot stop the key (a third-party dialog), listen to the dialog's `cancel` event and call `preventDefault()` while a field is dirty. Browsers may refuse to cancel a `cancel` event when the user pressed Esc repeatedly without other interaction (derived, not verified; test in the browsers you support).
- A search input with `type="search"` is cleared by Esc natively in some browsers. Decide whether that or your ladder wins, and test it (derived, not verified).

## 4. The commit pipeline

All typed fields (number, money, time, date) share one pipeline. Build it once and reuse it. (Derived.)

1. Filter at typing time: reject characters that can never be valid in this field (a letter in a number field) and strip them on paste. Filter in `beforeinput` or `onChange`, not in `keydown` (keydown misses paste, drop, IME and virtual keyboards).
2. Hold the raw text while the user types; do not reformat mid-typing, and do not recompute dependent fields. In React this means a controlled input whose state is the string; the parsed value lives next to it, not instead of it.
3. Commit on Enter or blur: parse the raw text with a tolerant parser (see the tables below) into a typed value (integer minor units or a decimal string, a time, a date, an `int`) or an error.
4. On success, write the display format back to the text (for example `930` becomes `09:30`) and raise the value to the parent through `onChange`. Dependent fields (end time after start time) recompute only now.
5. On failure, keep the text, mark the field invalid (`aria-invalid`, message in `aria-describedby`) and show a message that names the problem and the valid range. Do not overwrite or clear the input silently; WinUI's "overwrite invalid input" mode swallows the user's text, so do not use it for important data. ([WinUI number box][wl-numberbox])
   No stale value after a failed commit: the parent state must not silently keep the previous valid value while the field shows the rejected text, or a Save button writes a value the user cannot see. Two patterns (Derived):
   - Text state in the parent: publish the raw text with no parsed value (`value: undefined`), so the form sees "no value" instead of the old one.
   - Typed state in the parent: the field reports `{ value, valid }` or throws the error into a form-level `errors` map, and the submit handler refuses to run while any field is invalid. A successful commit and Esc clear the error.
   Test: type garbage, commit, assert the submit button or handler refuses (or the value is empty); type a valid value, commit, assert it works again.
6. Esc restores the last committed value and selects it. ([Spin button source][gh-spinbuttonlogic])
7. An empty field means "no value", which is not zero. Required fields report the empty state as an error; optional ones commit "no value".
8. Enter commits first, then the form submits. In React, `onSubmit` runs after keydown but the commit on blur may not have happened yet when Enter is pressed; call the commit function in the field's own `onKeyDown` for Enter (without `preventDefault`) or read the value from the input element in `onSubmit`. Derived.

Because separating raw text from the parsed value lets a user type freely, makes tests simple (parser unit tests with a table of inputs) and keeps formatting a display concern.

Path A note: Fluent's `Input` is a controlled-or-uncontrolled native input with `onChange(ev, { value })`. It has no parser; build the pipeline around it. `SpinButton` has its own commit rule (section 8).

## 5. Single-line text

- Name, address, email, phone, short note: `<input type="text">`, or `email`, `tel`, `url` where the type brings the right keyboard and light validation (`type="email"` accepts `a@b`; do not rely on it as a real check). Path A: `<Input type="email" />`. Enter in a single-line field submits the form through implicit submission (section 3). Not in multi-line fields. Derived. ([WinUI dialogs][wl-dialogs])
- Tab entry: browsers select the whole content when a user tabs into a text field. That fits fast fields (time, number, search), where the user replaces. For free text the common case is editing, so Derived advice is to put the caret at the end instead: track whether the focus came from a pointer (`pointerdown` sets a flag before `focus`), and when it did not, call `setSelectionRange(len, len)` in `onFocus`. The native selection may be applied after the `focus` event, so defer by one `requestAnimationFrame` (derived, not verified per browser; test in Chromium, Firefox and WebKit). Do not use `:focus-visible` to tell keyboard from mouse here: it matches text inputs after a click too. Overriding a native behavior has a cost: if the brief does not ask for it, the native default is acceptable; record the choice. WinUI recommends selecting all when replacement is the main case. ([WinUI text box][wl-textbox], [MDN :focus-visible][mdn-focusvisible])
- Selection APIs fail on some types: `setSelectionRange` and `selectionStart` throw or return `null` for `type="email"` and `type="number"` (HTML spec), so a select-all or caret rule must use `select()` or switch the field to `type="text"`. Derived.
- Click always places the caret and selects nothing. Double-click selects a word, triple-click the line, Ctrl+A everything. Native; leave it alone.
- Clear (x) button: use it for search fields; skip it in ordinary form fields where an accidental click could erase required data (Derived). Path A: `Input` has `contentAfter` for a custom button; the clear control needs an accessible name and `tabIndex={-1}` only if the Esc ladder already clears the field. ([WinUI text box][wl-textbox], [Searchbox][f2-searchbox])
- Paste: `maxlength` already truncates pasted text silently, which is the opposite of helpful. Intercept `onPaste`, remove line breaks and leading or trailing spaces (including non-breaking), compare with the limit and show a warning such as "Shortened to 80 characters." (Derived.) Note that `maxlength` counts UTF-16 code units, so one emoji counts as two; decide whether that is acceptable. ([WinUI text box][wl-textbox], [MDN maxlength][mdn-maxlength])
- Read-only fields look editable and confuse users: use `readonly` (focusable, submitted) only as a temporary state; keep the text selectable and copyable; if the text is never editable, show plain text. `disabled` is not read-only. ([WinUI text box][wl-textbox])
- Spell check: `spellcheck="false"` for names, phone numbers, codes and emails; leave it on for notes and free text. `autocapitalize="off"` for emails and user names. Derived. ([MDN spellcheck][mdn-spellcheck])

## 6. Multi-line text

- Fixed height, not growing as the user types; vertical scroll bar on overflow; `resize` only if you want it. Path A: `Textarea` with `size` and `resize` (`none` is the default, `both`, `horizontal`, `vertical`); the source sets min heights 40, 52, 64 and max heights 200, 260, 320 for small, medium and large (verified). Auto-growing text areas are possible with `field-sizing: content` in current Chromium; Fluent does not use it (derived, not verified for other browsers). ([Textarea][f2-textarea], [Textarea source][gh-textarea], [WinUI text box][wl-textbox])
- Counter: for limited text show a running count below ("120 characters left"); warn near the limit (for example from 90 percent). Link the counter with `aria-describedby`. Do not put the changing number in a polite live region on every keystroke; announce at thresholds (for example at 90 and 100 percent) with `role="status"`. Derived. ([WinUI text box][wl-textbox])
- Enter inserts a line break (native), Tab leaves the field, Ctrl+Enter submits the form: implement with `form.requestSubmit()` in `onKeyDown`, because the browser does not do it. Derived.
- Plain text only unless rich text is truly required; if rich text is required, a `contenteditable` is a different component and needs its own accessibility review. ([WinUI text box][wl-textbox])
- Counter logic reads the text and the limit. Test it with the limit set before and after the text arrives (props arrive in any order in React), and with pasted text longer than the limit. Derived.

## 7. Search field

- Magnifier icon at the start, clear button only when there is content, optional filter icon; same rest-to-focus transition as the input. On a narrow screen collapse to the magnifier and expand on click. Path A: `SearchBox` renders `<input type="search">` with a dismiss control (`role="button"`, `aria-label="clear"`, verified) that you should localize. Path B: `<input type="search">` inside an element with `role="search"` (or the `<search>` element); hide the browser's built-in cancel button (`::-webkit-search-cancel-button`) if you draw your own. ([Searchbox][f2-searchbox], [Searchbox source][gh-searchbox], [MDN search][mdn-search])
- On focus show recent searches; while typing, suggestions replace them; most relevant first; related topics after hits. With no result show one line such as "No results" plus the way to create or broaden. Suggestions are a combobox with a listbox: follow section 12 for the roles. ([Searchbox][f2-searchbox], [WinUI auto-suggest][wl-autosuggest])
- Keys: Down moves into the list, Up/Down choose, Enter picks, Esc closes the list, a second Esc clears the field, a third closes the dialog (Derived). Space in the list does not pick while the user types, because text input has priority. ([WinUI keyboard][wl-keyboard], [WinUI auto-suggest][wl-autosuggest])
- Enter or the magnifier submits the query when no suggestion is highlighted. Put the field in a `<form role="search">` so Enter works without code. ([WinUI auto-suggest][wl-autosuggest])
- Debounce the query (about 200 to 300 ms, Derived) and announce the result count in a polite live region ("12 results"), so screen reader users learn that the list changed. ([ARIA live regions][mdn-live])

## 8. Number field

Fluent's spin button changes a value in small steps and still allows typing. Under about three possible values use a plain input; for imprecise values use a slider. ([Spin button][f2-spin])

- Native `type="number"` is often the wrong tool. It returns an empty string for unreadable input, so code cannot tell "empty" from "garbage" (`validity.badInput` is the only hint); it accepts `e`, `+` and `-` in places you do not want; it ignores the app's locale for the decimal separator and uses the browser's; browsers may change the value on mouse wheel or arrow keys while focused; it strips leading zeros; it has no `selectionStart`; and some assistive technology announces spin arrows that nobody needs. Use it for plain small integers (a quantity of 1 to 99, a page number) if you accept those limits. For amounts, durations, codes (postal code, phone, IBAN) and anything with a locale, use `type="text"` with `inputmode="numeric"` or `"decimal"` and your own parser. Fluent's `SpinButton` is itself `<input type="text" role="spinbutton" autocomplete="off">` (verified), which is the same decision. Derived. ([MDN number][mdn-number], [GOV.UK note][govuk-number])
- `inputmode="decimal"` shows a keypad with a decimal key on most phones, but some keyboards offer only a dot while the locale wants a comma; the parser must accept both. `inputmode="numeric"` has digits only (no decimal, no minus). Neither restricts what a desktop keyboard types. Derived. ([MDN inputmode][mdn-inputmode])
- Path A: `SpinButton` with `min`, `max`, `step`, `stepPage` (default 1), `precision`, `value` or `defaultValue`, `displayValue` (for units such as "20 min"), `onChange(ev, { value, displayValue })`, `size`, `appearance`. It parses only plain numbers; if the user types a unit or a comma, the value falls back, so for locale parsing use a `Input` with your own parser (a hybrid is possible, `onChange` with `displayValue` and a parse of the text). Wrap it in a `Field` so the label and range hint are linked.
- Layout (source): height 24 or 32; two stacked step buttons in a 24 px wide column (each 16 high), left padding 10, radius 4, underline as for inputs. Show arrows only for small ranges (up to roughly 20 steps); omit them otherwise. ([Spin button source][gh-spinbutton])
- Typing: allow digits, the decimal separator, the group separator, and minus only when the minimum is below zero. Reject everything else at typing time and strip it on paste. Derived. ([WinUI number box][wl-numberbox])
- Keys (Fluent source, verified): Up/Down step; Page Up/Down large step (`stepPage`); Home/End jump to minimum/maximum if set; Enter commits; Esc discards the typed text and shows the last value. Holding a key repeats after 300 ms, then accelerates to a minimum delay of 80 ms over about one second. Shift+Up/Down for the smallest step and mouse wheel only while focused are Derived (the wheel handler should call `preventDefault` only while the field has focus, so page scroll is not blocked). ([Spin button source][gh-spinbuttonlogic], [WinUI number box][wl-numberbox])
- Limits: at minimum or maximum the step button is disabled but the input stays active so the target remains large enough (verified: the button's `disabled` follows the bound, the input does not). Clamp on step; do not wrap around. ([Spin button][f2-spin])
- Commit: on Enter and blur the value is accepted and rounded to the step precision; formatting by the user is replaced by the configured format without an error. Out-of-range or non-numeric input is an error that names the valid range, for example "The value is between 0 and 120." (Derived; do not use silent overwrite.)
- Expressions: WinUI can evaluate `+ - * / ^`. Leave that off wherever numbers must be exact or auditable; formulas invite surprises. Derived. ([WinUI number box][wl-numberbox])
- Unit: Fluent puts the unit in the placeholder ("0 cm"). A project may put it in the label ("Duration (min)"), which stays visible while typing. Either is fine; do not do both. ([Spin button][f2-spin])
- Display: `font-variant-numeric: tabular-nums`; value left-aligned in forms (same edge as the label) and right-aligned in table cells (`text-align: end`). Derived.
- Accessibility: the field needs `role="spinbutton"` with `aria-valuemin`, `aria-valuemax`, `aria-valuenow` and `aria-valuetext` (such as "20 minutes") when it behaves like a spin button; Fluent sets them (verified). A plain text number field has no such role and needs only a label and a hint ("Minutes, 0 to 120"). Name the step buttons ("Increase", "Decrease"; Fluent's English defaults are "Increment value" and "Decrement value", verified, so pass localized labels) and keep them out of the tab order (`tabIndex={-1}`, verified in Fluent) because the keyboard has Up and Down. Derived from the APG. ([Spin button][f2-spin], [APG spinbutton][apg-spinbutton])

## 9. Money field

Fluent has no money component. WinUI's number box with a decimal formatter covers currency and fraction digits. ([WinUI number box][wl-numberbox])

- Build it on the number field with `type="text"` and `inputmode="decimal"`, `autocomplete="off"`: no step arrows, fixed fraction digits (usually two), the currency symbol in the label or a suffix, a width suited to the largest amount. Derived.
- JavaScript `number` is a binary float: `0.1 + 0.2` is not `0.3`. Hold amounts as integer minor units (cents in a `number` or `bigint`) or as a decimal string with a decimal library, and format with `Intl.NumberFormat`. Never do arithmetic on the parsed float. Do not round silently: more fraction digits than allowed is an error ("At most two decimal places.") because quiet rounding changes the user's number and can break audit requirements. Derived. ([MDN Intl.NumberFormat][mdn-intl])
- Parsing follows the culture. Read the separators from `new Intl.NumberFormat(locale).formatToParts(12345.6)` instead of hard-coding them. Example for a locale with decimal comma and group dot: `12` is 12.00, `12,5` is 12.50, `1.234,56` is 1234.56, `1234` is 1234.00 (no automatic decimal shift), `12,505` is an error. Numpad convenience: a single dot followed by one or two digits and no comma reads as a decimal (`12.5` is 12.50). Strip spaces, currency signs and non-breaking and narrow no-break spaces (U+00A0, U+202F, which several locales use as group separators) on paste. (Derived.)
- Keys: Up/Down plus or minus 1.00, Shift+Up/Down 0.10, Page Up/Down 10.00, Home/End only with limits, wheel only while focused. These keys need a key handler; a text input does nothing on Up/Down by itself. Derived.
- Display on commit: rewrite in the display format of the locale (example locale: `1.234,50`) with `Intl.NumberFormat`, `minimumFractionDigits` and `maximumFractionDigits` both 2. Negative amounts in the danger color with a minus sign, not parentheses (the default `currencySign: "standard"`). Empty is not 0.00; empty means "not given". Derived.
- Set `lang` on the page or the field so assistive technology and `Intl` agree with the visible format.

## 10. Time field

Native and custom both have a place; choose deliberately (Derived).

- `<input type="time">`: right for simple forms, mobile (the system picker is good) and when the browser's locale display is acceptable. Its `value` is always the 24-hour string `HH:mm` (or `HH:mm:ss`), whatever the display; `min`, `max` and `step` (in seconds) work; the fields are segmented, so a user edits hour and minute separately. Weak points: the display follows the browser or system locale, not your app's; a user cannot type `930` and have it understood; styling is limited; the picker UI differs per browser. ([MDN time][mdn-time])
- A text field with a tolerant parser: right for fast keyboard entry (planning, booking, time sheets), for an app-controlled format and for easy paste and correction. Path A: `Input` plus the parser. Fluent UI React v9 also ships a `TimePicker` in the compat package `@fluentui/react-timepicker-compat` (a combobox of times with free text and `onTimeChange`; check the package's current status before relying on it, derived, not verified). WinUI's time picker shows a time and opens a selection overlay; it supports a 24-hour clock, a minute increment and an unset state. ([WinUI time picker][wl-timepicker])

Recommended default for fast keyboard entry (Derived): a text field in `HH:mm` with `inputmode="numeric"` (the parser accepts `930`, so no colon key is needed), tabular digits, width about 100 px, 24-hour clock, with step equal to the calendar grid (5, 10 or 15 minutes). A picker popup is optional. Decide between tolerant parsing with normalization on blur (recommended: fast typists, easy paste and correction) and a fixed mask `__:__` (harder to edit and paste).

Parser table (24-hour example locale):

| Input | Result |
| --- | --- |
| `9`, `09` | 09:00 |
| `930`, `0930` | 09:30 |
| `9:30`, `9.30`, `9,30` | 09:30 |
| `9:5` | 09:05 |
| `24`, `9:60` | Range error: "The time is between 00:00 and 23:59." |
| `abc` | Format error: "Enter a time such as 09:30." |

A field that explicitly allows "until midnight" may accept 24:00. For 12-hour locales extend the parser with am/pm suffixes and keep the same display rule.

- Allowed characters: digits, colon, dot, comma; at most five characters. Tab selects all (native); click places the caret.
- Keys: Up/Down plus or minus the step, Shift+Up/Down one minute, Page Up/Down one hour, Home/End only with limits (for example opening hours). No wrap past midnight: clamp. Wheel only while focused.
- Commit: on Enter or blur write `HH:mm`. Dependent fields (end after start) recalculate only after commit, never during typing. End before or equal to start is an error on the field: "The end must be after the start." A zero-length range is rarely meant; a field that allows it says so.
- Accessibility: label "Start" plus a hint that states the format; with a native time input the label alone is enough. Time zones and daylight saving are a separate problem: a bare `HH:mm` is a local wall-clock time, so combine it with a date and zone only in your data layer. ([WinUI accessibility][wl-a11y])

## 11. Date field

Pick by use. WinUI's date picker (day, month, year) suits known dates such as a birthday where calendar context is irrelevant. The calendar date picker suits dates with context (an appointment, a departure): a calendar overlays the page, shows weekdays, can show load, can be cleared by selecting the chosen day again, and respects min and max dates. ([WinUI date picker][wl-datepicker], [WinUI calendar date picker][wl-calendardatepicker], [WinUI date and time][wl-datetime])

Native or custom (Derived):

- `<input type="date">`: right for simple forms and phones. `value` is always `yyyy-MM-dd`; display and picker follow the browser locale; `min` and `max` work; `showPicker()` opens the picker from your own button. Weak points: no free typing of `211026`, the calendar cannot show availability or closed days, styling is limited, and the first day of the week is the browser's. Pitfall: `valueAsDate` and `new Date("2026-10-21")` are UTC midnight, which shifts the day in time zones west of UTC; keep dates as `yyyy-MM-dd` strings or a date-only type and never route them through `Date` without a zone. ([MDN date][mdn-date])
- Text field with a parser plus an optional calendar popup: right when you need tolerant typing, a locale-fixed display, blocked days or a load display. Path A: `DatePicker` from `@fluentui/react-datepicker-compat` (with `Calendar` from `@fluentui/react-calendar-compat`), whose package names mark them as compat packages; check their current status and keyboard support in your version before relying on them (derived, not verified). Path B: build the parser first, add the calendar as a `dialog` or popover afterwards.

Recommended default (Derived): one date field with two variants, with and without the calendar button. Display format per locale (for example `dd.MM.yyyy`), width about 160 px, calendar icon 16 px at the end with an accessible name ("Choose date"). Week starts on the locale's first day, today highlighted. Format with `Intl.DateTimeFormat`, not by hand.

Parser table (day-first example locale, assuming the current year is 2026):

| Input | Result |
| --- | --- |
| `21102026` | 21.10.2026 |
| `211026`, `21.10.26` | 21.10.2026 |
| `21.10.`, `21.10` | 21.10.2026 (current year) |
| `1.2.26` | 01.02.2026 |
| `30.02.2026` | Error: "30.02.2026 does not exist." |

A two-digit year resolves to the century closest to today; for a birthday it must not land in the future. A date without a year is only valid when the field says so (for example a recurring birthday). A month-first locale needs its own parser order; parameterize it by culture. Validate existence by building the date and comparing the parts back (`30.02` rolls over in `Date`).

- Keys in the field: Up/Down plus or minus one day, Shift+Up/Down one week, Page Up/Down one month, Ctrl+Page one year, wheel only while focused; with no value, Up sets today.
- Opening the calendar: click on the icon, or a key (Alt+Down is a common desktop habit for opening choice fields; derived, not verified for date pickers).
- Inside the calendar popup: arrows move by day and week, Page Up/Down by month, Ctrl+Page by year, Home/End to week start/end, Enter selects and closes, Esc closes without change and returns focus to the field (and does not close the dialog around it, see the Esc ladder). The popup is a grid (`role="grid"`) with the selected day marked `aria-selected`; blocked days are dimmed, set `aria-disabled` and explain why in a tooltip. The popup overlays and pushes nothing aside. ([WinUI calendar date picker][wl-calendardatepicker], [WinUI keyboard][wl-keyboard], [APG date picker dialog][apg-datepicker])
- Out-of-range input is an error that states the range ("The date is between 22.10.2026 and 21.10.2027."), not a silent clamp.
- Date and time together: two fields side by side (for example 160 + 100 wide, 12 apart) bound to one value; changing the date keeps the time. Avoid `type="datetime-local"` when you also need parsing or a zone. ([WinUI date and time][wl-datetime])

## 12. Choice fields: select, combobox, list

- Pick the component by the number of options. Fluent: a native Select for at least four options; Dropdown for custom list styling and multi-select (a button-like trigger that does not accept typing); Combobox for choosing or typing with filter, long lists and free input. WinUI: fewer than five options are better as radio buttons or checkboxes; a long list of rich items is a list view; selection that is secondary and has a default should not dominate the layout. A project rule such as "2 to 4 radio buttons, up to about 12 in a list, beyond that type-ahead" is a valid concrete choice. ([Select][f2-select], [Dropdown][f2-dropdown], [Combobox][f2-combobox], [WinUI combo box][wl-combobox])

| Need | Path A (Fluent UI React v9) | Path B (own markup) |
| --- | --- | --- |
| Pick one of 4 to about 12, no custom rendering | `Select` (wraps a native `<select>`) | native `<select>` with `<label for>` |
| Pick one with custom rows, icons, groups | `Dropdown` with `Option` | ARIA select-only combobox (APG) |
| Pick one of many or type to filter | `Combobox` (`freeform` allows values outside the list) | APG editable combobox with list autocomplete |
| Suggestions for free text | `Combobox freeform` | `<input list>` with `<datalist>` for low stakes, otherwise APG |
| Several values | `Dropdown multiselect`, `Combobox multiselect`, `TagPicker` | APG combobox with `aria-multiselectable` listbox, or checkboxes |

- Native `<select>` is the best default for plain lists: perfect keyboard and screen reader support, the system picker on phones, type-ahead built in. Costs: the open list can barely be styled (Chromium's `appearance: base-select` changes that, but it is not baseline, derived, not verified), no filtering, no rich rows. Keys: Space, Enter, Alt+Down or Down open it (browser dependent); letters jump to a match, also when closed; Esc closes without change. A placeholder option needs `value=""` and `disabled` or `hidden`, or it will be selectable and submitted. ([MDN select][mdn-select])
- `<input list>` plus `<datalist>`: a cheap suggestion list for free text. The value stays free input, the list cannot be styled or rendered richly, behavior and screen reader support differ per browser and on phones. Use it where a wrong or missing suggestion costs nothing; use a combobox where the list is the product. Derived. ([MDN datalist][mdn-datalist])
- Custom combobox, markup (APG): DOM focus stays on the input or trigger with `role="combobox"`, `aria-expanded`, `aria-controls` (the listbox id), `aria-autocomplete="list"` for editable ones and `aria-activedescendant` pointing at the highlighted option; the popup is `role="listbox"` with `role="option"` children and `aria-selected`. Fluent's trigger does exactly this (verified: `role="combobox"`, `aria-expanded`, `aria-controls`, an active-descendant controller). Path B should copy it; do not move DOM focus into the options. ([APG combobox][apg-combobox], [Combobox source][gh-combobox])
- Open and pick (Fluent source, verified in `dropdownKeyActions.ts`): when closed, Down, Up, Enter and Space open the list; letters type or jump. When open: Down and Up move the highlight, Home and End go to first and last, Page Up and Page Down move by 10 options, Enter picks and closes, Alt+Up picks and closes, Esc closes without change (and stops the event), Tab picks the highlighted option and moves on in single-select mode. Typing a letter does not pick. For multi-select, Space toggles the highlighted option and the list stays open. Fluent treats Space as "pick" for single-select; in an editable Combobox that conflicts with typing a space in a value such as "New York" (derived, not verified whether the Combobox guards against it: type a value with a space into an open `Combobox` and test it). In your own widget let Space type a space whenever the input has text. WinUI: arrows in an open list do not change the selection until Enter or click; Esc restores the initial value. ([Combobox][f2-combobox], [Key actions source][gh-keyactions], [WinUI combo box][wl-combobox], [WinUI keyboard][wl-keyboard])
- Editable: submit on Enter or blur when no item matches; if invalid, show a field error and keep the text, rather than quietly resetting. Valid free input may optionally be added to the list. In Path A without `freeform` the typed text that matches no option is discarded on blur, so check the value after blur and show your own message if the text and the selection differ (derived, not verified). Derived. ([WinUI combo box][wl-combobox])
- List content: items phrased in parallel (all nouns or all verbs), no shared first word, "None" where meaningful, sentence case. One line per item, logical order: most frequent first, names alphabetical, numbers numeric, dates chronological. Long lists scroll and are virtualized only beyond a few hundred rows. ([Dropdown][f2-dropdown], [WinUI combo box][wl-combobox])
- Listbox surface (Fluent default, source): min width 138, max width 300, padding 4, item min height 32, radius 4 (WinUI overlays 8), shadow 16. A list item height of 40 matches WinUI list rows; keep to one project value. Show about eight items before scrolling; the list is as wide as the field (Derived). Render the popup in a portal or with the Popover API so `overflow: hidden` ancestors do not clip it; make sure Esc handling follows section 3. ([Menu source][gh-menu], [Geometry][wl-geometry], [MDN Popover API][mdn-popover])

## 13. Multi-select and tag picker

- Dropdown or combobox multi-select: a checkbox per item (Fluent shows a check in the option), the list stays open until Esc or an outside click, and the choice is shown elsewhere (tags in the field or a count). Path A: `multiselect` on `Dropdown` or `Combobox`; `clearable` is not supported in multiselect mode (a console error in the source, verified). ([Combobox][f2-combobox], [Dropdown][f2-dropdown])
- Tag picker. Path A: `TagPicker` with `TagPickerControl`, `TagPickerGroup`, `Tag` (dismissible), `TagPickerInput`, `TagPickerList`, `TagPickerOption`. Typing filters, Up/Down navigate, Enter picks the highlighted option, Esc closes the list. Backspace or Left arrow with the caret at position 0 of the input moves focus to the last tag, it does not delete it directly (verified in `useTagPickerInput.tsx`); the user then removes the focused tag with its dismiss key or button. If your brief wants "Backspace removes the last tag", that is a deviation to implement and test; note it. Optional "remove all"; tags wrap. ([Tag picker][f2-tagpicker], [TagPickerInput source][gh-tagpickerinput])
- Tags: plain or interactive, removable; column gap 8 / 6 / 4 px (medium / small / extra small; verified in the TagGroup source); overflow shown as "+n". A dismiss button needs an accessible name that includes the tag ("Remove Spa"). ([Tag][f2-tag], [TagGroup source][gh-taggroup])
- Path B: a tag picker is a combobox (section 12) plus a list of removable chips; keep the chips in the tab order or give the group a roving tab stop; announce additions and removals in a polite live region ("Spa added, 3 selected"). Derived from the APG.
- Derived guidance: use chips or checkboxes for a handful of quick options (up to about six) and a tag picker above that, so the screen does not become a chip cloud. State the keyboard behavior in a short help text.

## 14. Checklists

Each item names how to check it. The tools: **React Testing Library with user-event** (`render`, `await user.tab()`, `await user.type(...)`, `await user.keyboard('{Enter}')`, queries by role and name, `jest-dom` matchers such as `toBeInvalid`, `toHaveAccessibleName`, `toHaveAccessibleDescription`); **Playwright** (real browser keyboard through `page.keyboard`, screenshots with `toHaveScreenshot`, `page.emulateMedia({ colorScheme: 'dark', reducedMotion: 'reduce', forcedColors: 'active' })`); **axe-core** (`@axe-core/playwright` or `jest-axe`) for names, roles, labels and contrast. jsdom has no layout and unreliable focus ring and selection-on-tab behavior, so tests of select-all, caret position, `:focus-visible` and popups run in Playwright. Derived. ([user-event][tl-userevent], [Playwright keyboard][pw-keyboard], [Playwright emulateMedia][pw-media], [Playwright accessibility][pw-a11y], [axe-core][axe])

### Any field

- [ ] Label above the input, sentence case, no colon; verified in a screenshot of the form.
- [ ] A real `<label for>` (or `Field label`) names the control; `getByRole('textbox', { name: 'Start time' })` finds it (RTL query) and axe reports no `label` violation.
- [ ] Help and error are linked: `toHaveAccessibleDescription` contains both texts (RTL); the control has `aria-invalid` in the error state (`toBeInvalid`).
- [ ] Required: `required` on native controls (or `aria-required`) plus a visible marker; a test submits empty and expects the error.
- [ ] Border contrast 3:1 or a darker bottom edge, computed from the final computed colors (script or axe).
- [ ] Placeholder contrast measured on the computed color with opacity applied, 4.5:1 per theme (script output).
- [ ] The error-on-focus choice (neutral like Fluent, or danger border kept) is recorded and drawn (Playwright screenshot of a focused field with an error).
- [ ] Rest, hover, focus, disabled, error (and pressed, selected where relevant) drawn; Playwright screenshot per state in light and dark.
- [ ] Disabled fields keep label and help readable; an explanation is available when the reason is not obvious.
- [ ] A `maxlength` or documented limit exists where relevant; paste handling tested (`user.paste`).
- [ ] Focus after a failed submit goes to one defined place (first invalid field or the message bar), covered by a test that asserts `document.activeElement`.
- [ ] Validation channel: one of native constraint validation or app messages, not both (search the form for `noValidate`).
- [ ] The focus underline animates in 200 ms and out in 50 ms, and both are about zero under `reducedMotion: 'reduce'` (Playwright, computed `transition-duration`).
- [ ] `autocomplete` tokens set on personal data fields and `off` on amounts and codes (grep the markup).

### Text and search

- [ ] Tab entry leaves the caret at the end (text) or selects all (fast fields); Playwright test presses Tab and reads `selectionStart` and `selectionEnd`; a second test clicks into the field and checks the caret is not forced.
- [ ] Enter submits the form from a single-line field and inserts a line break in a textarea (RTL: `user.type(field, '{Enter}')` and assert `onSubmit` or the value).
- [ ] The default button is the first submit button and every other button has `type="button"` (grep the markup).
- [ ] During IME composition Enter and Esc are ignored (unit test with `isComposing`).
- [ ] Counter tested with props arriving in different orders and with pasted overlong text.
- [ ] Esc restores the last committed value, a second Esc passes to the dialog; test with a field inside a native `<dialog>` in Playwright and assert the dialog's open state after each Esc.
- [ ] The clear button appears only in search fields and only with content, and has an accessible name.
- [ ] Search shows recent items on focus, one "no results" line, the result count in a live region and the Esc ladder (test).

### Number, money

- [ ] Parser unit tests cover every row of the tables above plus an invalid and an empty case, and run with the separators of at least two locales.
- [ ] After a failed commit the submit is refused or the value is empty, never the old value (test, section 4).
- [ ] Money is held as integer minor units or a decimal type and rejects extra fraction digits (grep the diff for `parseFloat`, `Number(` and `toFixed` on amounts).
- [ ] The field is not `type="number"` unless the integer-only reasons in section 8 apply; if it is, a test types `e` and `1,5` and checks the behavior.
- [ ] Up/Down, Page, Home/End, wheel-only-when-focused, clamp without wrap: user-event keyboard tests.
- [ ] Step buttons are disabled at the limits while the input remains active, and are not in the tab order.
- [ ] Spin buttons expose `aria-valuemin`, `aria-valuemax`, `aria-valuenow` and `aria-valuetext` (`getByRole('spinbutton')` plus attribute assertions).

### Time, date

- [ ] Parser tables are unit tests; impossible inputs produce a range error that names the valid range, unreadable inputs a format error with an example.
- [ ] End equal to start is an error unless the field says otherwise (test).
- [ ] Dependent fields recompute only after commit (test that typing does not change the end field).
- [ ] Native `type="date"` or `type="time"` is used only where the browser's locale display is acceptable; the stored value is never passed through a UTC `Date` (grep for `new Date(` on date-only strings).
- [ ] Calendar popup: arrows, Page keys, Enter selects, Esc closes without change, focus returns to the field (Playwright).
- [ ] No silent clamp to min or max.

### Choice

- [ ] Component matches the number of options (see section 12).
- [ ] Esc closes without change and does not close the dialog around it; Enter picks; type-ahead works (Playwright in a native `<dialog>`).
- [ ] Combobox roles are right: `getByRole('combobox')`, `aria-expanded` flips, `aria-activedescendant` follows the highlight (RTL).
- [ ] The list is as wide as the field and scrolls beyond about eight items.
- [ ] Multi-select above six values uses a tag picker, and the Backspace behavior is the documented one (test).

## 15. Sources

[f2-field]: https://fluent2.microsoft.design/components/web/react/core/field/usage
[f2-label]: https://fluent2.microsoft.design/components/web/react/core/label/usage
[f2-input]: https://fluent2.microsoft.design/components/web/react/core/input/usage
[f2-button]: https://fluent2.microsoft.design/components/web/react/core/button/usage
[f2-rai]: https://fluent2.microsoft.design/responsible-AI/
[f2-searchbox]: https://fluent2.microsoft.design/components/web/react/core/searchbox/usage
[f2-spin]: https://fluent2.microsoft.design/components/web/react/core/spin/usage
[f2-textarea]: https://fluent2.microsoft.design/components/web/react/core/textarea/usage
[f2-select]: https://fluent2.microsoft.design/components/web/react/core/select/usage
[f2-dropdown]: https://fluent2.microsoft.design/components/web/react/core/dropdown/usage
[f2-combobox]: https://fluent2.microsoft.design/components/web/react/core/combobox/usage
[f2-tagpicker]: https://fluent2.microsoft.design/components/web/react/core/tagpicker/usage
[f2-tag]: https://fluent2.microsoft.design/components/web/react/core/tag/usage
[f2-messagebar]: https://fluent2.microsoft.design/components/web/react/core/messagebar/usage
[wl-textbox]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/text-box
[wl-numberbox]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/number-box
[wl-timepicker]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/time-picker
[wl-datepicker]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/date-picker
[wl-calendardatepicker]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/calendar-date-picker
[wl-datetime]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/date-and-time
[wl-combobox]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/combo-box
[wl-autosuggest]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/auto-suggest-box
[wl-dialogs]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs
[wl-keyboard]: https://learn.microsoft.com/en-us/windows/apps/develop/input/keyboard-interactions
[wl-a11y]: https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview
[wl-geometry]: https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/geometry
[gh-button]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-button/library/src/components/Button/useButtonStyles.styles.ts
[gh-input]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-input/library/src/components/Input/useInputStyles.styles.ts
[gh-field]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-field/library/src/components/Field/useFieldStyles.styles.ts
[gh-fieldcontrol]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-field/library/src/contexts/useFieldControlProps.ts
[gh-label]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-label/library/src/components/Label/useLabelStyles.styles.ts
[gh-link]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-link/library/src/components/Link/useLinkStyles.styles.ts
[gh-textarea]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-textarea/library/src/components/Textarea/useTextareaStyles.styles.ts
[gh-searchbox]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-search/library/src/components/SearchBox/useSearchBox.tsx
[gh-spinbutton]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-spinbutton/library/src/components/SpinButton/useSpinButtonStyles.styles.ts
[gh-spinbuttonlogic]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-spinbutton/library/src/components/SpinButton/useSpinButton.tsx
[gh-combobox]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-combobox/library/src/utils/useTriggerSlot.ts
[gh-keyactions]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-combobox/library/src/utils/dropdownKeyActions.ts
[gh-tagpickerinput]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tag-picker/library/src/components/TagPickerInput/useTagPickerInput.tsx
[gh-taggroup]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tags/library/src/components/TagGroup/useTagGroupStyles.styles.ts
[gh-menu]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-menu/library/src/components/MenuItem/useMenuItemStyles.styles.ts
[html-implicit]: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission
[mdn-label]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label
[mdn-required]: https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/required
[mdn-ariainvalid]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid
[mdn-errormessage]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-errormessage
[mdn-autocomplete]: https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
[mdn-inputmode]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inputmode
[mdn-enterkeyhint]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/enterkeyhint
[mdn-focusvisible]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
[mdn-dialog]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog
[mdn-popover]: https://developer.mozilla.org/en-US/docs/Web/API/Popover_API
[mdn-maxlength]: https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/maxlength
[mdn-spellcheck]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/spellcheck
[mdn-search]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/search
[mdn-live]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
[mdn-number]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number
[mdn-intl]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat
[mdn-time]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/time
[mdn-date]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
[mdn-select]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select
[mdn-datalist]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist
[govuk-number]: https://technology.blog.gov.uk/2020/02/24/why-the-gov-uk-design-system-team-changed-the-input-type-for-numbers/
[apg-combobox]: https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
[apg-spinbutton]: https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/
[apg-datepicker]: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/
[wcag-135]: https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html
[wcag-141]: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
[wcag-143]: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
[wcag-1411]: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
[wcag-332]: https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html
[tl-userevent]: https://testing-library.com/docs/user-event/intro
[pw-keyboard]: https://playwright.dev/docs/api/class-keyboard
[pw-media]: https://playwright.dev/docs/api/class-page#page-emulate-media
[pw-a11y]: https://playwright.dev/docs/accessibility-testing
[axe]: https://github.com/dequelabs/axe-core
