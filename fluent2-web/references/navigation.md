# Navigation: tabs, navigation pane, menus, toolbar, tooltips

Read this file when you build or review tab strips, a navigation pane or rail, breadcrumbs, menus and context menus, toolbars with overflow, tooltips and keyboard shortcut lists in a web app. If the project brief or token file defines these components, its values win; Fluent supplies behavior and fallback numbers.

Two paths apply throughout. **Fluent UI React v9** projects (`@fluentui/react-components`) get most of the behavior from the components named below; verify the props, do not re-implement them. **Own components** projects (React, HTML and CSS written in the project) borrow Fluent's values and behavior and build on the WAI-ARIA Authoring Practices (APG) patterns. Where the two differ, the text says which path it means. Mapping from Fluent concepts to HTML, CSS and tokens: [web-mapping.md](web-mapping.md); v8 to v9 names: [fluent-ui-react-notes.md](fluent-ui-react-notes.md).

## Contents

1. [Tabs](#1-tabs)
2. [Navigation pane](#2-navigation-pane)
3. [Breadcrumb](#3-breadcrumb)
4. [Menu and context menu](#4-menu-and-context-menu)
5. [Toolbar and overflow](#5-toolbar-and-overflow)
6. [Tooltip](#6-tooltip)
7. [Shortcut list](#7-shortcut-list)
8. [Checklists](#8-checklists)
9. [Sources](#9-sources)

## 1. Tabs

Appearance:

- Fluent default (source): the selected tab shows a 2 px underline in the brand color (3 px for vertical tabs); hover shows a gray underline on unselected tabs; focus a 2 px ring. Heights small, medium, large are about 32, 44 and 52 (derived, not verified: computed from padding plus the 20 px line height). Padding small 6/6, medium 12/10, large 16/10, text 14/20. ([Tab source][gh-tab])
- A segmented strip (tinted track, selected tab as a raised surface with accent text) is a legitimate compact alternative. Record it as a deviation. ([Tablist][f2-tablist])

Markup and behavior:

- Own components: `role="tablist"` containing `role="tab"` buttons, each with `aria-selected` and `aria-controls`, and a `role="tabpanel"` with `aria-labelledby` pointing at its tab. This is the APG tabs pattern. Use real `<button type="button">` elements for the tabs. ([APG tabs][apg-tabs])
- Fluent UI React v9: `TabList` with `Tab` children; each `Tab` needs a unique `value`, and `TabList` takes `selectedValue` or `defaultSelectedValue` and `onTabSelect`. The package renders the tab buttons and roving focus; you render the panel yourself and hide the inactive ones. `size` is `small`, `medium` or `large`, `vertical` switches the arrow axis, `appearance` is `transparent` (default), `subtle`, `subtle-circular` or `filled-circular`. ([TabList types][gh-tablist-types], [Tab types][gh-tab-types])
- Exactly one tab is active, already on first render. The horizontal strip neither wraps nor scrolls: when not everything fits, put the rest into an overflow menu (section 5). Tabs use text, text plus icon, or icon only, consistently; labels are short and parallel. ([Tablist][f2-tablist])
- Icon-only tabs need an accessible name (`aria-label` on the tab) and a tooltip. In Fluent UI React v9 `Tab` sets `iconOnly` itself when only the `icon` slot is filled; the `aria-label` is still yours to supply. ([Tab types][gh-tab-types])
- One tab stop for the strip (roving tabindex): the active tab has `tabindex="0"`, all others `tabindex="-1"`; Tab lands on the active tab, the next Tab leaves the strip into the panel; Left/Right (Up/Down for vertical tabs) move focus between tabs; Home and End jump to first and last. Fluent UI `TabList` does this for you; own components set `tabindex` in the key handler and move focus with `.focus()`. ([APG tabs][apg-tabs])
- Automatic versus manual activation: in automatic activation, focus moves selection (best when the panel renders instantly); in manual activation, arrows move focus and Space or Enter selects (best when switching costs a request). Fluent UI React v9 defaults to manual: `selectTabOnFocus` is `false` unless you set it. Pick one model per project, state it in the brief, and test it. ([APG tabs][apg-tabs], [TabList types][gh-tablist-types])
- Arrow keys wrap from the last tab to the first in the APG pattern; Fluent's own guidance does not insist on it. Either is acceptable if it is consistent and tested (derived, not verified for Fluent UI's wrap behavior; check in the running component).
- The active tab is exposed as selected (`aria-selected="true"`). Do not also use `aria-current` on tabs. ([APG tabs][apg-tabs])
- Browser shortcuts: Ctrl+Tab, Ctrl+1 to 9 and Ctrl+W belong to the browser. Do not bind them in a web app. An installed desktop-style PWA is no exception for Ctrl+Tab. Derived from the platform; the equivalent desktop shortcuts of WinUI tab views are dropped on the web.
- How many icon-only tabs fit (Derived): count 32 px per tab plus 2 px between tabs, so n tabs need 34 n - 2 px (a 240 px strip holds 7). Show the overflow button only when not all tabs fit, and reserve its width only then. The selected tab and the most recently used tab are always among the visible ones: when the overflow takes the last tabs, swap a hidden selected or last-used tab with the last visible one, because a user who cannot see where they are loses the point of the strip. Tabs with text labels need more width each, so measure them (`ResizeObserver` plus `getBoundingClientRect`, section 5) instead of copying the icon-only count.
- Closeable tabs: ask before closing a tab with unsaved changes (see [dialogs-and-messages.md](dialogs-and-messages.md)). A close button inside a tab is a nested control; give it its own `aria-label` ("Close tab Invoices") and make Delete on the focused tab the keyboard route (Derived from the APG tabs example with deletable tabs). ([APG tabs][apg-tabs])

## 2. Navigation pane

- A list of links to top-level areas, collapsible, at most two levels. Fluent default width 260; inline on wide viewports, overlay (a drawer, see [dialogs-and-messages.md](dialogs-and-messages.md), section 3) below about 640 px. Show the selection. Categories can be an accordion with the chevron in a fixed place. A secondary action (at most one) appears on hover and must be reachable without hover. Tooltips for collapsed items go to the side, not above. ([Nav][f2-nav])
- Markup: `<nav aria-label="Main">` around a list of links (`<ul>` of `<a href>`), the current page marked with `aria-current="page"`. Use real links for navigation between pages or routes, buttons only for in-page actions. If the page has more than one `<nav>`, each needs a distinct `aria-label` ("Main", "Breadcrumb", "Footer"). ([MDN nav][mdn-nav], [MDN aria-current][mdn-aria-current])
- Fluent UI React v9: `Nav` family from `@fluentui/react-nav` (re-exported by `@fluentui/react-components`): `NavDrawer` (with `NavDrawerHeader`, `NavDrawerBody`, `NavDrawerFooter`), `Nav`, `NavItem`, `NavCategory`, `NavCategoryItem`, `NavSubItemGroup`, `NavSubItem`, `NavSectionHeader`, `NavDivider`, `SplitNavItem`, `Hamburger`. `NavItem` sets `aria-current="page"` on the selected item in the source, and `Nav` takes the selection by `selectedValue`. Add an `aria-label` to the surrounding landmark yourself. ([Nav source][gh-nav])
- A narrow icon rail (for example 88 px wide with 12 px labels) is a valid choice. Keep label text at or above 12 px and put tooltips to the right of the item. Derived.
- Switching between main areas: use a short cross-fade rather than sliding large regions, and zero it under `prefers-reduced-motion` (see [accessibility.md](accessibility.md), section 10). ([Motion][f2-motion])
- Single-page apps: after a route change, move focus to the new page heading or the `<main>` container and update `document.title`, otherwise keyboard and screen-reader users stay on the link they pressed. Derived from WCAG 2.4.3 Focus Order and 2.4.2 Page Titled. ([WCAG 2.4.3][wcag-focus-order])

## 3. Breadcrumb

- Use only when the product has real hierarchy of at least two levels. Does not wrap; overflow goes into a menu starting from the second item (the first and last stay visible); long item names are shortened after about 30 characters with a tooltip up to about 80; mark the last item as current; label the navigation landmark. ([Breadcrumb][f2-breadcrumb])
- Markup: `<nav aria-label="Breadcrumb"><ol>` with one `<li>` per level, links for ancestors, and `aria-current="page"` on the last item (a link or plain text). ([APG breadcrumb][apg-breadcrumb])
- Fluent UI React v9: `Breadcrumb` renders a `<nav>` with a default `aria-label` of "breadcrumb" and an `<ol>`; `BreadcrumbItem`, `BreadcrumbButton` (sets `aria-current="page"` when `current`) and `BreadcrumbDivider` are the parts. Override the default label with a translated `aria-label`. The package also exports `partitionBreadcrumbItems` for the overflow split. ([Breadcrumb source][gh-breadcrumb])
- If the app has no hierarchical navigation, do not add one.

## 4. Menu and context menu

- Purpose: a list of actions hidden behind a trigger. Entry kinds: action, checkbox, radio. Put frequent actions first and risky ones last, separated; use group headings and dividers; avoid submenus. Shortcut text is secondary content and must trigger the same action. ([Menu][f2-menu])
- Surface (Fluent default, source): width 138 to 300, padding 4, gap between entries 2, entry min height 32 with padding 6, radius 4, shadow 16. Overlay surfaces in a denser brief may use radius 8. ([Menu source][gh-menu])
- Do not confuse a menu with navigation. A list of links in a dropdown is a disclosure (a button with `aria-expanded` that shows a list of links), not an ARIA menu; `role="menu"` is for application commands. ([APG menu button][apg-menubutton], [APG disclosure navigation][apg-disclosure-nav])
- Own components (APG menu button): trigger `<button aria-haspopup="menu" aria-expanded>`, popup `role="menu"` with `role="menuitem"`, `menuitemcheckbox` or `menuitemradio` children, which are not in the tab order (`tabindex="-1"`, focus moved by script).
- Fluent UI React v9: `Menu` wraps `MenuTrigger` (the button), `MenuPopover` (the surface) and `MenuList` (the list); entries are `MenuItem`, `MenuItemCheckbox`, `MenuItemRadio`, with `MenuGroup`, `MenuGroupHeader` and `MenuDivider` for structure. `MenuTrigger` sets `aria-haspopup="menu"` and `aria-expanded` on its child. Wrap a plain button child; set `disableButtonEnhancement` only when the child is already a proper button. ([Menu types][gh-menu-types], [MenuTrigger source][gh-menutrigger])
- Keyboard: open with Enter, Space or Down at the trigger (Down opening the menu is the APG convention; Fluent UI behavior is derived, not verified, check in the running component); inside the popup Up and Down move between entries and wrap, Home and End jump, typing a letter jumps to a matching entry (type-ahead), Esc closes and returns focus to the trigger, Tab closes the menu. A submenu opens with Right and closes with Left. ([APG menu button][apg-menubutton])
- Context menu: listen for the `contextmenu` event, which browsers also raise for the Menu key and Shift+F10, so one handler covers pointer and keyboard; call `preventDefault()` only on elements that really have a menu, never on the whole page, and keep the browser's menu available on text fields and links where users expect it (Derived). Position the popup at the pointer for mouse events and at the element for keyboard events (`event.detail === 0` or zero client coordinates). ([MDN contextmenu][mdn-contextmenu])
- Fluent UI React v9: `Menu` with `openOnContext` and a `MenuTrigger` around the area opens the menu from `contextmenu`; the trigger handler in the source calls `preventDefault` in that mode. Test the keyboard route (Shift+F10) in a real browser. ([Menu types][gh-menu-types], [MenuTrigger source][gh-menutrigger])
- Focus on open: after opening from the keyboard focus lands on the first entry; after opening by pointer it may stay on the popup surface. Record which entry has focus in your test and assert the arrow results from that state (Derived; the behavior differs between implementations).
- Focus return: closing by Esc or by choosing an entry returns focus to the trigger, unless the action itself moves focus (opens a dialog, navigates). Check by test. ([APG menu button][apg-menubutton])
- Entries without an icon: reserve the icon column (an empty 16 x 16 box) so texts line up with entries that have icons. The entry text must never be wider than the surface: shorten with `text-overflow: ellipsis` or raise the width, and test with the longest label of the app in every language (Derived).
- Never put the main action of a split button into its own menu again. ([Button][f2-button])
- Do not use a menu for a single action. Use a button.

## 5. Toolbar and overflow

- A toolbar gives quick access to frequent actions. It never wraps. When space runs out, the last items move into an overflow menu ("..." or "More") that shows text labels for icon-only items. Group related items with a divider or spacing; keep destructive actions apart; name each toolbar if there are several; icon buttons have a tooltip plus an accessible name. ([Toolbar][f2-toolbar])
- Own components (APG toolbar): `role="toolbar"` with `aria-label` (and `aria-orientation="vertical"` for vertical bars). Roving tabindex like tabs: the toolbar is one tab stop, Left/Right move between controls, Home and End jump. Do not use `role="toolbar"` for fewer than three controls; a plain group of buttons is enough. Do not put controls that need the arrow keys themselves (text fields, sliders) in a toolbar without a documented exception. ([APG toolbar][apg-toolbar])
- Fluent UI React v9: `Toolbar` renders `role="toolbar"` with arrow-key navigation (it uses the Tabster arrow-navigation group on both axes in the source), `size` small, medium or large, and `vertical`. Items are `ToolbarButton`, `ToolbarToggleButton`, `ToolbarRadioButton`, `ToolbarDivider` and `ToolbarGroup`; give the toolbar an `aria-label`. ([Toolbar types][gh-toolbar-types], [Toolbar source][gh-toolbar])
- Prefer an overflow menu over horizontal scrolling of a header row, because everything stays reachable by keyboard and nothing hides off-screen. Derived from the guidance above; a project brief that chose scrolling must record why.
- Overflow from the available width. Own components: observe the container with `ResizeObserver`, measure the item widths once (or on content change), keep those that fit plus the width of the overflow button, and render the rest as entries of the overflow menu, last item first. Re-run on resize so the items return at a wide width. Keep the overflow button in the tab order. ([MDN ResizeObserver][mdn-resizeobserver])
- Fluent UI React v9: wrap the toolbar in `Overflow` (from `@fluentui/react-components`, package `react-overflow`), wrap each item in `OverflowItem` with an `id` and an optional `priority`, and build the "More" button with the `useOverflowMenu` hook, which returns a `ref`, `overflowCount` and `isOverflowing`; render the hidden items in the menu with `useIsOverflowItemVisible(id)` to decide which ones belong in it. The library measures with a `ResizeObserver` internally. ([Overflow source][gh-overflow], [useOverflowMenu][gh-overflowmenu])
- Items that do not fit must be hidden completely: `display: none`, `visibility: hidden` or the `inert` attribute, not only `opacity: 0`, because invisible items that stay focusable clog the tab order. Fluent UI `Overflow` sets `data-overflowing` on hidden items and styles them out (confirm in your CSS reset that nothing overrides it). Derived.
- The menu shows a text label for every hidden item, including icon-only ones. Rebuild its entries after the layout change, not during the measuring pass, to avoid a resize loop.

## 6. Tooltip

- Content: supplementary, short, plain text, never essential. Shown on hover and on keyboard focus. Gap to the target 4 px; delay 250 ms in and out, but 0 ms when another tooltip is already open; Esc hides it. Fluent default surface: padding 4/11/6/11, radius 4, 12/16 text, max width 240. ([Tooltip][f2-tooltip], [Tooltip source][gh-tooltip], [Tooltip logic][gh-tooltipbase])
- The `title` attribute is not enough. It does not show on keyboard focus, not on touch, cannot be styled or dismissed, and screen readers treat it inconsistently. Use a real tooltip component for anything beyond a convenience hint. ([MDN title][mdn-title])
- WCAG 1.4.13 Content on Hover or Focus: additional content that appears on hover or focus must be dismissible without moving the pointer (Esc), hoverable (the pointer can move onto the tooltip without it vanishing), and persistent until dismissed, the pointer leaves or focus moves. Test all three. ([WCAG 1.4.13][wcag-1413])
- Own components: the tooltip element has `role="tooltip"` and an `id`; the trigger points to it with `aria-describedby`. For an icon-only button whose tooltip is the only name, use `aria-label` on the button instead (or `aria-labelledby`), and let the tooltip repeat it; do not rely on `aria-describedby` for the name. Show on `focus` and `pointerenter` (not on `mouseenter` alone, which misses touch and pen), hide on `blur`, `pointerleave` and Esc. ([APG tooltip][apg-tooltip])
- Fluent UI React v9: `Tooltip` requires `relationship` (`label`, `description` or `inaccessible`) and `content`; `label` sets `aria-label` or `aria-labelledby` on the trigger and is the right choice for icon-only buttons, `description` sets `aria-describedby`, and `inaccessible` hides the tooltip from assistive technology and is only for text that is available elsewhere. `showDelay` and `hideDelay` default to 250 ms, `positioning` defaults to above, and the tooltip shows on hover and focus of its child. The source handles Esc through a document key listener (`documentKeyboardEvent` in `onVisibleChange`). ([Tooltip types][gh-tooltip-types])
- Text rules: for an unlabeled control a short noun phrase; for an active control what it enables; for a disabled control when it becomes available; do not repeat visible text; no interactive controls inside (if it needs a link or button, it is a popover, see [dialogs-and-messages.md](dialogs-and-messages.md), section 4); name the keyboard shortcut. Icon buttons that run an action may read better as verb plus object ("Move appointment"); that deviates from Fluent's noun-phrase advice and is a reasonable project choice. ([Tooltip][f2-tooltip])
- Disabled controls: a native `disabled` button receives no focus or pointer events in most browsers, so a tooltip on it never shows. Use `aria-disabled="true"` (and block the action in the handler) when the tooltip explains why, or put the tooltip on a wrapper. Derived from the HTML button behavior. ([MDN button][mdn-button])
- Contrast and inheritance: a tooltip rendered in a portal does not inherit the target's text color, but one rendered inside the target does; with the tooltip inside the target, a rule such as `.chip span` also matches the tooltip text. Seen on the desktop sibling of this skill as text in the target's color on the dark tooltip surface, contrast 1.0. Set the tooltip's own foreground explicitly and test every real tooltip of the page (opened, not assumed) at 4.5:1 in light and dark (Derived from that observation).
- Recommended treatment (Derived): radius 8 (overlay), one shadow token, 12/16 text, delay 250 ms, no tooltip on text that is already fully visible, one tooltip on every icon-only button. Set delay and placement once for the app (`FluentProvider` has no tooltip defaults; wrap `Tooltip` in one project component).
- Touch has no hover. Tooltips are an enhancement; anything needed to operate the control must be visible or in the accessible name.

## 7. Shortcut list

A shortcut list (help page, popover or dialog that shows the keys of the app) is a reference that is scanned, not read. Derived from Fluent's keyboard and content guidance; Microsoft does not specify the layout.

- Group by area ("Navigation", "Editing", "Calendar"), not alphabetically, and in the order the areas appear on screen. Show each group title at the section-heading step of the project's type ramp (Fluent default: 14/20 Semibold in compact popovers, 16/22 in sheets), above its rows. Users look for the area first and the key second.
- Markup: one heading per group, then a table or list of rows. A `<table>` with the description in `<th scope="row">` and the keys in the second cell reads well; do not build it from `div`s with a grid and no semantics. Derived.
- Two columns per row: keys on the left in a column of fixed width, the description on the right. Share the key column width across all groups (a `<table>` per group with a fixed `col` width, or CSS grid with a shared `grid-template-columns` custom property), so the descriptions start at the same x everywhere.
- Description: at most two lines, ideally one. Shorten the text (verb plus object, "New appointment"); guard with `-webkit-line-clamp: 2` so one long text cannot make the rows uneven. Test with the longest description of the app.
- Key chips: one `<kbd>` per key, all the same height (and a minimum width, so "N" and "Ctrl" look like the same kind of object), text at least 12 px, written the way the keycap reads ("Ctrl", "Shift", "Esc"). Put a "+" between the keys of a chord and "then" between the steps of a sequence. Chips do not carry meaning by color. `<kbd>` is the semantic element for keyboard input. ([MDN kbd][mdn-kbd])
- Hint at the top, one line: "Letter keys work only when no input field has focus." Single-character shortcuts are a hazard for speech input and typing (WCAG 2.1.4 Character Key Shortcuts), so they must not fire while a text field has focus, or must be possible to turn off or remap; the hint tells users why a key does nothing while they type. Shortcuts with a modifier work in fields; keep them in the same list. ([WCAG 2.1.4][wcag-214])
- Link "Show all shortcuts" from the list to the complete list in the help when the list shows only the common ones. A list that is complete needs no link.
- Accessible: each row reads as one unit, keys first and then the action ("Ctrl+N, New appointment"). Expose the shortcut on the control itself with `aria-keyshortcuts="Control+N"` (the value uses key names such as `Control`, `Shift`, `Alt`, `Meta`, joined by `+`; it only announces, it does not bind the key). The chips themselves may be hidden from assistive technology when the row text already has the keys (`aria-hidden="true"` on the `<kbd>` group and a visually hidden text), but do not hide both. ([MDN aria-keyshortcuts][mdn-keyshortcuts])
- The list opens from a menu entry or a button with a tooltip, closes on Esc, and focus returns to the invoker ([accessibility.md](accessibility.md), section 3). A common route is a dialog opened from `?` (a single-character shortcut, so subject to the rule above).
- Browsers and screen readers reserve many combinations (Ctrl+T, Ctrl+W, Alt+Left, screen reader modifier keys). Check each shortcut against the browser's own list and against NVDA and Narrator commands before binding it. Derived.
- Every key shown matches a real key binding (cross-check in code, [accessibility.md](accessibility.md), section 5); generate the list from the binding table where the app has one, so the two cannot drift apart.

## 8. Checklists

- [ ] Exactly one tab is active at first render (component test or Playwright: count `[aria-selected="true"]`).
- [ ] The strip is one tab stop, on the active tab (Playwright: Tab in lands on the active tab, Tab again lands in the panel or past the strip).
- [ ] Left/Right (Up/Down if vertical) move focus; Home and End jump; Enter or Space selects under manual activation, or focus selects under automatic activation; the chosen model is written down (keyboard test).
- [ ] A tab strip that does not fit shows an overflow menu; it never wraps or scrolls (test at minimum width and a wide width).
- [ ] Icon-only tabs, rail items and toolbar buttons have an accessible name and a tooltip (axe rule `button-name`, plus grep for `aria-label` on icon buttons).
- [ ] `<nav>` landmarks have distinct labels; the current page has `aria-current="page"`; breadcrumb is `nav aria-label="Breadcrumb"` with the last item current (accessibility tree check or `getByRole('navigation', { name })`).
- [ ] After a route change focus moves to the new heading or `<main>` and the title changes (Playwright).
- [ ] Menu: trigger has `aria-haspopup="menu"` and `aria-expanded`; Esc closes; focus returns to the trigger; Tab closes (keyboard test). A list of links is a disclosure, not `role="menu"` (review).
- [ ] Menu opened from the keyboard: the focused entry after open is recorded, and Down and Up behave as described in section 4 (keyboard test).
- [ ] Context menu opens from the pointer and from Shift+F10 or the Menu key; the browser menu stays available on text fields (manual keyboard pass).
- [ ] Dangerous entries are last and separated; shortcut text equals the real shortcut (cross-check key bindings).
- [ ] Toolbar overflow keeps every command reachable by keyboard (tab through at minimum width); hidden items are not tab stops (check `display: none` or `inert`).
- [ ] Icon-only tab strip: the number of tabs that fit follows 34 n - 2 px; the overflow button appears only when something is hidden; the selected and the last-used tab are visible at every width (test at three widths).
- [ ] Menu entries without an icon reserve the icon column; the longest label fits the menu surface (test).
- [ ] Tooltips: appear on focus as well as hover; Esc hides; the pointer can move onto the tooltip; none on fully visible text; disabled controls say when they become available; no reliance on `title` (Playwright: focus, hover, Esc).
- [ ] Every real tooltip of the page (opened, not assumed) has text contrast of at least 4.5:1 in light and dark (test with computed styles).
- [ ] Shortcut list: grouped by area, fixed shared key column, descriptions at most two lines, `<kbd>` chips of equal height, letter-key hint at the top, link to the full list, every key matches a real binding (screenshot plus cross-check).
- [ ] Letter-key shortcuts do not fire while a text field has focus, or can be turned off (Playwright: type the letter in a field).

## 9. Sources

[f2-tablist]: https://fluent2.microsoft.design/components/web/react/core/tablist/usage
[f2-nav]: https://fluent2.microsoft.design/components/web/react/core/nav/usage
[f2-motion]: https://fluent2.microsoft.design/motion
[f2-breadcrumb]: https://fluent2.microsoft.design/components/web/react/core/breadcrumb/usage
[f2-menu]: https://fluent2.microsoft.design/components/web/react/core/menu/usage
[f2-button]: https://fluent2.microsoft.design/components/web/react/core/button/usage
[f2-toolbar]: https://fluent2.microsoft.design/components/web/react/core/toolbar/usage
[f2-tooltip]: https://fluent2.microsoft.design/components/web/react/core/tooltip/usage
[apg-tabs]: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
[apg-breadcrumb]: https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/
[apg-menubutton]: https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/
[apg-disclosure-nav]: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/
[apg-toolbar]: https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/
[apg-tooltip]: https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
[wcag-1413]: https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html
[wcag-214]: https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html
[wcag-focus-order]: https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
[mdn-nav]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/nav
[mdn-aria-current]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-current
[mdn-contextmenu]: https://developer.mozilla.org/en-US/docs/Web/API/Element/contextmenu_event
[mdn-resizeobserver]: https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver
[mdn-title]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/title
[mdn-button]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button
[mdn-kbd]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/kbd
[mdn-keyshortcuts]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-keyshortcuts
[gh-tab]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tabs/library/src/components/Tab/useTabStyles.styles.ts
[gh-tab-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tabs/library/src/components/Tab/Tab.types.ts
[gh-tablist-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tabs/library/src/components/TabList/TabList.types.ts
[gh-nav]: https://github.com/microsoft/fluentui/tree/master/packages/react-components/react-nav
[gh-breadcrumb]: https://github.com/microsoft/fluentui/tree/master/packages/react-components/react-breadcrumb/library/src/components
[gh-menu]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-menu/library/src/components/MenuItem/useMenuItemStyles.styles.ts
[gh-menu-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-menu/library/src/components/Menu/Menu.types.ts
[gh-menutrigger]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-menu/library/src/components/MenuTrigger/useMenuTrigger.ts
[gh-toolbar]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-toolbar/library/src/components/Toolbar/useToolbar.ts
[gh-toolbar-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-toolbar/library/src/components/Toolbar/Toolbar.types.ts
[gh-overflow]: https://github.com/microsoft/fluentui/tree/master/packages/react-components/react-overflow
[gh-overflowmenu]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-overflow/library/src/useOverflowMenu.ts
[gh-tooltip]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tooltip/library/src/components/Tooltip/useTooltipStyles.styles.ts
[gh-tooltipbase]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tooltip/library/src/components/Tooltip/useTooltipBase.tsx
[gh-tooltip-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tooltip/library/src/components/Tooltip/Tooltip.types.ts
