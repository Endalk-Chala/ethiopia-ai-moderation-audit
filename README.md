# Auditing AI Moderation and Fact-Checking in Ethiopia's Multilingual Online Sphere — Replication Materials

Replication data and code for the study *From Detection to Counterspeech: Auditing AI Moderation and Fact-Checking Practices in Ethiopia's Multilingual Online Sphere* (*Media and Communication*).

This repository accompanies a mixed-methods audit of AI hate-speech moderation for Amharic and Afan Oromo. It provides the anonymized, slur-masked annotated corpus, the annotation codebook, a datasheet documenting corpus construction and sampling, and the classifier-audit code. It does not include the unmasked scoring file or interview transcripts (see *What is and isn't here*, below).

---

## What is and isn't here

| Artifact | Status | Location |
|---|---|---|
| Annotated corpus — anonymized, slur-masked | included | `data/corpus/` |
| Annotation codebook (scheme, collapse rules, agreement) | included | [`CODEBOOK.md`](CODEBOOK.md) |
| Datasheet (Gebru et al. 2021 structure) | included | [`DATASHEET.md`](DATASHEET.md) |
| Classifier-audit code | included | [`CODE.md`](CODE.md) |
| Unmasked scoring file used for evaluation | withheld to limit harm; access conditions in the datasheet | — |
| Interview transcripts | not released; participant consent and safety preclude it | — |

## Repository contents

| File | What it is |
|---|---|
| [`README.md`](README.md) | This overview |
| [`DATASHEET.md`](DATASHEET.md) | Datasheets-for-Datasets documentation of the corpus |
| [`CODEBOOK.md`](CODEBOOK.md) | Annotation scheme and data dictionary |
| [`CODE.md`](CODE.md) | How to reproduce the classifier audit |
| [`DATA.md`](DATA.md) | Notes on the corpus data |
| [`ETHICS.md`](ETHICS.md) | IRB, consent, masking, and withholding rationale |
| [`LICENSE`](LICENSE) | MIT — code |
| [`LICENSE-CC-BY-4.0-DATA.txt`](LICENSE-CC-BY-4.0-DATA.txt) | CC BY 4.0 — data |
| [`CITATION.cff`](CITATION.cff) | How to cite this repository |

## Corpus at a glance

- **838 audit-eligible items** (from 951 purposively sampled), Amharic *n* = 470, Afan Oromo *n* = 368.
- Public posts from political-activist pages, influencers, and ordinary users on **Facebook, X, and TikTok**, spanning **2020–2025**.
- Binary gold labels: **Hate = 1** (597 items); **Counter and Neutral = 0** (241 items).
- Three-class inter-annotator agreement **Cohen's κ = .971** (two independent coders).
- Anonymized at intake: usernames and identifying details removed, explicit slurs masked, post dates randomized within the collection window; public figures named in political contexts retained.

Full construction, sampling, and label definitions are in [`DATASHEET.md`](DATASHEET.md) and [`CODEBOOK.md`](CODEBOOK.md).

## Reproducing the audit

Three classifiers are evaluated against the binarized gold standard, disaggregated by language: **Perspective API** (generic; native and human-English-translation modes), a **fine-tuned AfroXLMR** model (Africa-centric, trained on the AfriHate Amharic split), and **Amharic mBERT** (language-specific, Amharic subset). See [`CODE.md`](CODE.md) for environment and run instructions.

## Licensing

- **Data** (`data/`): **CC BY 4.0** — see [`LICENSE-CC-BY-4.0-DATA.txt`](LICENSE-CC-BY-4.0-DATA.txt).
- **Code**: **MIT** — see [`LICENSE`](LICENSE).

## How to cite

See [`CITATION.cff`](CITATION.cff). Please cite both the article and this repository.

---

*This repository documents research materials on hate speech and online harm. Please handle the content with appropriate care; see [`ETHICS.md`](ETHICS.md).*
