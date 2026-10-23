# Content design: UI text, errors, formats

Read this file when you write or review any user-facing text in a web app: button labels, titles, messages, error text, empty states, tooltips, placeholders, help text, accessible names, and the format of numbers, dates, times and amounts. Fluent UI React v9 projects and projects with their own components follow the same rules; the web-specific items are in sections 4, 6 and 7.

Language note: the examples here are in English. The project's own language governs all real strings. Apply the rules, not the wording: a German, French or Japanese interface keeps its own capitalization, punctuation, politeness form and number format. If the project has a style guide or a term list, it wins over this file. Value tags: **Fluent default** (from Fluent guidance), **Derived** (built on Fluent principles and a web standard), **(derived, not verified)**; see [foundations.md](foundations.md), section 1.

## Contents

1. [Stance and tone](#1-stance-and-tone)
2. [Mechanics](#2-mechanics)
3. [Words to avoid](#3-words-to-avoid)
4. [Button labels and accessible names](#4-button-labels-and-accessible-names)
5. [Error messages](#5-error-messages)
6. [Numbers, dates, times, amounts](#6-numbers-dates-times-amounts)
7. [State texts](#7-state-texts)
8. [Where strings live](#8-where-strings-live)
9. [Checklist](#9-checklist)
10. [Sources](#10-sources)

## 1. Stance and tone

- Treat language as design material, like icons. Before writing, answer three questions: who reads this, what do they want to do next, and how much time do they have. Because text that fits the moment is shorter and calmer. ([Content design][f2-content])
- Content should simplify tasks, highlight decisions and prioritize next steps. ([Content design][f2-content])
- Tone matches intent: factual in navigation, headers, buttons and table heads; calm and friendly on dashboards, empty states and help; never jokey; no calls for enthusiasm. In conflicts and errors stay neutral and without blame. Because users in a hurry read tone as attitude. ([Content design][f2-content])
- Prefer common words, an appropriate amount of information and a clear recommended action; short sentences and fragments are fine. ([Content design][f2-content])
- Address: Fluent writes in the second person and uses first person only when it speaks for the reader. Choose the project's form once (for example formal "you" in languages that distinguish) and keep it. Never let the software speak as "I" or "we" with feelings (see [responsible-ai.md](responsible-ai.md)). ([Content design][f2-content])
- Tense and voice: mostly present tense, active voice unless the action matters more than the actor. After the user's own action report the result ("Appointment moved to Thu 14:30"). ([Content design][f2-content])
- Write the page language: set `<html lang="en">` (or the real language) and `lang` on passages in another language, so screen readers pick the right voice and browsers hyphenate and quote correctly. Derived. ([WCAG 3.1.1][wcag-lang], [WCAG 3.1.2][wcag-lang-parts])

## 2. Mechanics

- Sentence case for all UI text, including titles; only the first word and proper nouns are capitalized. Follow the language's own rules (for example capitalized nouns). No all-caps for emphasis; do not fake it with `text-transform: uppercase` (see [foundations.md](foundations.md), section 4). ([Content design][f2-content], [Typography][f2-typo])
- Punctuation: question marks always; periods only after full sentences; no periods in headings, buttons, labels, list items; avoid exclamation marks except for genuinely happy moments; no colons after labels (a `<label>` is not followed by a colon in the string; if the design shows one, draw it in CSS, not in the text, so the accessible name stays clean). Where the project writes help text as full sentences with a period, keep that rule consistently. ([Content design][f2-content])
- Keep a term list: pick one word per concept and use it everywhere ("customer", not "client" in one place and "guest" in another). Keep a glossary next to the manual. ([Content design][f2-content])
- Simplify jargon so a broad audience understands; keep terms consistent across product and docs. ([Content design][f2-content])
- Alt text for images is part of the content. Write it as short as a label and say what the image conveys, not "image of". Decorative images get `alt=""`; icons that sit next to a text label get `aria-hidden="true"`. Icon-only controls get an accessible name (section 4). ([Content design][f2-content], [Iconography][f2-icons], [WAI alt decision tree][wai-alt])
- Link text and heading text are read out of context by screen readers (lists of links, lists of headings), so each must make sense alone. Derived. ([WCAG 2.4.4][wcag-link])

## 3. Words to avoid

- Directional words ("above", "left", "below"): they assume sight, and the layout changes at other widths and in other languages. Refer to the card or group by name ("under Contact"). ([Content design][f2-content])
- "Click here" and bare "Learn more": link text must make sense alone. Also avoid "click" for actions in general ("Select", "Choose", or the verb of the action), because users tap, press and use a keyboard. ([Link][f2-link])
- Raw technical details in the main message; show them in an expandable detail or a log. ([Message bar][f2-messagebar])
- Terms like "Error" as a title; "invalid input" without saying what is valid.
- Search the code and the help content for these words when reviewing (grep for "above", "below", "left", "right", "here", "click").

## 4. Button labels and accessible names

Short rules; the full set is in [buttons-and-selection.md](buttons-and-selection.md).

| Purpose | Pattern | Example |
| --- | --- | --- |
| Create | "New" + object; in a menu: button "New", entries name the object | "New customer"; menu entries "Customer", "Note" |
| Add existing | "Add" + type | "Add product" |
| Confirm a dialog | Concrete answer to the title | "Delete" and "Cancel" for "Delete this file?" |
| Multi-step | "Next", "Back" | |
| Finish | "Done" (confirmation), "Finish" (selection applied), "Close" (informational), "Got it" (important notice), "Hide" (permanent) | |
| Discard | "Cancel" discards; "Close" changes nothing; no "x" next to "Close" | |
| Save | "Save" plus a toast or bar as feedback; ideally autosave | |
| Toast or bar action | One or two words, at most 36 characters; links start with a verb | "Undo", "Try again", "Check connection" |

([Button][f2-button], [Dialog][f2-dialog], [Toast][f2-toast], [Message bar][f2-messagebar])

Web-specific rules for names and labels (all Derived unless a Fluent page is cited):

- The visible label lives inside the element: `<button>Save</button>`, not `<div role="button" aria-label="Save">` and not a `<button>` whose text is only an `::after` pseudo-element. Text from `content:` in CSS is read inconsistently and cannot be translated or selected. ([MDN: button][mdn-button])
- Prefer visible text to `aria-label`. When an `aria-label` is needed (icon-only button), it must contain the visible text if there is any, so that voice-control users can say what they see ("Label in Name"). It states the action and the object, in sentence case, without the control type ("Delete customer", not "Delete customer button"; the role already says "button"). ([WCAG 2.5.3][wcag-label-in-name], [APG: names][apg-names])
- `aria-label` is not translated by browser tools the way visible text can be and is often forgotten in string files: keep it in the same i18n catalog as visible text (section 8).
- The `title` attribute is not a tooltip for keyboard users: it does not appear on focus, not on touch, and is exposed inconsistently as a name or description. Use it for nothing the user needs. For a tooltip use a real tooltip component (Fluent `Tooltip`, which shows on focus and hover and is linked with `aria-describedby` or `aria-labelledby`) or an `aria-describedby` hint; for an icon-only button the tooltip repeats the accessible name. ([Tooltip][f2-tooltip], [WCAG 1.3.1][wcag-info])
- Form fields: a `<label for>` or a wrapping `<label>` for every control; Fluent's `Field` component writes it for you. The placeholder is never the label ([foundations.md](foundations.md), section 5 and the `inputs.md` reference). ([Field][f2-field])
- Links go somewhere, buttons do something: use `<a href>` for navigation and `<button>` for actions, and write the text accordingly ("Open report" for a link, "Export report" for a button). ([MDN: a][mdn-a])
- Headings are text for navigation: one `<h1>` per page that names the page, no skipped levels, no heading used just to make text big. ([WCAG 1.3.1][wcag-info])

## 5. Error messages

Fluent asks for three things: name what failed, say why, and offer two ways forward. An error without a next step leaves people stuck. Technical detail goes into a collapsible section (`<details>`) or a log. ([Responsible AI][f2-rai], [Message bar][f2-messagebar])

| Part | Rule | Example (a report could not be saved) |
| --- | --- | --- |
| Title (what) | Concrete, sentence case, not "Error" | "Report not saved" |
| Text (why) | One sentence, no blame, no jargon | "The connection to the server was lost." |
| Way 1 (button) | One verb | "Try again" |
| Way 2 (link) | Verb plus object | "Check connection" |
| Detail | Collapsible or logged | "Show details" |

- Field errors state the problem and the way out: "The postal code has four digits." Never "Invalid input" without saying what is valid. ([Field][f2-field])
- Show a field error under the field, link it with `aria-describedby` and set `aria-invalid="true"` (Fluent `Field` with `validationState="error"` and `validationMessage` does both). Do not show an error before the user has left the field or submitted: style invalid state with `:user-invalid`, not `:invalid`, which matches an empty required field on first paint. Derived. ([MDN: :user-invalid][mdn-userinvalid], [WCAG 3.3.1][wcag-error], [WCAG 3.3.3][wcag-suggestion])
- Errors that appear without a page load are announced: put a field error in the field's description, a form-level summary or a message bar in a live region (`role="alert"` or `aria-live="assertive"` for errors, `role="status"` or `aria-live="polite"` for confirmations). Derived. ([WCAG 4.1.3][wcag-status])
- A dialog is only for a decision; field problems stay at the field. ([WinUI dialogs][wl-dialogs])
- For failures of an AI feature always offer a way that does not need the AI ("Write the reply yourself"). ([Responsible AI][f2-rai])
- Availability messages say why something is unavailable and what to do: "AI replies are paused because no API key is set. Add one under Settings > AI." not "AI unavailable". ([Responsible AI][f2-rai])
- Do not rely on the browser's built-in validation bubbles for wording: they are generated by the browser, in the browser's language, and cannot carry your rules. Use `novalidate` with your own messages, or set them with `setCustomValidity` from your string catalog. Derived. ([MDN: constraint validation][mdn-validation])

## 6. Numbers, dates, times, amounts

Fluent defers to the Microsoft Writing Style Guide here, which was not read for this skill. The rules below are Derived from common practice and from the project-neutral needs of a web UI; the project's locale and style guide govern.

| Quantity | Rule | Example (example locale, day-first, 24-hour clock, decimal comma) |
| --- | --- | --- |
| Date in lists and headers | Abbreviated weekday plus day and month | "Wed 21.10." |
| Date in inputs and receipts | Full numeric date in the locale format | "21.10.2026" |
| Time | 24-hour `HH:mm` if the locale uses it; no "o'clock" in fields | "09:30" |
| Duration | Number plus abbreviated unit | "60 min" |
| Amount | Locale separators, two decimals; currency in the column header or after a non-breaking space | "1.234,50 EUR" |
| Percent | Number, non-breaking space where the locale uses it, percent sign | "38 %" |
| Numbers in text | In UI always digits, not words | "3 appointments to rebook" |

Always format through the platform, never with hand-built strings, and use non-breaking spaces between a number and its unit so the line does not break inside it. Use the same format in input, display and exports.

- Numbers and amounts: `new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(value)`; percent with `style: 'percent'`; units with `style: 'unit', unit: 'minute', unitDisplay: 'short'`. Reuse one formatter instance per locale and options set instead of constructing it per render. ([MDN: Intl.NumberFormat][mdn-numberformat])
- Dates and times: `new Intl.DateTimeFormat(locale, { weekday: 'short', day: 'numeric', month: 'numeric' })`; set `timeZone` explicitly for server times and `hour12: false` or `hourCycle: 'h23'` when the project fixes the clock. Never build a date with `` `${d}.${m}.${y}` ``. Relative text ("in 2 days") uses `Intl.RelativeTimeFormat`; lists use `Intl.ListFormat`. ([MDN: Intl.DateTimeFormat][mdn-datetimeformat])
- Machine-readable values stay machine-readable: `<time datetime="2026-10-21T09:30">Wed 21.10., 09:30</time>`, a number input's `value` as the plain number, API payloads in ISO 8601 and invariant decimals. The display format is a view concern only. ([MDN: time][mdn-time])
- `<input type="date">`, `type="time"` and `type="number"` render and parse in the browser's locale, not necessarily the app's; if the project needs its own format or masks, use a text input with a parser and say so in the tooltip or help text (see `inputs.md`). Derived.
- Sorting and comparing strings that users read: `Intl.Collator(locale)` or `localeCompare(b, locale)`, not `<` on strings. Derived. ([MDN: Intl.Collator][mdn-collator])
- Plurals: use `Intl.PluralRules` or an i18n library's plural syntax, not `count === 1 ? 'item' : 'items'`; many languages have more than two forms. Derived. ([MDN: Intl.PluralRules][mdn-plural])

## 7. State texts

| State | Rule | Example |
| --- | --- | --- |
| Loading | Progressive form, at most three words, ends with an ellipsis preceded by a space, concrete (repeats the action word) | "Loading ...", "Searching customers ..." |
| Empty | One sentence: what is missing and how to create it, with a button | "No entries yet." plus "Add entry" |
| No result | One line | "No results." |
| Tooltip, disabled control | When it becomes available | "Available once a name is entered." |
| Tooltip, icon only | Fluent: short noun phrase, sentence case, no final punctuation. Action icons often read better as verb plus object. | "Move appointment" |
| Placeholder | An example or format hint, no period; never the label | "e.g. 09:30" |
| Help text | A sentence or fragment, one line | "The name as on the ID." |

([Spinner][f2-spinner], [WinUI auto-suggest][wl-autosuggest], [Tooltip][f2-tooltip], [Input][f2-input], [Field][f2-field])

Web notes (Derived):

- A disabled `<button disabled>` is not focusable and does not fire hover events in every browser, so a tooltip on it is unreachable for keyboard users. Use `aria-disabled="true"` (Fluent: `disabledFocusable`) on a control that must explain itself, keep it focusable, block the action in the handler, and link the reason with `aria-describedby`. ([Button][f2-button], [MDN: aria-disabled][mdn-ariadisabled])
- Loading text lives in a status region (`role="status"`) so a screen reader hears it once; do not move focus for it. For a long operation also give the spinner an accessible name ("Loading customers"). ([Spinner][f2-spinner], [WCAG 4.1.3][wcag-status])
- The ellipsis in "Loading ..." is real text (`...` or the character `…`), not an animated CSS pseudo-element, and the animation stops under `prefers-reduced-motion` ([foundations.md](foundations.md), section 8).
- Placeholders disappear on input and are often too light to read; they are examples only. ([Input][f2-input])

## 8. Where strings live

Strings are content, so they live in one place per language, not in components.

- Path A and B: keep every user-facing string in a message catalog (react-intl `defineMessages`, i18next resource files, Lingui, or a typed `strings.ts` object when the app has one language) keyed by meaning, not by wording (`report.save.failed.title`, not `reportNotSaved`). A component receives the translated string or a message id; it does not contain English literals. Derived.
- Include the invisible strings in the catalog: `aria-label`, `aria-describedby` texts, `alt`, `title`, tooltip text, document `<title>`, live-region messages. These are the strings that get forgotten in translation. Derived.
- Use placeholders for values (`"Moved to {time}"`), never string concatenation; word order differs between languages. Plural and select forms belong in the message, not in code. Derived. ([ICU MessageFormat][icu-mf])
- Test the longest language and 200 percent text size; long German or Finnish words need `overflow-wrap: anywhere` or `hyphens: auto` with a correct `lang`. Derived.
- Keep the term list (section 2) as data next to the catalog, and let a lint rule or a review compare new strings against it.

## 9. Checklist

- [ ] Every string follows sentence case and the punctuation rules; a unit test or grep over the message catalog finds no all-caps and no trailing-colon labels, and the CSS has no `text-transform: uppercase` on running text.
- [ ] One term per concept; the glossary is current (review against the term list).
- [ ] No direction words, "click" or "click here" in strings or help (grep over the catalog and the help content).
- [ ] Every error has what, why and at least one way forward; AI errors have a no-AI path (review of the error messages in the catalog).
- [ ] Field errors are linked to the field (`aria-describedby`, `aria-invalid`) and announced; invalid styling uses `:user-invalid` (Testing Library: `getByRole('textbox', { name })` has `toBeInvalid()` and `toHaveAccessibleDescription(...)` after blur; axe-core run on the error state).
- [ ] Buttons are verbs; no "OK", "Yes", "No" in dialogs (grep for `>OK<` and `"Yes"` in the catalog).
- [ ] Every icon-only control has an accessible name that matches its tooltip, and no `title` attribute is the only carrier of a name or hint (Testing Library `getByRole('button', { name: 'Delete customer' })`; grep for `title=`).
- [ ] The visible label is inside the `<button>` or `<label>` and is contained in the `aria-label` when both exist (axe rule `label-content-name-mismatch`, review).
- [ ] Dates, times, amounts and percents use `Intl.*` formatters with the locale; no manual string formatting (grep for `toFixed(`, `.getMonth()` and template strings that build dates in view code; test with two locales).
- [ ] Machine values stay machine values: `<time datetime>` and API payloads are not locale formatted (review).
- [ ] Loading, empty, no-result and disabled-tooltip texts exist for every list and every non-obvious disabled control; disabled-with-reason controls use `aria-disabled`, not `disabled` (review; Testing Library `toHaveAttribute('aria-disabled', 'true')`).
- [ ] The text stays readable at 200 percent text size, 320 CSS px width and in the longest language (Playwright screenshots).

## 10. Sources

[f2-content]: https://fluent2.microsoft.design/content-design
[f2-typo]: https://fluent2.microsoft.design/typography
[f2-icons]: https://fluent2.microsoft.design/iconography
[f2-link]: https://fluent2.microsoft.design/components/web/react/core/link/usage
[f2-messagebar]: https://fluent2.microsoft.design/components/web/react/core/messagebar/usage
[f2-button]: https://fluent2.microsoft.design/components/web/react/core/button/usage
[f2-dialog]: https://fluent2.microsoft.design/components/web/react/core/dialog/usage
[f2-toast]: https://fluent2.microsoft.design/components/web/react/core/toast/usage
[f2-field]: https://fluent2.microsoft.design/components/web/react/core/field/usage
[f2-rai]: https://fluent2.microsoft.design/responsible-AI/
[f2-spinner]: https://fluent2.microsoft.design/components/web/react/core/spinner/usage
[f2-tooltip]: https://fluent2.microsoft.design/components/web/react/core/tooltip/usage
[f2-input]: https://fluent2.microsoft.design/components/web/react/core/input/usage
[wl-dialogs]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs
[wl-autosuggest]: https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/auto-suggest-box
[wcag-lang]: https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html
[wcag-lang-parts]: https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html
[wcag-link]: https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html
[wcag-label-in-name]: https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
[wcag-info]: https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
[wcag-error]: https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html
[wcag-suggestion]: https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html
[wcag-status]: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
[wai-alt]: https://www.w3.org/WAI/tutorials/images/decision-tree/
[apg-names]: https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/
[mdn-button]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button
[mdn-a]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a
[mdn-userinvalid]: https://developer.mozilla.org/en-US/docs/Web/CSS/:user-invalid
[mdn-validation]: https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation
[mdn-ariadisabled]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-disabled
[mdn-numberformat]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat
[mdn-datetimeformat]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat
[mdn-time]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/time
[mdn-collator]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator
[mdn-plural]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules
[icu-mf]: https://formatjs.github.io/docs/core-concepts/icu-syntax/
