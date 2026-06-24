# Conversation Writing Cleanup Rules

Use these rules when manually cleaning a generated conversation page after Phase 1.

The goal is readability and accessibility. Do not turn the conversation into a new article. Do not add new ideas, examples, claims, or transitions that were not already present.

## Core Rule

Preserve meaning.

You may remove obvious speech artifacts, fix obvious transcription errors, and add paragraph breaks. You should not improve the argument, make Kyle sound more polished than he was, or rewrite the conversation into a different voice.

## Safe Things to Remove

Remove filler words when they do not carry meaning:

- `well`
- `you know`
- `I mean`
- `like` when it is only filler
- `sort of` when it is only filler
- `kind of` when it is only filler
- duplicated sentence starts

Examples:

- `Well, I think...` -> `I think...`
- `The, the market...` -> `The market...`
- `It's and it's a structural trap.` -> `It's a structural trap.`

Keep filler words if they change tone, uncertainty, or meaning.

Example:

- `I would say by and large` can stay because it communicates qualification.

## Repeated Words and False Starts

Clean obvious speech-to-text repetitions:

- `the, the`
- `if we're, if we're`
- `very, very, very, very` may become `very` or `very, very` depending on emphasis
- restarted clauses where only the second version works

Do not remove repetition if the repetition is rhetorical emphasis.

If unsure whether repetition is a speech artifact or emphasis, ask Kyle.

## Punctuation Cleanup

Fix punctuation that is clearly wrong:

- Remove question marks that are obviously not questions.
- Split run-on sentences when punctuation clearly collapsed.
- Fix capitalization caused by transcription, such as `So It's Difficult` -> `So it's difficult`.
- Fix obvious missing commas when they improve readability without changing meaning.

Examples:

- `If we're simply talking about retail?` -> `If we're simply talking about retail,`
- `but For end users` -> `but for end users`

Do not add dramatic punctuation, rhetorical emphasis, or editorial framing.

## Obvious Transcription Errors

Fix clear transcription mistakes only when the intended phrase is obvious from context.

Examples:

- `or a 1K` -> `401(k)`
- `line go up` can remain if it is an intentional phrase
- `F M See. Key provider.` should not be guessed without context

If the intended phrase is not obvious, ask Kyle.

## Paragraph Breaks

Add paragraph breaks at natural thought shifts.

Good places to split:

- A new example begins.
- The speaker moves from setup to implication.
- The speaker shifts from one market, audience, or technology to another.
- A caveat begins.
- A conclusion begins after several supporting details.
- A long paragraph contains more than one major idea.

Do not reorder paragraphs.

Do not add section headings inside a speaker turn unless Kyle asks for them.

Paragraph breaks are formatting, not rewriting. The words should remain the same unless another cleanup rule applies.

## Links

Links may be added when they clarify an existing reference.

Allowed:

- Link `earlier crypto work` to an existing relevant page.
- Link named public projects, reports, or case studies if the link target already exists and is clearly relevant.

Not allowed:

- Add links that imply a claim Kyle did not make.
- Add links to make the transcript feel more researched.
- Add external links for every concept.

## What Not to Do

Do not:

- Add new arguments.
- Add new examples.
- Add new claims.
- Add transitions that change the flow.
- Convert answers into essay prose.
- Make Kyle sound more certain than he was.
- Remove caveats just because they are messy.
- Change terminology unless it is an obvious transcription error.
- Smooth over ambiguity when the ambiguity is part of the thought.

## When to Ask Kyle

Ask Kyle before changing anything when:

- The intended word or phrase is unclear.
- A sentence could be cleaned in more than one way.
- A repeated phrase might be intentional emphasis.
- A correction would require domain knowledge.
- The cleanup would remove a caveat or qualification.
- You are tempted to add a sentence.
- You are tempted to summarize a long answer instead of preserving it.
- A paragraph seems incoherent but the fix is not obvious.
- You need to decide whether a link is relevant enough to add.
- The transcript references a private, confidential, or sensitive topic.

## Good Cleanup Standard

After cleanup, the transcript should feel like a lightly edited interview:

- readable
- faithful
- still conversational
- easier for humans and bots to parse
- not rewritten into generic thought leadership

If the cleanup would make the transcript sound like a different document, stop and ask Kyle.
