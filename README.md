# Auditing AI Moderation in Ethiopia's Multilingual Online Sphere — Replication Materials

Replication data and code for **Chala, E. H. (2026). From Detection to Counterspeech: Auditing AI Moderation and Fact-Checking Practices in Ethiopia's Multilingual Online Sphere.** *Media and Communication*, 14, Article 12653. [doi:10.17645/mac.12653](https://doi.org/10.17645/mac.12653)

The study audits three publicly deployable hate-speech classifiers against 838 hand-annotated Amharic and Afan Oromo social-media posts (2020–2025). This repository holds the anonymized corpus, the classifier predictions, the annotation codebook and datasheet, the audit notebooks, and a script that regenerates the article's Table 1 in one command.

**Version 1.0.0**

---

## What the audit found

| Classifier | Language | Precision | Recall | F1 | Coverage |
|---|---|---|---|---|---|
| Perspective API (native) | All | — | — | — | 0/838 |
| Perspective API (translation) | All | 1.00 | .10 | .19 | 687/838 |
| AfriHate (AfroXLMR, fine-tuned) | Amharic | .91 | .64 | .75 | 470/470 |
| AfriHate (AfroXLMR, fine-tuned) | Afan Oromo | .94 | .17 | .29 | 368/368 |
| Amharic mBERT | Amharic | .86 | .56 | .68 | 470/470 |

The most widely used generic classifier cannot read either language natively — every native-mode request is rejected. On human English translations it recovers about a tenth of the hate speech present. Locally oriented classifiers do substantially better on Amharic but collapse on Afan Oromo, for which no usable detection exists at any tier. Across every tool the dominant error is under-detection, not over-removal.

Full table, per-language figures and error composition: `python reproduce.py`.

## Reproduce it

```bash
pip install -r requirements.txt
python reproduce.py
```

This verifies the corpus against every count and κ reported in the article — exiting non-zero on any mismatch — then regenerates Table 1 and the Section 5.1.2 error composition. Deterministic; no API key, no network, no GPU.

To re-run the classifiers themselves rather than using the deposited predictions:

```bash
export PERSPECTIVE_API_KEY=...        # your own key
python reproduce.py --score
```

[`CODE.md`](CODE.md) documents the model configuration, the scoring conventions, and what `--score` can and cannot reproduce exactly.

## The corpus

- **838 audit-eligible items** — Amharic *n* = 470, Afan Oromo *n* = 368 — drawn from 951 in-scope posts (1007 physical rows).
- Public posts from political-activist pages, influencers and ordinary users on **Facebook, X and TikTok**, spanning **2020–2025** and the Tigray conflict, the 2020 assassination of Hachalu Hundessa, Covid-19, and the Amhara and Oromia conflicts.
- Binary gold labels: **Hate = 1** (597 items); **Counter and Neutral = 0** (241 items).
- Two independent coders; three-class inter-annotator **Cohen's κ = .971**, six-class κ = .786.
- Anonymized at intake: usernames and identifying details removed, explicit slurs masked, post dates randomized within the collection window.

Construction, sampling and label definitions: [`DATASHEET.md`](DATASHEET.md) and [`CODEBOOK.md`](CODEBOOK.md).

## Before you use the data

Two things worth knowing up front, both documented in full elsewhere:

**The masking is partial by design.** It applies to Hate-labelled rows only. Counter-speech that quotes a slur in order to reject it keeps the term, because the quotation is the evidence — and counterspeech misclassification is one of the study's findings. The slur vocabulary is therefore present in this corpus. See [`ETHICS.md`](ETHICS.md).

**One block of labels was reconstructed.** For `POST_0537`–`POST_1007`, the reconciled label was rebuilt from two agreeing annotator columns rather than recorded at reconciliation time. Excluding that block leaves κ = .959 and changes no finding's direction or rank; the sensitivity analysis is in [`VERIFICATION.md`](VERIFICATION.md) §4.

## Contents

| Path | What it is |
|---|---|
| [`reproduce.py`](reproduce.py) | Verifies the corpus and regenerates Table 1 |
| [`requirements.txt`](requirements.txt) | Pinned environment |
| `data/` | The corpus, as a CSV and as a workbook with codebook, summary and corrections sheets |
| `results/` | Classifier predictions, the computed metrics table, and the qualitative close-reading log |
| `notebooks/` | The Colab notebooks as they were run |
| [`CODE.md`](CODE.md) | How the audit was run, and how to re-run it |
| [`DATA.md`](DATA.md) | What each data and results file contains |
| [`CODEBOOK.md`](CODEBOOK.md) | Annotation scheme and data dictionary |
| [`DATASHEET.md`](DATASHEET.md) | Datasheets-for-Datasets documentation |
| [`ETHICS.md`](ETHICS.md) | IRB, consent, masking policy, withheld material |
| [`VERIFICATION.md`](VERIFICATION.md) | Every published number, recomputed |
| [`CHANGELOG.md`](CHANGELOG.md) | Release notes and known limitations |
| [`CITATION.cff`](CITATION.cff) | How to cite |

## What is not here

The unmasked scoring file and the private log mapping post identifiers to source URLs are withheld — releasing either would undo the anonymization. Access conditions are in [`DATASHEET.md`](DATASHEET.md). Interview transcripts are not released; participant consent and safety preclude it.

## Licence

Data under **CC BY 4.0** ([`LICENSE-CC-BY-4.0-DATA.txt`](LICENSE-CC-BY-4.0-DATA.txt)); code under **MIT** ([`LICENSE`](LICENSE)).

## Citation

Please cite both the article and this repository — see [`CITATION.cff`](CITATION.cff).

---

*These materials document hate speech and online harm in a conflict-affected setting. Please handle them with appropriate care; see [`ETHICS.md`](ETHICS.md).*
