# Fluent UI React notes: v8 to v9 names, changed behavior, pitfalls

Read this file when code or examples from Fluent UI React v8 (`@fluentui/react`) do not compile or behave in v9 (`@fluentui/react-components`), when a v9 component ignores your styles, loses focus, or announces nothing, or before you trust a pitfall list from memory. The v8 to v9 names and the behavior differences come from the migration docs in [microsoft/fluentui][fluentui-src] (`apps/public-docsite-v9/src/Concepts/Migration/FromV8/`, read on the `master` branch); the rest is read from v9 source files (paths inline) or follows from web platform behavior. Each item carries a tag: **Fluent default** (stated by Fluent docs or source), **Derived** (follows from the platform or from reading the source; Fluent does not state it) or **(derived, not verified)** (not run, confirm before relying on it). Source was read at `@fluentui/react-components` 9.74.11. The patterns that use these items are in [web-mapping.md](web-mapping.md).

## Contents

1. [v8 to v9 names](#1-v8-to-v9-names)
2. [Changed behavior and API limits](#2-changed-behavior-and-api-limits)
3. [Observed pitfalls](#3-observed-pitfalls)
4. [Sources](#4-sources)

## 1. v8 to v9 names

Fluent default (component mapping table in `Migration/FromV8/ComponentMapping.mdx`). The right-hand column is the v9 name; many entries have their own migration guide in the same folder.

| v8 | v9 | What changes |
| --- | --- | --- |
| `TextField` | `Input` (single line) or `Textarea`, wrapped in `Field` | Label, hint and validation move to `Field` (`label`, `hint`, `validationState`, `validationMessage`); `errorMessage` becomes `validationMessage`. |
| `Dropdown` | `Dropdown` | New API; `onChange` becomes `onOptionSelect`; options are `Option` children; keys become strings (`value`, `selectedOptions`). |
| `ComboBox` | `Combobox` | Renamed; `VirtualizedComboBox` has no one-prop replacement. |
| `Panel` | `Drawer` (`OverlayDrawer`, `InlineDrawer`) | Composed of `DrawerHeader`, `DrawerBody`, `DrawerFooter`; `isOpen` becomes `open`. |
| `Callout` | `Popover` | `DirectionalHint` becomes `positioning` (`"above"`, `"below-start"`, `"before"` and so on). |
| `Modal`, `Dialog` | `Dialog` | One component with `open`, `onOpenChange`, `modalType`. |
| `MessageBar` | `MessageBar` | Composable: `MessageBarBody`, `MessageBarTitle`, `MessageBarActions`; `messageBarType` becomes `intent`. |
| `Stack` | CSS flexbox with `makeStyles` | No native `Stack`; `StackShim` from `@fluentui/react-migration-v8-v9` is a temporary bridge. |
| `DetailsList` | `DataGrid` (interactive) or `Table` (read-only) | Columns via `createTableColumn()`, render-prop body, selection as a `Set`. |
| `Persona` | `Persona` | `text` becomes `name`; `imageUrl` becomes `avatar={{ image: { src } }}`; `presence` becomes `presence={{ status }}`. |
| `CommandBar` | `Toolbar` (with `Overflow` for overflow) | JSX children replace the `items` array; `farItems` become a fixed sibling region. |
| `Pivot`, `PivotItem` | `TabList`, `Tab` | Panels move out of `TabList`; see the selection note in section 2. |
| `DefaultButton`, `PrimaryButton`, `ActionButton`, `IconButton` | `Button` with `appearance` | `PrimaryButton` is `appearance="primary"`; `ActionButton` is `appearance="transparent"`; `CompoundButton`, `ToggleButton`, `SplitButton`, `MenuButton` are separate components. |
| `ContextualMenu` | `Menu` (`MenuTrigger`, `MenuPopover`, `MenuList`, `MenuItem`) | Compose the menu under `Menu`. |
| `Toggle` | `Switch` | Renamed. |
| `ChoiceGroup` | `RadioGroup` with `Radio` children | Options become children. |
| `Checkbox` | `Checkbox` | `indeterminate` is `checked="mixed"`. |
| `ProgressIndicator` | `ProgressBar` | Renamed. |
| `Separator` | `Divider` | Renamed. |
| `Shimmer` | `Skeleton` | Renamed. |
| `TeachingBubble`, `Coachmark` | `TeachingPopover` | Replaced. |
| `Fabric`, `ThemeProvider` | `FluentProvider` | v9 themes have a different shape (tokens object); convert custom v8 themes at one explicit boundary. |
| `Layer`, `Overlay` | `Portal` (or the owning component, such as `Dialog`) | Layering through portals. |
| `FocusZone`, `FocusTrapZone` | Tabster hooks (`useArrowNavigationGroup`, `useFocusableGroup`) or `Dialog` | Prefer the owning v9 component; no direct instance API. |
| `SearchBox`, `SpinButton`, `Slider`, `Spinner`, `Tooltip`, `Link`, `Label`, `Text`, `Breadcrumb`, `Nav`, `Rating`, `Image` | Same name | Smaller API changes; each has a migration guide. |
| `DatePicker`, `Calendar`, `TimePicker` | `DatePickerCompat`, `CalendarCompat`, `TimePickerCompat` (compat packages) | Bridge packages; check their maturity before building on them. |
| `ActivityItem`, `HoverCard`, `MarqueeSelection`, `ResizeGroup`, `ScrollablePane` | No v9 equivalent | Custom implementation. |

Imports: v9 components, `makeStyles`, `mergeClasses`, `shorthands`, `tokens`, `FluentProvider` and the themes are all exported from `@fluentui/react-components` (checked in `react-components/src/index.ts`). Icons come from `@fluentui/react-icons` (for example `DismissRegular`).

## 2. Changed behavior and API limits

Each row names the pattern that fails and what to do instead. The first block is Fluent default (migration docs or source); the **Derived** rows follow from the platform.

| Pattern | What happens in v9 | Do instead |
| --- | --- | --- |
| Style a component with a `styles` prop or `mergeStyles` | The `styles` prop is gone; styling goes through `className` and Griffel | Write a `makeStyles` hook in the component, pass the class through `className`, combine with `mergeClasses` ([Styling components][fluent-styling]). Fluent default. |
| Call `makeStyles(...)` result outside a component or conditionally | `makeStyles` returns a hook (`useStyles()`) that reads the provider's renderer and direction | Call the hook at the top level of a component; pick variants with `mergeClasses(styles.a, cond && styles.b)`. Derived from the hook shape; the Fluent source follows it in every `use…Styles` hook. |
| Two classes set the same property and the wrong one wins | With Griffel, `mergeClasses` resolves conflicts per property so the last Griffel class wins; a plain CSS class does not take part in that resolution | Express overrides as `makeStyles` classes passed last to `mergeClasses`; for plain CSS use cascade layers or specificity ([web-mapping.md](web-mapping.md), section 3). Fluent default for `mergeClasses`; the plain CSS consequence is derived. |
| Render v9 components without a provider | No styling: the token variables are missing | Wrap the app in `FluentProvider` with a theme (`webLightTheme` is the usual v8 replacement) (`Troubleshooting.mdx`). Fluent default. |
| v9 component inside a v8 `Callout` or `Panel` | No styling: the v8 layer is outside the provider's element | Add `PortalCompatProvider` from `@fluentui/react-portal-compat` inside `FluentProvider` (`Troubleshooting.mdx`). Fluent default. |
| v8 `Callout` over a v9 `Dialog` | The Callout appears beneath the Dialog: both layers use the same `z-index` by default, so document order decides | Give the v9 side the v8 layer host with `PortalMountNodeProvider` (`Troubleshooting.mdx`). Fluent default. |
| `Dialog` with `hidden` or `isOpen` | The logic is inverted: v8 `hidden={false}` is visible, v9 `open={true}` is visible | Use `open` and `onOpenChange={(event, data) => setOpen(data.open)}` (`Components/Dialog.mdx`). Fluent default. |
| `isBlocking` mapped to `modalType="alert"` | `alert` is for urgent dialogs that need an explicit response, not for "block outside clicks" | Keep `modalType="modal"` and reject `data.type === 'backdropClick'` in `onOpenChange` when blocking. `modalType` values: `modal`, `non-modal`, `alert` (`Components/Dialog.mdx`). Fluent default. |
| Focus does not return to the opener when the opener is outside the `Dialog` | A controlled `open` prop does not say which element opened it | Put the opener in `DialogTrigger`, or apply `useRestoreFocusTarget()` to it (`Components/Dialog.mdx`). Fluent default. |
| `Dialog` assumed to be a native `<dialog>` | It renders a `div` with `role="dialog"` (or `alertdialog`), `aria-modal`, `tabIndex={-1}`, handles Escape in `onKeyDown`, and relies on Tabster for the focus trap (`useDialogSurface.ts`) | Do not expect `showModal()` semantics, the `cancel` event, or `::backdrop`; style the `DialogSurface` and backdrop slots. Fluent default (source). |
| `TabList` with no selection | v8 `Pivot` selects the first item when nothing is given; v9 `TabList` has no implicit initial selection | Initialize controlled state to the first value, or use `defaultSelectedValue` (`Components/Tabs.mdx`). Fluent default. |
| Tab panels inside the list | The v9 pattern keeps panels outside `TabList` as siblings | Give each `Tab` a stable `id` and each panel `role="tabpanel"` with `aria-labelledby`; render the selected one (`Components/Tabs.mdx`). Fluent default. |
| `Dropdown` and `Combobox` value handling | `onOptionSelect` returns the complete next selection; `selectedOptions` and option `value` are strings; a cleared single selection gives an empty array | Canonicalize keys to strings and keep an id-to-model lookup (`Components/Dropdown.mdx`). Fluent default. |
| `TextField` validation props | `Input` has no `errorMessage`; `Field` composes label, hint, validation and sets `aria-invalid` and an alert role on error and warning messages | Use `Field validationState` and `validationMessage`; do not duplicate the ARIA attributes by hand (`Components/Input.mdx`). Fluent default. |
| v8 validate-on-blur options | `validateOnFocusOut` and `deferredValidationTime` do not exist | Keep the policy in app state: run the validator from `onBlur`, debounce yourself, and guard against stale async results (`Components/Input.mdx`). Fluent default. |
| `MessageBar` defaults | v8 `isMultiline` defaults to `true`; v9 `layout` defaults to `auto` (responsive) | Set `layout="multiline"` to keep the v8 look (`Components/MessageBar.mdx`). Fluent default. |
| `MessageBar` live region | The component announces its text through the provider's announcer; `intent="info"` is polite and other intents assertive; `role` is `group` | Do not add a second `aria-live` around it. See the precedence pitfall in section 3. Fluent default (source: `useMessageBar.ts`). |
| `Checkbox` `indeterminate` | The prop is gone | Use `checked="mixed"` (`ComponentMapping.mdx`). Fluent default. |
| `SpinButton` values | Numeric `value` with `displayValue` for the formatted text | Parse in your handler; do not store the display string (`ComponentMapping.mdx`). Fluent default. |
| `Spinner` label | The default `labelPosition` changes from `bottom` to `after` | Set it explicitly if layout matters (`ComponentMapping.mdx`). Fluent default. |
| `DetailsList` virtualization and row identity | `DataGrid` does not virtualize rows; an array index as row id attaches selection and focus to the wrong item after reordering | Use `getRowId` with a stable key; add an external virtualizer for large sets (`Components/DetailsList.mdx`). Fluent default. |
| Hand-written roving `tabIndex` around v9 `Toolbar`, `TabList`, `Menu` | Duplicates and fights Tabster, which these components use for arrow navigation (`circular: true`; `TabList` also takes the axis from its orientation) | Use the owning component; use `useArrowNavigationGroup({ axis, circular })` only for custom composite widgets (`Components/Focus.mdx`; `useToolbar.ts`, `useTabList.ts`). Fluent default. |
| `Toast` dispatched with no `Toaster` | Nothing is shown: `useToastController(toasterId)` dispatches an event, and the `Toaster` with the same id renders it; without a `FluentProvider` document, the dispatch functions are no-ops (`useToastController.ts`) | Mount one `Toaster` near the root, pass its id to the controller, and keep it mounted. Fluent default (source); the missing-`Toaster` consequence is (derived, not verified). |
| Controlled and uncontrolled props | Components take a controlled prop (`value`, `open`, `checked`, `selectedValue`) or an uncontrolled starting value (`defaultValue`, `defaultOpen`, `defaultSelectedValue`) | Choose one per instance; switching between them while mounted is a React warning. In v9 `Input`, `onChange` has the signature `(event, data)` with `data.value`. Derived from the prop naming in the source and migration docs. |
| Server rendering | Griffel styles need a renderer, and ids need a stable prefix, or hydration fails | Provide `RendererProvider` (from `createDOMRenderer`), `SSRProvider` and `FluentProvider` at the root, and collect styles with `renderToStyleElements` (`Concepts/SSR/SSR.mdx`). Fluent default. A client-only Vite app needs none of this. |
| `defaultOpen` on `Menu` or `Popover` in SSR | React does not support hydrating portals, so a server-rendered open portal causes a hydration error | Open on mount with state after hydration (`useIsSSR`) (`Concepts/SSR/Portals.mdx`). Fluent default. |

## 3. Observed pitfalls

Items here are sourced from Fluent source or docs, or follow from the platform. None was run in a project of ours; confirm against your versions.

- **Reduced motion uses `0.01ms`, not `0s`.** Fluent's Button and Input set `transitionDuration: '0.01ms'` under `@media screen and (prefers-reduced-motion: reduce)` (`useButtonStyles.styles.ts`, `useInputStyles.styles.ts`). A test that expects the computed duration to be exactly `0s` fails on Fluent components; compare with a small threshold such as 0.0001 s ([web-mapping.md](web-mapping.md), section 5). Fluent default (source).
- **The input underline's curve sits in `transition-delay`.** In `useInputStyles.styles.ts` the focus-in and focus-out blocks assign `tokens.curveDecelerateMid` and `tokens.curveAccelerateMid` to `transitionDelay`, which reads like a typo for `transitionTimingFunction`. Copying the block into your CSS carries the quirk along; write `transition-timing-function`. (derived, not verified: whether the delay property ignores the value or the browser rejects it.)
- **`MessageBar` politeness expression.** `useMessageBar.ts` contains `politeness ?? intent === 'info' ? 'polite' : 'assertive'`. By JavaScript operator precedence this reads as `(politeness ?? (intent === 'info')) ? 'polite' : 'assertive'`: any explicit `politeness` value is truthy and yields `'polite'`, even `politeness="assertive"`; without it, `intent="info"` is polite and other intents assertive. Observed by reading `master` at commit `9a56ae0` (2026-08-13), not by running it; check on your version before relying on `politeness="assertive"`. Derived.
- **The focus ring needs `position: relative` and a Tabster attribute.** `createFocusOutlineStyle` draws the ring as an `::after` pseudo-element positioned against the element and keyed on `data-fui-focus-visible`, which Tabster's keyboard-navigation tracking sets; the source comment says the element needs `position: relative`. A custom component that copies the style onto an element without `position: relative`, or outside the provider's tracking, shows no ring or a misplaced one (`react-tabster/src/focus/createFocusOutlineStyle.ts`). Fluent default (source). A global `*:focus { outline: none }` removes the native fallback.
- **`Tooltip` needs a `relationship`.** The prop is required (`'label'`, `'description'`, `'inaccessible'`) and decides how the trigger refers to the tooltip; `'label'` on a button that already has text duplicates the name (`Tooltip.types.ts`). Defaults: `showDelay` 250 ms, `hideDelay` 250 ms, max width 240 px; Escape on the document hides it (`useTooltipBase.tsx`, `useTooltipStyles.styles.ts`). Fluent default (source). A tooltip on a disabled button needs a wrapper or `aria-disabled`, because a disabled button fires no focus or pointer events in all browsers (derived, not verified).
- **Esc closes a native `<dialog>` before your handler sees a decision.** In a native dialog, Esc triggers `cancel` and then `close` as a browser default; a field inside that wants "Esc restores the value, second Esc closes" must `preventDefault()` on its `keydown` (derived, not verified per browser). Fluent's `Dialog` is not native and handles Escape in its own `onKeyDown`, then stops propagation so nested Popover, Menu and Tooltip do not also react (`useDialogSurface.ts`). Derived ([HTML spec][html-dialog]).
- **Popover API and `<dialog>` share the top layer.** An element in the top layer ignores `z-index` against page content, and top-layer elements stack in the order they entered it, so a native popover opened from inside a modal `<dialog>` sits above it and one opened before it sits below. Fluent portals render in a normal `div` mount node with `z-index`, so mixing Fluent portals with native top-layer elements can produce the same "appears beneath" symptom as the v8 `Callout` case. Derived ([MDN: top layer][mdn-top-layer]).
- **`type="number"` is the wrong input for typed fields.** It accepts `e`, `+` and `-`, reports an empty `value` while the text is not a valid number, and a controlled input fed from numeric state loses leading zeros ("007" becomes 7) and cannot hold the half-typed text "1." — the cause of many "my cursor jumps" and "I cannot type a decimal point" reports. Use `type="text"` with `inputMode` and a parser ([web-mapping.md](web-mapping.md), section 7). Derived ([MDN][mdn-number]).
- **`:focus-visible` after a mouse click differs by element.** Text inputs match `:focus-visible` on any focus; buttons and links normally do not match after a click, and Safari does not focus a button on click at all. Fluent avoids the heuristic by tracking input modality with Tabster's keyborg and an attribute. A style that relies on `:focus-visible` for a button ring will not show after a click; that is intended ([MDN][mdn-focus-visible]). Derived.
- **`prefers-reduced-motion` and `prefers-color-scheme` are not available in jsdom.** `window.matchMedia` is not defined, so hooks that read it throw unless the test setup mocks it, and CSS media queries are never evaluated; test the CSS in a real browser (Playwright `emulateMedia`) and the hook with a mocked `matchMedia`. Derived ([Playwright][pw-emulate]).
- **`user-event` with fake timers.** `userEvent.setup()` waits between actions with real timers; under `vi.useFakeTimers()` it hangs unless you pass `advanceTimers: vi.advanceTimersByTime`. This bites tests for tooltip delays and debounced validation. Derived ([user-event options][user-event-options]).
- **Query Fluent components by role and name, not by class.** Class names such as `fui-Input__input` are implementation details, and the Fluent `Input` puts the `input` inside a root `span`; `getByRole('textbox', { name })` survives refactors. Derived.
- **Portal content is outside your component's DOM.** Dialogs, popovers, menus and toasts render into a portal mount node, so `container.querySelector` inside the rendered tree does not find them; use `screen` queries, and in Playwright locate from `page`. Derived.
- **`FluentProvider` per portal root.** Content that renders into a different document or a custom mount node needs the provider's theme variables there (`applyStylesToPortals` defaults to `true`, `useFluentProvider.ts`); a `mountNode` outside any provider shows unstyled content. Fluent default (source); the symptom is derived.

## 4. Sources

- Fluent UI React v9 source and docs: [microsoft/fluentui][fluentui-src]; migration docs under `apps/public-docsite-v9/src/Concepts/Migration/FromV8/`; the interactive docs are at [react.fluentui.dev][fluent-react-docs].
- Griffel: [griffel.js.org][griffel].
- Web platform: [HTML spec: dialog][html-dialog], [MDN: top layer][mdn-top-layer], [MDN: `:focus-visible`][mdn-focus-visible], [MDN: `input type=number`][mdn-number].
- Test tools: [Playwright emulateMedia][pw-emulate], [user-event options][user-event-options].

[fluentui-src]: https://github.com/microsoft/fluentui
[fluent-react-docs]: https://react.fluentui.dev/
[fluent-styling]: https://react.fluentui.dev/?path=/docs/concepts-developer-styling-components--docs
[griffel]: https://griffel.js.org/
[html-dialog]: https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element
[mdn-top-layer]: https://developer.mozilla.org/en-US/docs/Glossary/Top_layer
[mdn-focus-visible]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
[mdn-number]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number
[pw-emulate]: https://playwright.dev/docs/api/class-page#page-emulate-media
[user-event-options]: https://testing-library.com/docs/user-event/options/#advancetimers
