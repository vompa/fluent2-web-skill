# Accessibility: keyboard, focus, screen readers, contrast, motion

Read this file when you design or review keyboard navigation, focus order and restoration, landmarks and region switching, shortcuts, screen-reader support (the accessibility tree), contrast, forced-colors mode, zoom and text scaling or reduced motion in a web app. Accessibility applies from the first sketch; it is a build requirement, not a late audit.

Two paths apply. **Fluent UI React v9** components ship roles, keyboard handling (through the Tabster library), forced-colors styles and reduced-motion rules, so your job is to use them correctly, name them, and test the result. **Own components** projects build those parts from semantic HTML and the WAI-ARIA Authoring Practices (APG) and borrow Fluent's values. Mapping from Fluent concepts to HTML, CSS, tokens and tests: [web-mapping.md](web-mapping.md); v8 to v9 names and pitfalls: [fluent-ui-react-notes.md](fluent-ui-react-notes.md).

## Contents

1. [Standard and targets](#1-standard-and-targets)
2. [Keyboard as the primary model](#2-keyboard-as-the-primary-model)
3. [Focus order and restoration](#3-focus-order-and-restoration)
4. [Regions, landmarks and skip links](#4-regions-landmarks-and-skip-links)
5. [Shortcuts](#5-shortcuts)
6. [Screen readers and the accessibility tree](#6-screen-readers-and-the-accessibility-tree)
7. [Accessible names: scan and fix](#7-accessible-names-scan-and-fix)
8. [Contrast, color and text scale](#8-contrast-color-and-text-scale)
9. [Forced colors](#9-forced-colors)
10. [Reduced motion](#10-reduced-motion)
11. [Verification](#11-verification)
12. [Checklist](#12-checklist)
13. [Sources](#13-sources)

## 1. Standard and targets

- Fluent components meet or exceed WCAG 2.1 AA. WCAG 2.2 AA is stricter and the target for a new product. ([Accessibility][f2-a11y], [WCAG 2.2][wcag22])
- Text contrast 4.5:1; large text (18.5 px bold or 24 px regular and above) 3:1; non-text elements, icons, focus indicators and field borders 3:1. Disabled controls are exempt. ([Accessibility][f2-a11y], [WCAG 1.4.3][wcag-143], [WCAG 1.4.11][wcag-1411])
- A lighter third text tone must meet these ratios too: measure it, with the element's `opacity` applied, rather than trusting its token name, and restrict it to large text or icons if it falls short. "Secondary" colors are the usual place where contrast quietly fails. Derived.
- The criteria new in WCAG 2.2 at level A and AA, and what each means for the UI (Derived summaries of the success criteria):
  - 2.4.11 Focus Not Obscured (Minimum), AA: a focused element is not completely hidden by author-created content such as a sticky header, cookie banner or chat widget. Give scrollable containers `scroll-padding-top` (and bottom) at least the height of the sticky bar, and test by tabbing through the whole page with the sticky elements present. ([WCAG 2.4.11][wcag-2411])
  - 2.5.7 Dragging Movements, AA: anything done by dragging (reorder, resize, move a calendar entry) can also be done with a single pointer without dragging (buttons, menu, click-to-place) and by keyboard. ([WCAG 2.5.7][wcag-257])
  - 2.5.8 Target Size (Minimum), AA: pointer targets are at least 24 by 24 CSS px, or have enough spacing around them (a 24 px circle centered on a smaller target must not touch another target); inline links in text and native browser controls are exempt. Fluent's 32 px control height passes; small icon buttons (16 or 20 px) and dense table actions are where it fails. ([WCAG 2.5.8][wcag-258])
  - 3.2.6 Consistent Help, A: where help (contact, chat, FAQ link) appears on several pages, it sits in the same relative place. ([WCAG 3.2.6][wcag-326])
  - 3.3.7 Redundant Entry, A: do not make users re-enter information already given in the same process; prefill it or let them pick it (a shipping address copied to billing). ([WCAG 3.3.7][wcag-337])
  - 3.3.8 Accessible Authentication (Minimum), AA: no step that needs a cognitive test (remembering a password, solving a puzzle) unless an alternative exists; allow paste and password managers (`autocomplete="current-password"`, `autocomplete="one-time-code"`), never block paste. ([WCAG 3.3.8][wcag-338])
  - 2.4.12 Focus Not Obscured (Enhanced) and 2.4.13 Focus Appearance are AAA; treat their intent (a visible, thick, contrasting ring) as a good default. ([WCAG 2.4.13][wcag-2413])
- Reflow: usable at 400 percent zoom (a 320 CSS px wide viewport) without two-dimensional scrolling, except for content that needs it (data tables, maps, charts); text can be resized to 200 percent without loss. ([Accessibility][f2-a11y], [WCAG 1.4.10][wcag-1410], [WCAG 1.4.4][wcag-144])

## 2. Keyboard as the primary model

- Everything operable with a pointer is operable with the keyboard (WCAG 2.1.1). Tab order equals reading order; only operable elements are tab stops. Inside composite widgets (radio groups, tabs, menus, toolbars, listboxes, grids) use arrow keys for inner navigation so the widget is one tab stop; the roving tabindex pattern (one child `tabindex="0"`, the others `-1`) or `aria-activedescendant` does that. ([APG keyboard interface][apg-keyboard], [WCAG 2.1.1][wcag-211])
- Use native elements first: `<button>` (Enter and Space), `<a href>` (Enter), `<input>`, `<select>`, `<details>`. A `div` with `onClick` is not focusable and has no role. If a custom control cannot be avoided, it needs `role`, `tabindex`, a name, Enter and Space handlers, and focus styles; that is more work than the native element. ([MDN keyboard accessibility][mdn-keyboard])
- Key meanings: Tab and Shift+Tab move between operable elements; Space activates buttons and toggles checkboxes (not while typing text); Enter activates buttons and links and submits forms; Esc cancels only transient surfaces (menus, popovers, dialogs) and never page navigation; Home and End go to first and last in a composite widget; Page Up and Down move by page; text input outranks all other keys. ([APG keyboard interface][apg-keyboard])
- Initial focus goes to the first or most common element, never to a destructive action ([dialogs-and-messages.md](dialogs-and-messages.md), section 2).
- No keyboard traps (WCAG 2.1.2): focus can always leave a component with the standard keys, apart from a modal dialog, where Esc leaves. A third-party widget (an embedded map, an editor) that swallows Tab is a trap unless it documents an exit. ([WCAG 2.1.2][wcag-212])
- Focus visible (WCAG 2.4.7): never `outline: none` without a replacement. Use `:focus-visible` so the ring shows for keyboard use and not after a mouse click; Fluent default is a 2 px ring with a transparent outline layer so forced-colors mode can paint it (section 9). The ring needs 3:1 against both the element and its background. ([WCAG 2.4.7][wcag-247], [MDN :focus-visible][mdn-focusvisible])
- Esc and nested key handlers: a parent that handles Esc, Enter or arrows in the capture phase (`addEventListener(..., true)`) runs before the focused field, so the field never restores its value and the panel closes with the edit lost. Handle keys in the bubble phase, or let the parent ask first whether the focused field has a pending change (an attribute or state such as `data-pending`, true while the text differs from the committed value or its list is open) and leave the key to the field while it is true. Derived from the Esc ladder in [inputs.md](inputs.md).
- Field-level behavior (select on Tab, Esc ladder, commit on Enter) is in [inputs.md](inputs.md).
- Pointer gestures: anything that needs a path or multi-point gesture also needs a single-pointer alternative (WCAG 2.5.1), and a pointer action fires on release, not on press, so it can be cancelled (WCAG 2.5.2). ([WCAG 2.5.1][wcag-251])

## 3. Focus order and restoration

- Logical reading order, headings in a sensible hierarchy (one `<h1>`, no skipped levels), a Z-shaped focus path (left to right, top to bottom). ([Accessibility][f2-a11y], [WCAG 2.4.3][wcag-243])
- Focus order equals DOM order. Tab follows the order of the elements in the document, not the order on screen. CSS `order`, `flex-direction: row-reverse`, `grid` placement (`grid-area`, `grid-row`) and absolute positioning change what is painted and do not change tab order; so a footer written before the content in the DOM, or a sidebar written after it but painted first, sends keyboard and screen-reader users to the wrong place. Check the DOM, not the screenshot. Avoid positive `tabindex` values: they pull elements to the front of the order and are almost always a bug (`tabindex="0"` and `-1` only). ([MDN tabindex][mdn-tabindex], [MDN CSS order][mdn-order], [WCAG 1.3.2][wcag-132])
- Focus must not get lost when a temporary element closes: return it to the invoker after closing a menu, list, popover or dialog. The native `<dialog>` opened with `showModal()` does it for you; a popover with `popover` light dismiss returns focus as well; custom surfaces store `document.activeElement` before opening and call `.focus()` on it after closing. ([Accessibility][f2-a11y], [Dialog][f2-dialog])
- Focus loss on removal: when the focused element is removed from the DOM or hidden (a panel that closes itself via its own button, a row deleted by its own button, a list that re-renders with new keys), the browser moves focus to `<body>` and the next Tab starts at the top of the page, and key handlers attached to your view never fire because the event target is outside it. Move focus on purpose to the next row, the previous row, the list heading or the invoker. In React, a changed `key` or a parent re-created on every render unmounts the element and drops focus; keep element identity stable. Reproduce it in a test: close the panel by click, then press an arrow key and assert that `document.activeElement` is inside the view. Derived.
- After a route change in a single-page app, move focus to the page `<h1>` (with `tabindex="-1"`) or `<main>` and update `document.title`, so the new page is announced ([navigation.md](navigation.md), section 2). Derived from WCAG 2.4.2 and 2.4.3.
- Write the focus order as a numbered list in the pull request for every new screen. Derived from Fluent's advice to specify focus order and screen-reader notes in the design. ([Accessibility][f2-a11y]) Generate the list instead of typing it: a Playwright test presses Tab, records the accessible name of `document.activeElement` at each step and stops when an element repeats; the printed list is the one in the pull request, and the same test pins it afterwards. Derived.
- Hidden is not focusable: content that is visually collapsed must be out of the tab order (`display: none`, `hidden`, `visibility: hidden` or `inert`), not just `opacity: 0` or moved off-screen. The `inert` attribute removes a whole subtree from focus, clicks and the accessibility tree; use it for the page behind an overlay drawer and for off-screen panels. ([MDN inert][mdn-inert])
- Sticky headers and footers can cover the focused element (WCAG 2.4.11); set `scroll-padding` as in section 1.

## 4. Regions, landmarks and skip links

- Use landmarks so screen-reader users can jump between large regions: `<header>` (as page banner), `<nav>`, `<main>` (exactly one), `<aside>`, `<footer>` (as contentinfo) and, for other regions that matter, `<section>` with an accessible name or `role="region"` with `aria-label`. When a landmark type appears more than once (two `<nav>`), give each a distinct `aria-label` ("Main", "Breadcrumb"). Do not make everything a landmark: too many regions is noise. ([APG landmarks][apg-landmarks], [MDN landmark roles][mdn-landmarks])
- A skip link is the first focusable element on the page: `<a href="#main">Skip to content</a>`, visible when focused, and the target (`<main id="main" tabindex="-1">`) receives focus. In an app shell with a persistent navigation pane or toolbar, it saves a long Tab walk on every page. ([WCAG 2.4.1][wcag-241])
- F6 region cycling: browsers use F6 to move between the address bar and the page, not between regions of the page; screen readers provide landmark navigation instead (NVDA: D for the next landmark; VoiceOver: rotor). An app with a custom shell (calendar, editor, panes) may add its own region cycling as an app-level `keydown` handler on `document` (Derived, not a Fluent rule). The recipe, if you do it:
  - Mark each region with an attribute (for example `data-region="Navigation"`) that also supplies its `aria-label`, so the screen reader announces where focus lands.
  - Order the regions as they appear on screen (top to bottom, then left to right), not in DOM order, when the two differ.
  - A page that declares no region counts as one region, so F6 still moves focus into it instead of doing nothing.
  - Each region has an explicit focus target. When the region handles keys itself (calendar, canvas, custom list), the region element is the target (`tabindex="-1"`, focusable by script) and focus on its first button would send the arrow keys to the wrong handler. Without a target, use the first focusable descendant.
  - Check the F6 key against browser behavior (it moves focus to the address bar in most browsers, so you must `preventDefault()` in the handler and offer the same function through a menu or a documented shortcut); announce the shortcut in the shortcut list. Test with real keys: press F6 repeatedly and compare the region names with the expected order, including wrap-around; Shift+F6 runs it in reverse. Derived.
- Headings are the other main navigation: a heading per region, in order (`<h2>` for a region under `<h1>`), no skipped levels. Do not choose a heading level for its size; style it with CSS. Derived from WCAG 1.3.1 and 2.4.6. ([WCAG 2.4.6][wcag-246])

## 5. Shortcuts

- Accelerators for frequent commands (Ctrl+letter on Windows and Linux, Cmd+letter on macOS) and visible hints. Show the shortcut in the tooltip or menu text and expose it on the control with `aria-keyshortcuts="Control+S"` (it announces the shortcut; it does not bind it; the value uses key names such as `Control`, `Shift`, `Alt`, `Meta`). ([MDN aria-keyshortcuts][mdn-keyshortcuts])
- Every shortcut gets a tooltip or menu text, and every tooltip that names a shortcut matches a real key binding (cross-check in code). Derived.
- Single-character shortcuts (letter keys without a modifier) must be possible to turn off, remap, or act only while the relevant component has focus; they must also not fire while an input, textarea, select or `contenteditable` element has focus, otherwise they break typing and speech input (WCAG 2.1.4, Character Key Shortcuts). Check `event.target` and `event.isComposing`, and ignore events with modifiers you did not register. Say so in the app's shortcut list, whose layout and rules are in [navigation.md](navigation.md), section 7. ([WCAG 2.1.4][wcag-214])
- Browser and assistive-technology keys are taken (Ctrl+T, Ctrl+W, Ctrl+L, F5, F6, F11, Alt+Left, screen-reader modifier combinations such as Insert or Caps Lock plus a key). Pick combinations that do not collide, and let the app work without any shortcut. Derived.
- Do not use `accesskey` as the main mechanism: its modifier differs by browser and platform and collides with assistive technology. Derived. ([MDN accesskey][mdn-accesskey])

## 6. Screen readers and the accessibility tree

- Browsers build an accessibility tree from the DOM: role, name, description, state and value for each exposed element. Screen readers read that tree, not the pixels. Every interactive element needs a role, a name and its states. Native elements get these for free; custom ones must set them. ([MDN accessibility tree][mdn-a11ytree])
- The accessible name comes from, in order: `aria-labelledby`, `aria-label`, native sources (the `<label>` for an input, text content for a button or link, `alt` for an image, `<caption>` for a table, `<legend>` for a fieldset), then `title` as a last resort. Prefer visible text. A name must contain the visible label text (WCAG 2.5.3 Label in Name) so speech-input users can say what they see. `aria-describedby` adds a description (help text, an error), read after the name. ([Accname spec][accname], [WCAG 2.5.3][wcag-253])
- The first rule of ARIA: do not use ARIA when a native element does the job. A wrong or redundant role confuses assistive technology (`role="button"` on a `<button>`, `role="link"` on a `<div>` with no keyboard support). Roles replace semantics but add no behavior. ([ARIA in HTML][aria-in-html])
- States and properties must track the UI: `aria-expanded`, `aria-selected`, `aria-pressed`, `aria-checked`, `aria-current`, `aria-disabled`, `aria-invalid`, `aria-required`, `aria-busy`. Update them in the same render as the visual change. Expandable headers (accordion, disclosure, menu button) report `aria-expanded` ([data-display.md](data-display.md), section 6).
- Fields: name (label), role, value, required (`required` or `aria-required`), help (`aria-describedby`), error (`aria-invalid="true"` plus `aria-describedby` to the message). Range controls report minimum, maximum, value and unit (`aria-valuemin`, `aria-valuemax`, `aria-valuenow`, `aria-valuetext`). Radio buttons in a native group announce position ("2 of 4") from the DOM. ([Spin button][f2-spin])
- Live regions announce changes without moving focus: `role="status"` (polite) for results, counts and confirmations; `role="alert"` (assertive) for errors that need immediate attention; or `aria-live` set directly. The container must exist in the DOM before the content changes, or the first message is missed. Keep messages short, do not announce every keystroke or tick, and avoid `aria-live="assertive"` except for errors. Fluent UI `MessageBar` and `Toaster` feed a live region for you ([dialogs-and-messages.md](dialogs-and-messages.md), sections 5 and 6). ([MDN live regions][mdn-live])
- Images: informative ones have short `alt` text; decorative ones have `alt=""`. Icon buttons have a name on the button. Inline SVG icons are `aria-hidden="true"` and `focusable="false"`. ([Image][f2-image], [Iconography][f2-icons])
- Language: set `lang` on `<html>` (and on passages in another language) so screen readers choose the right voice (WCAG 3.1.1, 3.1.2). ([WCAG 3.1.1][wcag-311])
- Do not carry meaning by bold, italic or color alone (WCAG 1.4.1); use text, an icon or a pattern as well. ([Text][f2-text], [WCAG 1.4.1][wcag-141])
- Write text that is short, descriptive and self-contained, so each sentence works when read alone. Link text makes sense out of context ("Download the report", not "click here"). ([Accessibility][f2-a11y])
- `aria-hidden="true"` removes an element from the accessibility tree and must never be on, or contain, a focusable element. `display: none` and `hidden` remove it from both view and tree; a visually hidden helper text uses the `.sr-only` pattern (clip and 1 px size), not `display: none`. ([MDN aria-hidden][mdn-ariahidden])

## 7. Accessible names: scan and fix

Names fail quietly: an empty or wrong name looks fine on screen and in a screenshot. Typical causes on the web:

- A button that contains only an icon, an `<img>` without `alt`, or an SVG without a title has no name; a screen reader says "button" or reads the file name.
- A link whose text is a URL or "click here", or several links with the same text ("Read more") that go to different places.
- An input without a `<label>`, with only a placeholder, or with a label that is not associated (`for`/`id` mismatch, or a `<label>` that does not wrap the input). A placeholder is not a name and disappears on input.
- A list row built from `div`s with no content that identifies the row, or a custom control that exposes the wrong text (the first child's text instead of the row's meaning).
- Help and info buttons all called "Help": a screen reader's element list shows names without context, and ten entries called "Help" cannot be told apart. Name the topic ("Help on delivery date") and use the same string for the tooltip, from one localizable resource.

So treat names as something to test, not to review by eye.

- Scan every page with axe-core in an automated test, with the page in each state that matters (dialog open, menu open, error shown): the rules `button-name`, `link-name`, `input-button-name`, `label`, `image-alt`, `aria-input-field-name`, `aria-dialog-name`, `select-name`, `frame-title` and `duplicate-id-aria` fail on empty or missing names. Run it as the owner (highest-permission) role so that every page and control is reachable, and over every route; print all findings at once with the page, the selector and the rule. ([axe rules][axe-rules], [Playwright accessibility testing][pw-a11y])
- axe finds missing names, not wrong ones. Add a name-quality pass: collect the accessible names of all focusable elements (Playwright `page.accessibility` is deprecated; use `locator.ariaSnapshot()` or Chrome DevTools' accessibility tree) and fail on duplicates among controls with the same role in one region, on names that look like a file name or a type name (`.svg`, `[object Object]`, "undefined"), and on a visible label that is not contained in the name (WCAG 2.5.3). Derived. ([Playwright ariaSnapshot][pw-aria-snapshot])
- Buttons with non-text content: derive the name from the first text inside the content where there is one, and set an explicit `aria-label` where there is none (an icon-only button has nothing to derive from). `aria-label` is not translated automatically; take it from the same localization resources as other UI text.
- Fields without a visible label: `aria-labelledby` to the visible label element where there is one (a column header, a nearby heading), an `aria-label` otherwise. A search field with a visible magnifier button still needs a label ("Search appointments").
- Fluent UI React v9: `Field` associates the label, hint and validation message with the control through ids (`aria-labelledby`, `aria-describedby`); wrap every `Input`, `Select`, `Textarea` and similar in a `Field` with a `label`, or pass `aria-label` when no visible label exists. `Tooltip` needs `relationship="label"` for icon buttons whose tooltip is their only name. ([Tooltip types][gh-tooltip-types])
- Required state: assert it in tests with `toHaveAttribute('aria-required', 'true')` or the native `required` attribute, and that the visible asterisk has a text equivalent.
- Names are UI text: they follow [content-design.md](content-design.md) (sentence case, no technical terms, one term per concept) and come from resources, not literals.

## 8. Contrast, color and text scale

- Color is never the only carrier of meaning; calendar or status states also carry text or an icon. Red-green color blindness affects roughly 8 percent of men and 0.5 percent of women. ([Color][f2-color], [WCAG 1.4.1][wcag-141])
- Contrast checks cover every state (rest, hover, pressed, focus, disabled where relevant) and every theme (light, dark, forced colors). Measure with computed styles, not by eye: in a Playwright test read `getComputedStyle` color and background for each state and compute the ratio, or run axe's `color-contrast` rule (it cannot see gradients, images or pseudo-elements, so check those by hand). Fluent's own normal field border fails 3:1 (about 1.53:1 on the light theme) and relies on a darker bottom edge, so a field border needs the same bottom edge or a darker border token; do the measurement for your borders (see [foundations.md](foundations.md)). ([Input source][gh-input], [WCAG 1.4.11][wcag-1411])
- Typography minimums: 12 px Regular, 14 px Semibold (Fluent type ramp). Use relative units (`rem`, `em`) for font sizes, line heights and the spacing that follows text, so that browser font-size settings and zoom work; fixed `px` heights on text containers clip enlarged text. Do not disable zoom (`user-scalable=no`, `maximum-scale`). ([Windows typography][wl-typography], [Accessibility][f2-a11y], [WCAG 1.4.4][wcag-144])
- Text spacing (WCAG 1.4.12): content stays usable when users set line height to 1.5, paragraph spacing to 2 times the font size, letter spacing to 0.12 em and word spacing to 0.16 em; avoid fixed-height boxes and `overflow: hidden` on text. Test by applying those four values with a bookmarklet or injected CSS. ([WCAG 1.4.12][wcag-1412])
- Zoom: test at 200 percent (text still readable and unclipped) and at 400 percent, which is a 320 CSS px viewport: one-column layout, no horizontal page scroll, no loss of function (WCAG 1.4.10). Sticky bars that take a quarter of the viewport at 400 percent are a frequent failure, together with focus obscured (section 1). In Playwright set `viewport: { width: 320, height: 256 }` for the 400 percent case. ([WCAG 1.4.10][wcag-1410])
- Orientation and input purpose: do not lock to portrait or landscape (WCAG 1.3.4), and give personal-data fields the right `autocomplete` token (WCAG 1.3.5, `autocomplete="given-name"`, `"email"`). ([WCAG 1.3.5][wcag-135])

## 9. Forced colors

- Windows contrast themes (and other forced-colors setups) replace your colors with a small system palette. Detect it with `@media (forced-colors: active)`; use system color keywords there (`Canvas`, `CanvasText`, `LinkText`, `ButtonFace`, `ButtonText`, `Field`, `FieldText`, `Highlight`, `HighlightText`, `GrayText`). Hard-coded colors, background images that carry meaning and box-shadows are dropped or overridden, so use design tokens everywhere and test the contrast theme with every view. ([MDN forced-colors][mdn-forcedcolors], [MDN system colors][mdn-systemcolor])
- Things that break in forced colors: borders you made transparent (they disappear unless a real border or `outline` exists), shadows used as borders, SVG icons painted with a fixed `fill` (use `currentColor`), custom focus rings made of `box-shadow`, selected states shown only by background color. Keep a visible transparent `outline` on focus rings and borders (Fluent adds a 2 px transparent outline) so the system theme can paint it. ([Button source][gh-button])
- `forced-color-adjust: none` opts an element out of the override; use it sparingly and only with system colors inside (Fluent's button source uses it for selected and checked states, with `Highlight`, `HighlightText` and `ButtonText`). Do not set it on whole pages. ([MDN forced-color-adjust][mdn-fca], [Button source][gh-button])
- Fluent UI React v9 components carry `@media (forced-colors: active)` rules in their styles (verified in the Button and Input style sources), so they follow the system palette; your own `makeStyles` or CSS on top must do the same wherever it sets colors, borders or backgrounds. Whether a given Fluent UI component fully supports forced colors in your version is (derived, not verified); open the Windows contrast themes (Aquatic, Desert, Dusk, Night sky) or Chrome DevTools' "Emulate CSS media feature forced-colors" and look.
- Add forced colors as a third state next to light and dark when the product requires it; plan time for it, because it exposes every hard-coded color. A Playwright project can run with `forcedColors: 'active'` in the browser context options for a screenshot pass. ([Tokens][f2-tokens], [Playwright emulation][pw-emulation])

## 10. Reduced motion

- Honor `@media (prefers-reduced-motion: reduce)` and also provide an in-app "no motion" switch where users cannot reach the OS setting. When on: transitions and animations go to effectively zero (Fluent source: `transitionDuration: 0.01ms` under `prefers-reduced-motion: reduce`, verified in the Button and Input style sources), no flashing (WCAG 2.3.1: nothing flashes more than three times a second), no sudden jumps, motion only on the focused element, and no information carried by animation alone. ([Motion][f2-motion], [Button source][gh-button], [MDN prefers-reduced-motion][mdn-prm])
- Include every transition in the switch: opacity fades, press scales, slides of drawers and toasts, the input underline, skeleton shimmer, smooth scrolling (`scroll-behavior: smooth`), view transitions and auto-playing carousels or video. A global rule is the safest base:

  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```

  Use the same selector under a `[data-motion="off"]` attribute on `<html>` for the in-app setting. Derived. ([MDN prefers-reduced-motion][mdn-prm])
- Test it: in Playwright call `page.emulateMedia({ reducedMotion: 'reduce' })`, then assert that `getComputedStyle` of the animated elements has transition and animation durations of at most 0.01 ms, for every page. Derived.
- Auto-playing, moving or blinking content that lasts more than 5 seconds needs a pause, stop or hide control (WCAG 2.2.2). ([WCAG 2.2.2][wcag-222])

## 11. Verification

- Keyboard pass on every new screen without a mouse: reach every control, operate it, leave it, see focus at every step, never get trapped, nothing hidden behind a sticky bar. Record the result in the pull request.
- Screen reader pass: NVDA with Firefox or Chrome, or Narrator with Edge, on every new screen: name, role, value, required state and error are announced, landmarks and headings give a usable outline, and the focus order matches your list. Add VoiceOver with Safari when the product serves macOS or iOS users. Add "screen reader checked" to the acceptance list, next to "contrast measured". ([WebAIM screen reader survey][webaim-sr])
- Automated checks: axe-core (through `@axe-core/playwright` or `jest-axe`) over every page and state, Lighthouse accessibility audit in Chrome DevTools or CI, and the browser's accessibility tree (Chrome DevTools, Accessibility panel) for a structural look at names and roles. Automated tools find roughly a third to a half of the issues; they never replace the keyboard and screen reader passes. Lighthouse's score is a subset of axe rules, so a 100 does not mean accessible. ([axe][axe-core], [Lighthouse accessibility][lh-a11y])
- Playwright tests cover Tab order, focus restoration, key handling, live-region text (`toHaveText` on the status region), reduced motion and forced colors emulation, zoom viewports and the name scan. Playwright does not run a screen reader: `ariaSnapshot()` shows the accessibility tree the browser computes, which is close to but not the same as what NVDA says. Treat emulation as a smoke test and keep a manual screen reader pass. ([Playwright accessibility testing][pw-a11y], [Playwright emulation][pw-emulation])
- Test with real input modes as well: keyboard only, touch (target size, no hover dependence), voice control (Windows Voice Access or Voice Control: say the visible label of each control), and browser zoom plus a larger default font size.

## 12. Checklist

- [ ] Every interactive element has an accessible name that contains its visible label (axe rules `button-name`, `link-name`, `label`, `image-alt`; name-quality pass; accessibility tree).
- [ ] Icon-only buttons, info and help buttons name their target ("Help on <topic>"); required state is exposed (`required` or `aria-required`) (test).
- [ ] Native elements are used where they exist; ARIA roles are only on custom widgets and match the APG pattern (review, axe rules `aria-allowed-role`, `aria-required-attr`).
- [ ] Tab order matches reading order and DOM order; numbered list in the PR, generated by a Playwright Tab walk and pinned by a test; no positive `tabindex`; no CSS `order` or grid placement that contradicts the DOM (review the CSS, run the walk).
- [ ] Arrow keys navigate inside groups; each group is one tab stop (keyboard test).
- [ ] Focus returns to the invoker after every transient surface closes (test per surface).
- [ ] Focus is never lost when the focused element is removed or hidden (test: close a panel or delete a row, assert `document.activeElement` is not `body`).
- [ ] No focus trap outside modal dialogs; Esc leaves modals (keyboard pass).
- [ ] Focus is visible on every control, ring contrast 3:1, not covered by sticky bars (screenshot of each focus state; tab through with the sticky header present).
- [ ] Esc in an edited field restores the value before an enclosing panel closes (test: edit, press Esc, assert old value and panel still open; press Esc again, assert closed).
- [ ] Landmarks: one `<main>`, `<nav>` elements labelled uniquely, skip link works (accessibility tree or `getByRole('navigation', { name })`; Tab once and activate the link).
- [ ] If the app adds region cycling (F6): regions are cycled in screen order, each has a name and a focus target, a page without regions counts as one, and the key does not clash with the browser (test with real keys).
- [ ] Shortcuts appear in tooltips and `aria-keyshortcuts`; no tooltip names a shortcut that does not exist (cross-check).
- [ ] Letter-key shortcuts do not fire while a text field has focus and can be turned off or remapped (Playwright: type the letter in a field; WCAG 2.1.4), and the shortcut list says so ([navigation.md](navigation.md), section 7).
- [ ] Contrast measured for text (4.5:1), large text and non-text (3:1) in all themes and states (computed-style script plus axe `color-contrast`).
- [ ] Pointer targets are at least 24 by 24 CSS px or spaced (WCAG 2.5.8); drag actions have a non-drag alternative (WCAG 2.5.7) (review and test).
- [ ] No meaning is carried by color or emphasis alone (review plus grayscale screenshot).
- [ ] Layout works at 200 percent text and at 400 percent zoom (320 px viewport) without clipping or horizontal page scroll; text spacing override does not clip (Playwright at `320 x 256`).
- [ ] Reduced-motion rule zeroes all transitions and animations on every page (Playwright with `reducedMotion: 'reduce'`).
- [ ] Forced colors reviewed on every view (Playwright `forcedColors: 'active'` screenshots or Windows contrast themes), or the limitation documented.
- [ ] `lang` is set; page titles are unique and change on route change; headings form a sensible outline (axe rules `html-has-lang`, `document-title`, `heading-order`).
- [ ] Help placement is consistent (3.2.6), repeated data is not asked twice (3.3.7), paste and password managers work (3.3.8) (review).
- [ ] Screen reader pass recorded for each new screen.

## 13. Sources

[f2-a11y]: https://fluent2.microsoft.design/accessibility
[f2-color]: https://fluent2.microsoft.design/color
[f2-motion]: https://fluent2.microsoft.design/motion
[f2-tokens]: https://fluent2.microsoft.design/design-tokens
[f2-icons]: https://fluent2.microsoft.design/iconography
[f2-dialog]: https://fluent2.microsoft.design/components/web/react/core/dialog/usage
[f2-spin]: https://fluent2.microsoft.design/components/web/react/core/spin/usage
[f2-image]: https://fluent2.microsoft.design/components/web/react/core/image/usage
[f2-text]: https://fluent2.microsoft.design/components/web/react/core/text/usage
[wl-typography]: https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/typography
[wcag22]: https://www.w3.org/TR/WCAG22/
[wcag-132]: https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html
[wcag-135]: https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html
[wcag-141]: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
[wcag-143]: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
[wcag-144]: https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
[wcag-1410]: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
[wcag-1411]: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
[wcag-1412]: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
[wcag-211]: https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
[wcag-212]: https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html
[wcag-214]: https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html
[wcag-222]: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
[wcag-241]: https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html
[wcag-243]: https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
[wcag-246]: https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html
[wcag-247]: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
[wcag-2411]: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
[wcag-2413]: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
[wcag-251]: https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html
[wcag-253]: https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
[wcag-257]: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html
[wcag-258]: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
[wcag-311]: https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html
[wcag-326]: https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html
[wcag-337]: https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html
[wcag-338]: https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html
[apg-keyboard]: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
[apg-landmarks]: https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/
[aria-in-html]: https://www.w3.org/TR/using-aria/
[accname]: https://www.w3.org/TR/accname-1.2/
[mdn-keyboard]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Keyboard-navigable_JavaScript_widgets
[mdn-focusvisible]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
[mdn-tabindex]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/tabindex
[mdn-order]: https://developer.mozilla.org/en-US/docs/Web/CSS/order
[mdn-inert]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert
[mdn-landmarks]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles#landmark_roles
[mdn-keyshortcuts]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-keyshortcuts
[mdn-accesskey]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/accesskey
[mdn-a11ytree]: https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree
[mdn-live]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
[mdn-ariahidden]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-hidden
[mdn-forcedcolors]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors
[mdn-systemcolor]: https://developer.mozilla.org/en-US/docs/Web/CSS/system-color
[mdn-fca]: https://developer.mozilla.org/en-US/docs/Web/CSS/forced-color-adjust
[mdn-prm]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
[axe-rules]: https://dequeuniversity.com/rules/axe/html
[axe-core]: https://github.com/dequelabs/axe-core
[pw-a11y]: https://playwright.dev/docs/accessibility-testing
[pw-aria-snapshot]: https://playwright.dev/docs/aria-snapshots
[pw-emulation]: https://playwright.dev/docs/emulation
[lh-a11y]: https://developer.chrome.com/docs/lighthouse/accessibility/scoring
[webaim-sr]: https://webaim.org/projects/screenreadersurvey10/
[gh-button]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-button/library/src/components/Button/useButtonStyles.styles.ts
[gh-input]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-input/library/src/components/Input/useInputStyles.styles.ts
[gh-tooltip-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tooltip/library/src/components/Tooltip/Tooltip.types.ts
