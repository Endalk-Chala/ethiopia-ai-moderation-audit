# Datasheet — Amharic & Afan Oromo Hate-Speech Audit Corpus

Following the *Datasheets for Datasets* framework (Gebru et al., 2021). This documents the **anonymized, slur-masked** corpus released in this repository. Statistics are drawn from the accompanying study (manuscript 12653, *Media and Communication*).

---

## Motivation

- **For what purpose was the dataset created?** To evaluate how publicly deployable AI hate-speech classifiers perform on real-world Amharic and Afan Oromo social-media content drawn from outside their training distributions, and to characterize their error patterns (under- vs. over-enforcement). It supports an external algorithmic audit of moderation infrastructure in a low-resource, conflict-affected setting.
- **Who created it and for whom?** Created by the study author(s) for scholarly research. *(Author/affiliation withheld here for double-blind review; restore in `CITATION.cff` on acceptance.)*
- **Funding.** *(State any funding sources here, or "No external funding," consistent with the manuscript's Funding statement.)*

## Composition

- **What do the instances represent?** Individual public social-media **posts** (text) in Amharic or Afan Oromo, each with a human annotation label.
- **How many instances?** **951** items total (after removing 56 out-of-scope English rows, archived separately; by language, Amharic 530 / Afan Oromo 421). After annotation and exclusion of Misinformation/Ambiguous cases, **838** are audit-eligible: **Amharic *n* = 470**, **Afan Oromo *n* = 368**. The **113 excluded** rows comprise **Ambiguous 60 + Misinformation 52 + 1** cleanup-removed Hate row.
- **Label scheme.** Annotators used a **six-class** scheme (Hate speech, Counter speech, Political speech, Misinformation, Neutral, Ambiguous), reconciled into `FineLabel`, then collapsed to a three-class `Label3Class` (Political speech → Neutral; Misinformation/Ambiguous → excluded) and binarized for the audit. See [`CODEBOOK.md`](CODEBOOK.md) §2.
- **Label distribution (binarized gold standard).** **Hate = 1: 597** items; **Counter and Neutral = 0: 241** items. Per-language Hate: Amharic 331, Afan Oromo 266.
- **What data does each instance consist of?** Post text (anonymized, slur-masked), language, and gold label(s). See [`CODEBOOK.md`](CODEBOOK.md) for the exact field schema.
- **Is any information missing?** Yes, by design: usernames and identifying details are removed; explicit slurs are masked; the **unmasked scoring file** used for classifier evaluation is **withheld**; per-row platform-origin and content-type are **not** documented (the audit is language-level, not platform- or content-type-level).
- **Are there labels or a target?** Yes — a hate/not-hate gold label per item (collapsed from a three-class scheme; see codebook).
- **Sensitive content.** The corpus contains hate speech and related harmful language, in masked form. It concerns real political events and, in some cases, public figures named in political contexts (retained as matters of public record). Handle accordingly.

## Collection process

- **How was the data collected?** Real social-media content collected by the researcher from **public Facebook pages, X accounts, and TikTok video accounts** in Amharic and Afan Oromo.
- **Time frame.** Posts span **2020–2025** (collection window 2020-01-01 to 2025-03-31). The corpus spans major Ethiopian political events: the **Tigray conflict**, the **2020 assassination of Hachalu Hundessa**, **COVID-19**, and the **Amhara and Oromia conflicts**.
- **Sampling strategy.** Purposive (not probability) sampling, constructed for analytic range across languages and events rather than statistical representativeness. Platform- and content-type-level disaggregation are out of scope (the dataset was assembled over several years before the research question was formalized; retrospective per-row provenance tagging was not feasible).
- **Who collected/annotated it?** **Two coders** independently annotated each item (six-class scheme); labels were reconciled into `FineLabel`. *(Add annotator background/training as available.)*

## Preprocessing / cleaning / labeling

- **Annotation scheme.** Six-class reconciled `FineLabel` → three-class `Label3Class` → binary (**Hate = 1**; **Counter and Neutral = 0**). Full scheme and collapse rules in [`CODEBOOK.md`](CODEBOOK.md).
- **Inter-annotator agreement (Cohen's κ).** Three-class overall **κ = .971** (n=783; Amharic .955, Afan Oromo .993). Six-class overall **κ = .786** (n=951; Amharic .802, Afan Oromo .766). Six-class exact agreement 87.4%. Protocol target κ ≥ .70 (met).
- **Anonymization (applied at intake).** Usernames, profile URLs, and identifying details removed; **explicit slurs masked** with `[SLUR_OROMO]`/`[SLUR_AMHARA]`/`[SLUR_TIGRAY]`; **post dates randomized** uniformly within 2020-01-01…2025-03-31 (fixed **seed = 42**). Public figures named in political contexts retained. A private `PostID` → URL source log is not distributed.
- **Was raw data saved?** The private scoring file (with source URLs) exists but is **withheld** (see Distribution). ⚠️ Verify slur masking is fully applied on the released text before publishing (cleanup worklist still carries `MANUAL-MASK` flags).

## Uses

- **What has the dataset been used for?** Auditing three classifiers — **Perspective API** (generic), a **fine-tuned AfroXLMR** model (Africa-centric, trained on the AfriHate Amharic split), and **Amharic mBERT** — using precision, recall, and F1 against the binarized gold standard, disaggregated by language. See the manuscript's Results and [`code/`](code/).
- **What (other) tasks could it be used for?** Low-resource hate-speech detection benchmarking; error analysis; counterspeech-misclassification studies.
- **Are there tasks for which it should *not* be used?** It should **not** be used to train or deploy production moderation systems as-is, to deanonymize users, or to generate harmful content. It is language-level and not representative of platform-wide base rates.

## Distribution

- **How is it distributed?** Publicly, in **anonymized, slur-masked** form, via this repository, archived with a persistent DOI on publication.
- **What is withheld and why?** The **unmasked scoring file** is withheld to limit potential harm (access conditions described here / on request per the manuscript). **Interview transcripts** are **not released** because participant consent and safety preclude it.
- **License.** Data under **CC BY 4.0** (see [`LICENSE-CC-BY-4.0-DATA.txt`](LICENSE-CC-BY-4.0-DATA.txt)); code under **MIT** (see [`LICENSE`](LICENSE)).

## Maintenance

- **Who maintains it?** *(Corresponding author — restore contact/ORCID in `CITATION.cff` on acceptance.)*
- **Versioning & DOI.** Each GitHub release is archived by Zenodo with a version DOI plus a concept DOI for the latest version.
- **How can others contribute or report issues?** Via the repository's issue tracker after public release.

---

*Reference:* Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM, 64*(12), 86–92. https://doi.org/10.1145/3458723
