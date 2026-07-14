# Annotation Codebook & Data Dictionary

This documents the annotation scheme and the fields of the released corpus. All counts and inter-annotator agreement figures below are the values used in the study.

---

## 1. Corpus composition

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

## 3. Inter-annotator agreement

Protocol target: **Cohen's κ ≥ 0.70** (met for both languages, both schemes).

| Scheme | Overall | Amharic | Afan Oromo |
|---|---|---|---|
| **Six-class** Cohen's κ | **0.786** (n=951) | 0.802 (n=530) | 0.766 (n=421) |
| **Three-class** Cohen's κ *(excl. Misinfo/Ambiguous)* | **0.971** (n=783) | 0.955 (n=442) | 0.993 (n=341) |
| Six-class exact agreement | 87.4% | — | — |

> The headline **three-class κ = .971** is the three-class overall value (n = 783); it excludes rows where either annotator chose Misinformation or Ambiguous.

## 4. Enforcement operationalization (for the audit)

- **Under-enforcement** = false negatives on **Hate** items.
- **Over-enforcement** = false positives on **Counter** or **Neutral** items.

## 5. Anonymization applied

- **Explicit slurs masked** with placeholders **`[SLUR_OROMO]`, `[SLUR_AMHARA]`, `[SLUR_TIGRAY]`**; usernames, profile URLs, and identifying details within text removed at data entry.
- **Dates randomized** uniformly within the collection window **2020-01-01 to 2025-03-31**, fixed **seed = 42**, for both `Date` and `YearMonth` (preserves temporal distribution, prevents timestamp re-identification).
- A private source log mapping `PostID` → original URLs is **not distributed**.
- Explicit slurs in the released corpus are replaced with the placeholder tokens above.

## 6. Data dictionary

The corpus columns are listed below. The **In released corpus** column indicates which fields appear in the public, anonymized CSV.

| Column | Description | In released corpus |
|---|---|---|
| `PostID` | Anonymous sequential ID (`POST_0001`…`POST_1007`; non-contiguous after removals). | Yes |
| `Language` | `Amharic` or `Afan Oromo`. | Yes |
| `YearMonth` | Collection month/year (from randomized date). | Yes |
| `Date` | Full (randomized) datetime. | No — only `YearMonth` is released |
| `OriginalText` | Original-language text, **slur-masked**. | Yes |
| `EnglishTranslation` | Researcher-produced English gloss (used for Perspective translation mode; present for all 838 eligible rows). | Yes |
| `Annotator1` | First annotator's six-class label. | Yes |
| `Annotator2` | Second annotator's six-class label. | Yes |
| `FineLabel` | Reconciled six-class label. | Yes |
| `Label3Class` | Three-class audit label (blank if excluded). | Yes |
| `Target` / `TargetPrimary` / `TargetSecondary` | Target-domain string(s), e.g. "Ethnicity/Politics". | Yes |
| `IncludeInAudit` | Boolean; `True` = valid `Label3Class` used for P/R/F1. | Yes |
| `Notes` | Free-text annotator notes / contextual-dependency flags. | optional |
| `Link` | Source URL. | No — re-identifying |
| `AI_Draft_Analysis` | AI decision-support (label suggestion, term/discursive features). **Not ground truth.** | No |

**Withheld:** the private scoring file (with `Link`/source log) is not redistributed. Access conditions are described in the datasheet.

## 7. Classifiers evaluated

| Tier | Model (checkpoint) | Notes |
|---|---|---|
| Generic | **Perspective API** (`TOXICITY`) | Native mode (`am` for Amharic; auto-detect for Afan Oromo) **and** forced-English on the `EnglishTranslation`; hate = score ≥ 0.5. |
| Africa-centric | **AfroXLMR** — `Davlan/afro-xlmr-base-hate-v1` | Africa-centric hate classifier. |
| Language-specific | **Amharic mBERT** — `amengemeda/amharic-hate-speech-detection-mBERT` | Amharic subset only. |

