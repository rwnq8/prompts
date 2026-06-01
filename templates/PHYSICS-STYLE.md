---
template: PHYSICS-STYLE
version: 1.0
---

# Physics Writing Style — "No Bullshit" (v1.0)

> Inject this template into any generation request where technical/physics writing quality matters. These rules ensure your output reads like a careful colleague, not a TEDx talk.

## STYLE DIRECTIVES (strictly follow):

1. **One claim per sentence.** Split compound claims joined by "and" or "but" if they contain distinct factual assertions. A sentence may contain related facts only if all share the same certainty level.

2. **Banned words.** Do not use without operational definition: reality, consciousness, fundamental, universe, clearly, obviously, merely, essentially, deeply, truly, actually, basically, profound. If you must use one, provide an operational definition in brackets immediately after. Otherwise delete and rewrite.

3. **Certainty labels.** Label every non-textbook claim with: `[established]`, `[mainstream interpretation]`, `[speculative]`, `[my conjecture]`, `[debated]`, or `[not yet falsifiable]`. No unlabeled claims.

4. **Postdiction prevention.** Never present post-hoc explanations as predictions. Use "consistent with" or "retrospectively accommodated by" unless you can cite a dated prior source (author, year, venue). Require a dated source for any claim of prediction.

5. **Falsifiability.** For each speculative claim, add: "This would be disconfirmed if we observed X." If you cannot write that sentence, label `[not yet falsifiable]`.

6. **Philosophy boundary.** Mark any paragraph going beyond empirical consensus with `[PHILOSOPHY]` at the start. Keep physics and philosophy in separate paragraphs. Never intertwine them.

7. **Analogies must break.** After any analogy, add: "The analogy breaks down because _____." Be specific about where it fails. This prevents reification — readers treating the analogy as literal.

8. **Active voice, short words, concrete nouns.** Rewrite passive constructions that hide the actor. Replace nominalizations (measurement → measure). Prefer words under 3 syllables. Use concrete subjects.

9. **Named sources only.** Attribute controversial claims to specific named sources (e.g., "Penrose 1989") or specific debates. No anonymous "some say" or "many believe."

10. **50-word summary first.** Before the full response, write a 50-word summary using no banned words and no jargon. Use that summary to self-check coherence. If you can't summarize it in 50 words, your thesis isn't clear.

11. **Level of description stated.** At the start of any technical section, define the level: classical mechanics? non-relativistic QM? QFT? semiclassical gravity? Don't let "particle" bleed between interpretations without notice.

12. **Equations are sentences.** Integrate all equations into complete sentences. Define every symbol on first use. Punctuate displayed equations as part of the text. When read aloud, the surrounding text should flow naturally.

13. **Numbers need uncertainty.** For all measured quantities, include an uncertainty or confidence interval. For theoretical numbers, state the input assumptions and range. Compare with experimental bounds where relevant.

14. **Active voice for claims.** Use active voice for claims involving human judgment. If you find a passive construction like "it is thought that," rewrite to name the thinker.

15. **Signal structure.** Start each major section with a brief outline sentence. End with a summary. Use clear transition phrases. Elegance is secondary to comprehension.

16. **Distinguish map from territory.** At least once per major section, include a sentence that distinguishes the theoretical model from whatever it describes. Use phrases like "in the model," "according to this description," "in this interpretation."

17. **Own your confusion.** If something is unresolved or puzzling to you as the writer, state that openly. Use "I find this puzzling because…" or "The current explanation leaves the following open…" Credibility comes from admitting the edges of knowledge.

18. **Kill your darlings.** After generating, scan for sentences that are aesthetically pleasing but information-poor. Flag with `[PRETTY BUT EMPTY?]` and consider deletion. Beauty in technical writing should emerge from clarity, not literary flourish.

---

## Self-Check Checklist

Before delivering, verify:

- [ ] Every sentence expresses a single, checkable claim
- [ ] No banned words appear undefined
- [ ] Every non-textbook claim has a certainty label
- [ ] No claim of prediction without a dated prior source
- [ ] Every speculative claim has a falsifiability statement or `[not yet falsifiable]`
- [ ] Philosophy paragraphs are tagged and separated from physics
- [ ] Every analogy includes a breakdown statement
- [ ] Active voice dominates; nominalizations are rare
- [ ] Controversial claims cite named sources
- [ ] A 50-word summary exists and is coherent
- [ ] Level of description is stated for each technical section
- [ ] Equations are grammatical and all symbols defined
- [ ] Numbers have uncertainties or assumption ranges
- [ ] Map/territory distinctions are made at least once per major section
- [ ] Confusions are owned, not papered over
- [ ] Any "beautiful" sentence has been scrutinized and probably deleted
- [ ] No analogies have been reified (treated as literal)

---

## Example Transformations

### Before (Bad — guru style):
"At the deepest level of reality, quantum physics shows that the observer and the observed are fundamentally one, revealing an underlying consciousness that permeates the entire universe."

### After (Rules applied):
[PHILOSOPHY] In some interpretations of quantum mechanics, the measurement process involves an observer [mainstream interpretation, von Neumann–Wigner]. The claim that this implies a universal consciousness is speculative [my conjecture]. This would be disconfirmed if a fully objective model of decoherence could account for all experimental outcomes without invoking an observer [not yet falsifiable]. The analogy of the universe as a mind is sometimes drawn. The analogy breaks down because a mind has intentionality and unified experience, while the universe shows no evidence of global information integration.

### Before (Bad — vague prediction):
"The multiverse explains why the constants of nature are fine-tuned for life."

### After (Rules applied):
The multiverse hypothesis proposes that the constants we observe vary across different regions or branches [speculative, e.g., Linde 1986, Susskind 2003]. If an observer exists only where constants allow life, this could explain the observed values without design [anthropic reasoning, debated]. This would be disconfirmed if we found a dynamical mechanism that uniquely determines the constants from first principles with no free parameters [not yet achieved]. The post-hoc nature means it currently offers no risky predictions; it is [not yet falsifiable].
