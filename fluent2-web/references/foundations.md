# Foundations: layout, type, color, elevation, motion, shape, tokens

Read this file when you set up or review a theme, a token CSS file, spacing, typography, colors, shadows, transitions or corner radii for a web app. Component behavior lives in the other reference files; this file holds the values they build on. How Fluent concepts map to HTML, CSS, React and tests is in [web-mapping.md](web-mapping.md); Fluent UI React v8 to v9 names are in [fluent-ui-react-notes.md](fluent-ui-react-notes.md).

## Contents

1. [How to read the values](#1-how-to-read-the-values)
2. [Design principles](#2-design-principles)
3. [Layout and spacing](#3-layout-and-spacing)
4. [Typography](#4-typography)
5. [Color and contrast](#5-color-and-contrast)
6. [Icons](#6-icons)
7. [Elevation and material](#7-elevation-and-material)
8. [Motion](#8-motion)
9. [Shape: radius and stroke](#9-shape-radius-and-stroke)
10. [Tokens and themes](#10-tokens-and-themes)
11. [Recording deviations](#11-recording-deviations)
12. [Checklist](#12-checklist)
13. [Sources](#13-sources)

## 1. How to read the values

Every number in this skill carries one of three origins. Keep them apart, because they bind differently.

| Tag | Meaning | Binding |
| --- | --- | --- |
| **Fluent default** | Value taken from Fluent 2 guidance or from the Fluent UI React source (`@fluentui/tokens`, component styles) | Starting point only |
| **Derived** | Recommendation built on Fluent principles and a web standard (WCAG, WAI-ARIA APG, MDN), but not stated by Microsoft | Judgment call, adjust freely |
| **(derived, not verified)** | Derived and not confirmed against a source or a running page | Check before relying on it |

Rule zero: if the project has a design brief, a token file or an established style, its values win over every Fluent default here. Fluent is the fallback and the source of behavior; it does not replace the brief. Where the project differs from Fluent on purpose, write the deviation down once with the reason (section 11) so later changes do not undo it by accident.

Two audiences use this skill, and the text says which one a statement is for when they differ:

- **Path A, Fluent UI React v9.** The project imports `@fluentui/react-components` and wraps the app in `FluentProvider`. Tokens are the `tokens` object from `@fluentui/react-components` (for example `tokens.colorNeutralBackground1`); each entry is a `var(--colorNeutralBackground1)` reference, so the same values are available in plain CSS. Components already implement most behavior; your job is to use them, theme them and not fight them.
- **Path B, own React/HTML/CSS components.** The project builds its own components and borrows Fluent's values and behavior. Use the Fluent token names as a vocabulary, or map them to your own custom properties (section 10) and keep a mapping table next to the token file.

The Fluent web values below are verified against `@fluentui/tokens` on the `master` branch of microsoft/fluentui (links in section 13). Windows-native values (WinUI) differ in places; this skill uses them only where Fluent's web guidance is silent and says so.

## 2. Design principles

- Natural on each platform: use the habits of the browser and the operating system (native form controls, Tab order, focus drawing, text input behavior, scroll) and build bespoke patterns only where the product needs them. Because users carry platform expectations into every app. ([Principles][f2-principles])
- Built for focus: show as few simultaneous elements as the task allows. Because visual noise costs concentration; a form with fewer visible fields is faster to scan. ([Principles][f2-principles])
- One for all: design for different abilities from the first sketch, not as a late fix. Keyboard use is a first-class path equal to the mouse. ([Principles][f2-principles])
- Brand identity versus behavior: Fluent's signature look (color, sound, illustration) belongs to Microsoft products. Adopt the behavior and keep your own brand look. Because a product that copies the look without being a Microsoft product confuses ownership. ([Principles][f2-principles])
- Prefer the native element and style it over rebuilding it (`<button>`, `<input>`, `<dialog>`, `<details>`, `popover`). Because a native element already carries keyboard, accessibility-tree and form behavior you would otherwise re-create with ARIA. Derived. ([MDN: ARIA first rule][mdn-aria-first])

## 3. Layout and spacing

- Build on a 4 px grid. Fluent default spacing tokens: `spacingHorizontal*` and `spacingVertical*` with the same values, `None` 0, `XXS` 2, `XS` 4, `SNudge` 6, `S` 8, `MNudge` 10, `M` 12, `L` 16, `XL` 20, `XXL` 24, `XXXL` 32 (verified in `spacings.ts`). The Fluent layout guidance lists steps up to 56 (36, 40, 48, 52, 56 have no token; write them as multiples of 4). The values 2, 6 and 10 are nudges that compensate for icon padding. Because a single grid keeps rhythm predictable; the nudges exist so icons and text still align. ([Layout][f2-layout], [Spacing source][gh-spacing])
- Path A: use `tokens.spacingHorizontalM` and `tokens.spacingVerticalM` in `makeStyles`, never a number. Path B: define `--space-xs: 4px` and so on once and use `gap` and `padding` with those properties. `gap` replaces margin hacks between siblings. Derived.
- If the project brief allows only the multiples of 4, still permit 2, 6 and 10 for padding around icons and inside fields when the brief itself uses them. Because a brief that lists 4/8/12 but ships 6 and 10 contradicts itself. Derived.
- Measure spacing from the element's bounding box, not from the glyph. Because icons carry internal padding. ([Layout][f2-layout])
- Use `rem` for type and for spacing that should follow the user's font size, and `px` (or tokens) for borders and hairlines. A user who raises the browser's default font size must get larger text without a horizontal scrollbar. Derived, rests on WCAG 1.4.4 and 1.4.10. ([WCAG 1.4.4][wcag-resize], [WCAG 1.4.10][wcag-reflow])
- Breakpoints as Fluent describes them (web, Fluent default): 320, 480, 640, 1024, 1366, 1920 px. Techniques: reposition, resize, reflow, show/hide, restructure. Fluent publishes these as guidance, not as tokens; there is no `tokens.breakpoint*`. Declare them once as custom media or as constants in the project and say which ones you use. ([Layout][f2-layout])
- Prefer container queries (`@container`) for components that live in panes of different widths and media queries for page-level structure. Derived. ([MDN: container queries][mdn-container])
- Reflow: content must work at 320 CSS px width (a 1280 px window at 400 percent zoom) without two-dimensional scrolling, except for data tables, maps and similar content. Test it. ([WCAG 1.4.10][wcag-reflow])
- Proximity groups, equal spacing marks equal rank, and whitespace replaces divider lines. Align text left and center only icons and short captions under icons. Because grouping by distance is quieter than grouping by lines. ([Layout][f2-layout])
- Touch target Fluent default: 44 x 44 (iOS, web), 48 x 48 (Android). WCAG 2.2 AA requires at least 24 x 24 CSS px (or enough spacing) and notes 44 x 44 for AAA. A mouse-and-keyboard desktop web app may go below 44, but state the minimum (for example 32 or 34 high) and test touch-capable screens separately. Because the target size is a product decision tied to input devices. `@media (pointer: coarse)` can raise the size on touch screens. ([Layout][f2-layout], [WCAG 2.5.8][wcag-target])
- Forms: label above the field, left aligned. Fluent's WinUI example uses 80 px tall fields with 24 between fields and 48 between groups. With compact fields scale the gaps down but keep the group-to-field ratio above about 1.5 to 1. Because the ratio, not the number, is what lets the eye see groups. ([Forms][wl-forms])
- Text line length: 50 to 60 characters in running text, never under 20 or over 60 (WinUI guidance). On the web write `max-inline-size: 60ch` on the prose container. Limit help text columns accordingly. ([Typography][wl-typography])
- Use logical properties (`padding-inline`, `margin-block`, `inset-inline-start`) when the product may ship right-to-left languages. Derived. ([MDN: logical properties][mdn-logical])

## 4. Typography

Fluent default web type ramp (verified in `fonts.ts` and `typographyStyles.ts`; size/line height in px, `fontSizeBase*`, `fontSizeHero*` and `lineHeight*` tokens):

| Style (`typographyStyles`) | Size token | Size/line | Weight token |
| --- | --- | --- | --- |
| `caption2` | `fontSizeBase100` | 10/14 | `fontWeightRegular` 400 |
| `caption1` | `fontSizeBase200` | 12/16 | Regular |
| `body1` | `fontSizeBase300` | 14/20 | Regular |
| `body1Strong` | `fontSizeBase300` | 14/20 | `fontWeightSemibold` 600 |
| `body2` | `fontSizeBase400` | 16/22 | Regular |
| `subtitle2` | `fontSizeBase400` | 16/22 | Semibold |
| `subtitle1` | `fontSizeBase500` | 20/28 | Semibold |
| `title3` | `fontSizeBase600` | 24/32 | Semibold |
| `title2` | `fontSizeHero700` | 28/36 | Semibold |
| `title1` | `fontSizeHero800` | 32/40 | Semibold |
| `largeTitle` | `fontSizeHero900` | 40/52 | Semibold |
| `display` | `fontSizeHero1000` | 68/92 | Semibold |

The tokens are numbered 100 to 600 for the base sizes and 700 to 1000 for the hero sizes; `lineHeightBase100` to `lineHeightHero1000` follow the same numbering. Weights: Regular 400, Medium 500, Semibold 600, Bold 700 (`fontWeightRegular`, `fontWeightMedium`, `fontWeightSemibold`, `fontWeightBold`). There are also `Strong` and `Stronger` variants (`caption1Strong`, `body1Stronger`, `subtitle2Stronger`) that use Semibold or Bold. ([Typography][f2-typo], [Font tokens][gh-fonts], [Typography styles][gh-typostyles])

Windows ramp for reference (WinUI): Caption 12/16, Body 14/20, Body strong 14/20 Semibold, Body large 18/24, Subtitle 20/28 Semibold, Title 28/36 Semibold, Title large 40/52 Semibold, Display 68/92 Semibold. The web ramp has the same sizes from 12 up except Body large (18/24) and Subtitle 2 (16/22). A web app on Windows can use the web ramp unchanged. ([Windows typography][wl-typography])

Path A: apply the ramp with the `Text` component and its variants (`<Text as="h2" size={600} weight="semibold">`), or the heading components `Title1`, `Subtitle1`, `Body1`, `Caption1`, or `typographyStyles` inside `makeStyles` (`...typographyStyles.body1`). Path B: define one custom property or class per step (`--font-size-300: 14px`, `--line-height-300: 20px`) and use the Fluent names in comments. Use the right element for the role (`<h1>` to `<h6>` for headings) and style it separately; the visual size does not decide the heading level. Derived. ([MDN: headings][mdn-headings])

Rules:

- Font family. Fluent default `fontFamilyBase` is `'Segoe UI', 'Segoe UI Web (West European)', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif`; `fontFamilyMonospace` is `Consolas, 'Courier New', Courier, monospace`; `fontFamilyNumeric` starts with `Bahnschrift` and then falls back to the base stack (all verified). Segoe UI Variable is the Windows 11 system face; putting `"Segoe UI Variable Text"` in front of the stack is (derived, not verified) and only helps on Windows. If the brand uses another typeface, choose it deliberately, host it (`@font-face` with `font-display: swap`), and keep a system stack as fallback. Because a missing font must degrade to something legible, not to a random default. ([Typography][f2-typo], [MDN: font-display][mdn-fontdisplay])
- Smallest text: 12 px Regular, 14 px Semibold. `caption2` (10 px) is for non-essential labels only; do not use it for anything a user must read. The Windows guidance gives 12 and 14 as the floor because smaller text becomes unreadable in some scripts. ([Windows typography][wl-typography])
- Regular and Semibold are the working weights. Medium (500) is carried by the tokens; use it only if the typeface renders it well and the project brief names it. Avoid bold and italic for emphasis: use Semibold, because italics reduce readability for people with dyslexia. ([Windows typography][wl-typography])
- Never convey meaning by bold or italic alone. Because screen readers do not announce emphasis. If emphasis carries meaning, use `<strong>` or `<em>` for semantics and add words. ([Text][f2-text])
- Sentence case for every UI string including titles; never all-caps for emphasis. Follow the language's own capitalization rules (for example nouns capitalized in German) rather than English title case. Do not use `text-transform: uppercase` to fake it, because it changes what some screen readers and copy-paste produce and hides bad source strings. Because all-caps text is harder to read and scales badly. ([Typography][f2-typo], [Content design][f2-content])
- Truncating: wrap by default. Use an ellipsis (`text-overflow: ellipsis` with `overflow: hidden; white-space: nowrap`, or `line-clamp`) only when the container is clearly bounded or a "show more" affordance follows, and then expose the full text in a way a keyboard can reach (see `navigation.md`, tooltips, and `content-design.md`). Do not truncate tags or badges. A project brief may be stricter ("wrap, truncate only table cells and cards with a tooltip"); follow it. ([Windows typography][wl-typography])
- Alignment: left (start). Do not justify text in UI. ([Windows typography][wl-typography])
- Use tabular (equal-width) digits for numbers that change or line up in columns: `font-variant-numeric: tabular-nums`, if the typeface supports it. `fontFamilyNumeric` exists for this purpose in Fluent. Derived. ([MDN: font-variant-numeric][mdn-numeric])
- Let text scale: no fixed `height` on text containers, `min-height` instead; do not disable zoom with `user-scalable=no`. Check the page at 200 percent text size. ([WCAG 1.4.4][wcag-resize], [WCAG 1.4.12][wcag-spacing]) Derived.

## 5. Color and contrast

- Think in three palettes: neutral (surfaces, text, layout), shared (accents for avatars, calendars, badges; adjusted saturation in dark mode) and brand. Global tokens hold raw values; alias tokens give meaning ("text on brand"). Components should reference aliases only. Because changing a theme then touches one layer. ([Color][f2-color], [Tokens][f2-tokens])
- Token families (Fluent default, names verified in `types.ts`):
  - Neutral: `colorNeutralForeground1` to `colorNeutralForeground5`, `colorNeutralForegroundDisabled`; `colorNeutralBackground1` to `colorNeutralBackground8`, `colorNeutralBackgroundDisabled`; `colorNeutralStroke1`, `colorNeutralStroke2`, `colorNeutralStrokeAccessible`, `colorNeutralStrokeDisabled`; each with `Hover`, `Pressed` and `Selected` variants where it applies.
  - Subtle and transparent: `colorSubtleBackground` (+ `Hover`, `Pressed`, `Selected`) for toolbar buttons and list rows with no resting surface.
  - Brand: `colorBrandBackground`, `colorBrandForeground1`, `colorBrandForegroundLink`, `colorBrandStroke1`, `colorCompoundBrandStroke`, `colorNeutralForegroundOnBrand`.
  - Status: `colorStatusDanger*`, `colorStatusWarning*`, `colorStatusSuccess*` (each with `Background1` to `Background3`, `Border1`, `Border2`, `Foreground1` to `Foreground3`), plus the palette tokens `colorPaletteRedBackground1` and its siblings. The informative role uses the brand and neutral tokens (`colorNeutralBackground3`, `colorBrandForeground1`); whether a `colorStatusInformative*` family exists in your installed version is (derived, not verified), so check `@fluentui/tokens` `types.ts` for the version you use.
  - Focus: `colorStrokeFocus1` and `colorStrokeFocus2`; overlay: `colorBackgroundOverlay`.
- Interaction ladder: rest is lightest, hover one step darker, pressed two steps darker, selected darkest (neutral backgrounds in the light theme: `colorNeutralBackground1` `#ffffff`, `Hover` `#f5f5f5`, `Pressed` `#e0e0e0`, `Selected` `#ebebeb`; verified). Focus does not change color, it adds a ring or thickens an edge. WinUI inverts this (controls get lighter on interaction). Pick one direction project-wide and keep web and desktop consistent if both exist. Because a mixed direction reads as an inconsistency. ([Color][f2-color], [Light alias tokens][gh-lightcolor])
- Status colors only for status: red danger, yellow or orange caution, green positive. Always pair with text or an icon. Warnings are not red when red means error in the same product. Because color alone fails color-blind users. ([Color][f2-color], [WCAG 1.4.1][wcag-color])
- Contrast targets (WCAG): 4.5:1 for text, 3:1 for large text (18.66 px bold or 24 px regular and up) and for non-text elements such as icons, field borders and focus rings. Fluent states conformance to WCAG 2.1 AA; WCAG 2.2 AA is stricter and a good target. Disabled controls are exempt. ([Accessibility][f2-a11y], [WCAG 1.4.3][wcag-contrast], [WCAG 1.4.11][wcag-nontext])
- Field borders: Fluent's normal field border `colorNeutralStroke1` (`#d1d1d1`) has only about 1.53:1 against white (computed with the WCAG formula). Fluent closes the gap with a darker bottom edge: the Input sets `borderBottomColor: colorNeutralStrokeAccessible` (`#616161`, about 6.19:1; verified in `useInputStyles.styles.ts` and `lightColor.ts`). In the dark theme the values are `#666666` and `#adadad`. If your field border is lighter than 3:1, copy that approach: darken the bottom edge or the whole border (`border-bottom-color`). Do not assume a "strong line" token reaches 3:1; measure it. ([Input source][gh-input], [Light alias tokens][gh-lightcolor])
- Placeholder text: Fluent default `colorNeutralForeground4` `#707070` on white, about 4.95:1 (dark theme `#999999`). Browsers style `::placeholder` in their own default sheet, and that default can differ from your text color; set `color` explicitly and `opacity: 1` on `::placeholder`, then measure the effective color with the element's `opacity` applied. Effective color is the foreground blended over the surface by the opacity; check each theme and state. Derived. ([Input source][gh-input], [MDN: ::placeholder][mdn-placeholder])
- Fluent neutral values (light theme, Fluent default, verified): text `#242424` (`Foreground1`), `#424242` (`2`), `#616161` (`3`), `#707070` (`4`); surfaces `#ffffff` (`Background1`), `#fafafa` (`2`), `#f5f5f5` (`3`), `#f0f0f0` (`4`), `#ebebeb` (`5`), `#e6e6e6` (`6`); strokes `#d1d1d1` (`Stroke1`), `#e0e0e0` (`Stroke2`); disabled text `#bdbdbd`; overlay `rgba(0,0,0,0.4)` (dark theme overlay `rgba(0,0,0,0.5)`, surfaces `#292929` for `Background1` and `#1f1f1f` for `Background2`, text `#ffffff`). Use them as a reference scale, not as a palette to paste over a brand. ([Grey tokens][gh-colors], [Light alias tokens][gh-lightcolor], [Dark alias tokens][gh-darkcolor])
- Brand: `webLightTheme` and `webDarkTheme` use the `brandWeb` ramp, 16 steps from 10 (darkest, `#061724`) to 160 (lightest, `#ebf3fc`); step 80 is `#0f6cbd` and is the light-theme `colorBrandBackground`; the dark theme uses step 70 (`#115ea3`). Code comments in the generated alias files still show older hex values, so read `brandColors.ts`. A product with its own brand passes its own ramp to `createLightTheme(brand)` and `createDarkTheme(brand)`. ([Brand colors][gh-brand])
- Mapping technique (Path B especially): when you describe a Fluent component, map its neutral/brand/status roles to your tokens in one table (`colorNeutralBackground1` to your base surface, `colorNeutralStroke1` to your strong line, `colorBrandBackground` to your accent, `colorStatusDangerForeground1` to your error text) and keep that table next to the token file. Derived.
- Check contrast per state and per theme (light, dark, high contrast) with a script and with axe-core (rule `color-contrast`; it cannot see gradients, images or pseudo-element content, so it passes some failures and flags some passes), and keep the numbers in the pull request. Derived. ([axe rules][axe-rules])

## 6. Icons

- Regular (outline) icons for orientation; filled icons to mark a selected state. A project with a single stroke set may show selection by surface and text instead; that is a valid deviation. Path A: `@fluentui/react-icons` ships `Regular` and `Filled` variants of each icon (for example `Save20Regular`, `Save20Filled`) and `bundleIcon` pairs them. ([Iconography][f2-icons])
- Icons of 12 px are informational only, never interactive. Larger touch-oriented screens need larger icons. ([Iconography][f2-icons])
- Fluent default sizes in source: icon inside a button 20 (small 20, large 24); in an input 20 (small 16, large 24); in a message bar 20; in a WinUI menu item 16 (the size in Fluent UI React's menu item is (derived, not verified)). Dense desktop UIs often use 16; that is acceptable if recorded. ([Button source][gh-button], [Input source][gh-input], [Menu source][gh-menu])
- Use literal metaphors named for their shape; put modifiers (plus, check) filled at the bottom right; use one color, inheriting the parent's text color (`fill: currentColor`, so forced-colors mode and the disabled state work). ([Iconography][f2-icons])
- Decorative icons get `aria-hidden="true"` (and `focusable="false"` on inline SVG for old browsers). Every icon-only control needs an accessible name and a tooltip that a keyboard can reach: `aria-label` on the button, not on the SVG. Icons read differently across cultures, so do not rely on them alone for critical actions. ([Iconography][f2-icons], [WAI-ARIA APG: names][apg-names])
- Prefer inline SVG or an icon component over an icon font: an icon font breaks when the font fails to load and in forced-colors mode. Derived.

## 7. Elevation and material

- Fluent default shadow tokens: `shadow2`, `shadow4`, `shadow8`, `shadow16`, `shadow28`, `shadow64`. Each is a soft ambient shadow plus a sharper key shadow, and the number is the key shadow's blur radius. Verified in `utils/shadows.ts`:

  | Token | CSS value (ambient, key) |
  | --- | --- |
  | `shadow2` | `0 0 2px A, 0 1px 2px K` |
  | `shadow4` | `0 0 2px A, 0 2px 4px K` |
  | `shadow8` | `0 0 2px A, 0 4px 8px K` |
  | `shadow16` | `0 0 2px A, 0 8px 16px K` |
  | `shadow28` | `0 0 8px A, 0 14px 28px K` |
  | `shadow64` | `0 0 8px A, 0 32px 64px K` |

  `A` and `K` come from `colorNeutralShadowAmbient` and `colorNeutralShadowKey`: `rgba(0,0,0,0.12)` and `rgba(0,0,0,0.14)` in the light theme, `rgba(0,0,0,0.24)` and `rgba(0,0,0,0.28)` in the dark theme. `shadow2Brand` to `shadow64Brand` use the brand shadow colors. ([Elevation][f2-elev], [Shadow source][gh-shadows])
- Typical use (Fluent default): card 2 or 4, tooltip 8, toast 8, menu and listbox 16, drawer 28, dialog 64. Overlaying surfaces carry the higher values. An inline (non-overlaying) side panel needs no shadow, a border is enough. Because shadow communicates "floats above content". ([Elevation][f2-elev], [Toast source][gh-toast])
- Provide a small set of shadow tokens: card, popup (menu, list, tooltip) and dialog. Hover should not add a shadow in a flat design. Derived.
- A shadow carries a color, so it is a token like any other: declare each one as a custom property per theme (dark themes need a stronger alpha) and never write `box-shadow: 0 2px 8px rgb(0 0 0 / 25%)` inside a component. Because a literal in a component cannot follow the theme and slips past a scan that only looks for color properties. Path A: `boxShadow: tokens.shadow16`. Path B: `--shadow-popup: 0 0 2px var(--shadow-ambient), 0 8px 16px var(--shadow-key)`. Derived.
- Shadows disappear in forced-colors mode (the browser removes `box-shadow`), so an overlay needs a border (`border: 1px solid transparent` is mapped to a visible color) to stay visible. Derived. ([MDN: forced-colors][mdn-forced])
- Materials. Solid is the common one. Smoke dims everything behind a modal: Path A `colorBackgroundOverlay` (translucent black, 0.4 light and 0.5 dark; it is the `::backdrop` of a `<dialog>` or the backdrop of Fluent's `Dialog`). Acrylic (blurred translucent surface) can be approximated with `backdrop-filter: blur()`; keep a solid fallback with `@supports` and for `prefers-reduced-transparency`, because the effect costs paint time and lowers contrast. Mica has no web counterpart; drop it. (derived, not verified) ([Material][f2-material], [MDN: backdrop-filter][mdn-backdrop])

## 8. Motion

- Principles: functional, natural, consistent, engaging; bigger elements and longer distances need more time; nothing may feel sluggish or abrupt. Animate to explain a state change, not to decorate. ([Motion][f2-motion])
- Fluent default duration tokens (verified in `durations.ts`): `durationUltraFast` 50 ms, `durationFaster` 100, `durationFast` 150, `durationNormal` 200, `durationGentle` 250, `durationSlow` 300, `durationSlower` 400, `durationUltraSlow` 500. ([Durations][gh-durations])
- Fluent default curves (verified in `curves.ts`, `cubic-bezier` values):

  | Token | Value | Use |
  | --- | --- | --- |
  | `curveEasyEase` | `0.33, 0, 0.67, 1` | hover and color changes, symmetric moves |
  | `curveEasyEaseMax` | `0.8, 0, 0.2, 1` | stronger symmetric ease for larger moves |
  | `curveDecelerateMin` / `Mid` / `Max` | `0.33, 0, 0.1, 1` / `0, 0, 0, 1` / `0.1, 0.9, 0.2, 1` | things entering |
  | `curveAccelerateMin` / `Mid` / `Max` | `0.8, 0, 0.78, 1` / `1, 0, 1, 1` / `0.9, 0.1, 1, 0.2` | things leaving |
  | `curveLinear` | `0, 0, 1, 1` | continuous motion (spinner, progress) |

  Entering elements should arrive quickly and settle (decelerate), leaving ones should start slowly and go (accelerate). WinUI names the pair "fast out, slow in" and "slow out, fast in". ([Curves][gh-curves], [Timing and easing][wl-timing])
- Button: Fluent animates background, border and text color with `durationFaster` (100 ms) and `curveEasyEase`, and does not scale on press. A press scale (for example 0.97) is a legitimate brand choice if recorded; drop it when motion is reduced. ([Button source][gh-button])
- Input underline: the 2 px brand underline (`::after`, `colorCompoundBrandStroke`) grows from the center on focus in `durationNormal` (200 ms, `scaleX` 0 to 1) and disappears in `durationUltraFast` (50 ms) on blur. Nothing else on an input animates. Verified in `useInputStyles.styles.ts`. ([Input source][gh-input])
- Transitions that fit: show/hide for menus and dialogs, elevation changes, top-level swaps as a quick cross-fade instead of sliding large elements, container transforms. Skeletons may pulse or wave. Animate `opacity` and `transform` where you can; they do not trigger layout. Derived. ([Motion][f2-motion], [Skeleton][f2-skeleton])
- Reduced motion: honor `prefers-reduced-motion: reduce` everywhere: durations to about 0, no flashing, no sudden jumps, motion only on the focused element, no information carried by animation alone. Fluent's own source drops transition durations to `0.01ms` inside `@media screen and (prefers-reduced-motion: reduce)` (verified in Button and Input). Include every transition in the switch, including opacity fades and press scales. Path A: `makeStyles` components already do this; your own `makeStyles` code does not unless you add the media query. Path B: one rule near the top of the cascade, for example
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
  Motion started from JavaScript (Web Animations API, a motion library, `scrollIntoView({ behavior: 'smooth' })`) does not see the CSS rule; read `window.matchMedia('(prefers-reduced-motion: reduce)')` and skip or shorten it. Derived. ([Motion][f2-motion], [Button source][gh-button], [MDN: prefers-reduced-motion][mdn-reduced])
- Testing reduced motion: with Playwright call `page.emulateMedia({ reducedMotion: 'reduce' })`, open each page and fail on any visible element whose computed `transition-duration` or `animation-duration` is above 1 ms (read `getComputedStyle` in `page.evaluate`, or `document.getAnimations()` and check `effect.getComputedTiming().duration`). Ignore elements that are not rendered. Details: `web-mapping.md`. Derived.
- Do not animate actions the user repeats many times per minute with the keyboard. Derived.

## 9. Shape: radius and stroke

- Fluent default radius tokens (verified in `borderRadius.ts`): `borderRadiusNone` 0, `borderRadiusSmall` 2, `borderRadiusMedium` 4, `borderRadiusLarge` 6, `borderRadiusXLarge` 8, `borderRadius2XLarge` 12, `borderRadius3XLarge` 16, `borderRadius4XLarge` 24, `borderRadius5XLarge` 32, `borderRadius6XLarge` 40, `borderRadiusCircular` 10000. Default controls use `borderRadiusMedium` (4), controls under 32 px high use 2 (`borderRadiusSmall`), large components 8 or 12. ([Radius tokens][gh-radius], [Shapes][f2-shapes])
- WinUI on Windows 11, for a web app that should feel at home next to native Windows apps: 8 for windows, flyouts, dialogs, menus and teaching tips (overlays); 4 for controls (button, checkbox, combo box, text box, list view) and bars (progress, scroll, slider); tooltips 4 as an exception because of their size; 0 where edges meet (two halves of a split button, a flyout touching its trigger). Because radius signals hierarchy: overlays rounder than the controls inside. ([Geometry][wl-geometry])
- A brand may round more softly (for example 8 for controls, 12 for cards). That is fine when recorded as a deliberate deviation. Derived.
- Stroke tokens (verified in `strokeWidths.ts`): `strokeWidthThin` 1, `strokeWidthThick` 2, `strokeWidthThicker` 3, `strokeWidthThickest` 4 px; round line caps; match stroke to size (small spinner 2, large 4). Focus rings are 2 px (`strokeWidthThick`). ([Stroke tokens][gh-stroke], [Shapes][f2-shapes])
- Focus ring: Fluent draws a double ring from `colorStrokeFocus1` and `colorStrokeFocus2` (light theme white and black, dark theme black and white), so it is visible on any surface, and switches the ring to the system color `Highlight` in forced-colors mode (verified in `createFocusOutlineStyle.ts`). Path A: components do this through `createFocusOutlineStyle` and `useFocusableGroup`. Path B: use `:focus-visible` (not `:focus`) with `outline: 2px solid`, `outline-offset: 2px` and a second contrasting `box-shadow` ring, never `outline: none` without a replacement. Derived. ([MDN: :focus-visible][mdn-focusvisible], [WCAG 2.4.7][wcag-focus])
- Shapes by role: rectangle for buttons, fields and cards; circle for people; pill for slider tracks, switch tracks, tags and badges. ([Shapes][f2-shapes])

## 10. Tokens and themes

- Two layers: global (raw hex, type, radius, stroke, animation) and alias (meaning, such as "text on brand"). Themes: light, dark, high contrast and brand color. ([Tokens][f2-tokens])
- Fluent UI React v9 themes (verified in `themes/web` and `themes/teams`): `webLightTheme`, `webDarkTheme`, `teamsLightTheme`, `teamsDarkTheme`, `teamsHighContrastTheme`. A theme is a flat object of token name to value; `FluentProvider theme={webLightTheme}` writes every entry as a CSS custom property on its wrapper element (`--colorNeutralBackground1`), and `tokens.colorNeutralBackground1` is the string `var(--colorNeutralBackground1)`. There is no `webHighContrastTheme`; use `teamsHighContrastTheme` or rely on forced-colors mode (below). ([Themes][gh-themes], [Tokens object][gh-tokens])
- Path A: apply fonts, base colors and theme once at the root (`FluentProvider` near `createRoot`), pick the theme from `window.matchMedia('(prefers-color-scheme: dark)')` and a user override, and override locally only on purpose (a nested `FluentProvider` or a `makeStyles` rule). ([Fluent provider][f2-fluentprovider])
- Path B: declare tokens once on `:root` in a CSS file, in a cascade layer so that component CSS cannot override them by accident, and switch themes with a media query plus an attribute:
  ```css
  @layer tokens, base, components;
  @layer tokens {
    :root { color-scheme: light dark; --color-surface-1: #ffffff; --color-text-1: #242424; }
    @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --color-surface-1: #292929; --color-text-1: #ffffff; } }
    :root[data-theme="dark"] { --color-surface-1: #292929; --color-text-1: #ffffff; }
    @media (forced-colors: active) { :root { --color-surface-1: Canvas; --color-text-1: CanvasText; } }
  }
  ```
  `color-scheme` makes native controls, scrollbars and `::backdrop` follow the theme. The function `light-dark()` can replace the paired declarations when your browser support allows it. Derived. ([MDN: color-scheme][mdn-colorscheme], [MDN: @layer][mdn-layer])
- Keep one source of truth for tokens (a design brief plus a token file); do not maintain a parallel Figma kit by hand unless you also keep it in sync. The Fluent 2 Figma kits are linked from the Fluent 2 site. ([Get started: design][f2-start-design])
- In CSS and CSS-in-JS never hard-code colors in components: not hex, not `rgb()`, not named colors (`white`, `black`), not the color inside a `box-shadow`. Hard-coded colors are the reason dark mode and high contrast fail. Scan the component folders for `#[0-9a-fA-F]{3,8}\b`, `rgba?\(`, `hsla?\(` and the named colors the project uses; Stylelint's `color-no-hex` and `declaration-property-value-disallowed-list` can enforce it in CI. Derived. ([Stylelint rules][stylelint-rules])
- High contrast. Windows high contrast and other forced-colors modes replace your colors with a small system palette. Fluent's high-contrast theme maps the roles to those system colors (verified in `highContrastColor.ts`): text `CanvasText`, surface `Canvas`, strokes `CanvasText`, disabled `GrayText`, text on brand `ButtonText`, brand background `ButtonFace`, selection and focus `Highlight`. Check in this order: (1) interactive controls keep a border (`border: 1px solid transparent` becomes visible), (2) focus rings use `outline` or the system `Highlight`, not only `box-shadow`, (3) icons use `currentColor`, (4) state is not carried by color alone, (5) `forced-color-adjust: none` is used only on a small element that must keep its color (a color swatch) and then sets system colors itself. Test with Playwright `page.emulateMedia({ forcedColors: 'active' })` for structure and once on a real Windows contrast theme. Derived. ([Accessibility overview][wl-a11y], [MDN: forced-colors][mdn-forced])

## 11. Recording deviations

When the project deviates from a Fluent default, write one entry in the project's design document or next to the tokens. In a Markdown design file use a table:

```text
| Deviation | Reason | Applies to | Decided |
| --- | --- | --- | --- |
| Control height 34 instead of Fluent 32 | Larger target for fast desktop use; one height for all controls | Buttons, text fields, comboboxes | <who>, <date> |
```

In the token CSS use a comment block at the declaration:

```css
/* Deviation: control height 34 instead of Fluent 32 (tokens.* medium input).
   Reason: larger target for fast desktop use; one height for all controls.
   Applies to: buttons, text fields, comboboxes.
   Decided: <who>, <date>. */
--control-height: 34px;
```

Path A: a deviation is a theme override (`const theme = { ...webLightTheme, borderRadiusMedium: '6px' }`) or a `makeStyles` rule; put the comment above that line and keep overrides in one theme file. Because a deviation without a reason looks like a bug to the next reviewer, and an unrecorded Fluent default looks like an omission. A review should report "differs from Fluent, recorded" as fine and "differs from Fluent, not recorded" as a finding.

## 12. Checklist

- [ ] Spacing values are on the grid or are the documented nudges 2, 6, 10 (search the styles for off-grid pixel values, or use a Stylelint allow-list on `padding`, `margin`, `gap`).
- [ ] Type sizes follow the ramp; nothing below 12 px for readable text; no all-caps strings (search for `text-transform: uppercase`, `toUpperCase()` and upper-case literals in the UI strings).
- [ ] Text contrast is 4.5:1 or better in every theme and state; borders, icons and focus rings 3:1 (axe-core `color-contrast` in Playwright for each theme, plus a script output attached for the states axe cannot reach).
- [ ] Field border contrast is measured, and the bottom edge or border is darkened if the border is under 3:1 (script output).
- [ ] Placeholder contrast is measured with the element's `opacity` applied, in each theme (script output).
- [ ] Colors come from tokens (`var(--...)` or `tokens.*`), with no hex literals, `rgb()` or named colors and no inline `box-shadow` color in components (the scans in section 10 over the component folders).
- [ ] Shadow tokens exist for card, popup and dialog per theme; inline panels have none (search for `box-shadow` literals).
- [ ] Every transition uses a token duration and curve; with `prefers-reduced-motion: reduce` emulated, no visible element has a transition or animation above 1 ms (Playwright test over every page, section 8).
- [ ] Focus is visible on every interactive element with `:focus-visible`, at 3:1, and survives forced-colors mode (Playwright screenshot with `forcedColors: 'active'`; manual Tab walk).
- [ ] The layout reflows at 320 CSS px and at 200 percent text size without horizontal scrolling (Playwright viewport 320 x 640, screenshot).
- [ ] Radius values follow the project tokens; deviations from Fluent are recorded.
- [ ] Every deliberate difference from Fluent has a recorded reason (section 11).

## 13. Sources

[f2-principles]: https://fluent2.microsoft.design/design-principles
[f2-layout]: https://fluent2.microsoft.design/layout
[f2-typo]: https://fluent2.microsoft.design/typography
[f2-color]: https://fluent2.microsoft.design/color
[f2-icons]: https://fluent2.microsoft.design/iconography
[f2-elev]: https://fluent2.microsoft.design/elevation
[f2-motion]: https://fluent2.microsoft.design/motion
[f2-shapes]: https://fluent2.microsoft.design/shapes
[f2-material]: https://fluent2.microsoft.design/material
[f2-a11y]: https://fluent2.microsoft.design/accessibility
[f2-tokens]: https://fluent2.microsoft.design/design-tokens
[f2-content]: https://fluent2.microsoft.design/content-design
[f2-start-design]: https://fluent2.microsoft.design/get-started/design
[f2-fluentprovider]: https://fluent2.microsoft.design/components/web/react/core/fluentprovider/usage
[f2-text]: https://fluent2.microsoft.design/components/web/react/core/text/usage
[f2-skeleton]: https://fluent2.microsoft.design/components/web/react/core/skeleton/usage
[wl-forms]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/forms
[wl-typography]: https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/typography
[wl-geometry]: https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/geometry
[wl-timing]: https://learn.microsoft.com/en-us/windows/apps/design/motion/timing-and-easing
[wl-a11y]: https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview
[gh-durations]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/durations.ts
[gh-curves]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/curves.ts
[gh-radius]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/borderRadius.ts
[gh-stroke]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/strokeWidths.ts
[gh-spacing]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/spacings.ts
[gh-fonts]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/fonts.ts
[gh-typostyles]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/typographyStyles.ts
[gh-colors]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/colors.ts
[gh-brand]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/brandColors.ts
[gh-lightcolor]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/alias/lightColor.ts
[gh-darkcolor]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/alias/darkColor.ts
[gh-shadows]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/utils/shadows.ts
[gh-themes]: https://github.com/microsoft/fluentui/tree/master/packages/tokens/src/themes
[gh-tokens]: https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/tokens.ts
[gh-button]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-button/library/src/components/Button/useButtonStyles.styles.ts
[gh-input]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-input/library/src/components/Input/useInputStyles.styles.ts
[gh-menu]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-menu/library/src/components/MenuItem/useMenuItemStyles.styles.ts
[gh-toast]: https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-toast/library/src/components/Toast/useToastStyles.styles.ts
[wcag-resize]: https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
[wcag-reflow]: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
[wcag-spacing]: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
[wcag-color]: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
[wcag-contrast]: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
[wcag-nontext]: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
[wcag-target]: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
[wcag-focus]: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
[apg-names]: https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/
[axe-rules]: https://dequeuniversity.com/rules/axe/html/4.10/color-contrast
[stylelint-rules]: https://stylelint.io/user-guide/rules/
[mdn-aria-first]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_in_HTML#first_rule_of_aria_use
[mdn-container]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
[mdn-logical]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
[mdn-headings]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements
[mdn-fontdisplay]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display
[mdn-numeric]: https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
[mdn-placeholder]: https://developer.mozilla.org/en-US/docs/Web/CSS/::placeholder
[mdn-forced]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors
[mdn-backdrop]: https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter
[mdn-reduced]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
[mdn-focusvisible]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
[mdn-colorscheme]: https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme
[mdn-layer]: https://developer.mozilla.org/en-US/docs/Web/CSS/@layer
