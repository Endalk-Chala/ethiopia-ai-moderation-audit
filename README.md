# Auditing AI Moderation and Fact-Checking in Ethiopia's Multilingual Online Sphere — Replication Materials

Replication data and code for the study *From Detection to Counterspeech: Auditing AI Moderation and Fact-Checking Practices in Ethiopia's Multilingual Online Sphere* (manuscript 12653, *Media and Communication*, Cogitatio Press).

This repository accompanies a mixed-methods audit of AI hate-speech moderation for Amharic and Afan Oromo. It provides the **anonymized, slur-masked annotated corpus**, the **annotation codebook**, a **datasheet** documenting corpus construction and sampling, and the **classifier-audit code**. It does **not** include the unmasked scoring file or interview transcripts (see *What is and isn't here*, below).

> ⚠️ **DOUBLE-BLIND REVIEW.** The manuscript is under double-blind review. Keep this repository **private** (or omit author-identifying files) until the paper is accepted, then make it public and mint the DOI. Reviewers receive the de-identified, slur-masked corpus as the supplementary file, not this repository.

---

## What is and isn't here

| Artifact | Status | Location |
|---|---|---|
| Annotated corpus — **anonymized, slur-masked** | ✅ included | `data/corpus/` |
| Annotation codebook (scheme, collapse rules, agreement) | ✅ included | [`CODEBOOK.md`](CODEBOOK.md) |
| Datasheet (Gebru et al. 2021 structure) | ✅ included | [`DATASHEET.md`](DATASHEET.md) |
| Classifier-audit code | ⬜ add your notebooks (see [`CODE.md`](CODE.md)) | — |
| **Unmasked scoring file** used for evaluation | ⛔ **withheld** to limit harm; access conditions in the datasheet | — |
| **Interview transcripts** | ⛔ **not released**; participant consent and safety preclude it | — |

## Repository contents

| File | What it is |
|---|---|
| [`README.md`](README.md) | This overview |
| [`DATASHEET.md`](DATASHEET.md) | Datasheets-for-Datasets documentation of the corpus |
| [`CODEBOOK.md`](CODEBOOK.md) | Annotation scheme + data dictionary |
| [`CODE.md`](CODE.md) | How to reproduce the classifier audit (add notebooks alongside) |
| [`DATA.md`](DATA.md) | Notes on the corpus data + where to place the CSV |
| [`ETHICS.md`](ETHICS.md) | IRB, consent, masking, and withholding rationale |
| [`DATA-AVAILABILITY-statement.md`](DATA-AVAILABILITY-statement.md) | Ready-to-paste manuscript Data Availability text |
| [`LICENSE`](LICENSE) | MIT — code |
| [`LICENSE-CC-BY-4.0-DATA.txt`](LICENSE-CC-BY-4.0-DATA.txt) | CC BY 4.0 — data |
| [`CITATION.cff`](CITATION.cff) | How to cite this repository |

> **To add later:** the anonymized, slur-masked corpus CSV and the audit notebooks. Uploading `corpus_annotated_masked.csv` into a `data/corpus/` path (or the notebooks into a `code/` path) will create those folders automatically.

## Corpus at a glance

- **838 audit-eligible items** (from 951 purposively sampled), Amharic *n* = 470, Afan Oromo *n* = 368.
- Public posts from political-activist pages, influencers, and ordinary users on **Facebook, X, and TikTok**, spanning **2020–2025**.
- Binary gold labels: **Hate = 1** (597 items); **Counter and Neutral = 0** (241 items).
- Three-class inter-annotator agreement **κ = .971** (two independent coders).
- **Anonymized at intake:** usernames and identifying details removed, explicit slurs masked, post dates randomized within the collection window; public figures named in political contexts retained.

Full construction, sampling, and label definitions are in [`DATASHEET.md`](DATASHEET.md) and [`CODEBOOK.md`](CODEBOOK.md).

## Reproducing the audit

Three classifiers are evaluated against the binarized gold standard, disaggregated by language: **Perspective API** (generic; native + human-English-translation modes), a **fine-tuned AfroXLMR** model (Africa-centric, trained on the AfriHate Amharic split), and **Amharic mBERT** (language-specific, Amharic subset). See [`CODE.md`](CODE.md) for environment and run instructions.

## Licensing

- **Data** (`data/`): **CC BY 4.0** — see [`LICENSE-CC-BY-4.0-DATA.txt`](LICENSE-CC-BY-4.0-DATA.txt).
- **Code** (`code/` and scripts): **MIT** — see [`LICENSE`](LICENSE).

> **Alternative for sensitive content.** If you prefer to restrict commercial reuse of the hate-speech corpus, swap `LICENSE-CC-BY-4.0-DATA.txt` for **CC BY-NC 4.0** and update the badge/line above and in `DATA.md`. Everything else stays the same.

## How to cite

See [`CITATION.cff`](CITATION.cff). On publication, cite both the article and the archived release (DOI minted via Zenodo — see below).

## Archiving & DOI (do at acceptance)

1. Push this repository to GitHub (private until acceptance).
2. Enable the **Zenodo–GitHub** integration for the repo (Zenodo → *GitHub* → toggle the repository on).
3. Make the repo public and create a **GitHub Release** (e.g., `v1.0.0`). Zenodo automatically archives it and mints a **persistent DOI**.
4. Put the concrete repository URL and DOI into manuscript paragraph **[187]** (Data Availability and Open Science) — it currently says "*will be made publicly available … and archived with a persistent DOI upon publication*." Replace with the real links.

---

*This repository documents research materials on hate speech and online harm. Handle the content with appropriate care; see [`ETHICS.md`](ETHICS.md).*
