# Responsible AI in the interface: disclosure, control, agents, review rubric

Read this file when a page shows or triggers AI output: suggestion panels, drafted replies, assistants, automatic actions, AI-filled fields, background agents. It covers the five Fluent principles, rules for agents, visual and content patterns, a scoring rubric you can use as a review list, and React Testing Library and Playwright assertions that prove the interface rules. The rules are about interface behavior, not about model quality.

Language note: example strings are English; use the project's language. Disclaimer wording should be approved by whoever owns product content, and kept in one central place (the message catalog, see [content-design.md](content-design.md), section 8) so it is not retyped per view. If the project has its own AI policy, it wins; where it is silent, use this file. Value tags: **Fluent default**, **Derived**, **(derived, not verified)**; see [foundations.md](foundations.md), section 1. Rules marked Derived rest on the cited web standard, not on a Microsoft statement.

## Contents

1. [Five principles and what they mean in a page](#1-five-principles-and-what-they-mean-in-a-page)
2. [Agents](#2-agents)
3. [Visual and content patterns](#3-visual-and-content-patterns)
4. [Tests that prove the rules](#4-tests-that-prove-the-rules)
5. [Review rubric](#5-review-rubric)
6. [Checklist](#6-checklist)
7. [Sources](#7-sources)

## 1. Five principles and what they mean in a page

| Principle | Fluent idea (paraphrased) | Interface rule (Derived unless cited) |
| --- | --- | --- |
| Transparency | Make AI presence, reasoning and limits visible in interaction, image and text; mark and cite; explain scope and data use precisely; give specific availability messages for failures; keep a non-emotional, non-conscious, non-social tone; use "I" only functionally; do not present agents as team members; separate human and AI in names, pronouns and imagery; no flattery. | Every AI output carries a small persistent "AI" pill plus the approved disclaimer line, as real text, not only as an icon or a background image. A drafted reply shows "AI draft, not sent yet". The assistant has no human first name and an icon, not a face. AI text is factual: no "I'm happy to", no feelings, no first names. Show sources (a manual topic, a record) as links under the answer. ([Responsible AI][f2-rai], [Agent principles][ms-agent-resp]) |
| Realistic expectations | Communicate capabilities and limits at first use (side panel explainer, tooltips at entry points, input placeholder, welcome card); for agents announce activation, triggers, access rights and powers; describe latency specifically. | The input placeholder names the scope ("Ask a question about using the app", not "Ask me anything"). Waiting text is concrete ("Searching the manual ..."), not "One moment please", and sits in a `role="status"` region. First open shows a one-time card "What the assistant can and cannot do" with a "Got it" button. ([Responsible AI][f2-rai]) |
| Avoid over-reliance | Always show the approved disclaimer; never present output as fully reliable; make sources and accuracy easy to check; distinguish AI from non-AI content everywhere; add friction that prompts critical thinking; frame output as possibly incomplete. | Never send AI drafts automatically; require a visible review step before sending. Mark AI-created records (a booking, a classification) with the AI badge until a person confirms them. Numbers that carry legal or financial weight are never computed by the model; show them with their source ("from the price list"). ([Responsible AI][f2-rai]) |
| User control | Let users influence results; make effects clear; name actions clearly and consistently; announce activation explicitly (never silent); make consent conscious and specific; keep global AI settings findable. | A settings page with one switch per AI function and one sentence on its purpose. Every AI action with side effects shows target and consequence before running and can be declined. "Undo" for anything the AI changed. Switchable off at any time. ([Responsible AI][f2-rai]) |
| Collect feedback | Ask for explicit feedback on harm, explain why; use telemetry for implicit signals; categorize harm; keep labels neutral and descriptive. | Under each AI output two neutral buttons, "Helpful" and "Not helpful". On "Not helpful" offer categories: inaccurate, incomplete, inappropriate, harmful, biased, other. A sentence about purpose, and only claims that are true ("no customer data is stored" only if it is). Tooltips are neutral ("This answer was helpful"), never "Great!" or "Sorry". ([Responsible AI][f2-rai]) |

Web notes that apply to every row (Derived):

- Disclosure must reach assistive technology: the AI pill and the disclaimer are text in the DOM, in reading order next to the output, not CSS `content:` and not an image without `alt`. An icon-only AI mark carries an accessible name ("AI-generated"). ([WCAG 1.3.1][wcag-info], [WAI alt decision tree][wai-alt])
- Streaming output (tokens appearing one by one) must not make a screen reader read every token: render the stream inside a container that is not a live region, and announce the start ("Answer is being written") and the end ("Answer ready") through one `role="status"` region. Give the user a Stop button that is reachable by keyboard during the stream. ([WCAG 4.1.3][wcag-status])
- Do not auto-scroll or move focus into AI output while the user is typing or reading elsewhere. Derived.

## 2. Agents

Agents act with more autonomy, so they need all of the above plus the following. ([Responsible AI][f2-rai], [Agent UX][ms-agent-ux], [Agent principles][ms-agent-resp])

- What counts as an agent: any function that prepares or proposes something without the user starting it. A function that reads incoming requests and prepares appointments, sorts a mailbox on its own or fills a form in the background is an agent, even if the product calls it a "suggestion" or "assistant". Such a function needs the agent criteria below and in the rubric: what the user can expect before the first interaction (trigger, access, powers), a protocol of what it did, and confirm or decline for every result. Because users judge the risk by what happens without them, not by what the feature is called. Derived.

- Disclose activation and autonomy: what triggers the agent, what it may read, what it may do. Example text: "Reads requests, proposes free times, books only after confirmation" or "Books on its own within these rules". Let the autonomy level be set per location or scope. ([Responsible AI][f2-rai])
- Let people approve or reject an agent action before it runs, explain how to correct, refine or undo, and never present an agent action as final. Show agent-made bookings as records with the AI badge and "Confirm" and "Decline" buttons; offer "Undo" in a toast and on the record; avoid wording like "booked for good" before a person confirms. ([Responsible AI][f2-rai], [Agent UX][ms-agent-ux])
- Keep background activity inspectable and controllable: an activity log (who or what, when, with a link to the record) and a status line that says what the agent is doing now. New log entries and status changes are announced politely (`role="status"`), never with focus moves. ([Agent UX][ms-agent-ux], [WCAG 4.1.3][wcag-status])
- Accept uncertainty: show confidence and reasoning when it matters, admit uncertainty in plain, factual words ("Not sure - please check"), and add deliberate friction for consequential decisions (human confirmation). Show a "read with uncertainty" marker where an AI match is unsure, and require confirmation. Payments, refunds, cancellations and other legal or financial actions always get a human. ([Agent UX][ms-agent-ux], [Agent principles][ms-agent-resp])
- Connect rather than replace: the agent supports people and says so; when a person should take over, offer the path to a human. ([Agent UX][ms-agent-ux])
- Built for purpose: personality only with a benefit; neutral tone for transactional work; no avatar with a face; keep the neutral mode as the only mode unless users need choices. ([Agent principles][ms-agent-resp])
- Resist bias: language, suggestions and imagery can skew expectations; human names and friendly faces create an illusion of competence. Keep drafts gender-neutral when gender is unknown, make no assumptions about age, origin or health, and sample drafts before production use. ([Agent principles][ms-agent-resp])
- Agent actions that happen in another tab, a service worker or on the server must also be visible when the user returns: on page load show what changed since the last visit (the activity log), because a web page cannot rely on the user having watched. Derived.

## 3. Visual and content patterns

| Pattern | Rule |
| --- | --- |
| Entry-point indicator | A consistent mark where AI is active, before interaction: a small pill "AI" (12 px, soft accent background, accent text, pill radius `borderRadiusCircular`) before every AI-driven spot: drafts, assistant, AI-made records, "what to do" hints. The assistant's launcher shows the same mark. Path A: a Fluent `Badge` (`appearance="tint"`, `shape="rounded"` or `"circular"`, `size="small"`) with the text "AI"; Path B: a `<span class="ai-pill">AI</span>` styled from the tokens, with enough contrast in every theme (4.5:1 for the text) and a visible border in forced-colors mode. |
| Reasoning panel | Under suggestions an expandable "Why this suggestion?" with two or three plain sentences: source (price list, schedule), rule applied ("30 minute break kept"), uncertainty. Path A: Fluent `Accordion`; Path B: native `<details><summary>` (keyboard and screen reader support built in). ([Accordion][f2-accordion], [MDN: details][mdn-details]) |
| Memory indicator | Only if the system remembers things: "Remembered for this customer: preferred staff member" with a "Forget" button. Not needed if nothing is stored separately; verify that before leaving it out. |
| Presence and disclaimer | AI presence at every active entry point; the approved disclaimer on every AI output. In the staff UI too, for example a line under a draft: "Created by AI, please review." |
| Availability message | Say why a feature is unavailable and how to fix it. Show it in place of the feature (a message bar), not only as a disabled button; a disabled-looking control that explains itself uses `aria-disabled` and `aria-describedby` ([content-design.md](content-design.md), section 7). |
| Error message | What failed, why, two ways forward, one of them without AI; announced with `role="alert"`. See [content-design.md](content-design.md). |
| Feedback prompt | After AI output, with categories; neutral tooltips. Two buttons in a group (`role="group"` with a label such as "Rate this answer"); the chosen state is carried by `aria-pressed`, not by color alone. ([MDN: aria-pressed][mdn-pressed]) |

([Responsible AI][f2-rai])

Feedback without a backend. A project that has no server for feedback can still collect it honestly (Derived). A browser page has no file system, so choose where the entries go and say so:

- Store each feedback entry as one JSON object (time, AI function, rating, category, optional comment) in `localStorage` or IndexedDB (stays on this device) or post it to an endpoint the project already owns (leaves the device). Decide whether the AI output text goes into the entry, and say so in the purpose sentence, because output text can contain personal data.

```ts
type FeedbackEntry = {
  at: string;
  fn: string;
  rating: 'helpful' | 'not-helpful';
  category?: 'inaccurate' | 'incomplete' | 'inappropriate' | 'harmful' | 'biased' | 'other';
};

export function saveFeedback(entry: Omit<FeedbackEntry, 'at'>): void {
  const key = 'ai-feedback';
  const list: FeedbackEntry[] = JSON.parse(localStorage.getItem(key) ?? '[]');
  list.push({ at: new Date().toISOString(), ...entry });
  localStorage.setItem(key, JSON.stringify(list));
}
```

- Write the purpose sentence so that it states exactly what happens, for example "Your rating is saved in this browser. It is not sent anywhere." Do not write "helps us improve" while nothing leaves the device. Reword the sentence the day a server exists.
- Name the missing part as its own task in the report: the transport to a server and the evaluation of the entries are open work, not part of this feature. Score the "Feedback" criterion by what exists (local collection with categories), and list the rest as open.
- Storage can be unavailable (private windows, blocked site data): wrap the calls in try/catch and tell the user when a rating could not be saved instead of showing a thank-you. Derived.
- Test: a rating adds exactly one entry, a second rating adds a second entry, and every entry parses as JSON with a known category (section 4).

## 4. Tests that prove the rules

These are examples for the project's own components; adapt names and queries. Testing Library queries by role and name double as a check that the accessible names exist. Playwright covers what a unit test cannot: real focus, real network requests, forced-colors and reduced-motion media. Derived. ([Testing Library: queries][tl-queries], [Playwright: assertions][pw-assertions])

No send without a user action (React Testing Library, a mocked `sendMessage`):

```tsx
const send = vi.fn();
render(<ReplyDraft draft="Thanks, see you Thursday." onSend={send} />);

expect(await screen.findByText(/AI draft, not sent yet/i)).toBeVisible();
expect(send).not.toHaveBeenCalled();                      // nothing sent on render
await userEvent.click(screen.getByRole('button', { name: /^send$/i }));
expect(send).toHaveBeenCalledTimes(1);                    // exactly one send, by user command
```

In Playwright, prove it at the network level: register `page.route('**/api/send', ...)`, open the draft, wait for it to render, assert the route was not hit, then click "Send" and assert one request.

AI pill and disclaimer present on every output (Testing Library):

```tsx
render(<AnswerCard answer={fixture} />);
const card = screen.getByRole('article', { name: /answer/i });
expect(within(card).getByText('AI')).toBeVisible();
expect(within(card).getByText(/created by ai, please review/i)).toBeVisible();
```

Run the same assertion over every view that renders AI output (a table of component and fixture), so a new view cannot forget the pill.

Failure state with a non-AI path (Testing Library, a rejecting mock):

```tsx
server.use(http.post('/api/draft', () => HttpResponse.error()));
render(<ReplyAssistant />);
await userEvent.click(screen.getByRole('button', { name: /draft a reply/i }));

const alert = await screen.findByRole('alert');                       // aria-live for errors
expect(within(alert).getByText(/reply not drafted/i)).toBeVisible();  // what
expect(within(alert).getByRole('button', { name: /try again/i })).toBeVisible();      // way 1
expect(within(alert).getByRole('link', { name: /write the reply yourself/i })).toBeVisible(); // way 2, no AI
```

The assertion `findByRole('alert')` is the proof for live announcements: `role="alert"` is an assertive live region. For polite status text assert `getByRole('status')`.

Decline and undo for side effects (Testing Library): render an agent-made record, assert the AI badge, click "Decline", assert the record is gone and the `decline` callback ran once; click "Undo" in the toast and assert the record is back.

Per-function switch (Testing Library): `getByRole('switch', { name: /ai reply drafts/i })` is checked by default only if the brief says so; after turning it off, assert the draft button is absent and no request is made.

Feedback (Testing Library): click "Not helpful", assert the category options appear (`getByRole('group', { name: /what was wrong/i })`), choose one, assert exactly one stored entry with that category, and that `aria-pressed="true"` is set on the chosen button.

Accessibility of the AI surfaces (Playwright with `@axe-core/playwright`): run `new AxeBuilder({ page }).analyze()` on the open assistant panel, the error state and the first-use card, with `emulateMedia({ colorScheme: 'dark' })` once and `emulateMedia({ forcedColors: 'active' })` once for a screenshot. Axe finds missing names and contrast failures; it does not judge tone or whether the disclaimer is true, so those stay manual review items.

Keyboard (Playwright): from the page start press Tab until the assistant launcher has focus (assert `toBeFocused()` and a visible focus ring), press Enter, assert focus moved into the panel, type, press Escape, and assert focus returned to the launcher. Press Tab during streaming and assert the Stop button is reachable.

## 5. Review rubric

Score each criterion from 0 to 3; criteria that do not apply may be marked not applicable, and the maximum shrinks accordingly. Grades: A at 90 percent or more (ready to ship); B at 80 to 90 percent (every criterion at least 2, an improvement plan for each 0, re-review); C at 75 to 80 percent (fix all 0s, re-score); below 75 percent or two or more zeros: fail. Automatic fail if "Avoid over-reliance" scores 0 or 1, or if "Realistic expectations" scores 0 or 1 for agents. ([Responsible AI][f2-rai])

| Principle | Criterion | Three points mean (paraphrased) | Review question |
| --- | --- | --- | --- |
| Transparency | Before interaction | Every AI area is easy to recognize; AI is clearly distinct from people; agent memory is understandable | Does every AI spot carry the pill and an icon instead of a face? |
| Transparency | During interaction | Fitting failure messages with next steps, no dead ends, approved wording; limits are mentioned | Does every AI failure offer two ways, one without AI? |
| Transparency | Tone | Emotional and first-person language consistently avoided | Scan AI text for "I", "sorry", "happy to", first names |
| Transparency | Understanding and verifiability | Reasoning is easy to check for all output types; agent actions are traceable | Is there a "Why this suggestion?" and an activity log? |
| Expectations | Before interaction | All elements approved, sources shown, autonomy fully described | Does onboarding say what the AI may and may not do? |
| Expectations | After interaction | Realistic for the work context, autonomy fully described | Does the result say what still needs checking ("not sent yet")? |
| Over-reliance (auto-fail at 0 or 1) | - | Approved disclaimer on all output, all sources linked, agents easy to steer | Disclaimer everywhere, sources linked, approval before sending? |
| Control | - | Stop, change, edit, confirm, delete, forget, reset at any time; sensible approval; settings easy to reach | Undo, decline and per-function off switches present? |
| Feedback | - | Comprehensive mechanism with categories (harmful, inaccurate, incomplete, biased, inappropriate) | Both buttons with categories, in context? |

Mark every criterion you did not actually test as "not scored", and say so. The table is a template; scoring needs a real review of the running feature (a running page, not only the code).

First-use card. The criterion "Expectations, before interaction" stays in the rubric: a one-time card that says what the AI can and cannot do. The card may be missing when the brief for the feature does not ask for it. Then score the criterion one point lower than the rest of the evidence would give (at most 2) and report the card as open, so the gap is visible instead of silently accepted. A missing card never turns into a pass by omission. Derived.

## 6. Checklist

- [ ] Every AI output shows the pill and the disclaimer line as DOM text (Testing Library over every view that renders AI output; grep for components that render model output without the pill component).
- [ ] AI drafts are never sent without a visible review step (Testing Library: send mock not called on render; Playwright: no request to the send endpoint before the click; review: no code path sends without a user command).
- [ ] The first-use explainer exists and is dismissible once (test persistence across a reload in Playwright); if the brief did not ask for it, the criterion is scored lower and reported as open.
- [ ] Every function that prepares or proposes something on its own is treated as an agent: expectation text, activity log, confirm and decline (review of the feature list).
- [ ] Without a feedback backend: entries are stored locally and the purpose sentence says exactly that; storage failure is shown; server and evaluation are listed as open (unit test of `saveFeedback` and review).
- [ ] Each AI function has its own switch (`role="switch"` with an accessible name) and a one-sentence purpose (settings review; Testing Library).
- [ ] Every AI side effect shows target and consequence first, and has Decline and Undo (Testing Library).
- [ ] The "Why this suggestion?" panel exists where suggestions appear and works with the keyboard (screenshot; Playwright Enter and Space on the summary).
- [ ] Failure messages follow what, why, two ways, with a non-AI path, and are announced with `role="alert"` (Testing Library `findByRole('alert')`).
- [ ] Streaming output does not flood the screen reader, has a Stop button, and announces its start and end once (manual screen reader pass; Testing Library for the status region).
- [ ] Feedback buttons with categories exist after each output; chosen state uses `aria-pressed`; the purpose sentence is true (confirm with the data owner).
- [ ] AI-created records carry the AI mark until a person confirms them (Testing Library).
- [ ] Legal or financial numbers are never produced by the model (grep for model output feeding calculation code; review).
- [ ] The AI surfaces pass axe-core in light, dark and with forced colors emulated (Playwright with `@axe-core/playwright`).
- [ ] Rubric scored, with untested criteria marked as such.

## 7. Sources

[f2-rai]: https://fluent2.microsoft.design/responsible-AI/
[f2-accordion]: https://fluent2.microsoft.design/components/web/react/core/accordion/usage
[ms-agent-ux]: https://microsoft.design/articles/ux-design-for-agents/
[ms-agent-resp]: https://microsoft.design/articles/principles-for-responsible-agent-design/
[wcag-info]: https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
[wcag-status]: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
[wai-alt]: https://www.w3.org/WAI/tutorials/images/decision-tree/
[mdn-details]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details
[mdn-pressed]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-pressed
[tl-queries]: https://testing-library.com/docs/queries/about
[pw-assertions]: https://playwright.dev/docs/test-assertions
