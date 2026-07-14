# Audit code

Code to reproduce the classifier audit (Strand 1 of the study).

## Add your notebooks/scripts here
From the author's working environment (Google Drive), the relevant notebooks are:
- `Stage1b_amharic_mbert.ipynb` — Amharic mBERT evaluation.
- `ethiopia_moderation_audit_2024_real.ipynb` — main audit (Perspective API + AfroXLMR).

Export these to this folder (optionally also as `.py` for readability/diffing).

## What the audit does
Evaluates three classifiers against the binarized gold standard, disaggregated by language:
1. **Perspective API** (generic) — native mode and human-English-translation mode.
2. **AfroXLMR (fine-tuned)** — trained on the AfriHate Amharic split.
3. **Amharic mBERT** — Amharic subset only.

Reports **precision, recall, F1**, plus error composition (under- vs. over-enforcement and
counterspeech false positives).

## Reproducibility checklist (fill in before release)
- [ ] `requirements.txt` / environment (Python version, key package versions).
- [ ] Random seeds and fine-tuning hyperparameters for AfroXLMR.
- [ ] Perspective API version/date and request settings.
- [ ] Exact paths: reads the **withheld unmasked** scoring file — document how a user with
      approved access supplies it (the public corpus is masked and reproduces the corpus, not
      the exact scored inputs).
- [ ] A `make audit` or single entry-point script that regenerates the results tables.

## License
Code: MIT (see top-level `LICENSE`).
