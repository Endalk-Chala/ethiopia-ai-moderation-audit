# Audit code

Code to reproduce the classifier audit (Strand 1 of the study).

## Notebooks

Run in order:

1. `Stage1_run_classifiers.ipynb` — scores **Perspective API** and the fine-tuned **AfroXLMR (AfriHate)** model on the 838 audit-eligible rows.
2. `Stage1b_amharic_mbert.ipynb` — adds **Amharic mBERT** and computes the final precision/recall/F1 for all three classifiers, by language.

Outputs are cleared; add your Perspective API key where indicated and re-run to reproduce. The scoring inputs are the audit-eligible rows of the corpus (the unmasked scoring file is withheld; see the datasheet).

## What the audit does

Evaluates three classifiers against the binarized gold standard, disaggregated by language:

1. **Perspective API** (generic) — native mode and human-English-translation mode.
2. **AfroXLMR (fine-tuned)** — trained on the AfriHate Amharic split.
3. **Amharic mBERT** — Amharic subset only.

It reports precision, recall, and F1, plus error composition (under- vs. over-enforcement and counterspeech false positives).

## Reproducibility notes

- Environment: see `requirements.txt` for Python and package versions.
- Random seeds and fine-tuning hyperparameters for AfroXLMR are set in the notebook.
- Perspective API version/date and request settings are recorded in the audit notebook.
- The evaluation reads the unmasked scoring file, which is withheld to limit harm; the public corpus is the masked, redistributable version. Access to the scoring file is described in the datasheet.

## License

Code: MIT (see [`LICENSE`](LICENSE)).
