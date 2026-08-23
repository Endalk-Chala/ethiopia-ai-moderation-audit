# Changelog

## [1.0.0] — 2026-08-23

First public release of the replication materials for *From Detection to Counterspeech: Auditing AI Moderation and Fact-Checking Practices in Ethiopia's Multilingual Online Sphere* (*Media and Communication*, 2026, Vol. 14, Article 12653).

Contains the anonymized annotated corpus (838 audit-eligible items), the classifier predictions, the annotation codebook and datasheet, the audit notebooks, and `reproduce.py`, which verifies the corpus against every figure reported in the article and regenerates Table 1.

### Prepared for release

The working files used during the study were cleaned before deposit. None of the changes below alters a published result — `reproduce.py` verifies this on every run.

**Data corrections.** Several fields in the working corpus had drifted out of agreement with the codebook and with the rows the audit actually scored:

- `Label3Class` reconciled with the adjudicated `FineLabel` for three rows where the collapse had not been reapplied (`POST_0002`, `POST_0025`, `POST_0511`). In each case the corrected value is the one the audit scored.
- Trailing whitespace stripped from label values and from the `Link` column header.
- `IncludeInAudit` reconciled with the 838 rows the audit scored: two Ambiguous rows had been flagged for inclusion, one Hate-speech row excluded, and the 56 out-of-scope English rows had never been unflagged. `IncludeInAudit == True` now returns exactly the audited set.
- `ExclusionReason` column added, so the path from 1007 physical rows to 838 audit-eligible rows reconciles row by row.
- `FineLabel` populated for 471 rows where the reconciled column had been left blank; see *Known limitations* below.
- The `Summary` sheet, which had been superseded by later annotation, recomputed from the corrected `Dataset` tab.
- `POST_1005`, excluded in cleanup as incoherent, no longer carries an audit label.

Every change is logged row by row, with its justification, on the `Corrections` sheet of the corpus workbook.

**Anonymization completed.** The intake masking had been applied unevenly:

- Masking extended to two further ethnic slurs that had never been masked, so the corpus no longer masks the slur against one group while leaving the slur against another in the clear.
- Masking extended to the `EnglishTranslation` column, to inflected Amharic forms, and to Latin-script transliterations. A masked row is now masked in both languages.
- Two profile URLs that survived intake masking are replaced with `[PROFILE_URL_REMOVED]`.
- `POST_0590`, a targeted-harassment post, has its named individual and two vehicle plate numbers replaced with `[NAME_REMOVED]` and `[PLATE_REMOVED]`, in every file.
- The source `Link`, the full randomized `Date`, and the `AI_Draft_Analysis` cleaning notes are removed from every released file — the codebook marks all three as withheld.
- The slur variant list and the substitution mapping are withheld from every sheet and every document.

**Code and reproducibility.**

- `reproduce.py` added: verifies the corpus against the published figures and exits non-zero on any mismatch, then regenerates Table 1 and the Section 5.1.2 error composition. `--score` re-runs the classifiers.
- `requirements.txt` added, with notes on what is and is not exactly reproducible.
- API keys in the notebooks replaced with placeholders; the original credentials revoked. Notebook outputs masked to match the released corpus, and Colab account identifiers removed.

### Known limitations

**Reconciled labels for one block of rows.** For `POST_0537`–`POST_1007`, the reconciled `FineLabel` was reconstructed from two agreeing annotator columns rather than recorded at reconciliation time. These rows supply 416 of the 597 gold Hate items, and because both coders agree throughout the block, it raises the agreement statistics.

The article's conclusions do not depend on it. Excluding the block entirely leaves three-class κ = .959 and six-class κ = .720, both above the protocol target, and preserves the direction and ranking of every classifier result: Perspective remains the weakest, Afan Oromo the least served, under-detection the dominant error mode.

**Masking is partial by design.** It applies to Hate-labelled rows only. Counter-speech that quotes a slur in order to reject it retains the term, because the quotation is the evidence the row documents. The slur vocabulary is therefore present in the corpus, and the masking limits its gratuitous reproduction rather than putting it out of reach. See [`ETHICS.md`](ETHICS.md).

**Released text differs slightly from scored text.** The classifiers ran before the masking was extended. For the rows affected, the released text substitutes a placeholder for a term that was present when the row was scored. The published metrics are unaffected — they are recomputed from the stored predictions, not by re-scoring — but `--score` on the released corpus will differ marginally on those rows.
