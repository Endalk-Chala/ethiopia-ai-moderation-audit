# Verification report

Every quantitative claim in *"From Detection to Counterspeech: Auditing AI Moderation and Fact-Checking Practices in Ethiopia's Multilingual Online Sphere"* (*Media and Communication*, 2026, Vol. 14, Article 12653), recomputed from the deposited files.

**Result: no discrepancy.** Every count, κ, precision, recall, F1, coverage figure and error percentage in the article reproduces from the data in this repository.

Run `python reproduce.py` to regenerate everything below. Metrics are computed with scikit-learn from `results/predictions_full.csv`, over rows a classifier actually scored, with gold = `Label3Class == 'Hate'`.

## 1. Corpus and gold standard

| Article | Recomputed | |
|---|---|---|
| 951 Amharic + Afan Oromo posts sampled | 1007 rows − 56 English = 951 | ✅ |
| 838 audit-eligible | 838 rows with `IncludeInAudit == True` | ✅ |
| Amharic *n* = 470; Afan Oromo *n* = 368 | 470 / 368 | ✅ |
| 597 Hate, 241 not-Hate | 597 Hate; 130 Neutral + 111 Counter = 241 | ✅ |
| Amharic Hate = 331; Afan Oromo Hate = 266 | 331 / 266 | ✅ |
| Three-class κ = .971 | .971 (n = 783) | ✅ |
| Six-class κ = .786 | .786 (n = 951) | ✅ |

## 2. Table 1 — binary detection performance

Article values are rounded to two decimals; recomputed values to three.

| Classifier | Language | Article P / R / F1 | Recomputed P / R / F1 | Coverage | |
|---|---|---|---|---|---|
| Perspective (native) | All | — | — | 0/838, all requests rejected | ✅ |
| Perspective (translation) | All | 1.00 / .10 / .19 | 1.000 / .104 / .188 | 687/838 | ✅ |
| Perspective (translation) | Amharic | 1.00 / .11 / .20 | 1.000 / .113 / .203 | 409/470 | ✅ |
| Perspective (translation) | Afan Oromo | 1.00 / .09 / .16 | 1.000 / .090 / .164 | 278/368 | ✅ |
| AfriHate (AfroXLMR) | All | .92 / .43 / .59 | .918 / .430 / .586 | 838/838 | ✅ |
| AfriHate (AfroXLMR) | Amharic | .91 / .64 / .75 | .914 / .640 / .753 | 470/470 | ✅ |
| AfriHate (AfroXLMR) | Afan Oromo | .94 / .17 / .29 | .938 / .169 / .287 | 368/368 | ✅ |
| Amharic mBERT | Amharic | .86 / .56 / .68 | .864 / .556 / .676 | 470/470 | ✅ |
| Amharic mBERT | Afan Oromo | — | — | 0/368 | ✅ |

Native-mode rejection is evidenced in `notebooks/01_run_classifiers.ipynb`: HTTP 400 `LANGUAGE_NOT_SUPPORTED_BY_ATTRIBUTE` for Amharic (`am`, both explicitly requested and auto-detected) and for Afan Oromo (auto-detected).

AfroXLMR fine-tuning validation macro-F1 = .72 in the article → `eval_macro_f1 = 0.7142` in the training output of `notebooks/Stage1_run_classifiers.ipynb`. ✅

## 3. Section 5.1.2 — error composition

| Article | Recomputed | |
|---|---|---|
| Perspective caught 52 of 502 scored Hate items | TP = 52; scored gold-Hate = 502 | ✅ |
| Perspective missed 450 of 502 (89.6%) | FN = 450; 89.64% | ✅ |
| AfroXLMR missed 119 of 331 Amharic (36.0%) | FN = 119; 35.95% | ✅ |
| AfroXLMR missed 221 of 266 Afan Oromo (83.1%) | FN = 221; 83.08% | ✅ |
| AfroXLMR caught 45 of 266 Afan Oromo Hate | TP = 45 | ✅ |
| mBERT missed 147 of 331 Amharic (44.4%) | FN = 147; 44.41% | ✅ |
| Perspective produced no false positives | FP = 0 in every split | ✅ |
| Precision range .86–1.00 | min .864 (mBERT), max 1.000 | ✅ |
| Of AfriHate's 20 Amharic FPs, 17 (85%) counterspeech | 20 FPs → 17 Counter, 3 Neutral = 85.0% | ✅ |
| Of mBERT's 29 FPs, 20 (69%) counterspeech | 29 FPs → 20 Counter, 9 Neutral = 69.0% | ✅ |
| mBERT training F1 .92 → 24-point decrement | .92 − .68 = .24 | ✅ |

## 4. Sensitivity to the reconstructed-label block

`FineLabel` for `POST_0537`–`POST_1007` was reconstructed from two agreeing annotator columns rather than recorded at reconciliation time (see [`CHANGELOG.md`](CHANGELOG.md), *Known limitations*). Those rows supply 416 of the 597 gold Hate items. Excluding them entirely:

| | Published | Block excluded |
|---|---|---|
| Three-class κ | .971 (n = 783) | **.959** (n = 366) |
| Six-class κ | .786 (n = 951) | **.720** (n = 534) |
| Perspective F1, overall | .19 | .36 |
| AfriHate F1, Amharic | .75 | .72 |
| AfriHate F1, Afan Oromo | .29 | .27 |
| mBERT F1, Amharic | .68 | .63 |

Both κ values stay above the protocol target of .70, and every substantive finding survives: Perspective remains by far the weakest, Afan Oromo the least served at every tier, under-detection the dominant error mode, and the ordering of the three classifiers unchanged.

## 5. Reproducibility

| Item | Status |
|---|---|
| Environment | `requirements.txt`, pinned, verified on Python 3.11 |
| Random seeds | seed = 42, for both the date randomization and the AfroXLMR fine-tune |
| API version | Perspective `commentanalyzer` `v1alpha1`, collected June 2026. The hosted model is not pinnable; this is stated rather than papered over |
| Data access | [`DATA.md`](DATA.md) and [`DATASHEET.md`](DATASHEET.md); withheld components and their access conditions named |
| Automated reproduction | `python reproduce.py` — verifies the corpus against the published figures, then regenerates Table 1 and the 5.1.2 composition. Exits non-zero on any mismatch |

One gap remains: the two Hugging Face checkpoints are unversioned repository references. Passing `revision=<commit-sha>` would close it, at the cost of a one-time lookup.

## 6. Pre-publication checks

Before release, every file in this deposit — including each XML part inside every workbook and every stored output inside every notebook — was scanned for credentials, platform URLs, account identifiers, and the withheld fields. All are absent. Masking coverage was verified in both directions: no slur survives in any Hate-labelled row, and the terms deliberately left intact (ordinary Amharic words that merely resemble a slur, and the surname of a public figure) are confirmed unaltered.
