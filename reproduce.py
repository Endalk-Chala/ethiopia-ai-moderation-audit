#!/usr/bin/env python3
"""
Reproduce the computational audit reported in:

    Chala, E. H. (2026). From Detection to Counterspeech: Auditing AI Moderation and
    Fact-Checking Practices in Ethiopia's Multilingual Online Sphere.
    Media and Communication, 14, Article 12653.

Two modes:

    python reproduce.py                # verify corpus + regenerate Table 1 from stored predictions
    python reproduce.py --score        # additionally re-run the classifiers from scratch

`--score` needs a Perspective API key (PERSPECTIVE_API_KEY in the environment), network
access, and ideally a GPU. It takes roughly 20 minutes and its Perspective scores may
differ slightly from the deposited ones, because the hosted model is versioned by Google
and not pinned. The default mode is deterministic and reproduces the published numbers
exactly.

Outputs are written to out/.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "data" / "ethiopia_moderation_audit_corpus.xlsx"
PREDS = ROOT / "results" / "predictions_full.csv"
OUT = ROOT / "out"

SEED = 42
THRESHOLD = 0.50                      # Perspective TOXICITY -> hate
POSITIVE = "Hate"                     # binarization: Hate = 1; Counter and Neutral = 0
AFRO_XLMR = "Davlan/afro-xlmr-base-hate-v1"
AM_MBERT = "amengemeda/amharic-hate-speech-detection-mBERT"

CLASSIFIERS = [
    ("Perspective API (translation)", "persp_pred"),
    ("AfriHate (AfroXLMR, fine-tuned)", "afrihate_pred"),
    ("Amharic mBERT", "ammbert_pred"),
]
SCOPES = ["All", "Amharic", "Afan Oromo"]


# ----------------------------------------------------------------------------- corpus
def verify_corpus() -> pd.DataFrame:
    """Check the deposited corpus against the values reported in the article."""
    d = pd.read_excel(CORPUS, sheet_name="Dataset")
    elig = d[d.IncludeInAudit == True]  # noqa: E712  (explicit: the column holds real booleans)

    checks = [
        ("physical rows", len(d), 1007),
        ("in-scope (non-English) rows", int((d.Language != "English").sum()), 951),
        ("audit-eligible rows", len(elig), 838),
        ("  Amharic", int((elig.Language == "Amharic").sum()), 470),
        ("  Afan Oromo", int((elig.Language == "Afan Oromo").sum()), 368),
        ("gold Hate", int((elig.Label3Class == POSITIVE).sum()), 597),
        ("gold not-Hate", int((elig.Label3Class != POSITIVE).sum()), 241),
        ("  Hate, Amharic", int(((elig.Language == "Amharic") & (elig.Label3Class == POSITIVE)).sum()), 331),
        ("  Hate, Afan Oromo", int(((elig.Language == "Afan Oromo") & (elig.Label3Class == POSITIVE)).sum()), 266),
    ]

    collapse = {"Hate speech": "Hate", "Counter speech": "Counter",
                "Neutral": "Neutral", "Political speech": "Neutral"}
    ne = d[d.Language != "English"]
    k3 = ne[ne.Annotator1.isin(collapse) & ne.Annotator2.isin(collapse)]
    kappa3 = cohen_kappa_score(k3.Annotator1.map(collapse), k3.Annotator2.map(collapse))
    kappa6 = cohen_kappa_score(ne.Annotator1, ne.Annotator2)

    print("Corpus verification")
    print("-" * 62)
    ok = True
    for label, got, want in checks:
        good = got == want
        ok &= good
        print(f"  {label:<32} {got:>6}   expected {want:>6}   {'OK' if good else 'MISMATCH'}")
    for label, got, want in [("three-class kappa", kappa3, 0.971), ("six-class kappa", kappa6, 0.786)]:
        good = abs(got - want) < 0.001
        ok &= good
        print(f"  {label:<32} {got:>6.3f}   expected {want:>6.3f}   {'OK' if good else 'MISMATCH'}")
    print("-" * 62)
    print("  corpus matches the published figures\n" if ok else "  CORPUS DOES NOT MATCH — stop here\n")
    if not ok:
        sys.exit(1)
    return d


# ------------------------------------------------------------------------- evaluation
def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    recall = tp / (tp + fn) if (tp + fn) else float("nan")
    f1 = 2 * precision * recall / (precision + recall) if (tp + fp) and (tp + fn) and (precision + recall) else 0.0
    return dict(precision=precision, recall=recall, f1=f1,
                TP=int(tp), FP=int(fp), FN=int(fn), TN=int(tn),
                accuracy=(tp + tn) / (tp + tn + fp + fn))


def evaluate(preds: pd.DataFrame) -> pd.DataFrame:
    """Table 1 plus the confusion counts behind Section 5.1.2.

    Metrics are computed on covered rows only — rows where the classifier returned a
    prediction. Coverage is reported alongside, so an uncovered row is never silently
    counted as a correct negative.
    """
    rows = []
    for name, col in CLASSIFIERS:
        for scope in SCOPES:
            sub = preds if scope == "All" else preds[preds.Language == scope]
            covered = sub[sub[col].notna()]
            row = dict(classifier=name, language=scope, n=len(sub),
                       coverage=f"{len(covered)}/{len(sub)}")
            if len(covered):
                row.update(_metrics((covered.Label3Class == POSITIVE).astype(int).to_numpy(),
                                    covered[col].astype(int).to_numpy()))
            else:
                row.update(dict.fromkeys(["precision", "recall", "f1", "accuracy"], float("nan")),
                           **dict.fromkeys(["TP", "FP", "FN", "TN"], 0))
            rows.append(row)
    return pd.DataFrame(rows)


def counterspeech_breakdown(preds: pd.DataFrame) -> pd.DataFrame:
    """Section 5.1.2: how the two local models' false positives distribute over
    Counter vs Neutral."""
    rows = []
    for name, col in [("AfriHate", "afrihate_pred"), ("Amharic mBERT", "ammbert_pred")]:
        for scope in SCOPES:
            sub = preds if scope == "All" else preds[preds.Language == scope]
            fp = sub[(sub[col] == 1) & (sub.Label3Class != POSITIVE)]
            if not len(fp):
                continue
            counter = int((fp.Label3Class == "Counter").sum())
            rows.append(dict(classifier=name, language=scope, false_positives=len(fp),
                             counterspeech=counter, neutral=len(fp) - counter,
                             pct_counterspeech=round(100 * counter / len(fp), 1)))
    return pd.DataFrame(rows)


def print_table1(t: pd.DataFrame) -> None:
    def fmt(v):
        return "—" if pd.isna(v) else f"{v:.2f}".lstrip("0") if v < 1 else "1.00"
    print("Table 1. Binary hate-detection performance by classifier and language subset.")
    print("-" * 86)
    print(f"{'Classifier':<34}{'Language':<13}{'n':>5}{'Precision':>11}{'Recall':>9}{'F1':>7}{'Coverage':>12}")
    print("-" * 86)
    print(f"{'Perspective API (native)':<34}{'All':<13}{838:>5}{'—':>11}{'—':>9}{'—':>7}{'0/838':>12}")
    for _, r in t.iterrows():
        cov = "0/368" if r.classifier == "Amharic mBERT" and r.language == "Afan Oromo" else r.coverage
        print(f"{r.classifier:<34}{r.language:<13}{r.n:>5}"
              f"{fmt(r.precision):>11}{fmt(r.recall):>9}{fmt(r.f1):>7}{cov:>12}")
    print("-" * 86)
    print("Note: native = original-language text; translation = human English translations.")
    print("Coverage = proportion of eligible items the classifier returned a score for.\n")


def print_errors(t: pd.DataFrame) -> None:
    print("Section 5.1.2 — error composition (under-enforcement dominates)")
    print("-" * 72)
    for _, r in t.iterrows():
        if r.TP + r.FN == 0:
            continue
        hate = r.TP + r.FN
        print(f"  {r.classifier:<34}{r.language:<12} missed {r.FN:>3} of {hate:>3} Hate "
              f"({100 * r.FN / hate:5.1f}%)   FP={r.FP}")
    print("-" * 72 + "\n")


# ---------------------------------------------------------------------------- scoring
def score_from_scratch(corpus: pd.DataFrame) -> pd.DataFrame:
    """Re-run all three classifiers. Requires network, a Perspective key, ideally a GPU."""
    import torch
    from googleapiclient import discovery
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, set_seed

    set_seed(SEED)
    key = os.environ.get("PERSPECTIVE_API_KEY")
    if not key:
        sys.exit("PERSPECTIVE_API_KEY is not set. Export it, or run without --score.")

    df = corpus[corpus.IncludeInAudit == True].reset_index(drop=True)  # noqa: E712
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Scoring {len(df)} rows on {device}\n")

    # --- Perspective: native mode, then on the human English translation ---------
    client = discovery.build(
        "commentanalyzer", "v1alpha1", developerKey=key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False)

    def perspective(text: str, languages: list[str] | None):
        body = {"comment": {"text": str(text)[:20000]},
                "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}
        if languages:
            body["languages"] = languages
        try:
            r = client.comments().analyze(body=body).execute()
            return r["attributeScores"]["TOXICITY"]["summaryScore"]["value"], "ok"
        except Exception as exc:                       # noqa: BLE001 — status is the datum
            return None, type(exc).__name__

    native_lang = {"Amharic": ["am"], "Afan Oromo": None}
    native, translated = [], []
    for _, row in df.iterrows():
        native.append(perspective(row.OriginalText, native_lang.get(row.Language))[0])
        translated.append(perspective(row.EnglishTranslation, ["en"])[0])
        time.sleep(1.05)                               # 1 QPS quota
    df["persp_native_score"] = native
    df["persp_score"] = translated
    df["persp_pred"] = [None if s is None else int(s >= THRESHOLD) for s in translated]
    print(f"  Perspective: native {sum(s is not None for s in native)}/{len(df)} scored, "
          f"translation {sum(s is not None for s in translated)}/{len(df)}")

    # --- transformer classifiers -------------------------------------------------
    def run(checkpoint: str, texts: list[str], positive) -> list[int]:
        tok = AutoTokenizer.from_pretrained(checkpoint)
        mdl = AutoModelForSequenceClassification.from_pretrained(checkpoint).to(device).eval()
        preds = []
        for i in range(0, len(texts), 32):
            enc = tok([str(t)[:512] for t in texts[i:i + 32]], padding=True, truncation=True,
                      max_length=256, return_tensors="pt").to(device)
            with torch.no_grad():
                for p in mdl(**enc).logits.argmax(-1).cpu().numpy():
                    preds.append(positive(mdl.config.id2label[int(p)], int(p)))
        return preds

    df["afrihate_pred"] = run(
        AFRO_XLMR, df.OriginalText.tolist(),
        lambda label, _idx: int(any(k in str(label).lower() for k in ("hate", "abus"))))

    amharic = df.Language == "Amharic"
    df["ammbert_pred"] = None
    df.loc[amharic, "ammbert_pred"] = run(
        AM_MBERT, df.loc[amharic, "OriginalText"].tolist(), lambda _label, idx: int(idx == 1))

    OUT.mkdir(exist_ok=True)
    # never write the withheld fields, even if a future corpus revision reintroduces them
    withheld = [c for c in ("Link", "Date", "AI_Draft_Analysis") if c in df.columns]
    df.drop(columns=withheld).to_csv(OUT / "predictions_rescored.csv", index=False)
    if withheld:
        print(f"  withheld fields excluded from output: {withheld}")
    print(f"  wrote {OUT / 'predictions_rescored.csv'}\n")
    return df


# ------------------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--score", action="store_true",
                    help="re-run the classifiers instead of using the deposited predictions")
    args = ap.parse_args()

    corpus = verify_corpus()
    preds = score_from_scratch(corpus) if args.score else pd.read_csv(PREDS)

    table1 = evaluate(preds)
    print_table1(table1)
    print_errors(table1)
    fp = counterspeech_breakdown(preds)
    print("Section 5.1.2 — where the local models' false positives land")
    print(fp.to_string(index=False), "\n")

    OUT.mkdir(exist_ok=True)
    table1.to_csv(OUT / "table1_performance.csv", index=False)
    fp.to_csv(OUT / "false_positive_composition.csv", index=False)
    print(f"Wrote {OUT / 'table1_performance.csv'} and {OUT / 'false_positive_composition.csv'}")


if __name__ == "__main__":
    main()
