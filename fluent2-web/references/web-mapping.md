# Web mapping: how Fluent concepts become HTML, CSS, React, tokens, behaviors and tests

Read this file when you turn a Fluent rule from the other reference files into web code: choosing selectors for states, wiring tokens, writing transitions, adding keyboard behavior, exposing accessible names, restoring focus, and testing with Testing Library and Playwright. Fluent itself says little about how to write this code; everything here is practical guidance, so treat it as **Derived** unless a line says otherwise. Examples are TypeScript, TSX and CSS for React 19 and Fluent UI React v9 (`@fluentui/react-components`). The v8 to v9 names, changed behavior and observed pitfalls of Fluent UI React are in [fluent-ui-react-notes.md](fluent-ui-react-notes.md). Property, token and hook names change between versions, so confirm each one against the versions your project locks before copying it. Statements about Fluent UI React source were read on the `master` branch of [microsoft/fluentui][fluentui-src] (package `@fluentui/react-components` 9.74.11 at the time of reading); the file paths are given inline.

## Contents

1. [Start from what the project already has](#1-start-from-what-the-project-already-has)
2. [Tokens: two paths](#2-tokens-two-paths)
   - [Path a: Fluent UI React v9](#path-a-fluent-ui-react-v9)
   - [Path b: own components with CSS custom properties](#path-b-own-components-with-css-custom-properties)
   - [Scans for literal colors and shadows](#scans-for-literal-colors-and-shadows)
3. [States as pseudo-classes and attributes](#3-states-as-pseudo-classes-and-attributes)
   - [Precedence](#precedence)
4. [Field anatomy](#4-field-anatomy)
5. [Transitions and reduced motion](#5-transitions-and-reduced-motion)
6. [Behaviors](#6-behaviors)
   - [Roving tabindex](#roving-tabindex)
   - [Toolbar overflow](#toolbar-overflow)
   - [Tooltip defaults](#tooltip-defaults)
   - [F6 regions](#f6-regions)
   - [Shortcut registry](#shortcut-registry)
7. [Typed fields: parser, component, state](#7-typed-fields-parser-component-state)
8. [Keyboard, focus and navigation](#8-keyboard-focus-and-navigation)
   - [Focus ring](#focus-ring)
   - [Tab order walk](#tab-order-walk)
   - [Dialogs, popovers and focus restoration](#dialogs-popovers-and-focus-restoration)
9. [Accessibility API](#9-accessibility-api)
   - [Names, descriptions and live regions](#names-descriptions-and-live-regions)
   - [Name scan with axe](#name-scan-with-axe)
10. [Tests](#10-tests)
    - [Testing Library](#testing-library)
    - [Playwright](#playwright)
    - [Reading transitions](#reading-transitions)
    - [What the tools do not show](#what-the-tools-do-not-show)
11. [Checklist](#11-checklist)
12. [Sources](#12-sources)

Fluent UI React v8 to v9 names, changed behavior and a list of pitfalls live in [fluent-ui-react-notes.md](fluent-ui-react-notes.md). The Fluent rules that the code below implements are in [foundations.md](foundations.md), [inputs.md](inputs.md), [buttons-and-selection.md](buttons-and-selection.md), [navigation.md](navigation.md), [dialogs-and-messages.md](dialogs-and-messages.md), [data-display.md](data-display.md), [content-design.md](content-design.md), [accessibility.md](accessibility.md) and [responsible-ai.md](responsible-ai.md).

## 1. Start from what the project already has

- Find the style setup first: the design brief (`design.md`, `DESIGN.md`, `docs/design*`), the token CSS file, `index.css` (or `global.css`), the theme provider (`FluentProvider`, a `ThemeContext`, or a `data-theme` switch on `<html>`), and the existing components. Note heights, radii, colors, the font and any recorded deviations. Extend those; do not add a second style system. Because two sources of truth drift apart, and a component library and a hand-written stylesheet that both define "the" focus ring show two rings.
- Check which of the two token paths in [section 2](#2-tokens-two-paths) the project already uses, and stay on it. A project with `FluentProvider` in `main.tsx` is on path a, a project with `:root { --... }` and no Fluent packages is on path b. A project with both has a boundary; find it before editing either side.
- Fluent UI React v9 follows Fluent 2, but a project that loads it still may carry its own heights and radii (a brief with 34 px fields and radius 8, for example). Compare the real DOM against `inputs.md` and `foundations.md` and override only what the brief requires.
- Prefer a CSS rule or a `makeStyles` override on the existing component over a new component, and a new component (small API, controlled by props) over copying markup into each view. Because behavior such as parsing and Esc handling belongs in one place.
- Look at how the project names things (`--color-surface` or `--colorNeutralBackground1`, BEM or utility classes, CSS Modules or global CSS) and copy that. A rule that restyles `input` globally is a different system from one that styles `.field__control`; match what is there.
- Before changing a style, find out which layer the current rule lives in (`@layer` order, CSS Modules, Griffel, inline `style`); [Precedence](#precedence) shows why a new rule that is "obviously more specific" may still lose.

## 2. Tokens: two paths

Whichever path the project uses, every color, radius, height, duration and shadow comes from a named token, and views do not contain literals. The scans at the end of this section make that checkable.

### Path a: Fluent UI React v9

`FluentProvider` writes the theme as CSS custom properties on its root element, and the `tokens` object (from `@fluentui/tokens`, re-exported by `@fluentui/react-components`) holds strings of the form `var(--colorNeutralBackground1)`. Verified in `packages/tokens/src/tokens.ts`. A component that is not inside a `FluentProvider` therefore has no values for these variables, and the v8-to-v9 migration notes list "no styling" as the first troubleshooting case (`apps/public-docsite-v9/src/Concepts/Migration/FromV8/Troubleshooting.mdx`).

```tsx
import { useSyncExternalStore, type ReactNode } from 'react';
import { FluentProvider, webDarkTheme, webLightTheme, type Theme } from '@fluentui/react-components';

const darkQuery = '(prefers-color-scheme: dark)';

function useSystemDark(): boolean {
  return useSyncExternalStore(
    (notify) => {
      const media = window.matchMedia(darkQuery);
      media.addEventListener('change', notify);
      return () => media.removeEventListener('change', notify);
    },
    () => window.matchMedia(darkQuery).matches,
    () => false,
  );
}

// Project deviations live in one place and are spread over the Fluent theme.
const light: Theme = { ...webLightTheme, borderRadiusMedium: '8px' };
const dark: Theme = { ...webDarkTheme, borderRadiusMedium: '8px' };

export function AppTheme({ children }: { children: ReactNode }) {
  return <FluentProvider theme={useSystemDark() ? dark : light}>{children}</FluentProvider>;
}
```

`webLightTheme` and `webDarkTheme` are exported by `@fluentui/react-theme` and re-exported by `@fluentui/react-components`; `createLightTheme(brand)` and `createDarkTheme(brand)` build a theme from a brand ramp, and `teamsHighContrastTheme` exists too (checked in `packages/tokens/src/index.ts`). Whether `teamsHighContrastTheme` is the right answer for Windows contrast themes is (derived, not verified): the platform route is `forced-colors` in [section 3](#3-states-as-pseudo-classes-and-attributes) and [section 10](#playwright).

Styles for your own components use Griffel (`makeStyles`) with `tokens`; `mergeClasses` combines class names so that the last Griffel class for a property wins:

```tsx
import { makeStyles, mergeClasses, shorthands, tokens } from '@fluentui/react-components';

const useStyles = makeStyles({
  control: {
    minHeight: '34px', // project brief; Fluent default is 32 px
    borderRadius: tokens.borderRadiusMedium,
    backgroundColor: tokens.colorNeutralBackground1,
    color: tokens.colorNeutralForeground1,
    fontFamily: tokens.fontFamilyBase,
    ...shorthands.border('1px', 'solid', tokens.colorNeutralStroke1),
    borderBottomColor: tokens.colorNeutralStrokeAccessible,
    ':hover': { borderBottomColor: tokens.colorNeutralStrokeAccessibleHover },
  },
  invalid: { borderBottomColor: tokens.colorPaletteRedForeground1 },
});

export function TextControl({ invalid, className, ...rest }: React.ComponentProps<'input'> & { invalid?: boolean }) {
  const styles = useStyles();
  return <input className={mergeClasses(styles.control, invalid && styles.invalid, className)} {...rest} />;
}
```

Rules for this path:

- Use the tokens object, never a hex value, in `makeStyles` (Fluent default; the Fluent source does the same, for example `useFieldStyles.styles.ts` and `useInputStyles.styles.ts`). The token names are the contract; the values change per theme.
- Put the `FluentProvider` at the root, and pass `theme` explicitly. In the Fluent source, a provider without any theme logs a warning (`useFluentProvider.ts`).
- Components that render into portals (Dialog, Popover, Menu, Tooltip, Toast) take their tokens from the provider that wraps them; with several providers, the portal uses the nearest one (`applyStylesToPortals`, default `true`, in `useFluentProvider.ts`).
- The `shorthands` helper is still used inside Fluent's own source (`shorthands.borderColor(...)` in `useInputStyles.styles.ts`). Whether the pinned Griffel version also accepts plain CSS shorthand strings in `makeStyles` is (derived, not verified); the helper works either way.
- Heights, widths and spacing that the brief fixes (34 px) have no token; write them as literals in `makeStyles` or as your own custom properties, and record them as deviations ([foundations.md](foundations.md), section 11).

### Path b: own components with CSS custom properties

Declare the tokens once on `:root`, repeat the dark values in a `prefers-color-scheme` block that a `[data-theme="light"]` attribute can switch off, and add a `[data-theme="dark"]` block for the manual choice. Names follow the Fluent token names (the second column) so that a later move to path a is a rename-free change, and so that [foundations.md](foundations.md) can be read without a translation table. The hex values below are the Fluent defaults read from `packages/tokens/src/alias/lightColor.ts` and `darkColor.ts`; the project's own values win.

```css
/* tokens.css: the only file that may contain color literals */
:root {
  color-scheme: light;
  --colorNeutralBackground1: #ffffff;
  --colorNeutralForeground1: #242424;
  --colorNeutralForeground3: #616161;
  --colorNeutralStroke1: #d1d1d1;
  --colorNeutralStrokeAccessible: #616161;
  --colorNeutralStrokeAccessibleHover: #575757;
  --colorNeutralStrokeDisabled: #e0e0e0;
  --colorCompoundBrandStroke: #0078d4;
  --colorStrokeFocus1: #ffffff;
  --colorStrokeFocus2: #000000;
  --colorPaletteRedForeground1: #b10e1c; /* placeholder: Fluent derives it from its red status palette; use the project's danger text color */
  --borderRadiusMedium: 4px;     /* project brief may say 8px */
  --controlHeight: 32px;         /* project brief may say 34px */
  --durationUltraFast: 50ms;
  --durationFaster: 100ms;
  --durationNormal: 200ms;
  --curveEasyEase: cubic-bezier(0.33, 0, 0.67, 1);
  --curveDecelerateMid: cubic-bezier(0, 0, 0, 1);
  --curveAccelerateMid: cubic-bezier(1, 0, 1, 1);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --colorNeutralBackground1: #292929;
    --colorNeutralForeground1: #ffffff;
    --colorNeutralForeground3: #adadad;
    --colorNeutralStroke1: #666666;
    --colorNeutralStrokeAccessible: #adadad;
    --colorNeutralStrokeAccessibleHover: #bdbdbd;
    --colorCompoundBrandStroke: #2899f5;
    --colorStrokeFocus1: #000000;
    --colorStrokeFocus2: #ffffff;
  }
}

:root[data-theme="dark"] {
  color-scheme: dark;
  --colorNeutralBackground1: #292929;
  /* ...the same dark values again; keep both blocks in step (see the note below) */
}
```

Notes:

- The duration and curve values are from `packages/tokens/src/global/durations.ts` and `curves.ts` (Fluent default): `durationUltraFast` 50 ms, `durationFaster` 100 ms, `durationNormal` 200 ms, `curveEasyEase` `cubic-bezier(0.33,0,0.67,1)`, `curveDecelerateMid` `cubic-bezier(0,0,0,1)`, `curveAccelerateMid` `cubic-bezier(1,0,1,1)`.
- The dark values are written twice (media query and attribute). That duplication is the known cost of a manual override; a test that compares the two blocks is cheap, or generate both from one source. The alternative without duplication is `color: light-dark(#242424, #ffffff)` together with `color-scheme: light dark` on `:root` and `color-scheme: light` or `dark` set by the `[data-theme]` attribute; `light-dark()` works for colors only, not for lengths or durations ([MDN: light-dark()][mdn-light-dark]). Derived.
- Set `color-scheme` so that built-in controls (scrollbars, form controls, canvas text) follow the theme ([MDN: color-scheme][mdn-color-scheme]). Derived.
- A manual `[data-theme]` choice must be applied before first paint (inline script in `index.html` or the framework's equivalent), or the page flashes the wrong theme. Derived.
- If a project mixes both paths, own `:root` variables with the same names as Fluent's are shadowed inside a `FluentProvider` (the provider sets them on its own element). Use a different prefix for own tokens (`--app-`) when both exist, or read the provider's values (derived, not verified for your version).
- Contrast of the Fluent default field border: `#d1d1d1` on white measures 1.53:1 in the light theme and `#666666` on `#292929` 2.53:1 in the dark theme, which is why Fluent draws the bottom edge with `colorNeutralStrokeAccessible` (`#616161` on white 6.19:1, `#adadad` on `#292929` 6.48:1; measured with the WCAG formula). See [foundations.md](foundations.md) for the rule and the source of the border tokens.

Shadows are colors too. Declare them as tokens per theme (a dark theme needs a stronger shadow alpha than a light one) and reference the token:

```css
:root { --shadow16: 0 8px 16px rgb(0 0 0 / 0.14), 0 0 2px rgb(0 0 0 / 0.12); } /* placeholder; use the project's value */
:root[data-theme="dark"] { --shadow16: 0 8px 16px rgb(0 0 0 / 0.28), 0 0 2px rgb(0 0 0 / 0.24); }
.popover { box-shadow: var(--shadow16); }
```

The values are placeholders; use the project's shadow tokens ([foundations.md](foundations.md), section 7).

### Scans for literal colors and shadows

Run these in CI over the source folders, excluding the token file, and read each hit. Adjust the folder names (`src` here) and extend the color-name list with the names your code base uses; allow `transparent`, `currentColor` and `inherit` where they are meant. Every literal that gets through is a color that the dark theme and forced colors cannot repaint. Scanning for `#` alone misses color functions, named colors, shadows and colors built in code, so run all of them.

```bash
# 1. hex colors (3 to 8 digits, with alpha) in CSS, also inside box-shadow and gradients
rg -n --glob '*.css' --glob '!src/styles/tokens.css' '#[0-9A-Fa-f]{3,8}\b' src
# 2. color functions in CSS
rg -n --glob '*.css' --glob '!src/styles/tokens.css' '\b(rgb|rgba|hsl|hsla|hwb|lab|lch|oklab|oklch|color-mix)\(' src
# 3. named colors in color-bearing properties
rg -n --glob '*.css' -e '(color|background(-color)?|border(-[a-z]+)?-color|fill|stroke|outline-color)\s*:\s*(white|black|red|green|blue|gray|grey|yellow|orange|purple)\b' src
# 4. hex and color functions in TS and TSX (Griffel styles, inline styles, constants)
rg -n --glob '*.{ts,tsx}' '#[0-9A-Fa-f]{3,8}\b|\b(rgb|rgba|hsl|hsla)\(' src
# 5. inline style attributes that carry colors or shadows
rg -n --glob '*.tsx' 'style=\{\{[^}]*(color|background|border|boxShadow|fill|stroke)' src
# 6. SVG presentation attributes with literals
rg -n --glob '*.tsx' '(fill|stroke|stop-color|stopColor)="#' src
# 7. shadows written inline instead of through a token (CSS and Griffel)
rg -nP --glob '*.css' 'box-shadow\s*:\s*(?!var\(|none|inherit|unset)' src
rg -nP --glob '*.{ts,tsx}' 'boxShadow\s*:\s*[\x27"`](?!var\()' src
# 8. colors built or set in code
rg -n --glob '*.{ts,tsx}' 'new Color\(|chroma\(|tinycolor|\.style\.(color|background|borderColor)|style\.setProperty\(\x27(color|background)' src
```

Also check that no component hard-codes a `color-scheme` or reads `matchMedia('(prefers-color-scheme')` on its own; the theme provider is the only place that does. Derived.

## 3. States as pseudo-classes and attributes

| Fluent state | CSS selector | Note |
| --- | --- | --- |
| Hover | `:hover` | Wrap in `@media (hover: hover)` when touch devices should not keep a sticky hover. |
| Pressed | `:active` | Buttons and toggle buttons. For text inputs a pressed look is rarely needed. |
| Keyboard focus | `:focus-visible` | The browser decides: keyboard focus yes; mouse focus on a button no; focus in a text input always yes ([MDN][mdn-focus-visible]). That is what a field needs, because the field must show where typing goes. |
| Focus inside a composite | `:focus-within` | Container highlight; Fluent's Input draws its underline on `:focus-within` of the root (`useInputStyles.styles.ts`). |
| Disabled | `:disabled` for form controls; `[aria-disabled="true"]` for elements that stay focusable | Avoid dimming labels and help text through the container. |
| Invalid | `[aria-invalid="true"]` (set by your code from state) and `:user-invalid` | `:user-invalid` matches only after the user interacted, which matches "no error on a field nobody touched" ([MDN][mdn-user-invalid]). It follows constraint validation, so a custom parser error still needs `aria-invalid`. |
| Selected, current | `[aria-selected="true"]`, `[aria-current="page"]`, `[aria-pressed="true"]`, `[aria-checked="true"]` | Style by the attribute you set for assistive technology, so look and semantics cannot drift apart. |
| Open, closed, active (headless libraries) | `[data-state="open"]` and similar `data-*` attributes | Only when a library or your code sets them; there is no standard `data-state`. |
| Read-only | `input[readonly]` | `:read-only` also matches `select`, checkboxes and non-editable elements, so it is the wrong selector for "a field that cannot be edited". |
| Placeholder | `::placeholder` | Check its contrast (about 4.5:1) like any text; browsers default to a reduced opacity. |
| Forced colors | `@media (forced-colors: active)` | System colors replace yours; use system color keywords (`GrayText`, `Highlight`, `ButtonText`) where a state would otherwise vanish. Fluent's Input does this for its disabled border (`GrayText`) and its focus outline (`Highlight`). |

Rules that save debugging time:

- State colors live in the stylesheet, not in the element. An inline `style` attribute beats every selector, so a hand-set `style={{ background }}` makes hover and disabled look broken. Derived from the cascade (below).
- A hover rule that reuses the same token as the rest state is invisible. When you change the rest state, re-check every state that shares the token.
- Fluent's disabled state is exempt from contrast rules, but keep the label and help text readable: put the disabled look on the control element, not on the field container (`opacity` on a wrapper dims the label too).
- `:disabled` removes the element from the tab order and from the accessibility tree's focusable set. When a disabled button needs an explanation (a tooltip that says why), prefer `aria-disabled="true"` with a click handler that does nothing, so keyboard users can still reach the explanation. Derived; trade-off: the browser no longer blocks the click, so the handler must.
- Do not remove `outline` without a replacement; use `:focus-visible` and see [Focus ring](#focus-ring).
- `:user-invalid` is not supported everywhere in the same way and does not know about your parser; the reliable pattern is a state flag in React that sets `aria-invalid` and a class. Derived.

### Precedence

On the web the cascade decides which value a property ends up with. The order below is the CSS cascade ([MDN: Cascade][mdn-cascade]; [CSS Cascade Level 5][css-cascade]); the consequences are derived from it.

1. **Importance and origin.** An author `!important` declaration beats a normal author declaration; for `!important`, the layer order reverses (the earlier layer wins).
2. **The `style` attribute** beats every normal selector in every layer. React `style={{ ... }}` is this.
3. **Cascade layers** (`@layer`): among normal declarations a later layer beats an earlier one regardless of specificity, and **unlayered** rules beat all layers.
4. **Specificity**, then 5. **source order**.

Consequences seen in practice:

| Situation | What happens | What to do |
| --- | --- | --- |
| A component library ships unlayered CSS and your override sits in an early `@layer` | Your rule loses regardless of specificity | Declare the layer order once (`@layer reset, tokens, library, app;`) and put your overrides in a later layer than the library's. Griffel's classes are not in a layer by default, so overrides against Fluent components go unlayered or through `mergeClasses` (derived, not verified for your Griffel setup). |
| Your plain class competes with Fluent's Griffel classes | Griffel emits state rules such as `:hover` and `:focus-within` with higher specificity than a base class, so a base override can lose exactly in those states | Pass the override through `className` and `mergeClasses` with a `makeStyles` class, so Griffel resolves the conflict per property and the last class wins. Derived; Fluent's component styles are merged so that a user `className` comes last ([Styling components][fluent-styling]). |
| Inline `style` on an element that also has hover styles | Hover never shows | Move the value into a class or a custom property: `style={{ '--field-bg': value }}` and `background: var(--field-bg, var(--colorNeutralBackground1))` in the stylesheet. |
| `!important` | Beats everything, including later layers | Reserve it for the two cases that must outrank unknown styles: `@media (forced-colors: active)` fixes and the reduced-motion override ([section 5](#5-transitions-and-reduced-motion)). Anything else is a sign that the layer order is wrong. Derived. |
| Dialog layout set by an attribute | A class cannot override `style="..."` | Move such values from the element into a stylesheet, so another rule can override them (compact layout, narrow window). |
| A tooltip or popover rendered in a portal | Styles keyed to a parent selector (`.chip span`) do not reach the portal content, and tokens come from the provider that wraps the portal | Style the portal content by its own class; check that the theme variables exist in the portal root (see [fluent-ui-react-notes.md](fluent-ui-react-notes.md)). |

When a property does not change, find out which rule wins before changing anything: DevTools "Styles" pane shows struck-through losers and the layer name; `getComputedStyle(element).getPropertyValue(...)` shows the result; a Playwright check on the computed value proves the fix ([Playwright](#playwright)).

## 4. Field anatomy

A field is label, control, help text and error text, wired together with `id` and `aria-describedby`. The rules are in [inputs.md](inputs.md); this section is the markup.

```tsx
import { useId, type ReactNode } from 'react';

type FieldProps = {
  label: string;
  required?: boolean;
  help?: string;
  error?: string | null;
  children: (control: { id: string; 'aria-describedby'?: string; 'aria-invalid'?: true; 'aria-required'?: true }) => ReactNode;
};

export function Field({ label, required, help, error, children }: FieldProps) {
  const id = useId();
  const helpId = `${id}-help`;
  const errorId = `${id}-error`;
  const describedBy = [error ? errorId : help ? helpId : null].filter(Boolean).join(' ') || undefined;

  return (
    <div className="field" data-invalid={error ? '' : undefined}>
      <label className="field__label" htmlFor={id}>
        {label}
        {required && <span className="field__required" aria-hidden="true"> *</span>}
      </label>
      {children({ id, 'aria-describedby': describedBy, 'aria-invalid': error ? true : undefined, 'aria-required': required ? true : undefined })}
      {error ? (
        <p className="field__error" id={errorId} role="alert">{error}</p>
      ) : help ? (
        <p className="field__help" id={helpId}>{help}</p>
      ) : null}
    </div>
  );
}
```

Points that matter:

- **Label above the control, always visible.** A placeholder is an example, not a label ([inputs.md](inputs.md)); the `label` element with `htmlFor` gives the control its accessible name and makes the label a click target.
- **Required marker.** The asterisk is decorative (`aria-hidden`) and the control carries `required` or `aria-required="true"`, so the screen reader says "required" once. Use the native `required` attribute only when the browser's own validation bubbles are wanted; with custom validation use `aria-required` and `noValidate` on the form. Derived from [WAI-ARIA `aria-required`][aria-required] and the HTML spec.
- **Error replaces help** in the same slot (the example shows one or the other), and is tied to the control with `aria-describedby` and `aria-invalid="true"`. The error text names the problem and the way out ([content-design.md](content-design.md)); color alone never carries the error, so add an icon and the text.
- **`role="alert"` on the error** makes a screen reader announce it when it appears. It announces on insertion, so render the element only when there is an error, or the first error is spoken twice (once as an alert, once when the control is focused). Whether to prefer `aria-live="polite"` for an error that appears while the user is still typing elsewhere is (derived, not verified); the Fluent `Field` follows the alert approach (below).
- **Fluent's Field alternative (path a).** `Field` from `@fluentui/react-components` wires label, hint, validation message and icon, sets `aria-invalid` and gives error and warning messages an alert role; the v8-to-v9 notes tell you not to duplicate those attributes by hand (`Migration/FromV8/Components/Input.mdx`). Props verified in `Field.types.ts`: `label`, `hint`, `validationState` (`'error' | 'warning' | 'success' | 'none'`), `validationMessage`, `required` (asterisk and `aria-required`), `orientation` (`'vertical' | 'horizontal'`). Its message styles use `colorPaletteRedForeground1` for errors and `colorNeutralForeground3` for the secondary text, 12 px icon (`useFieldStyles.styles.ts`).

```tsx
<Field label="Start time" required hint="Hours and minutes, for example 9:30" validationState={error ? 'error' : 'none'} validationMessage={error ?? undefined}>
  <Input value={text} onChange={(_, data) => setText(data.value)} onBlur={commit} />
</Field>
```

### The underline

Fluent's Input has a 1 px border with a darker bottom edge and a 2 px brand underline on focus that grows from the center. In the Fluent source (`useInputStyles.styles.ts`, Fluent default) it is a `::after` pseudo-element on the root:

- Rest: `transform: scaleX(0)`, `transitionProperty: transform`, duration `durationUltraFast` (50 ms) for the way out.
- `:focus-within::after`: `transform: scaleX(1)`, duration `durationNormal` (200 ms) for the way in.
- Height `max(2px, borderRadiusMedium)` with a 2 px `borderBottom` in `colorCompoundBrandStroke`, clipped so that the corners do not show "horns"; hover and pressed use `colorNeutralStrokeAccessibleHover` and `colorNeutralStrokeAccessiblePressed` for the bottom border.
- Under `prefers-reduced-motion: reduce` the durations become `0.01ms`.
- The source assigns the curve tokens (`curveDecelerateMid`, `curveAccelerateMid`) to `transitionDelay`. A curve is not a valid delay, so this reads like a typo for `transitionTimingFunction` (derived, not verified); in your own CSS write `transition-timing-function`.

Own-CSS version of the same behavior:

```css
.field__box {
  position: relative;
  display: flex;
  align-items: center;
  min-height: var(--controlHeight);
  border: 1px solid var(--colorNeutralStroke1);
  border-bottom-color: var(--colorNeutralStrokeAccessible);
  border-radius: var(--borderRadiusMedium);
  background: var(--colorNeutralBackground1);
}
.field__box::after {
  content: "";
  position: absolute;
  inset: auto -1px -1px;                     /* sit on the bottom border */
  height: max(2px, var(--borderRadiusMedium));
  border-bottom: 2px solid var(--colorCompoundBrandStroke);
  border-radius: 0 0 var(--borderRadiusMedium) var(--borderRadiusMedium);
  clip-path: inset(calc(100% - 2px) 0 0 0);  /* trims the "horns" at the corners */
  transform: scaleX(0);
  transition: transform var(--durationUltraFast) var(--curveAccelerateMid);   /* leaves in about 50 ms */
  pointer-events: none;
}
.field__box:focus-within::after {
  transform: scaleX(1);
  transition: transform var(--durationNormal) var(--curveDecelerateMid);      /* grows in about 200 ms */
}
.field__box:hover { border-bottom-color: var(--colorNeutralStrokeAccessibleHover); }
.field__box:has([aria-invalid="true"]) { border-bottom-color: var(--colorPaletteRedForeground1); }
.field__box:has(input:disabled) { border-color: var(--colorNeutralStrokeDisabled); }
.field__box:has(input:disabled)::after { content: none; }

.field__control {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: 0;                                /* the underline is the focus indicator on this element */
  background: transparent;
  color: inherit;
  font: inherit;
}
@media (forced-colors: active) {
  .field__box::after { border-bottom-color: Highlight; }
  .field__box:has(input:disabled) { border-color: GrayText; }
}
```

The wrapper draws the underline, so the underline shows on `:focus-within` and therefore also after a mouse click; the focus indicator must always show where typing goes. The `outline: 0` on the inner control is acceptable only because the underline replaces it and meets the 3:1 non-text contrast (check `colorCompoundBrandStroke` against the field background; Fluent's light value `#0078d4` on white measures 4.53:1). In forced colors `Highlight` keeps it visible. Derived; the transition values are Fluent default.

## 5. Transitions and reduced motion

Transitions explain state changes; they do not decorate. Rules:

- Animate **color, opacity and transform** only. Transitioning `width`, `height`, `top`, `margin` or `padding` forces layout on every frame. For size changes use `transform`, or animate a grid track (`grid-template-rows: 0fr` to `1fr`) deliberately and test it. Derived; see [web.dev: animations guide][webdev-animations].
- Durations and curves come from the tokens in [section 2](#2-tokens-two-paths). Fluent's Button transitions `background`, `border` and `color` over `durationFaster` (100 ms) with `curveEasyEase` (`useButtonStyles.styles.ts`, Fluent default). Enter about 200 ms with a decelerating curve, exit shorter (50 to 120 ms) with an accelerating curve ([foundations.md](foundations.md), motion).
- List the properties; never `transition: all`, because it animates properties you did not mean to (including layout ones added later). Derived.

```css
.button {
  background: var(--colorNeutralBackground1);
  transition-property: background-color, border-color, color;
  transition-duration: var(--durationFaster);
  transition-timing-function: var(--curveEasyEase);
}
.button:active { transform: scale(0.97); transition: transform var(--durationUltraFast) var(--curveEasyEase); }
```

### Reduced motion

Provide two inputs that lead to the same result: the operating system preference (`prefers-reduced-motion`) and an in-app "reduce motion" setting that applies a class on `<html>`. Both zero every transition and animation, including press scales, fades and the input underline ([WCAG 2.3.3 Animation from Interactions][wcag-233], [technique C39][wcag-c39]).

```css
/* tokens.css: durations follow the switch, so every consumer of a token is covered */
@media (prefers-reduced-motion: reduce) {
  :root { --durationUltraFast: 0.01ms; --durationFaster: 0.01ms; --durationNormal: 0.01ms; }
}
:root.reduce-motion { --durationUltraFast: 0.01ms; --durationFaster: 0.01ms; --durationNormal: 0.01ms; }

/* catch-all for code that does not use the tokens (third-party CSS, hand-written values) */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }
}
:root.reduce-motion *, :root.reduce-motion *::before, :root.reduce-motion *::after {
  transition-duration: 0.01ms !important;
  animation-duration: 0.01ms !important;
  animation-iteration-count: 1 !important;
  scroll-behavior: auto !important;
}
```

```ts
// reduced-motion.ts: one switch, three sources (setting, OS, default)
const storageKey = 'reduce-motion';

export function applyReducedMotion(setting: 'system' | 'on' | 'off'): void {
  const root = document.documentElement;
  root.classList.toggle('reduce-motion', setting === 'on');
  try { localStorage.setItem(storageKey, setting); } catch { /* storage may be blocked */ }
}
```

Why the duration is `0.01ms` and not `0s`: Fluent's own components do the same under `@media screen and (prefers-reduced-motion: reduce)` (`useButtonStyles.styles.ts`, `useInputStyles.styles.ts`; Fluent default), so a transition still fires `transitionend` and code that waits for it does not hang. A duration of `0s` starts no transition at all and never fires the event. That reasoning is derived; the 0.01 ms values are from the source. The `!important` is the one accepted use besides forced-colors fixes: the override must outrank Griffel's unlayered atomic classes and any third-party CSS ([Precedence](#precedence)). Derived.

The in-app class matters because the OS setting is not always reachable (managed machines, kiosks, a user who wants it off only in this app). A test that can only run when the OS setting is on never runs; that is why the Playwright test below uses `emulateMedia`.

Test that proves no transition remains (Playwright, real browser, so real computed styles):

```ts
import { expect, test } from '@playwright/test';

const toSeconds = (list: string): number[] =>
  list.split(',').map((part) => {
    const value = parseFloat(part);
    return part.trim().endsWith('ms') ? value / 1000 : value;
  });

test('reduced motion leaves no visible transition', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  for (const route of ['/', '/bookings/new', '/settings']) {
    await page.goto(route);
    const leaks = await page.evaluate(() => {
      const toSec = (list: string) => list.split(',').map((p) => (p.trim().endsWith('ms') ? parseFloat(p) / 1000 : parseFloat(p)));
      const result: string[] = [];
      for (const element of document.querySelectorAll<HTMLElement>('body *')) {
        if (element.getClientRects().length === 0) continue;              // not rendered, not seen by the user
        for (const pseudo of [null, '::before', '::after'] as const) {
          const style = getComputedStyle(element, pseudo);
          const longest = Math.max(...toSec(style.transitionDuration), ...toSec(style.animationDuration));
          if (longest > 0.0001) result.push(`${element.tagName}.${element.className} ${pseudo ?? ''} ${style.transitionDuration} / ${style.animationDuration}`);
        }
      }
      return result;
    });
    expect(leaks, route).toEqual([]);
  }
});
```

The threshold is `0.0001` s so that Fluent's `0.01ms` (1e-5 s) passes and 100 ms does not. `getComputedStyle(...).transitionDuration` returns a comma-separated list per property (for example `0.1s, 0.1s, 0.1s`); the helper splits it. Run the same walk without the emulation once and check that the token durations (50, 100, 200 ms) are found, so the test cannot pass by finding nothing. Also run it with the in-app class set (`page.evaluate(() => document.documentElement.classList.add('reduce-motion'))`) and without `emulateMedia`.

## 6. Behaviors

Put keyboard and focus behavior that applies to many components into hooks or small components, so a component opts in with one call and one test pins the behavior. In Fluent UI React v9 components (Tabs, Toolbar, Menu, Radio group), do not write your own roving tabindex around them; Fluent delegates it to Tabster, and the migration notes say not to add a manual implementation next to it (`Migration/FromV8/Components/Focus.mdx`). The hooks below are for your own components.

### Roving tabindex

A tab strip, radio group or toolbar is one tab stop: Tab lands on the active item, the next Tab leaves the group, arrows move inside ([ARIA APG: Developing a keyboard interface][apg-keyboard], [Tabs pattern][apg-tabs]). Fluent's `TabList` and `Toolbar` use Tabster's `useArrowNavigationGroup` with `circular: true`; `TabList` also takes `axis` from its orientation (`useTabList.ts`, `useToolbar.ts`; Fluent default). Whether the ends wrap is a project decision; the APG allows both.

```tsx
import { useRef, useState, type KeyboardEvent } from 'react';

type Options = { count: number; orientation?: 'horizontal' | 'vertical'; wrap?: boolean; initial?: number; onMove?: (index: number) => void };

export function useRovingTabIndex({ count, orientation = 'horizontal', wrap = false, initial = 0, onMove }: Options) {
  const [active, setActive] = useState(initial);
  const items = useRef<(HTMLElement | null)[]>([]);

  const focusAt = (index: number) => {
    setActive(index);
    items.current[index]?.focus();
    onMove?.(index);                                  // radio groups and tabs with automatic activation select here
  };

  const onKeyDown = (event: KeyboardEvent) => {
    const forward = orientation === 'horizontal' ? 'ArrowRight' : 'ArrowDown';
    const backward = orientation === 'horizontal' ? 'ArrowLeft' : 'ArrowUp';
    let next = active;
    if (event.key === forward) next = active + 1;
    else if (event.key === backward) next = active - 1;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = count - 1;
    else return;
    if (next < 0 || next >= count) {
      if (!wrap) return;                              // no wrap at the ends
      next = (next + count) % count;
    }
    event.preventDefault();
    focusAt(next);
  };

  const getItemProps = (index: number) => ({
    ref: (element: HTMLElement | null) => { items.current[index] = element; },
    tabIndex: index === active ? 0 : -1,              // programmatic focus still works with -1
    onFocus: () => setActive(index),                  // a click or a script moves the tab stop too
  });

  return { onKeyDown, getItemProps };
}
```

```tsx
function Segments({ options, value, onChange }: { options: string[]; value: string; onChange: (v: string) => void }) {
  const { onKeyDown, getItemProps } = useRovingTabIndex({
    count: options.length,
    initial: Math.max(0, options.indexOf(value)),
    onMove: (index) => onChange(options[index]),      // selection follows focus (radio group)
  });
  return (
    <div role="radiogroup" aria-label="View" onKeyDown={onKeyDown}>
      {options.map((option, index) => (
        <button key={option} type="button" role="radio" aria-checked={option === value} {...getItemProps(index)}>{option}</button>
      ))}
    </div>
  );
}
```

Tests: Tab into the group lands on the selected item; the next Tab leaves the group; Right and Left move focus (and selection for radios); the last item does not wrap (or wraps, by the decision); `focus()` on an item with `tabIndex={-1}` still works. With no selection yet, the first item must be the tab stop (`initial` 0), or the group cannot be entered by keyboard. Derived.

### Toolbar overflow

A toolbar that never wraps moves the items that do not fit into a menu ([navigation.md](navigation.md)). With Fluent UI React v9 use `Overflow`, `OverflowItem`, `useIsOverflowItemVisible` and `useOverflowMenu` from `@fluentui/react-components` (exports checked in `react-overflow/library/src/index.ts`); the v8 `CommandBar` notes map it to `Toolbar` plus `Overflow` (`Migration/FromV8/Components/CommandBar.mdx`). For your own toolbar, measure the natural width of each item once while all are rendered (and again after `document.fonts.ready` or a language switch), observe the container with a `ResizeObserver`, and keep as many items as fit next to the "More" button (Derived):

```tsx
const recompute = () => {
  let used = moreButtonWidth;
  let count = 0;
  for (const width of naturalWidths) {
    if (used + width > container.clientWidth) break;
    used += width;
    count += 1;
  }
  setVisible(total <= container.clientWidth ? itemCount : count);
};
new ResizeObserver(recompute).observe(container);
```

Render items `0..visible-1` in the toolbar and the rest in a menu opened by a "More" button. Remove hidden items from the tab order completely: do not render them, or give them the `hidden` or `inert` attribute; an item that is only transparent (`opacity: 0`) or moved off screen still takes Tab stops. Because the visible layout and the focus order must agree. Icon-only items need a text label in the menu. The measuring pass needs all items rendered once, so measure on mount and when labels change (fonts loading or a language switch changes widths; re-measure on `document.fonts.ready`). Tests: at the minimum viewport and at a wide viewport, press Tab through the toolbar and compare the focus sequence with the visible items plus "More" (Playwright, because jsdom has no layout); open the menu and check that every hidden command is in it.

### Tooltip defaults

Fluent default (`useTooltipBase.tsx`): `showDelay` 250 ms and `hideDelay` 250 ms; the tooltip shows on focus of the trigger as well as on hover; Escape on the document hides it; max width 240 px, 12 px text (`useTooltipStyles.styles.ts`, `Tooltip.types.ts`). `relationship` is required: `'label'`, `'description'` or `'inaccessible'`, which decides how the trigger refers to it (`aria-labelledby` or `aria-describedby`).

For your own tooltip keep one default for the whole app (the project's tokens, not constants), show it on focus as well as hover, and give the open tooltip a document-level Escape handler:

```tsx
useEffect(() => {
  if (!open) return;
  const onKey = (event: KeyboardEvent) => { if (event.key === 'Escape') { event.stopPropagation(); hide(); } };
  document.addEventListener('keydown', onKey, true);   // capture phase: runs before the dialog's handler
  return () => document.removeEventListener('keydown', onKey, true);
}, [open]);
// trigger: onFocus/onMouseEnter -> setTimeout(show, 250); onBlur/onMouseLeave -> hide; aria-describedby={tooltipId}
// tooltip: role="tooltip" id={tooltipId}, max-width 240px
```

Esc must dismiss the tooltip without closing the surrounding dialog; the capture-phase handler with `stopPropagation` does that, as Fluent's does ("stop propagation to avoid conflicting with other elements that listen for Escape", in `useTooltipBase.tsx`). A tooltip must stay open while the pointer is over it and be dismissible without moving the pointer ([WCAG 1.4.13 Content on Hover or Focus][wcag-1413]). Tests: focus the trigger, advance fake timers by 250 ms, expect the tooltip; press Esc, expect it gone while the dialog around it stays open. A disabled button does not fire focus or pointer events in all browsers; see [Section 3](#3-states-as-pseudo-classes-and-attributes) for `aria-disabled`.

### F6 regions

Windows apps cycle between panes with F6; browsers use F6 for the address bar, so the web counterpart is an app-level convention (Derived). Mark landmark regions (`header`, `nav`, `main`, `aside`, `footer`, or `role="region"` with a name) and let one document handler cycle focus through them in screen order. Check that no global shortcut already uses F6 and that the browser's own F6 is not the only way to reach the regions (a skip link and landmark navigation in screen readers remain the baseline: [WCAG 2.4.1 Bypass Blocks][wcag-241]).

```ts
const regionSelector = '[data-region], main, nav, aside, header, footer, [role="region"][aria-label], [role="region"][aria-labelledby]';

function visibleRegions(): HTMLElement[] {
  return [...document.querySelectorAll<HTMLElement>(regionSelector)]
    .filter((element) => element.getClientRects().length > 0)
    .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top || a.getBoundingClientRect().left - b.getBoundingClientRect().left);   // screen order, not DOM order
}

function focusRegion(region: HTMLElement) {
  const target = region.querySelector<HTMLElement>('[data-region-focus]')
    ?? region.querySelector<HTMLElement>('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])');
  (target ?? region).focus();   // a region without focusable content needs tabindex="-1" to take focus
}

export function installRegionCycling(): () => void {
  const onKeyDown = (event: KeyboardEvent) => {
    if (event.key !== 'F6' || event.defaultPrevented) return;
    const regions = visibleRegions();
    if (regions.length === 0) return;
    const current = regions.findIndex((region) => region.contains(document.activeElement));
    const step = event.shiftKey ? -1 : 1;
    const from = current >= 0 ? current : step > 0 ? -1 : 0;
    focusRegion(regions[(from + step + regions.length) % regions.length]);
    event.preventDefault();
  };
  document.addEventListener('keydown', onKeyDown);
  return () => document.removeEventListener('keydown', onKeyDown);
}
```

Rules in the code: order by screen position, because DOM order and layout differ with grid and flex `order`; an explicit `data-region-focus` target for a region that handles keys itself (a calendar grid with its own arrows); regions need a name (`aria-label`) so a screen reader announces where focus landed. Test with real keys: press F6 repeatedly and compare the region names that hold focus with the expected order including wrap-around; Shift+F6 reverses. The rule text is in [accessibility.md](accessibility.md).

### Shortcut registry

One registry makes shortcuts discoverable (tooltips, help dialog) and keeps conflicts visible. Expose each shortcut to assistive technology with `aria-keyshortcuts` (a hint only; it does not bind the key: [WAI-ARIA 1.2][aria-keyshortcuts]).

```tsx
type Shortcut = { id: string; keys: string; label: string; run: () => void };   // keys in ARIA form: "Control+S"

const registry = new Map<string, Shortcut>();   // useShortcut(shortcut) adds it in an effect, removes it on cleanup and returns { 'aria-keyshortcuts': shortcut.keys }

document.addEventListener('keydown', (event) => {   // installed once
  if (event.defaultPrevented) return;
  for (const shortcut of registry.values()) {
    if (matches(event, shortcut.keys)) { event.preventDefault(); shortcut.run(); return; }
  }
});
```

Show the shortcut in the button's tooltip text ("Save (Ctrl+S)"). Do not bind single printable keys without a modifier while a text field has focus ([WCAG 2.1.4 Character Key Shortcuts][wcag-214]); the sketch does not check that, so add a guard for editable targets. Test: a registered shortcut fires; the same keys typed into an input do not run a single-character shortcut; the element has the `aria-keyshortcuts` value. Derived.

## 7. Typed fields: parser, component, state

Follow the pipeline in [inputs.md](inputs.md), section 4:

1. A **pure parser module** per type (time, date, number, money): no React, no DOM, a function from text and locale to a result or an error. The error text comes from a message table, not from a literal in the parser.
2. A **controlled input component** that owns the raw text, calls the parser on Enter and on blur, writes the display format back and reports a typed value through `onCommit`.
3. The page state holds the **committed typed value** and a validation state; it never sees raw text.
4. Parser unit tests drive a table of inputs and expected results straight from the tables in [inputs.md](inputs.md), plus invalid and empty input.

Money uses integers in minor units or a decimal library, never `number` arithmetic on fractions; the display and parse paths take a locale (`Intl.NumberFormat`); an empty field is not zero. Dependent fields (end after start) recompute on the committed value, not on every keystroke.

```ts
// time-parser.ts: pure, no React
export type ParseResult<T> = { ok: true; value: T } | { ok: false; error: string };

/** "930", "0930", "9:30", "9.30", "9,30" -> "09:30"; "9", "09" -> "09:00"; "9:5" -> "09:05". */
export function parseTime(text: string): ParseResult<string> {
  const input = text.trim();
  if (input === '') return { ok: false, error: 'Enter a time between 00:00 and 23:59.' };
  const match = /^(\d{1,2})(?:[:.,](\d{1,2}))?$|^(\d{3,4})$/.exec(input);
  if (!match) return { ok: false, error: 'Enter a time between 00:00 and 23:59.' };

  let hours: number;
  let minutes: number;
  if (match[3]) {                                    // "930" or "0930"
    hours = Number(match[3].slice(0, -2));
    minutes = Number(match[3].slice(-2));
  } else {
    hours = Number(match[1]);
    minutes = match[2] === undefined ? 0 : Number(match[2]);
  }
  if (hours > 23 || minutes > 59) return { ok: false, error: 'Enter a time between 00:00 and 23:59.' };
  return { ok: true, value: `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}` };
}
```

(`9:5` becomes `09:05` here because the second group is read as minutes; if the project reads it as 50 minutes, change the rule and the table together.)

```tsx
// TimeField.tsx
import { useId, useState, type KeyboardEvent } from 'react';
import { parseTime } from './time-parser';

type TimeFieldProps = {
  label: string;
  value: string | null;                  // committed "HH:mm" or null
  onCommit: (value: string | null) => void;
  required?: boolean;
  help?: string;
  error?: string | null;                 // external error, for example "End must be after start"
};

const stepMinutes = 15;                  // the project's increment

function shift(committed: string | null, delta: number): string {
  const [h, m] = (committed ?? '00:00').split(':').map(Number);
  const total = Math.min(23 * 60 + 59, Math.max(0, h * 60 + m + delta));   // no wrap past midnight
  return `${String(Math.floor(total / 60)).padStart(2, '0')}:${String(total % 60).padStart(2, '0')}`;
}

export function TimeField({ label, value, onCommit, required, help, error: externalError }: TimeFieldProps) {
  const id = useId();
  const [text, setText] = useState(value ?? '');
  const [ownError, setOwnError] = useState<string | null>(null);
  const [lastValue, setLastValue] = useState(value);

  // Re-sync when the committed value changes from outside (a reset, a loaded record), not while typing.
  if (value !== lastValue) {
    setLastValue(value);
    setText(value ?? '');
    setOwnError(null);
  }

  const error = ownError ?? externalError ?? null;

  const commit = (): boolean => {
    if (text.trim() === '') {
      if (required) { setOwnError('Enter a time between 00:00 and 23:59.'); return false; }
      setOwnError(null);
      onCommit(null);
      return true;
    }
    const result = parseTime(text);
    if (!result.ok) { setOwnError(result.error); return false; }   // keep the text; do not clear
    setOwnError(null);
    setText(result.value);                                          // write the display format back
    onCommit(result.value);
    return true;
  };

  const onKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      if (!commit()) event.preventDefault();                        // an invalid time must not submit the form
    } else if (event.key === 'Escape' && text !== (value ?? '')) {
      setText(value ?? '');                                         // restore the last committed value
      setOwnError(null);
      event.stopPropagation();                                      // the next Esc closes the form
    } else if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'PageUp' || event.key === 'PageDown') {
      event.preventDefault();
      const base = parseTime(text);
      const size = event.key.startsWith('Page') ? 60 : event.shiftKey ? 1 : stepMinutes;
      const next = shift(base.ok ? base.value : value, event.key.endsWith('Up') ? size : -size);
      setText(next);
      setOwnError(null);
      onCommit(next);
    }
  };

  return (
    <Field label={label} required={required} help={help ?? 'Hours and minutes, for example 9:30'} error={error}>
      {(control) => (
        <input
          {...control}
          type="text"
          inputMode="numeric"
          autoComplete="off"
          spellCheck={false}
          maxLength={5}
          value={text}
          onChange={(event) => setText(event.target.value.replace(/[^\d:.,]/g, '').slice(0, 5))}   // typing is filtered, never reformatted
          onFocus={(event) => event.currentTarget.select()}      // fast fields replace, they do not edit
          onBlur={commit}
          onKeyDown={onKeyDown}
        />
      )}
    </Field>
  );
}
```

Decisions in the code, each with its reason:

- **State the component holds: text, committed value, error.** Text is what the user sees; the committed value is a prop owned by the page; the error is derived from the last commit. A failed commit keeps the text and shows the error; it never restores or clears silently.
- **`type="text"` with `inputMode`, not `type="number"` or `type="time"`.** A `type="number"` input accepts `e`, `+` and `-`, reports an empty `value` while the typed text is not a valid number, loses leading zeros as soon as a controlled input is fed from numeric state, and can change its value with the mouse wheel or arrow keys in some browsers; `type="time"` renders a browser-specific segmented control that cannot accept "930" ([MDN: input type=number][mdn-number]; see [fluent-ui-react-notes.md](fluent-ui-react-notes.md)). `inputmode="numeric"` asks for a digit keyboard on touch devices ([MDN: inputmode][mdn-inputmode]); it is a hint, not a filter, which is why `onChange` filters. A keypad without separators cannot type `9:30`; use `inputMode="text"` when the separators must be typeable on a phone (Derived). Use the `pattern` attribute only if the browser's native validation is wanted; it does not replace the parser.
- **Never reformat while typing.** Filtering characters is allowed (digits, colon, dot, comma, five characters at most); rewriting the text (inserting a colon) moves the caret and fights the user.
- **Select all on focus** for fast fields (time, date, number, money, search) and caret at the end for text fields ([inputs.md](inputs.md), section 5). Browsers differ: a mouse click places the caret after the focus handler selected all, so select on keyboard focus only if the click should place the caret. A `focus` event cannot tell the two apart; `:focus-visible` can (`event.currentTarget.matches(':focus-visible')`). Derived; test it per browser.
- **Enter** commits and lets the form submit if valid; with a parse error it prevents the submit. Whether the form's `onSubmit` sees the committed value in the same tick depends on when your state update lands: read the committed value from a ref or have `onCommit` write synchronously if the submit handler needs it (derived, not verified for your state library).
- **Esc** restores the last committed value and stops propagation; the second Esc, with nothing changed, reaches the dialog's handler. A native `<dialog>` handles Esc itself before React sees it, see [Dialogs, popovers and focus restoration](#dialogs-popovers-and-focus-restoration) for the consequence.
- **Arrow steps** use the configured increment; Shift one minute; Page Up and Down one hour; no wrap past midnight. The mouse wheel changes the value only while focused, if at all (not implemented above).
- **Dependent fields** (end after start) are validated by the page on the committed values and passed back as the `error` prop of the end field; the end field is recalculated after commit, not while typing.
- **Date and number** follow the same shape with their own parser module; format output with `Intl.DateTimeFormat` and `Intl.NumberFormat` using the user's locale ([content-design.md](content-design.md)).

Tests for this component are in [Testing Library](#testing-library): the parser table with `it.each`, and a user-event run for Tab, typing, arrows, Esc and Enter.

## 8. Keyboard, focus and navigation

- **One tab stop per group** with arrows inside: [Roving tabindex](#roving-tabindex). Tab follows DOM order, so write the DOM in reading order and do not rely on CSS `order`, `position` or `flex-direction: row-reverse` to arrange focusable items; the visual order and the focus order then disagree ([WCAG 2.4.3 Focus Order][wcag-243]; [WCAG 1.3.2 Meaningful Sequence][wcag-132]).
- **`tabindex` rules.** `0` puts a non-interactive element in the tab order; use it only for custom widgets that you give a role and keyboard handling. `-1` makes an element focusable by script and click but not by Tab; use it for roving items, for headings or regions you move focus to, and for dialog containers. **Never a positive value**: it reorders the whole page and nobody maintains that order. Prefer native elements (`button`, `a[href]`, `input`) which are focusable and keyboard-operable without any of this.
- **Restoring focus after a transient surface closes:** store the invoker before opening, focus it after closing ([Dialogs, popovers and focus restoration](#dialogs-popovers-and-focus-restoration)). When the focused element removes itself (a close button inside a panel that unmounts), focus falls back to `body`, and key handlers on the view never fire. Move focus deliberately to the invoker or the next sensible target before unmounting.
- **Esc and parent handlers.** If a parent handles Esc during the capture phase (to close a panel), its handler runs before the focused field, so the field never restores its value and the panel closes with the edit lost. Pattern: the field marks pending changes (`data-pending="true"` while the text differs from the committed value or a list is open) and the parent asks before it acts:

```ts
function onPanelKeyDown(event: KeyboardEvent) {
  if (event.key !== 'Escape') return;
  const active = document.activeElement as HTMLElement | null;
  if (active?.dataset.pending === 'true') return;   // the field restores its value first; the next Esc reaches this handler
  closePanel();
}
```

- **Enter and the default button.** In a `<form>`, Enter in a single-line input submits through the first submit button (implicit submission, [HTML spec][html-implicit-submission]). A multi-line `textarea` handles Enter itself (newline), so it does not submit. Add Ctrl+Enter per textarea if the design wants "send": `onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) send(); }}`. Several visible forms with their own submit buttons are separate `<form>` elements, so Enter in one never runs the action of another; do not hang Enter on a document handler.
- **Destructive dialogs:** put initial focus on the safe button (Cancel), mark the destructive one as not default, and let Esc cancel ([dialogs-and-messages.md](dialogs-and-messages.md)).
- **Skip link:** the first focusable element of the page is a link to `#main-content` that is visible on focus ([WCAG 2.4.1][wcag-241]):

```css
.skip-link { position: absolute; inset-inline-start: 8px; inset-block-start: -48px; padding: 8px 12px; background: var(--colorNeutralBackground1); color: var(--colorNeutralForeground1); }
.skip-link:focus-visible { inset-block-start: 8px; }
```

```html
<a class="skip-link" href="#main-content">Skip to main content</a>
<main id="main-content" tabindex="-1">...</main>
```

### Focus ring

Fluent default (`createFocusOutlineStyle` in `react-tabster/src/focus/createFocusOutlineStyle.ts`): a 2 px ring in `colorStrokeFocus2` (black in the light theme, white in the dark theme) with `borderRadiusMedium` radius, drawn as an `::after` pseudo-element (the element needs `position: relative`), keyed on a `data-fui-focus-visible` attribute that Tabster's `keyborg` sets for keyboard focus, and `Highlight` in forced colors. Native `:focus-visible` is the web-platform counterpart for your own components:

```css
:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline: 2px solid var(--colorStrokeFocus2);
  outline-offset: 2px;
  box-shadow: 0 0 0 2px var(--colorStrokeFocus1);   /* light halo in the gap: the ring reads on dark and light backgrounds */
}
```

The dark ring with a light halo keeps the indicator visible on every background (Derived; [WCAG 1.4.11 Non-text Contrast][wcag-1411], [2.4.7 Focus Visible][wcag-247], [2.4.11 Focus Not Obscured][wcag-2411]). Check that a sticky header does not cover the focused element (`scroll-padding-top` on `html` equal to the header height). Text inputs match `:focus-visible` after a mouse click too, but buttons and links usually do not ([MDN][mdn-focus-visible]); if a design needs a ring on every click, use `:focus` for that component and say so. Inside a `FluentProvider`, Fluent components draw their own ring; do not add a second one on top, and do not remove it with a global `*:focus { outline: none }`.

### Tab order walk

A pull request that changes layout needs the numbered focus list ([accessibility.md](accessibility.md)). Let a test print it. With Testing Library, `userEvent.tab()` follows the tab order that jsdom implements (it ignores layout, so it will not catch a visual order that differs from the DOM):

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

async function tabOrder(max = 60): Promise<string[]> {
  const user = userEvent.setup();
  const names: string[] = [];
  const seen = new Set<Element>();
  for (let i = 0; i < max; i += 1) {
    await user.tab();
    const active = document.activeElement;
    if (!active || active === document.body || seen.has(active)) break;   // left the document or wrapped
    seen.add(active);
    names.push(active.getAttribute('aria-label') ?? active.textContent?.trim() ?? active.tagName);
  }
  return names;
}

it('has the documented focus order', async () => {
  render(<BookingEditor />);
  expect(await tabOrder()).toEqual(['Start time', 'End time', 'Notes', 'Cancel', 'Save']);
});
```

In Playwright the same walk uses the real browser and layout: `await page.keyboard.press('Tab')`, then `page.evaluate(() => document.activeElement?.getAttribute('aria-label') ?? document.activeElement?.textContent)`; add a position check (`getBoundingClientRect().top` must not decrease by more than a row) to catch a visual order that disagrees with the DOM order. The name used is what a screen reader would hear, so a missing name shows up at once. A roving group appears once. Run the walk per screen and per layout state (side panel open and closed).

### Dialogs, popovers and focus restoration

The native `<dialog>` element opened with `showModal()` traps focus inside, makes the rest of the page inert, closes on Esc and returns focus to the previously focused element when it closes ([HTML spec: dialog][html-dialog]; [MDN: dialog][mdn-dialog]). Prefer it for your own dialogs. Fluent UI React v9's `Dialog` is different: it renders a `div` with `role="dialog"` (or `alertdialog` for `modalType="alert"`), `aria-modal` and `tabIndex={-1}`, handles Escape itself in `onKeyDown`, and relies on Tabster for the trap (`react-dialog/.../useDialogSurface.ts`, Fluent default).

```tsx
import { useEffect, useRef, type ReactNode } from 'react';

type ConfirmDialogProps = { open: boolean; title: string; onClose: () => void; children: ReactNode };

export function ConfirmDialog({ open, title, onClose, children }: ConfirmDialogProps) {
  const ref = useRef<HTMLDialogElement>(null);
  const invoker = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) {
      invoker.current = document.activeElement as HTMLElement | null;   // store before opening
      dialog.showModal();
    } else if (!open && dialog.open) {
      dialog.close();
    }
  }, [open]);

  return (
    <dialog
      ref={ref}
      aria-labelledby="confirm-title"
      onClose={() => { onClose(); invoker.current?.focus(); }}         // explicit restore; also covers the case the invoker was re-rendered
      onCancel={(event) => { /* Esc: let the dialog close; call event.preventDefault() to veto it */ }}
    >
      <h2 id="confirm-title">{title}</h2>
      {children}
      <form method="dialog">
        <button value="cancel" autoFocus>Cancel</button>               {/* destructive question: focus and Enter on Cancel */}
        <button value="delete">Delete</button>
      </form>
    </dialog>
  );
}
```

Points:

- **Esc is handled by the dialog before React sees a `keydown` on the page.** The browser fires `cancel` and then `close`. A `keydown` handler on `document` that closes something else will still run, but it cannot stop the dialog from closing except by `preventDefault()` on `cancel`. Consequence for the Esc ladder: a field inside a native dialog that wants to restore its value on Esc must call `event.preventDefault()` on `keydown` (this stops the cancel in Chromium, and the second Esc closes); test it in each target browser (derived, not verified for every engine). See [fluent-ui-react-notes.md](fluent-ui-react-notes.md).
- **Focus restoration.** `showModal()` and `close()` restore focus to the previously focused element per the spec; the explicit `invoker.focus()` is a safety net for invokers that were re-rendered or removed. For a menu, drawer or popover built from non-native parts, store the invoker before opening and focus it after closing, as the code does. In Fluent UI React v9, `DialogTrigger` marks the opener and restores focus; an opener outside the dialog needs `useRestoreFocusTarget()` (`Migration/FromV8/Components/Dialog.mdx`).
- **Popover API.** `popover="auto"` gives light dismiss, Esc and focus return to the invoker without script ([MDN: Popover API][mdn-popover]); it uses the top layer like `<dialog>`, so stacking order between a popover and a modal dialog follows top-layer order, not `z-index`.
- **Modal means inert.** Everything outside a modal dialog is inert, so tests that look for content behind it, or that click on it, fail on purpose. For non-native modals set `inert` on the app root while the dialog is open ([MDN: inert][mdn-inert]).
- **Initial focus:** the first focusable element, or the one with `autofocus`; never the destructive action. A dialog with long text starts at the heading (`tabindex="-1"` on the heading) so a screen reader reads from the top. Derived.
- **Test:** open from a button, press Tab through, close with Esc and with each button, assert `document.activeElement` is the invoker. Playwright, because jsdom does not implement `showModal()` completely (derived, not verified for your jsdom version).

## 9. Accessibility API

The accessibility tree is built from the DOM: roles from elements and `role`, names from content, labels and `aria-*`. Where a native element exists, use it; ARIA only fills gaps ([First rule of ARIA][aria-first-rule]). The rules for what to name and announce are in [accessibility.md](accessibility.md).

### Names, descriptions and live regions

| Need | Mechanism |
| --- | --- |
| Accessible name from visible text | The element's content (buttons, links), `label[for]` (inputs), `aria-labelledby` pointing at the visible label |
| Accessible name without visible text | `aria-label` (icon-only buttons). Name the target ("Help on delivery date"), not only "Help"; use the same text as the tooltip |
| Hint, format, range text | `aria-describedby` pointing at the help element |
| Required | `required` or `aria-required="true"` |
| Invalid | `aria-invalid="true"` plus the error element in `aria-describedby` |
| Shortcut | `aria-keyshortcuts` (and the tooltip text) |
| Expanded or collapsed state of a header | `aria-expanded` on the button and `aria-controls` pointing at the panel |
| Current page or step | `aria-current="page"` or `"step"` |
| Live region for messages | `role="status"` (polite) or `role="alert"` (assertive), or `aria-live="polite"` / `"assertive"` |
| Hide decorative elements | `aria-hidden="true"` on icons next to text; empty `alt=""` on decorative images |

Rules that cause trouble:

- **`aria-label` replaces visible text in the name.** If a button shows "Save" and has `aria-label="Store the booking"`, voice-control users who say "click Save" fail ([WCAG 2.5.3 Label in Name][wcag-253]). Start the label with the visible text. Derived.
- **`aria-labelledby` can reference hidden elements**, and it beats `aria-label` and content. Use it to compose a name from two visible pieces ("Delete" plus the row title).
- **Placeholders are not labels.** Browsers expose a placeholder as a fallback name for some inputs, but it disappears on input and often fails contrast.
- **Live regions announce changes, not initial content.** The container (`role="status"`) must already be in the DOM when its text changes; inserting a new `role="alert"` element announces it, inserting a new `aria-live` container with text does not reliably. Keep one persistent status container for toasts and save confirmations, and write into it. Errors that need attention use `role="alert"` (assertive); everything else polite ([MDN: ARIA live regions][mdn-live]). Fluent's `MessageBar` announces its text through the provider's announcer: `politeness` or `intent` decides polite or assertive (`useMessageBar.ts`); read the note on that expression in [fluent-ui-react-notes.md](fluent-ui-react-notes.md). Loading text is concrete ("Writing draft..."), not "Loading".
- **Expanded state:** a native `<details>` and `<summary>` reports it for you; for a custom accordion set `aria-expanded` from the same state that shows the panel and `aria-controls` to the panel id. Fluent's `Accordion` does this for you.
- **Icon-only buttons** in Fluent UI React v9 still need `aria-label` on the `Button`; the icon prop does not provide a name (derived, not verified for every icon component).
- **Headings and landmarks:** one `h1`, no skipped levels, `main`, `nav` with a name when there are several, so F6 regions and screen reader landmark lists make sense.

### Name scan with axe

Browsers and screen readers compute names from the DOM in ways that look right in a screenshot and are wrong in the tree (an empty button, a generic `div` with a click handler, a list row without a name). Scan every page with axe-core in a real browser:

```ts
import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const routes = ['/', '/bookings', '/bookings/new', '/settings', '/inbox'];

test.use({ storageState: 'tests/.auth/owner.json' });        // log in once as the role with the most pages

for (const route of routes) {
  test(`axe: ${route}`, async ({ page }) => {
    await page.goto(route);
    await page.waitForLoadState('networkidle');
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(', ')}`)).toEqual([]);
  });
}

test('names exist on controls', async ({ page }) => {
  await page.goto('/bookings/new');
  const results = await new AxeBuilder({ page })
    .withRules(['button-name', 'link-name', 'label', 'image-alt', 'select-name', 'input-button-name', 'aria-input-field-name', 'aria-dialog-name', 'aria-command-name', 'aria-toggle-field-name', 'aria-valid-attr', 'aria-valid-attr-value', 'aria-required-attr', 'aria-roles'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

Notes:

- Run it as the role that reaches the most pages (the owner or admin), and again for a restricted role if the UI differs; a page the test role cannot see is a page nobody checked. Include every state that changes the DOM: open dialog, error state, empty state, side panel open.
- The rule ids are axe-core rule names (`button-name`, `link-name`, `label`, `image-alt` and the `aria-*` rules are listed in the [axe rules][axe-rules]); confirm each against the axe-core version you lock, and read `results.incomplete` too, which lists what axe could not decide.
- axe finds roughly the mechanical share of the problems (names, roles, valid ARIA, contrast of text on solid backgrounds); it does not judge whether a name makes sense, whether focus order is logical or whether the screen reader announces the right thing. Say that in the report. Add a name quality check by hand for list rows and icon buttons.
- axe reports contrast for text on solid backgrounds; it cannot measure borders and focus rings against the page. Compute those from the resolved tokens ([Playwright](#playwright)).
- A custom control needs the role, the name, the state and the keyboard behavior of the pattern it imitates ([ARIA APG patterns][apg-patterns]); for a spin-style field with `role="spinbutton"` that includes `aria-valuenow`, `aria-valuemin` and `aria-valuemax`. A text field with an `inputMode` and a parser is still a plain `input` and needs none of that.

## 10. Tests

Two tools, each for what it can see. Say in the report which one covered which rule.

| Rule | Testing Library (jsdom) | Playwright (real browser) |
| --- | --- | --- |
| Parser results | Yes (pure unit tests) | No need |
| Keyboard paths in a component (Tab, typing, arrows, Esc, Enter) | Yes, with `user-event` | Yes, for focus-visible behavior and real browser defaults |
| Accessible roles and names | Yes (`getByRole`, `getByLabelText`) | Yes, plus axe |
| States set by code (`aria-invalid`, `disabled`) | Yes | Yes |
| CSS values, transitions, pseudo-classes | No (no real cascade for your stylesheet and no transitions) | Yes (`getComputedStyle`, screenshots) |
| Layout, sizes, overflow, tap targets | No (no layout) | Yes |
| Light and dark, forced colors, reduced motion | No (media queries are not evaluated unless mocked) | Yes (`emulateMedia`) |
| Dialog, popover, top layer | Partly (depends on jsdom support) | Yes |
| Real screen reader output | No | No |

### Testing Library

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { parseTime } from './time-parser';
import { TimeField } from './TimeField';

describe('parseTime', () => {
  it.each([
    ['9', '09:00'], ['09', '09:00'], ['930', '09:30'], ['0930', '09:30'],
    ['9:30', '09:30'], ['9.30', '09:30'], ['9,30', '09:30'], ['9:5', '09:05'],
  ])('reads %s as %s', (text, expected) => {
    expect(parseTime(text)).toEqual({ ok: true, value: expected });
  });

  it.each(['24', '9:60', 'abc', '', '12345'])('rejects %s with the valid range in the message', (text) => {
    const result = parseTime(text);
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.error).toMatch(/00:00 and 23:59/);
  });
});

describe('TimeField', () => {
  it('commits on Enter, keeps invalid text, restores on Escape', async () => {
    const user = userEvent.setup();
    const onCommit = vi.fn();
    render(<TimeField label="Start time" value="08:00" onCommit={onCommit} />);
    const input = screen.getByRole('textbox', { name: /start time/i });

    await user.click(input);
    await user.clear(input);
    await user.type(input, '930{Enter}');
    expect(onCommit).toHaveBeenLastCalledWith('09:30');
    expect(input).toHaveValue('09:30');

    await user.clear(input);
    await user.type(input, '9:60{Enter}');
    expect(input).toHaveValue('9:60');                       // not cleared
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveAccessibleDescription(/00:00 and 23:59/);

    await user.keyboard('{Escape}');
    expect(input).toHaveValue('08:00');                      // restores the committed value
    expect(input).not.toHaveAttribute('aria-invalid');
  });

  it('selects the text when Tab moves in', async () => {
    const user = userEvent.setup();
    render(<><button>Before</button><TimeField label="Start time" value="09:30" onCommit={() => {}} /></>);
    await user.tab();                                         // the button
    await user.tab();                                         // the field
    const input = screen.getByRole('textbox', { name: /start time/i }) as HTMLInputElement;
    expect(input.selectionStart).toBe(0);
    expect(input.selectionEnd).toBe(input.value.length);
  });

  it('steps with the arrows and does not pass midnight', async () => {
    const user = userEvent.setup();
    const onCommit = vi.fn();
    render(<TimeField label="Start time" value="23:50" onCommit={onCommit} />);
    await user.click(screen.getByRole('textbox', { name: /start time/i }));
    await user.keyboard('{ArrowUp}');
    expect(onCommit).toHaveBeenLastCalledWith('23:59');
  });
});
```

Notes:

- Query by role and name (`getByRole('textbox', { name })`) so the test fails when the accessible name is wrong; `getByTestId` hides that.
- `toHaveAccessibleDescription` and `toHaveValue` come from `@testing-library/jest-dom`; the `aria-describedby` wiring is tested through them.
- `user-event` v14 needs `userEvent.setup()` before the render; use `await` for every call.
- Test composite components (a field with a counter, derived text, enabled states) with the props arriving in more than one order and through a re-render with a new `value`; React applies props as a set, but effects and derived state that read two props at once can still miss a sequence (derived).
- For Fluent components the structure of the DOM belongs to Fluent: query by role and name, not by `.fui-Input__input` class names, which are an implementation detail (derived).
- Mock `matchMedia` in the test setup (jsdom does not define it), and expect that `prefers-reduced-motion` and `prefers-color-scheme` are not evaluated: test the hook that reads them with a mocked `matchMedia`, test the CSS in Playwright.

### Playwright

```ts
import { expect, test } from '@playwright/test';

test('field states in light and dark', async ({ page }) => {
  await page.goto('/components/time-field');
  const field = page.getByLabel('Start time');

  for (const scheme of ['light', 'dark'] as const) {
    await page.emulateMedia({ colorScheme: scheme });
    await expect(page.locator('.field')).toHaveScreenshot(`field-rest-${scheme}.png`);
    await field.focus();
    await expect(page.locator('.field')).toHaveScreenshot(`field-focus-${scheme}.png`, { animations: 'disabled' });
  }
});

test('focus shows after a mouse click on the input', async ({ page }) => {
  await page.goto('/components/time-field');
  await page.getByLabel('Start time').click();
  const transform = await page.locator('.field__box').evaluate((el) => getComputedStyle(el, '::after').transform);
  expect(transform).not.toBe('none');                   // the underline is scaled in (matrix(1, 0, 0, 1, 0, 0) at full width)
});

test('forced colors keep the focus indicator', async ({ page }) => {
  await page.emulateMedia({ forcedColors: 'active' });
  await page.goto('/components/time-field');
  await page.getByLabel('Start time').focus();
  await expect(page.locator('.field')).toHaveScreenshot('field-focus-forced-colors.png');
});

test('border contrast against the surface', async ({ page }) => {
  await page.goto('/components/time-field');
  for (const scheme of ['light', 'dark'] as const) {
    await page.emulateMedia({ colorScheme: scheme });
    const [border, surface] = await page.evaluate(() => {
      const style = getComputedStyle(document.querySelector('.field__box')!);
      return [style.borderBottomColor, style.backgroundColor];
    });
    expect(contrast(border, surface), scheme).toBeGreaterThanOrEqual(3);
  }
});

function contrast(a: string, b: string): number {
  const luminance = (css: string) => {
    const [r, g, bl] = (css.match(/[\d.]+/g) ?? []).slice(0, 3).map(Number).map((v) => {
      const s = v / 255;
      return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * bl;
  };
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

test('layout at small viewport and 320 CSS px reflow', async ({ page }) => {
  for (const [width, height] of [[1280, 800], [768, 1024], [375, 812], [320, 640]]) {
    await page.setViewportSize({ width, height });
    await page.goto('/bookings/new');
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    expect(overflow, `${width}px`).toBe(false);          // no horizontal scroll ([WCAG 1.4.10 Reflow][wcag-1410])
  }
});
```

Notes:

- `emulateMedia` takes `colorScheme`, `reducedMotion`, `forcedColors` and `media`; the emulation applies to the page until it is changed again ([Playwright: emulateMedia][pw-emulate]). Set it before the screenshot, and let a short transition finish (`animations: 'disabled'` in `toHaveScreenshot` fast-forwards CSS animations and transitions).
- Take one screenshot per state (rest, hover, focus, error, disabled) and theme. Keep image tests in their own, smaller runs if the suite is large, and store the baselines per OS (fonts differ); run the baselines in the CI container, not on a laptop.
- Measure sizes, not impressions: `await locator.boundingBox()` for small icon buttons against the design size (a `min-height: 34px` rule on `button` turns a 28 px icon button into 28 x 34); WCAG 2.2 target size minimum is 24 x 24 CSS px ([2.5.8][wcag-258]).
- Use `page.keyboard.press('Tab')` and real focus checks for the keyboard path, `locator.focus()` only for setup.
- Contrast of borders, focus rings and placeholders is computed from resolved styles as above; axe covers only text on solid backgrounds.
- Test the pages as the role with most rights ([Name scan with axe](#name-scan-with-axe)).

### Reading transitions

`getComputedStyle(element).transitionDuration` and `.transitionProperty` return comma-separated lists, aligned by index; `transitionDelay` and `transitionTimingFunction` likewise. For pseudo-elements pass the pseudo as the second argument. To see what is running right now, ask for the animation objects: `element.getAnimations()` returns `CSSTransition` and `CSSAnimation` objects with `transitionProperty` and `effect.getTiming().duration` ([MDN: Element.getAnimations][mdn-getanimations]). A test that focuses the field and then checks `document.getAnimations().length` is 0 under reduced motion proves that nothing runs, which is stronger than reading the declared durations:

```ts
const running = await page.evaluate(() => document.getAnimations().map((a) => (a as CSSTransition).transitionProperty ?? a.constructor.name));
expect(running).toEqual([]);
```

With the setting off, the same walk should find the token durations (50, 100, 200 ms) and not zero. This works in a real browser only; jsdom has neither transitions nor `getAnimations`.

### What the tools do not show

- **jsdom has no layout.** `offsetWidth`, `getBoundingClientRect()` and `ResizeObserver` do not measure anything, so overflow, tap target sizes and responsive behavior need Playwright. It also does not apply your stylesheet's cascade the way a browser does, does not run CSS transitions, does not evaluate `prefers-reduced-motion` or `prefers-color-scheme` (there is no `matchMedia` unless you mock it), and its support for `<dialog>` `showModal()`, the Popover API and `inert` depends on the jsdom version (derived, not verified).
- **Playwright is not a screen reader.** It confirms the accessibility tree (roles, names, `aria-*`) and the keyboard path; it cannot tell what NVDA, JAWS, Narrator or VoiceOver speak, nor whether live-region announcements arrive. Do a manual pass with at least one screen reader and record it; do not tick the box from code inspection alone.
- **Screenshots depend on the OS font rendering**; baselines from another machine are noise.
- Not verified by either tool: behavior at browser zoom 200 percent and 400 percent (test reflow at 320 CSS px as a proxy), real touch devices, Windows high contrast themes beyond `forced-colors` emulation, and Safari or Firefox unless the project runs them (set up `projects` for the browsers you support).

## 11. Checklist

- [ ] No hex colors, color functions, named colors or inline `box-shadow` values outside the token file; no literal colors in TSX or inline styles (the scans in [section 2](#scans-for-literal-colors-and-shadows) are clean).
- [ ] All tokens exist for light and dark (and forced colors where a state would vanish); a Playwright run in both schemes shows no unthemed surface (screenshots).
- [ ] State styling uses the selectors of [section 3](#3-states-as-pseudo-classes-and-attributes), with no `style=` attributes that set state-dependent colors (search `style={{` in TSX).
- [ ] Every hover, pressed and disabled rule differs from the rest rule (screenshot per state).
- [ ] A property that does not change was traced to the winning rule (layer, specificity, inline style) and changed there ([Precedence](#precedence)).
- [ ] The field has label, optional help, error text tied by `aria-describedby`, `aria-invalid` on error, a required marker that is not color alone ([section 4](#4-field-anatomy); Testing Library asserts them).
- [ ] The focus indicator shows on keyboard focus and after a mouse click in text inputs, meets 3:1 against the field and the page, and survives forced colors (Playwright screenshot and computed style).
- [ ] Transitions list their properties, use token durations and curves, and animate only color, opacity and transform (search for `transition: all` and layout properties in transitions).
- [ ] Reduced motion: the OS media query and the in-app class both leave no visible duration above zero on any route (Playwright walk in [section 5](#5-transitions-and-reduced-motion)).
- [ ] Parsers are pure modules with a table test; no floating-point arithmetic in the money path (`it.each` table, grep for `parseFloat` in money code).
- [ ] Typed fields: filtered typing, commit on Enter and blur, invalid text kept with an error, Esc restores, no reformatting while typing, `inputMode` set (Testing Library run of [section 7](#7-typed-fields-parser-component-state)).
- [ ] Groups are one tab stop and the stop is the selected item; arrows follow the wrap decision (Testing Library `userEvent.tab()` and arrow keys).
- [ ] The Tab walk of each screen matches the numbered focus list and the visual order; no positive `tabindex` anywhere (`rg 'tabIndex=\{?[1-9]'`; the walk in [Tab order walk](#tab-order-walk)).
- [ ] F6 and Shift+F6 cycle named regions in screen order; a page without regions is one region (Playwright with real keys).
- [ ] An overflow toolbar hides items completely and Tab visits only visible items (Playwright at minimum and wide viewport).
- [ ] Tooltips: delay from one default, shown on focus, dismissed by Esc without closing the dialog around, hover-persistent (Testing Library with fake timers, Playwright for the hover case).
- [ ] Shortcuts come from one registry, have `aria-keyshortcuts`, and single-key shortcuts are inactive in editable fields (unit test).
- [ ] Dialog: initial focus is never on a destructive action, Esc closes, focus returns to the invoker, the rest of the page is inert (Playwright; for non-native modals check `inert`).
- [ ] Every control has an accessible name; the axe run over every route as the owner role reports no violations; list rows and icon buttons have names that identify their target (axe plus a manual read of the name list).
- [ ] Messages use live regions with the right politeness (status for confirmations, alert for errors); the container exists before the text changes (Testing Library `getByRole('status')`/`('alert')`).
- [ ] Target size measured: small icon buttons are at least 24 x 24 CSS px, or the design size, with `boundingBox()` in a Playwright check.
- [ ] Fluent UI React: a `FluentProvider` wraps the app and every portal root; `Toaster` is mounted; no second focus ring or global `outline: none` (screenshot and grep).
- [ ] A screen reader pass was done and recorded, or the report says that it was not.
- [ ] Every property, hook and token used here was checked against the versions in the lockfile.

## 12. Sources

Fluent UI React source and docs are the authority for component behavior and token names; the web platform documents are the authority for CSS, HTML and ARIA behavior. The Fluent and WCAG rules these patterns implement are cited in the other reference files.

- Fluent UI React v9 source: [microsoft/fluentui][fluentui-src]; paths read for this file: `packages/tokens/src/tokens.ts`, `packages/tokens/src/global/durations.ts`, `packages/tokens/src/global/curves.ts`, `packages/tokens/src/alias/lightColor.ts`, `packages/tokens/src/alias/darkColor.ts`, `packages/react-components/react-input/library/src/components/Input/useInputStyles.styles.ts`, `packages/react-components/react-field/library/src/components/Field/useFieldStyles.styles.ts`, `packages/react-components/react-button/library/src/components/Button/useButtonStyles.styles.ts`, `packages/react-components/react-tooltip/library/src/components/Tooltip/useTooltipBase.tsx`, `packages/react-components/react-dialog/library/src/components/DialogSurface/useDialogSurface.ts`, `packages/react-components/react-message-bar/library/src/components/MessageBar/useMessageBar.ts`, `packages/react-components/react-tabster/src/focus/createFocusOutlineStyle.ts`.
- Fluent UI React storybook and docs: [react.fluentui.dev][fluent-react-docs]; styling guide: [Styling components][fluent-styling].
- Fluent 2 design system: [fluent2.microsoft.design][fluent2].
- Griffel: [griffel.js.org][griffel].
- CSS and HTML: [MDN CSS cascade][mdn-cascade], [CSS Cascade Level 5][css-cascade], [`:focus-visible`][mdn-focus-visible], [`:user-invalid`][mdn-user-invalid], [`light-dark()`][mdn-light-dark], [`color-scheme`][mdn-color-scheme], [`<dialog>`][mdn-dialog], [HTML spec: the dialog element][html-dialog], [Popover API][mdn-popover], [`inert`][mdn-inert], [`inputmode`][mdn-inputmode], [`input type=number`][mdn-number], [implicit submission][html-implicit-submission], [`getAnimations`][mdn-getanimations], [ARIA live regions][mdn-live].
- WAI-ARIA Authoring Practices: [keyboard interface][apg-keyboard], [tabs pattern][apg-tabs], [patterns][apg-patterns]; [first rule of ARIA][aria-first-rule]; [`aria-required`][aria-required]; [`aria-keyshortcuts`][aria-keyshortcuts].
- WCAG 2.2: [1.3.2][wcag-132], [1.4.10][wcag-1410], [1.4.11][wcag-1411], [1.4.13][wcag-1413], [2.1.4][wcag-214], [2.3.3][wcag-233], [C39][wcag-c39], [2.4.1][wcag-241], [2.4.3][wcag-243], [2.4.7][wcag-247], [2.4.11][wcag-2411], [2.5.3][wcag-253], [2.5.8][wcag-258].
- Tests: [Testing Library][tl], [user-event][user-event], [Playwright emulateMedia][pw-emulate], [axe rules][axe-rules].

[fluentui-src]: https://github.com/microsoft/fluentui
[fluent-react-docs]: https://react.fluentui.dev/
[fluent-styling]: https://react.fluentui.dev/?path=/docs/concepts-developer-styling-components--docs
[fluent2]: https://fluent2.microsoft.design/
[griffel]: https://griffel.js.org/
[mdn-cascade]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Cascade
[css-cascade]: https://www.w3.org/TR/css-cascade-5/
[mdn-focus-visible]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
[mdn-user-invalid]: https://developer.mozilla.org/en-US/docs/Web/CSS/:user-invalid
[mdn-light-dark]: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark
[mdn-color-scheme]: https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme
[mdn-dialog]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog
[html-dialog]: https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element
[mdn-popover]: https://developer.mozilla.org/en-US/docs/Web/API/Popover_API
[mdn-inert]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inert
[mdn-inputmode]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inputmode
[mdn-number]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number
[html-implicit-submission]: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission
[mdn-getanimations]: https://developer.mozilla.org/en-US/docs/Web/API/Element/getAnimations
[mdn-live]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions
[webdev-animations]: https://web.dev/articles/animations-guide
[apg-keyboard]: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
[apg-tabs]: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
[apg-patterns]: https://www.w3.org/WAI/ARIA/apg/patterns/
[aria-first-rule]: https://www.w3.org/TR/using-aria/#rule1
[aria-required]: https://www.w3.org/TR/wai-aria-1.2/#aria-required
[aria-keyshortcuts]: https://www.w3.org/TR/wai-aria-1.2/#aria-keyshortcuts
[wcag-132]: https://www.w3.org/TR/WCAG22/#meaningful-sequence
[wcag-1410]: https://www.w3.org/TR/WCAG22/#reflow
[wcag-1411]: https://www.w3.org/TR/WCAG22/#non-text-contrast
[wcag-1413]: https://www.w3.org/TR/WCAG22/#content-on-hover-or-focus
[wcag-214]: https://www.w3.org/TR/WCAG22/#character-key-shortcuts
[wcag-233]: https://www.w3.org/TR/WCAG22/#animation-from-interactions
[wcag-c39]: https://www.w3.org/WAI/WCAG22/Techniques/css/C39
[wcag-241]: https://www.w3.org/TR/WCAG22/#bypass-blocks
[wcag-243]: https://www.w3.org/TR/WCAG22/#focus-order
[wcag-247]: https://www.w3.org/TR/WCAG22/#focus-visible
[wcag-2411]: https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum
[wcag-253]: https://www.w3.org/TR/WCAG22/#label-in-name
[wcag-258]: https://www.w3.org/TR/WCAG22/#target-size-minimum
[tl]: https://testing-library.com/docs/react-testing-library/intro/
[user-event]: https://testing-library.com/docs/user-event/intro
[pw-emulate]: https://playwright.dev/docs/api/class-page#page-emulate-media
[axe-rules]: https://dequeuniversity.com/rules/axe/
