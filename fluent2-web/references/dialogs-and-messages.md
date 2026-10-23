# Dialogs, drawers, messages, toasts and progress

Read this file when you build or review confirmation dialogs, side panels (drawers), popovers and info buttons, message bars, toasts, progress bars, spinners or skeleton loading in a web app. It also tells you which surface to use for which kind of message. Project briefs win over Fluent defaults; record deviations.

Two paths apply. **Fluent UI React v9** projects use `Dialog`, `Drawer`, `Popover`, `MessageBar`, `Toaster` and the progress components, which carry roles, focus handling and live regions. **Own components** projects use the platform: the native `<dialog>` element, the Popover API (`popover` attribute), ARIA live regions and `role="progressbar"`, and borrow Fluent's values. Where the two differ, the text says which one it means. Mapping from Fluent concepts to HTML and CSS: [web-mapping.md](web-mapping.md); v8 to v9 names: [fluent-ui-react-notes.md](fluent-ui-react-notes.md).

## Contents

1. [Choosing the surface](#1-choosing-the-surface)
2. [Dialog](#2-dialog)
3. [Drawer (side panel)](#3-drawer-side-panel)
4. [Popover and info label](#4-popover-and-info-label)
5. [Message bar](#5-message-bar)
6. [Toast](#6-toast)
7. [Progress, spinner, skeleton](#7-progress-spinner-skeleton)
8. [Checklists](#8-checklists)
9. [Sources](#9-sources)

## 1. Choosing the surface

Use the least intrusive surface that still does the job (Derived from the component guidance below):

| Situation | Surface |
| --- | --- |
| Input is invalid at one place | Field error at the field. Never a dialog. |
| A persistent, page-level condition the user must know about or fix | Message bar |
| A short confirmation of the user's own, completed action | Toast |
| A decision before data loss or a destructive action | Alert dialog |
| Work in a side context next to the content | Drawer (inline) |
| Optional, short explanation next to a control | Popover or tooltip |
| A long-running operation | Progress bar; spinner for short blocking waits |

A toast disappears, so it must not carry information the user cannot find elsewhere. Errors and warnings therefore belong in a message bar, not in a toast. ([Toast][f2-toast], [Message bar][f2-messagebar])

## 2. Dialog

Size and surface (Fluent default, source): padding 24, gap 8 between parts, radius 8, shadow 64, 1 px transparent border, max width 600, title 20/26 Semibold, backdrop `rgba(0,0,0,0.4)`, at most three footer actions. A brief may choose its own width and radius (for example 420 wide, radius 12, backdrop 0.45); that is fine when recorded. On narrow viewports let the dialog fill the width minus a gutter and scroll its content, not the page. ([Dialog source][gh-dialogsurface], [Dialog constants][gh-dialogconst])

Choose the technology:

- Own components: the native `<dialog>` opened with `showModal()`. The browser puts it in the top layer, renders `::backdrop`, makes everything outside inert (not focusable, not clickable, hidden from assistive technology), fires `cancel` on Esc, moves focus into the dialog and restores it to the previously focused element on close. That replaces a focus-trap library. Do not use `show()` for a modal dialog and do not toggle the `open` attribute by hand, because that skips the modal behavior. ([MDN dialog][mdn-dialog], [HTML spec dialog][html-dialog])
- Fluent UI React v9: `Dialog` (props `open`, `onOpenChange`, `modalType`, `inertTrapFocus`, `unmountOnClose`) with `DialogTrigger`, `DialogSurface`, `DialogBody`, `DialogTitle`, `DialogContent` and `DialogActions`. The surface is an element with `role="dialog"` (`role="alertdialog"` for `modalType="alert"`) and `aria-modal` unless non-modal, labelled by the title unless you pass `aria-label`. ([Dialog types][gh-dialog-types], [DialogSurface source][gh-dialogsurface-hook])
- Fluent UI `Dialog` traps focus with a script by default. Set `inertTrapFocus` to get the HTML-spec behavior where outside elements become inert; the type documentation describes it as the standard behavior of the `dialog` element's `showModal()`. Prefer it where your supported browsers allow `inert`. ([Dialog types][gh-dialog-types])
- Either way: a dialog needs an accessible name (the title, via `aria-labelledby`, or `aria-label`) and, for a dialog that mainly asks a question, `aria-describedby` pointing at the message text. ([APG dialog][apg-dialog])

Kinds and dismissal:

- Modal: closes by outside click, Esc or footer action; without a Cancel button show a close "x". Non-modal: close "x" at top right, Esc, footer (not outside click). Alert: only the footer buttons close it; use it solely for data loss or destructive actions. ([Dialog][f2-dialog])
- Fluent UI: `modalType` is `modal` (default), `non-modal` or `alert`; `onOpenChange` reports the cause in `data.type` as `escapeKeyDown`, `backdropClick` or `triggerClick`, so you can veto a close (for example when unsaved input exists). ([Dialog types][gh-dialog-types])
- Native: Esc raises `cancel` and then `close`. Call `preventDefault()` on `cancel` for an alert dialog or to ask first. Browsers may stop honoring repeated prevention of Esc as an anti-abuse measure, so give an alert dialog a visible Cancel button as well. A click on the backdrop is not special: it is a click on the `<dialog>` element itself (check that the event target is the dialog and the pointer is outside its content box), or use the `closedby` attribute where supported (`any`, `closerequest`, `none`; support is recent, derived, not verified for your browser matrix). Use `<form method="dialog">` for buttons that close with a `returnValue`. ([MDN dialog][mdn-dialog])
- Never nest dialogs; at least one operable element; header and footer stay fixed while the content scrolls (`position: sticky` or a flex column with `overflow: auto` on the content). A confirmation that opens from a drawer is the one common stacking case; Fluent UI gives nested dialogs a transparent backdrop. ([Dialog][f2-dialog], [DialogSurface types][gh-dialogsurface-types])
- Esc equals the close button and yields "no action". Do not use a dialog for field validation.

Focus:

- On open, focus moves inside; on close, it returns to the element that opened it. The native `<dialog>` does both. Fluent UI `Dialog` does it when opened through a `DialogTrigger`; when you control `open` yourself without a trigger, return focus in code (store `document.activeElement` before opening; derived, not verified for every Fluent UI version, so test it). ([Dialog][f2-dialog], [MDN dialog][mdn-dialog])
- Where initial focus lands depends on the question, not on which button is primary. A dialog with input fields focuses the first field. A neutral confirmation focuses the primary button, which is the default button: it gets brand styling and answers Enter. A destructive question ("Delete ...?", "Discard changes?") puts initial focus and Enter on the safe action, "Cancel" or "Keep editing", and the destructive button needs a deliberate Tab and press. Esc equals Cancel in every case. The primary button stays the one the layout highlights; only focus moves to the safe one.
- Native: put the `autofocus` attribute on the element that should receive initial focus; without it the browser picks the first focusable element, which is often the destructive button if the footer is first in the DOM. Fluent UI: put `autoFocus` on the element (React renders `autofocus`) and confirm in the running dialog which element is focused (derived, not verified; test it).
- Initial focus never lands on a destructive control. The shortcut "focus the primary action" is wrong for destructive questions.
- After closing any transient surface (menu, popover, list), focus must not be lost. If the element that had focus is removed from the DOM, focus falls back to `<body>` and the next Tab starts at the top of the page; move focus deliberately to the invoker or the nearest sensible element. ([Accessibility][f2-a11y], [WCAG 2.4.3][wcag-focus-order])
- Scroll lock: a modal dialog should not let the page scroll behind it. The native top layer does not lock scrolling by itself; set `overflow: hidden` on the document while it is open, or use `overscroll-behavior: contain` on the dialog (Derived). Fluent UI does not promise to lock scroll either (derived, not verified).

Content:

- Title states the main point, sentence case, no final punctuation except a question mark, never just "Error". Text puts the consequence first and does not repeat the title. Buttons are the concrete answer to the title in one or two words. ([Dialog][f2-dialog])
- Example: title "Delete this appointment permanently?", text "After this it is no longer in the calendar.", buttons "Delete" (destructive) and "Cancel" (safe). Not "Yes", "No" or "OK". Derived.
- Button order and the primary button: see [buttons-and-selection.md](buttons-and-selection.md). In `DialogActions`, `position` is `start` or `end` and `fluid` stacks the buttons at narrow widths. ([DialogActions types][gh-dialogactions-types])

## 3. Drawer (side panel)

- Inline (next to content, no dim) or overlay (modal, dimmed). Structure: header (title, close, quick actions), body, footer (primary button at the start). Header and footer stay fixed. Four widths: small (default), medium, large, full. Warn before data loss on close; keep multi-step flows to two or three steps; show an error as a message bar at the top of the drawer; navigation drawers sit on the left, notification drawers on the right. ([Drawer][f2-drawer])
- Fluent UI React v9: `Drawer` with `type="overlay"` or `type="inline"`, or the specific `OverlayDrawer` and `InlineDrawer`; parts are `DrawerHeader`, `DrawerHeaderTitle`, `DrawerBody` and `DrawerFooter`. Props: `position` (`start`, `end`, `bottom`), `size` (`small` 320 px, `medium` 592 px, `large` 940 px, `full` 100vw), `open`, `onOpenChange`. `OverlayDrawer` wraps `Dialog` and takes `modalType` and `inertTrapFocus`, so the dialog rules in section 2 apply to it: name, focus in, focus back, Esc. ([Drawer base types][gh-drawer-types], [OverlayDrawer types][gh-overlaydrawer-types])
- Own components: an overlay drawer is a modal dialog styled as a side sheet; use `<dialog>` with `showModal()` and a slide transition, and zero the transition under `prefers-reduced-motion`. An inline drawer is a `<aside aria-label="...">` landmark in the page layout, not a dialog; it needs no focus trap.
- An inline side panel needs no overlay shadow; a left or right border is enough. ([Elevation][f2-elev])
- Closing a panel or tab that has unsaved changes should ask "Discard changes?" with "Discard" and "Keep editing" (Derived); this is a destructive question, so initial focus sits on "Keep editing" (section 2, Focus). ([Drawer][f2-drawer])
- Responsive (Derived): an inline drawer that would squeeze the content below a usable width should switch to overlay; an overlay at `full` size on a phone is a dialog that fills the screen, with the same focus rules.

## 4. Popover and info label

- Popover: a small surface at its trigger. Never for essential information. Do not nest popovers; Esc closes; trap focus when interactive; limit size and scroll in one direction; a "learn more" link goes at the bottom. ([Popover][f2-popover])
- Own components: the Popover API. Give the surface the `popover` attribute and a button `popovertarget="id"`; `popover="auto"` (default) gives light dismiss (click outside or Esc closes it) and closes other auto popovers, `popover="manual"` needs explicit `hidePopover()`. The browser puts it in the top layer and returns focus to the invoker on close for light-dismiss. It does not trap focus and adds no role: add `role="dialog"` with a name if it holds interactive content, and move focus into it yourself. Anchor it with CSS anchor positioning where supported, or script positioning otherwise. The invoker button gets `aria-expanded` kept in sync by script (the browser does not set it on `popovertarget` buttons in every browser, derived, not verified). Use `popover` for the info label and menu-like surfaces; use `<dialog>` for anything modal. ([MDN Popover API][mdn-popover])
- Fluent UI React v9: `Popover` with `PopoverTrigger` and `PopoverSurface`; props include `open`, `onOpenChange`, `trapFocus`, `withArrow`, `positioning`, `openOnHover`, `size`. With `trapFocus` the surface renders `role="dialog"` and `aria-modal`; without it, `role="group"`. The trigger gets `aria-expanded`. ([Popover source][gh-popover])
- Hover-only popovers fail touch and keyboard users; whatever opens on hover must also open on focus and on click or Enter (WCAG 1.4.13, see [navigation.md](navigation.md), section 6).
- Info label: label plus an info button (small, 20 x 20, at least 2 px away from other controls). Enter opens, Esc closes. More than two or three per area signals a design problem. Content is one or two short sentences with at most one link having concrete text. The info button needs a name that says the topic ("Help on delivery date"), not only "Help". ([Info label][f2-infolabel])
- Fluent UI: `InfoLabel` takes `info` (the content), `label`, and renders an `InfoButton`; it is built on `Popover`. Supply a specific `aria-label` for the info button through the `infoButton` slot (derived, not verified which prop name your version uses; check the `InfoLabel.types.ts` of your version). ([InfoLabel types][gh-infolabel-types])

## 5. Message bar

Sizes (Fluent default, source): min height 36, left padding 12, 1 px border, radius 4, icon 20 with 8 gap; multi-line adds top padding 10 and puts actions below; close "x". A denser brief may use radius 8 and a 16 px icon. Fluent UI offers `shape="square"` for page-level messages and `rounded` (default) for component-level ones. ([Message bar source][gh-messagebar], [MessageBar types][gh-messagebar-types])

Kinds and duties:

- Info (action optional), Success, Warning (does not block; needs a button or link), Error (blocks; needs a button or link). Every bar is dismissible. An unresolved warning or error returns in the next session. The bar never blinks. To make screen readers notice a changed message, close and reopen it. ([Message bar][f2-messagebar])
- Fluent UI React v9: `MessageBar` with `intent` (`info` default, `success`, `warning`, `error`), `layout` (`auto`, `singleline`, `multiline`), optional `politeness`; parts `MessageBarBody`, `MessageBarTitle`, `MessageBarActions`, and `MessageBarGroup` for animated stacks. The root has `role="group"`; the announcement is done through a live region that the component feeds, polite for `info` and assertive for the other intents unless you pass `politeness`. Give the actions real `Button`s and the close button an `aria-label`. ([MessageBar types][gh-messagebar-types], [useMessageBar][gh-usemessagebar])
- Own components: render the bar inside a container that exists in the DOM before the message appears. Use `role="status"` (polite live region) for info and success, and `role="alert"` (assertive) for warning and error. Do not use `role="alert"` for routine messages: it interrupts the screen reader. A bar that is present on page load is not announced; it is simply content, so place it where the reading order meets it. ([MDN status role][mdn-status], [MDN alert role][mdn-alert])
- Placement: on a page, under the toolbar inside the content, not above the navigation; in a container at the start or under the title; in tabs directly under the tab strip; in a card under the header; in a form at the top; in a drawer under the header. On a failed submit Fluent gives the bar focus while the fields additionally mark their errors. A form-level rule may instead focus the first invalid field (and use `aria-invalid` plus `aria-describedby` on it, see [inputs.md](inputs.md)); choose one and record it. ([Message bar][f2-messagebar])
- Stacking: sort errors, warnings, successes, info; collapse extras behind a count; "Dismiss all" becomes "Dismiss" when one remains; show a one-line form when space is short. A project may cap the visible bars (for example two, then "n more").
- Text: optional short concrete title in sentence case (not "Warning"); body one or two short sentences, at most two lines of about 100 characters; success without the word "success" or "successfully" and without congratulation; link text starts with a verb, never a URL, never "click here"; the button is usually a verb, with a noun if ambiguous. See [content-design.md](content-design.md). ([Message bar][f2-messagebar])
- Assistive technology: errors and warnings use an assertive live region, info and success a polite one. Use assertive sparingly. The icon is decorative (`aria-hidden`) when the intent is also in the text; otherwise give the bar a title that names the intent. Color and icon alone do not carry the intent (WCAG 1.4.1). ([Message bar][f2-messagebar], [WCAG 1.4.1][wcag-141])

## 6. Toast

- Surface (Fluent default, source): padding 12, radius 4, shadow 8, title 14/20 Semibold, body 14/20 Regular, subtitle 12, icon 16 with 8 gap, action link 12 from the text. Without an action it disappears after 7 s (Fluent 2 guidance) and pauses under the pointer; a toast without an action takes no keyboard focus; a close "x" only if the information can be found again; at most 4 at once with 16 px between; a fixed corner; never for required actions or critical information. A brief may choose another duration (for example 5 s, 8 s with "Undo"), position and radius, and one toast at a time; record that. ([Toast][f2-toast], [Toast source][gh-toast])
- Fluent UI React v9: put one `<Toaster toasterId="..." />` near the app root and dispatch with `const { dispatchToast, dismissToast } = useToastController(toasterId)`; the content is a `Toast` with `ToastTitle`, `ToastBody`, `ToastFooter` and `ToastTrigger`. `dispatchToast(content, { intent, timeout, position, politeness, pauseOnHover, pauseOnWindowBlur, priority })`. The library defaults in the source are not the guidance numbers: `timeout` 3000 ms, `position` `bottom-end`, `pauseOnHover` `false`, `pauseOnWindowBlur` `false`, and the `Toaster` `limit` is unlimited. Set `timeout: 7000`, `pauseOnHover: true`, `pauseOnWindowBlur: true` and `limit: 4` explicitly if you follow the guidance. ([Toast state types][gh-toast-types], [createToaster][gh-createtoaster], [useToastController][gh-toastcontroller])
- Own components: one toast container with `aria-live="polite"` (or `role="status"`) that exists from page load; append the toast element into it. Do not move focus to a toast without an action. A toast with an action must stay until dismissed (WCAG 2.2.1 Timing Adjustable: users can turn off, adjust or extend a time limit; auto-dismissal of a message with a button breaks it). Pause the timer on hover and on focus within, and resume on leave. ([WCAG 2.2.1][wcag-221], [MDN live regions][mdn-live])
- Text: short title; confirmations as past participle with the verb last ("File saved"); progress in progressive form with the noun; combine similar events into one toast; no period; body at most about 60 characters; button one or two words, at most 36 characters. ([Toast][f2-toast])
- Progress in a toast: "X minutes remaining", "X percent complete", "X of Y MB"; determinate duration uses a bar with percent, otherwise a spinner, never both. ([Toast][f2-toast])
- Provide "Undo" in the toast for reversible changes. Derived.
- Reduced motion: slide and fade of the toast go to zero under `prefers-reduced-motion` ([accessibility.md](accessibility.md), section 10).

## 7. Progress, spinner, skeleton

- Progress bar: only for operations longer than a second. Determinate is preferred; indeterminate only for short waits; static when paused. One bar for all steps and it never moves backward. Optional label, status text in progressive form with a trailing ellipsis preceded by a space ("Checking records ..."); avoid time estimates; an error replaces the status text with the problem plus the next step. Thickness 2 px (large 4), radius 4, 0.3 s change; cancel via a close button at the top right. ([Progress bar][f2-progressbar], [Progress source][gh-progress])
- Native and ARIA: `<progress value max>` is a determinate progress bar with the role built in (no `value` makes it indeterminate); with a custom element use `role="progressbar"` with `aria-valuemin`, `aria-valuemax`, `aria-valuenow` (omit `aria-valuenow` when indeterminate) and a name from `aria-label` or `aria-labelledby`. Update `aria-valuenow` rarely enough not to flood a screen reader (for example every 10 percent), or announce completion once in a status region. ([MDN progressbar][mdn-progressbar], [MDN progress][mdn-progress])
- Fluent UI React v9: `ProgressBar` with `value` (0 to `max`, `max` defaults to 1; no value means indeterminate), `thickness` (`medium`, `large`), `color` (`brand`, `success`, `warning`, `error`) and `shape`. The source sets `role="progressbar"`, `aria-valuemin`, `aria-valuemax` and `aria-valuenow`, and takes its name from a surrounding `Field` label. Color alone does not carry the state; the status text does. ([ProgressBar types][gh-progress-types], [useProgressBar][gh-useprogressbar])
- Spinner: from 1 second; centered over the loading area; blocks nothing else; a label from 3 seconds; label concrete, reuses the verb of the triggering action, at most three words, ending with an ellipsis preceded by a space; avoid vague words such as "Loading". Fluent UI `Spinner` has `label`, `labelPosition`, `size` and a `delay` prop (milliseconds after mount before it becomes visible, default 0): set `delay={1000}` to follow the one-second rule. Its root gets `role="progressbar"` by default. For your own spinner use `role="progressbar"` without a value (or `role="status"` with the label text) and hide the decorative SVG with `aria-hidden`. ([Spinner][f2-spinner], [Spinner types][gh-spinner-types], [useSpinner][gh-usespinner])
- Skeleton: for loads over about a second when the structure is known; wave (default) or pulse; start all queries at once; do not skeleton fixed elements. Fluent UI `Skeleton` and `SkeletonItem` set `role="progressbar"` and `aria-busy="true"` on the skeleton root. Own components: put `aria-busy="true"` on the region that is loading and remove it when content arrives; hide the placeholder shapes from assistive technology and do not lose focus after loading (keep the focused element, or move focus to the new content only if the user's action caused the load). ([Skeleton][f2-skeleton], [Skeleton source][gh-skeleton], [MDN aria-busy][mdn-busy])
- Loading must not change the layout beyond what the skeleton reserved: set heights on the skeleton so the content does not shift when it arrives (Core Web Vitals CLS, Derived). ([web.dev CLS][webdev-cls])
- All shimmer and pulse animations stop under `prefers-reduced-motion` ([accessibility.md](accessibility.md), section 10). Fluent UI's indeterminate bar takes `indeterminateMotion={null}` to disable its animation. ([ProgressBar types][gh-progress-types])

## 8. Checklists

### Dialog

- [ ] Width and radius from tokens or the project value; screenshot light and dark, and at 320 px width.
- [ ] Title states the point; buttons are concrete answers; no "OK", "Yes", "No" (grep the strings).
- [ ] The dialog has an accessible name (`aria-labelledby` or `aria-label`) and the right role (`dialog` or `alertdialog`) (`getByRole('dialog', { name })` in Playwright, axe rule `aria-dialog-name`).
- [ ] Opened with `showModal()` or a modal Fluent `Dialog`; the page behind is inert (Playwright: Tab many times, focus never leaves the dialog; click behind does nothing).
- [ ] Initial focus and Enter are on the safe action (Cancel, Keep editing) for a destructive dialog, and on the primary button or first field otherwise; Esc cancels in both (Playwright: open, read `document.activeElement`, press Enter, assert the result is Cancel; open again, press Esc).
- [ ] Focus returns to the invoker after close, also when closed by Esc and by backdrop click (test).
- [ ] Never opens from a dialog (except a documented confirmation); at most one open (test).
- [ ] Field errors never appear in a dialog (review).
- [ ] The page does not scroll behind the dialog (manual check at a long page).

### Message bar and toast

- [ ] Errors and warnings are message bars with an action; toasts carry nothing the user cannot find again.
- [ ] Message text length within the limits (unit test on the strings).
- [ ] Live region: assertive (`role="alert"`) for error and warning, polite (`role="status"`) for info and success; the container exists before the message (test the DOM; screen reader pass).
- [ ] The toast timer pauses on hover and on focus and is the project value (7 s by guidance); with an action it does not time out; reduced motion removes the slide (test with emulated `prefers-reduced-motion`).
- [ ] No more than the project's cap of toasts is visible (test dispatching 6).
- [ ] Unresolved warnings and errors return after reload (test, if the product keeps this rule).

### Progress

- [ ] Determinate bar for known duration; it never goes backward (test with a fake progress source).
- [ ] The progress element has role, min, max, now and a name (axe rules `aria-progressbar-name` and `aria-valid-attr-value`).
- [ ] Spinner or progress appears only after about 1 second (test with a delayed promise and fake timers).
- [ ] Status text uses progressive form and an ellipsis with a space before it.
- [ ] Errors give the problem and the next step, and a way to retry.
- [ ] Loading regions set `aria-busy` and the layout does not shift when content arrives (Lighthouse CLS or a screenshot diff).

## 9. Sources

[f2-toast]: https://fluent2.microsoft.design/components/web/react/core/toast/usage
[f2-messagebar]: https://fluent2.microsoft.design/components/web/react/core/messagebar/usage
[f2-dialog]: https://fluent2.microsoft.design/components/web/react/core/dialog/usage
[f2-drawer]: https://fluent2.microsoft.design/components/web/react/core/drawer/usage
[f2-popover]: https://fluent2.microsoft.design/components/web/react/core/popover/usage
[f2-infolabel]: https://fluent2.microsoft.design/components/web/react/core/infolabel/usage
[f2-progressbar]: https://fluent2.microsoft.design/components/web/react/core/progressbar/usage
[f2-spinner]: https://fluent2.microsoft.design/components/web/react/core/spinner/usage
[f2-skeleton]: https://fluent2.microsoft.design/components/web/react/core/skeleton/usage
[f2-a11y]: https://fluent2.microsoft.design/accessibility
[f2-elev]: https://fluent2.microsoft.design/elevation
[apg-dialog]: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
[wcag-focus-order]: https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
[wcag-141]: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
[wcag-221]: https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html
[mdn-dialog]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog
[html-dialog]: https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element
[mdn-popover]: https://developer.mozilla.org/en-US/docs/Web/API/Popover_API
[mdn-status]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/status_role
[mdn-alert]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/alert_role
[mdn-live]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
[mdn-progressbar]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/progressbar_role
[mdn-progress]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/progress
[mdn-busy]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy
[webdev-cls]: https://web.dev/articles/cls
[gh-dialogsurface]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-dialog/library/src/components/DialogSurface/useDialogSurfaceStyles.styles.ts
[gh-dialogsurface-hook]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-dialog/library/src/components/DialogSurface/useDialogSurface.ts
[gh-dialogsurface-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-dialog/library/src/components/DialogSurface/DialogSurface.types.ts
[gh-dialog-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-dialog/library/src/components/Dialog/Dialog.types.ts
[gh-dialogactions-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-dialog/library/src/components/DialogActions/DialogActions.types.ts
[gh-dialogconst]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-dialog/library/src/contexts/constants.ts
[gh-drawer-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-drawer/library/src/shared/DrawerBase.types.ts
[gh-overlaydrawer-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-drawer/library/src/components/OverlayDrawer/OverlayDrawer.types.ts
[gh-popover]: https://github.com/microsoft/fluentui/tree/master/packages/react-components/react-popover/library/src/components
[gh-infolabel-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-infolabel/library/src/components/InfoLabel/InfoLabel.types.ts
[gh-messagebar]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-message-bar/library/src/components/MessageBar/useMessageBarStyles.styles.ts
[gh-messagebar-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-message-bar/library/src/components/MessageBar/MessageBar.types.ts
[gh-usemessagebar]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-message-bar/library/src/components/MessageBar/useMessageBar.ts
[gh-toast]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-toast/library/src/components/Toast/useToastStyles.styles.ts
[gh-toast-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-toast/library/src/state/types.ts
[gh-createtoaster]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-toast/library/src/state/vanilla/createToaster.ts
[gh-toastcontroller]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-toast/library/src/state/useToastController.ts
[gh-progress]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-progress/library/src/components/ProgressBar/useProgressBarStyles.styles.ts
[gh-progress-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-progress/library/src/components/ProgressBar/ProgressBar.types.ts
[gh-useprogressbar]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-progress/library/src/components/ProgressBar/useProgressBar.tsx
[gh-spinner-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-spinner/library/src/components/Spinner/Spinner.types.ts
[gh-usespinner]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-spinner/library/src/components/Spinner/useSpinner.tsx
[gh-skeleton]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-skeleton/library/src/components/Skeleton/useSkeleton.ts
