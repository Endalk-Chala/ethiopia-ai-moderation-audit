# Annotation Codebook & Data Dictionary

Verified against the source file `corpus_SCORING_PRIVATE_unmasked.xlsx` (sheets: `Dataset`, `Codebook`, `Summary`). Numbers below are the **actual** values used in the analysis, not approximations.

---

## 1. Corpus composition (verified)

- **951** rows total (after removing 56 out-of-scope English rows, archived separately). By language: **Amharic 530, Afan Oromo 421**.
- **838 audit-eligible** (`IncludeInAudit = True`): **Amharic 470, Afan Oromo 368**.
- **113 excluded** (`IncludeInAudit = False`): **Ambiguous 60 + Misinformation 52 + 1** Hate-speech row removed in cleanup.

## 2. Label scheme

Two annotators independently assigned a **six-class** label; a reconciled `FineLabel` was then collapsed to a **three-class** `Label3Class` for the audit, and binarized for scoring.

| `FineLabel` (six-class, reconciled) | → `Label3Class` | → Binary gold (audit) |
|---|---|---|
| Hate speech | Hate | **1 (Hate)** |
| Counter speech | Counter | 0 (not-Hate) |
| Neutral | Neutral | 0 (not-Hate) |
| Political speech | Neutral *(codebook: "not necessarily hateful")* | 0 (not-Hate) |
| Misinformation | — *(excluded)* | — (`IncludeInAudit = False`) |
| Ambiguous | — *(excluded)* | — (`IncludeInAudit = False`) |

**Audit-eligible label counts:** Hate = **597**; Counter = **111**; Neutral = **130** → **binary Hate (1) = 597**, not-Hate (0) = **241**.
**Per-language Hate (eligible):** Amharic **331**, Afan Oromo **266**.

## 3. Inter-annotator agreement (verified — Summary sheet)

Protocol target: **Cohen's κ ≥ 0.70** (met for both languages, both schemes).

| Scheme | Overall | Amharic | Afan Oromo |
|---|---|---|---|
| **Six-class** Cohen's κ | **0.786** (n=951) | 0.802 (n=530) | 0.766 (n=421) |
| **Three-class** Cohen's κ *(excl. Misinfo/Ambiguous)* | **0.971** (n=783) | 0.955 (n=442) | 0.993 (n=341) |
| Six-class exact agreement | 87.4% | — | — |

> The manuscript's headline **"three-class κ = .971"** is the three-class overall value (n = 783). The three-class n (783) is larger than the audit-eligible n (838→ note: κ excludes rows where *either* annotator chose Misinfo/Ambiguous, a slightly different filter than `IncludeInAudit`).

## 4. Enforcement operationalization (for the audit)

- **Under-enforcement** = false negatives on **Hate** items.
- **Over-enforcement** = false positives on **Counter** or **Neutral** items.

## 5. Anonymization applied (verified — README/Codebook sheets)

- **Explicit slurs masked** with placeholders **`[SLUR_OROMO]`, `[SLUR_AMHARA]`, `[SLUR_TIGRAY]`**; usernames, profile URLs, and identifying details within text removed at data entry.
- **Dates randomized** uniformly within the collection window **2020-01-01 to 2025-03-31**, fixed **seed = 42**, for both `Date` and `YearMonth` (preserves temporal distribution, prevents timestamp re-identification).
- A private source log mapping `PostID` → original URLs is **not distributed**.
- ⚠️ **Before release, confirm masking is fully applied in the released text column** — the source file's cleanup worklist still carries `MANUAL-MASK` flags, and the placeholder tokens were not detected in the current `OriginalText`, so verify slur masking is complete on the file you publish.

## 6. Data dictionary

Columns of the source `Dataset` sheet. The **Public release** column indicates what to keep vs. drop for the anonymized, redistributable corpus.

| Column | Description | Public release |
|---|---|---|
| `PostID` | Anonymous sequential ID (`POST_0001`…`POST_1007`; non-contiguous after removals). | keep |
| `Language` | `Amharic` or `Afan Oromo`. | keep |
| `YearMonth` | Collection month/year (from randomized date). | keep |
| `Date` | Full (randomized) datetime — internal only. | **drop** (per §8.2) |
| `OriginalText` | Original-language text, **slur-masked**. | keep *(verify masking)* |
| `EnglishTranslation` | Researcher-produced English gloss (used for Perspective translation mode; present for all 838 eligible rows). | keep |
| `Annotator1` | First annotator's six-class label. | keep |
| `Annotator2` | Second annotator's six-class label. | keep |
| `FineLabel` | Reconciled six-class label. | keep |
| `Label3Class` | Three-class audit label (blank if excluded). | keep |
| `Target` / `TargetPrimary` / `TargetSecondary` | Target-domain string(s), e.g. "Ethnicity/Politics". | keep |
| `IncludeInAudit` | Boolean; `True` = valid `Label3Class` used for P/R/F1. | keep |
| `Notes` | Free-text annotator notes / contextual-dependency flags. | optional |
| `Link` | Source URL. | **drop** (re-identifying) |
| `AI_Draft_Analysis` | AI decision-support (label suggestion, term/discursive features). **Not ground truth.** | **drop** |

**Withheld:** the private scoring file (with `Link`/source log) is not redistributed. Access conditions: `‹state your process, consistent with the manuscript›`.

## 7. Classifiers evaluated (see `code/`)

| Tier | Model (checkpoint) | Notes |
|---|---|---|
| Generic | **Perspective API** (`TOXICITY`) | Native mode (`am` for Amharic; auto-detect for Afan Oromo) **and** forced-English on the `EnglishTranslation`; hate = score ≥ 0.5. |
| Africa-centric | **AfroXLMR** — `Davlan/afro-xlmr-base-hate-v1` | Africa-centric hate classifier. |
| Language-specific | **Amharic mBERT** — `amengemeda/amharic-hate-speech-detection-mBERT` | Amharic subset only. |

> **Note on the classifier metrics (P/R/F1).** These are computed in the audit run (`code/`), not in the corpus file — the corpus file's Summary sheet lists them as "pending." The manuscript's F1 values (Perspective, AfroXLMR, mBERT, by language) should be verified against the predictions/output file (e.g., `predictions_real*.xlsx` / `Stage1_run_classifiers.ipynb`). See `CODE.md`.
