# Data display: lists, tables, cards, people, badges, accordions

Read this file when you build or review lists, tables and data grids, cards, avatars and personas, badges and pills, accordions, dividers, images or the less common components (tree, carousel, rating) in a web app. Project briefs win over the Fluent defaults quoted here.

Two paths apply. **Fluent UI React v9** projects use `List`, `Table`, `DataGrid`, `Card`, `Avatar`, `Persona`, `Badge`, `Accordion` and so on. **Own components** projects write semantic HTML and CSS and borrow Fluent's values. In both cases start from the native element that fits (`<ul>`, `<table>`, `<details>`, `<img>`) and add ARIA only for what HTML cannot express. Mapping from Fluent concepts to HTML, CSS and tokens: [web-mapping.md](web-mapping.md); v8 to v9 names: [fluent-ui-react-notes.md](fluent-ui-react-notes.md).

## Contents

1. [List](#1-list)
2. [Table](#2-table)
3. [Card](#3-card)
4. [Avatar and persona](#4-avatar-and-persona)
5. [Badge and pill](#5-badge-and-pill)
6. [Accordion](#6-accordion)
7. [Divider and image](#7-divider-and-image)
8. [Components to skip unless the product needs them](#8-components-to-skip-unless-the-product-needs-them)
9. [Checklists](#9-checklists)
10. [Sources](#10-sources)

## 1. List

- Use for similar, independent items. Patterns: single action, several actions, selection as the main action, selection as a side action (checkbox). A click on the row selects; a click on an action runs only that action. No sub-levels (use a tree), no nested components. ([List][f2-list])
- Markup: a plain list of items is a `<ul>` (or `<ol>` when the order matters) with `<li>` children; that already has the list role and announces "list, 5 items". Use `role="listbox"` with `role="option"` children and `aria-selected` only when the user selects items from it with arrow keys, which is a composite widget with a roving tabindex or `aria-activedescendant`; a listbox cannot contain buttons or links as options' content that must stay separately reachable. Do not use `role="listbox"` for a list of links or a list with several actions per row. ([APG listbox][apg-listbox], [MDN list role][mdn-list])
- Fluent UI React v9: `List` with `ListItem` (from `@fluentui/react-list`, re-exported by the main package). `selectionMode` (`single` or `multiselect`) and `navigationMode` (`items` or `composite`) decide the role: the source derives the list role from them (a `listbox` when selectable, a `list` otherwise, and a `grid` for the composite mode), and sets `aria-multiselectable` for multiselect. Check the role in your DOM before styling around it. ([List types][gh-list-types], [useList][gh-uselist])
- Keyboard: Enter and Space invoke; Right moves into secondary actions, Left or Esc goes back; with selection as a side action Enter runs the main action and Space toggles selection; Home and End jump to first and last; Page Up and Down move by page (the last two are Derived from the APG listbox pattern). ([List][f2-list], [APG listbox][apg-listbox])
- Items are phrased in parallel, similar in length, with no empty or disabled filler entries. Row minimum height 40 (Derived; Fluent publishes no web value, the desktop default is 40).
- Selected row: brand background 2 and, if you like, a 3 px marker; keep it consistent with the project's tokens, and do not let color be the only sign of selection (`aria-selected` plus a visible check, marker or weight change; WCAG 1.4.1).
- Long lists: virtualize only when measured (hundreds of rows); virtualization removes rows from the DOM, so keep `aria-setsize` and `aria-posinset` on the items so assistive technology still reports "item 40 of 1200" (Derived from ARIA). Never virtualize a list whose items must be found by the browser's find-in-page without telling users. ([MDN aria-setsize][mdn-setsize])

## 2. Table

- Use a real `<table>` for tabular data: `<caption>` (or `aria-labelledby` to a heading), `<thead>` with `<th scope="col">`, row headers as `<th scope="row">`, `<tbody>` rows. Screen readers then announce the column and row header for each cell. Do not build tables from `div`s with `role="table"` unless you need a layout the native table cannot do, and then add every role (`rowgroup`, `row`, `columnheader`, `cell`). Do not use tables for layout. ([MDN table][mdn-table], [APG table][apg-table])
- Sortable columns: the header's text sits in a `<button>` inside the `<th>`; the `<th>` of the sorted column carries `aria-sort="ascending"` or `"descending"`; other sortable headers have no `aria-sort` or `none`. Announce the result of a sort in a polite status region ("Sorted by name, ascending"). ([MDN aria-sort][mdn-aria-sort])
- Fluent UI React v9 has two families. `Table` (with `TableHeader`, `TableHeaderCell`, `TableBody`, `TableRow`, `TableCell`, `TableCellLayout`) is the display table: with `sortable`, header cells render a button and set `aria-sort` from `sortDirection` (`none` by default), and with `noNativeElements` it renders `div`s with table roles instead of native elements. `DataGrid` (with `DataGridHeader`, `DataGridBody`, `DataGridRow`, `DataGridCell`, `DataGridHeaderCell`, `DataGridSelectionCell`) adds keyboard navigation between cells (`focusMode`), row selection (`selectionMode`), sorting and resizable columns, as a `grid`. Choose `Table` for read-mostly data and `DataGrid` only when you need cell-level keyboard navigation or selection; a grid is a heavier contract for screen-reader users. `useTableFeatures` with `useTableSort` and `useTableSelection` supplies the logic for `Table`. ([Table types][gh-table-types], [TableHeaderCell][gh-tablehead], [DataGrid types][gh-datagrid-types])
- Row height (Fluent default, source): 44 medium, 34 small, 24 extra small (`size` prop on `Table`); cell padding 0/8; bottom border 1 px in the second neutral border; selected row brand background 2; focus 2 px outline. A brief may set its own minimum row height (for example 36) and cell padding 12; that sits between small and medium and is fine when recorded. ([Table source][gh-table])
- Numbers right-aligned under a right-aligned header, tabular digits (`font-variant-numeric: tabular-nums`); text left-aligned. Derived.
- Truncation: tables and cards may truncate with an ellipsis if the full text is available (a tooltip is not reachable by touch; prefer a detail view or a cell that expands). Derived.
- Responsive: a wide table must not break the page layout at 320 px or 400 percent zoom. Put it in a scroll container (`overflow-x: auto`) that is focusable (`tabindex="0"`, `role="region"`, `aria-label`) so keyboard users can scroll it; keep the first column sticky where it helps. Do not reflow a table into cards without preserving the header association. Derived from WCAG 1.4.10 Reflow, which exempts two-dimensional data tables. ([WCAG 1.4.10][wcag-reflow])
- Virtualization: a table that renders thousands of rows needs row virtualization; keep `aria-rowcount`, `aria-rowindex` on the rows (and `aria-colcount`, `aria-colindex` for columns) so the position is announced correctly. Measure before virtualizing (Derived). ([MDN aria-rowcount][mdn-rowcount])

## 3. Card

- A container for one object; parts: preview, header, footer, all optional; vertical or horizontal; Fluent default padding 8, 12, 16 with radius 2, 4, 6; shadow 4; transparent border. A clickable card needs exactly one clear primary action; otherwise make it selectable. ([Card][f2-card], [Card source][gh-card])
- Fluent UI React v9: `Card` with `CardHeader`, `CardPreview` and `CardFooter`; `appearance` (`filled`, `filled-alternative`, `outline`, `subtle`), `orientation`, `size`, `focusMode` (`off`, `no-tab`, `tab-exit`, `tab-only`) and, for selectable cards, `selected` or `defaultSelected` with `onSelectionChange` (it renders an internal checkbox and `floatingAction` slot). The card root is a `div` with `role="group"`, made focusable (`tabIndex` 0) unless `focusMode` is `off` or the card is selectable (verified in the source). ([Card types][gh-card-types], [useCard][gh-usecard])
- A clickable card is a link or a button, not a `div` with `onClick`. A `div` with a click handler has no role, is not focusable and does not react to Enter or Space. Use one of these structures: the card's title is an `<a href>` (or `<button>`) whose `::after` pseudo-element is stretched over the whole card (`position: absolute; inset: 0`) so the whole card is clickable while the accessible name is only the title; or wrap the card in the `<a>`, if the card holds no other interactive content. Never nest a link or button inside another. The same applies to a Fluent `Card` with `onClick`: its root has the `group` role, not a link or button role, so put a real link or button inside (for example the `CardHeader` title) and test with the keyboard. ([MDN a][mdn-a], [WCAG 4.1.2][wcag-name-role-value])
- Keyboard for clickable cards: Tab reaches the card (or its link), Enter runs the primary action, secondary actions inside the card are separate tab stops after it. Derived.
- A brief may use radius 12, padding 16 or 20, a visible border and a different shadow. Record it.
- Card lists: render a set of cards as a `<ul>` of `<li>` so assistive technology reports the count; give each card a heading at the right level (`<h3>` under an `<h2>` section) so users can jump through them. Derived.

## 4. Avatar and persona

- Avatar: circle for a person, square for a group; Fluent default medium size 32 (a 30 px initials circle is close; the 4 px grid favors 32). Presence badge and activity ring are available. A presence badge at 32 px or less is hard to see: also state the status as text or a tooltip. Avatar groups (spread, stack, pie) show an overflow avatar with a count from five on. ([Avatar][f2-avatar], [Avatar group][f2-avatargroup])
- Fluent UI React v9: `Avatar` takes `name` (always pass it when known; it derives the initials and the accessible name), `image`, `icon`, `size` (16 to 128 in steps), `shape` (`circular`, `square`), `color` (`neutral`, `brand`, `colorful` or a named color), `active` and `activeAppearance`, `badge`. The source sets `role="img"` on the root and `aria-label` to the name, or `aria-labelledby` to the initials and badge; the image itself is `alt=""` and `aria-hidden`. `AvatarGroup` with `AvatarGroupItem` and `AvatarGroupPopover` handles overflow. ([Avatar types][gh-avatar-types], [useAvatar][gh-useavatar])
- Alt text rules (Derived from the WAI image tutorial): an avatar next to the person's name in text is decorative, so give it an empty name (`aria-hidden`) to avoid reading the name twice; an avatar that stands alone (a comment author, an assignee chip without text) is named with the person's name ("Ada Lovelace"), not "avatar" or "profile photo of"; a group of avatars is named by its purpose and count ("Assigned to 3 people") with the individual avatars hidden or listed. ([WAI images][wai-images])
- Persona: avatar plus presence plus up to four text lines, one word or short phrase per line. Fluent UI React v9 `Persona` takes `name`, `primaryText` (defaults to `name`), `secondaryText`, `tertiaryText`, `quaternaryText`, `avatar` and `presence` slots, and `textPosition`/`textAlignment`; when the persona text already shows the name, the avatar inside it should not repeat it. ([Persona][f2-persona], [Persona types][gh-persona-types])
- Presence is not shown by color alone: `PresenceBadge` has a `status` (`available`, `busy`, `away`, `do-not-disturb`, `out-of-office`, `offline`, `blocked`, `unknown`) and distinct icons per status; keep the status in text or the accessible name too ("Ada Lovelace, available"). ([PresenceBadge types][gh-presence-types], [WCAG 1.4.1][wcag-141])

## 5. Badge and pill

- Height 20 (small 16, large 24, extra large 32; tiny 6 and extra small 10 are dots), minimum width equal to the height, circular radius, 12 px text. One or two words, sentence case, never truncated, sizes not mixed, placed close to the thing described. Icon-only badges need an accessible label. Warning or danger colors come with a way to resolve. No focus unless it has a tooltip. ([Badge][f2-badge], [Badge source][gh-badge])
- Fluent UI React v9: `Badge` (`appearance`: `filled`, `ghost`, `outline`, `tint`; `color`: `brand`, `danger`, `important`, `informative`, `severe`, `subtle`, `success`, `warning`; `shape`; `size`; `iconPosition`), `CounterBadge` (`count`, `overflowCount`, `showZero`, `dot`) and `PresenceBadge`. A badge is a plain `span` without a role. ([Badge types][gh-badge-types])
- Not color alone: a red "danger" badge, a green dot or a colored count needs text, an icon or a pattern that carries the same meaning (WCAG 1.4.1 Use of Color), and the badge text must reach 4.5:1 against its fill, which several `filled` color pairs may not (measure per color and theme, see [accessibility.md](accessibility.md), section 8). ([WCAG 1.4.1][wcag-141], [WCAG 1.4.3][wcag-143])
- A count badge on an icon button needs the count in the accessible name ("Notifications, 3 unread"); the visible digit alone is read as a stray number. If the count changes while the page is open, announce it through a polite live region only when it matters (Derived). ([MDN aria-label][mdn-aria-label])
- The 12 px minimum applies to badge text; a brief with 11.5 px should move to 12. Derived from the type minimums in [foundations.md](foundations.md).

## 6. Accordion

- Groups collapsible sections, all closed by default; opening one closes the previous (several may stay open when that does not overwhelm); chevron at the start or end, consistent; the header is a button with an expanded state; header height at least 44 (small 32), padding 0/12/0/10; header text short, sentence case, no period. Content that is required for the task does not belong inside. ([Accordion][f2-accordion], [Accordion source][gh-accordion])
- Own components, option 1: native `<details>` and `<summary>`. The browser supplies the button role, the expanded state, the keyboard (Enter and Space toggle) and find-in-page that opens the panel. Style the marker with `summary::marker` or `list-style: none` plus your own chevron, and keep a visible focus ring on `summary`. Give several `<details>` the same `name` attribute for the exclusive (one open at a time) behavior where your browsers support it (recent; derived, not verified for your matrix). Do not use it when you need animated height before support is certain or when the header contains other interactive controls, since `summary` cannot hold nested buttons reliably. ([MDN details][mdn-details])
- Own components, option 2 (APG accordion): a heading element containing a `<button aria-expanded="true|false" aria-controls="panel-id">`, and a panel `<div id="panel-id">` that is hidden with the `hidden` attribute when collapsed (and `role="region" aria-labelledby` the button when there are few panels; skip the region role with six or more panels). Keep the button inside the heading so the structure shows up in the heading outline. ([APG accordion][apg-accordion])
- Fluent UI React v9: `Accordion` (`collapsible`, `multiple`, `openItems`, `defaultOpenItems`, `onToggle`) with `AccordionItem` (needs a `value`), `AccordionHeader` and `AccordionPanel`. The header renders a `<button>` with `aria-expanded` from the open state (verified in the source); the library default is that one panel is open at a time and, unless `collapsible`, the open one cannot be closed. The `navigation` prop (arrow keys between headers) is deprecated in the source, which says to use `Tree` where arrow navigation is a hard requirement. Set `expandIconPosition` consistently. ([Accordion types][gh-accordion-types], [useAccordionHeader][gh-useaccordionheader])
- Use it for rarely needed form fields ("More details") and open it automatically when it contains filled values or an error. Enter and Space toggle it. A header height of 34 matching the project control height is a legitimate deviation. Derived.
- Hidden panels must not be focusable: `hidden`, `display: none` or `inert`, never just `height: 0`. Animate height only with `prefers-reduced-motion` honored. Derived.

## 7. Divider and image

- Divider: block-wide or inset; keep at least 12 px above and below (8 with an icon); not directly under headings; text inside stays short. Prefer whitespace and group titles to dividers. ([Divider][f2-divider], [Divider source][gh-divider])
- Markup: an `<hr>` has the separator role and is announced; use it only when the break carries meaning (a change of topic). For purely decorative lines use a CSS border or `role="presentation"` so assistive technology skips it (Fluent's own guidance: a pure line is hidden from assistive technology). Fluent UI React v9 `Divider` renders `role="separator"` with `aria-orientation` and `aria-labelledby` for a divider with text; pass `role="presentation"` or `aria-hidden` for a decorative one (verify in your DOM). ([MDN hr][mdn-hr], [useDivider][gh-usedivider])
- Image: alt text is one or two short sentences that do not repeat the surrounding text; decorative images have `alt=""` (not a missing `alt`, which makes some screen readers read the file name); use shadows sparingly. For an image that is a link or button, the alt text describes the target, not the picture. Complex images (charts) get a short alt and a longer description nearby, linked with `aria-describedby`. ([Image][f2-image], [WAI images][wai-images])
- Performance and stability: set `width` and `height` attributes (or `aspect-ratio`) on every `<img>` so the browser reserves the space and the page does not shift (CLS); add `loading="lazy"` to images below the fold and never to the largest above-the-fold image (it is usually the LCP element, which should instead get `fetchpriority="high"`); use `srcset` and `sizes` for responsive widths and modern formats. Fluent UI React v9 `Image` is a styled `<img>` with `fit`, `shape`, `bordered`, `shadow` and `block`; the attributes above are yours to pass. ([MDN img][mdn-img], [web.dev CLS][webdev-cls])
- SVG icons: inline SVG next to text is `aria-hidden="true"` (the text names the control); an icon-only button gets the name on the `<button>`, not inside the SVG. Derived.

## 8. Components to skip unless the product needs them

- Tree: for nested data only; indent 24 (medium) or 12 (small), item min height 32 (small 24), at most one or two quick actions, multi-select with a mixed parent state. Use the APG tree view pattern (`role="tree"`, `treeitem`, `aria-expanded`, roving tabindex), or Fluent UI `Tree`. ([Tree][f2-tree], [Tree source][gh-tree], [APG tree][apg-tree])
- Carousel: auto-play must be pausable (WCAG 2.2.2 Pause, Stop, Hide) and stop under `prefers-reduced-motion`; full-screen below 600 px; reflow down to 320 px. ([Carousel][f2-carousel], [WCAG 2.2.2][wcag-222])
- Rating: stars with 3:1 contrast, 16 px up to 20, interactive ones extra large; implement as a radio group or the Fluent UI `Rating` and name it ("Rating, 3 of 5"). ([Rating][f2-rating])
- Breadcrumb: only with real hierarchy; see [navigation.md](navigation.md).

## 9. Checklists

- [ ] Row and item heights meet the project minimum (Playwright reads `boundingBox().height`).
- [ ] A list uses `<ul>` unless it is a selectable listbox; a listbox has one clear selection model and Home/End/Page keys work (keyboard test).
- [ ] Tables use `<table>`, `<th scope>`, and a caption or label; sortable headers are buttons with `aria-sort` on the sorted column (axe rules `th-has-data-cells`, `td-headers-attr`, `scope-attr-valid`; accessibility tree check).
- [ ] A wide table scrolls inside a focusable, labelled container at 320 px and does not break the page (test at 320 px and 400 percent zoom).
- [ ] Numeric columns are right-aligned with tabular digits (screenshot).
- [ ] A clickable card has exactly one primary action and is a link or button, never a bare `div` (review plus keyboard test: Tab reaches it, Enter runs it).
- [ ] Status is never carried by an avatar badge or a badge color alone; text, icon or accessible name exists (grayscale screenshot and accessibility tree).
- [ ] Avatars have the person's name as accessible name when standing alone and are hidden when the name is beside them.
- [ ] Badge text is 12 px or larger, not truncated, and reaches 4.5:1 (screenshot at 200 percent text scale; contrast measured).
- [ ] An accordion header is a button (or `<summary>`) with an expanded state; collapsed panels are not focusable; it opens by itself when it holds values or errors (test: read `aria-expanded`, Tab through while collapsed).
- [ ] Informative images have useful `alt`; decorative ones have `alt=""` or are CSS backgrounds (axe rule `image-alt`).
- [ ] Every `<img>` has `width` and `height` or `aspect-ratio`; below-the-fold images use `loading="lazy"` (Lighthouse "Properly size images" and CLS).

## 10. Sources

[f2-list]: https://fluent2.microsoft.design/components/web/react/core/list/usage
[f2-card]: https://fluent2.microsoft.design/components/web/react/core/card/usage
[f2-avatar]: https://fluent2.microsoft.design/components/web/react/core/avatar/usage
[f2-avatargroup]: https://fluent2.microsoft.design/components/web/react/core/avatargroup/usage
[f2-persona]: https://fluent2.microsoft.design/components/web/react/core/persona/usage
[f2-badge]: https://fluent2.microsoft.design/components/web/react/core/badge/usage
[f2-accordion]: https://fluent2.microsoft.design/components/web/react/core/accordion/usage
[f2-divider]: https://fluent2.microsoft.design/components/web/react/core/divider/usage
[f2-image]: https://fluent2.microsoft.design/components/web/react/core/image/usage
[f2-tree]: https://fluent2.microsoft.design/components/web/react/core/tree/usage
[f2-carousel]: https://fluent2.microsoft.design/components/web/react/core/carousel/usage
[f2-rating]: https://fluent2.microsoft.design/components/web/react/core/rating/usage
[apg-listbox]: https://www.w3.org/WAI/ARIA/apg/patterns/listbox/
[apg-table]: https://www.w3.org/WAI/ARIA/apg/patterns/table/
[apg-accordion]: https://www.w3.org/WAI/ARIA/apg/patterns/accordion/
[apg-tree]: https://www.w3.org/WAI/ARIA/apg/patterns/treeview/
[wcag-141]: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
[wcag-143]: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
[wcag-reflow]: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
[wcag-222]: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
[wcag-name-role-value]: https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
[wai-images]: https://www.w3.org/WAI/tutorials/images/
[mdn-list]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/list_role
[mdn-setsize]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-setsize
[mdn-table]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/table
[mdn-aria-sort]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-sort
[mdn-rowcount]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-rowcount
[mdn-a]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a
[mdn-aria-label]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-label
[mdn-details]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details
[mdn-hr]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/hr
[mdn-img]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img
[webdev-cls]: https://web.dev/articles/cls
[gh-list-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-list/library/src/components/List/List.types.ts
[gh-uselist]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-list/library/src/components/List/useList.ts
[gh-table]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-table/library/src/components/TableRow/useTableRowStyles.styles.ts
[gh-table-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-table/library/src/components/Table/Table.types.ts
[gh-tablehead]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-table/library/src/components/TableHeaderCell/useTableHeaderCell.tsx
[gh-datagrid-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-table/library/src/components/DataGrid/DataGrid.types.ts
[gh-card]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-card/library/src/components/Card/useCardStyles.styles.ts
[gh-usecard]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-card/library/src/components/Card/useCard.ts
[gh-card-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-card/library/src/components/Card/Card.types.ts
[gh-avatar-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-avatar/library/src/components/Avatar/Avatar.types.ts
[gh-useavatar]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-avatar/library/src/components/Avatar/useAvatar.tsx
[gh-persona-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-persona/library/src/components/Persona/Persona.types.ts
[gh-presence-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-badge/library/src/components/PresenceBadge/PresenceBadge.types.ts
[gh-badge]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-badge/library/src/components/Badge/useBadgeStyles.styles.ts
[gh-badge-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-badge/library/src/components/Badge/Badge.types.ts
[gh-accordion]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-accordion/library/src/components/AccordionHeader/useAccordionHeaderStyles.styles.ts
[gh-accordion-types]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-accordion/library/src/components/Accordion/Accordion.types.ts
[gh-useaccordionheader]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-accordion/library/src/components/AccordionHeader/useAccordionHeader.tsx
[gh-divider]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-divider/library/src/components/Divider/useDividerStyles.styles.ts
[gh-usedivider]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-divider/library/src/components/Divider/useDivider.ts
[gh-tree]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tree/library/src/components/TreeItemLayout/useTreeItemLayoutStyles.styles.ts
