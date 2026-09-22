"""Phase 4a — Predict Recommended (yes/no). Primary business-outcome task.

Features: Review text (TF-IDF 1-2grams) + review length + 7 service ratings
+ CabinType/TravelType/TripVerified/airline_group.
EXCLUDED for leakage: OverallScore (= near-duplicate outcome), Title
(paraphrases Review), Slug (= AirlineName dup), unique_id (key),
DateFlown/DatePub (post-booking/post-flight), OriginCountry/Route/Aircraft
(high-cardinality or sparse; documented choice, not leakage).

Models: Dummy(stratified) baseline, LogisticRegression, LinearSVC,
ComplementNB (text-only). Best by F1 saved to models/.
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.svm import LinearSVC

from src.nlp.features import cat_pipe, make_tfidf, numeric_pipe

BASE = Path(__file__).resolve().parents[2]
CLEAN_PATH = BASE / "data" / "processed" / "airline_reviews_clean.csv"
MODEL_PATH = BASE / "models" / "recommended_model.joblib"
METRICS_PATH = BASE / "models" / "recommended_metrics.json"
REPORT_PATH = BASE / "reports" / "model_recommended.md"
CM_PATH = BASE / "reports" / "figures" / "fig_cm_recommended.png"

SERVICE_COLS = ["SeatComfortRating", "ServiceRating", "FoodRating", "ValueRating",
                "GroundServiceRating", "EntertainmentRating", "WifiRating"]
LEN_COLS = ["review_char_len", "review_word_count"]
CAT_COLS = ["airline_group", "CabinType", "TravelType", "TripVerified"]
RANDOM_STATE = 42


def build_frame() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_PATH, low_memory=False)
    df["Review"] = df["Review"].fillna("")
    top_airlines = set(df["AirlineName"].value_counts().head(30).index)
    df["airline_group"] = df["AirlineName"].where(df["AirlineName"].isin(top_airlines), "Other")
    df["y"] = (df["Recommended"] == "yes").astype(int)
    return df


def full_preprocess() -> ColumnTransformer:
    return ColumnTransformer([
        ("text", make_tfidf(), "Review"),
        ("num", numeric_pipe(), SERVICE_COLS + LEN_COLS),
        ("cat", cat_pipe(), CAT_COLS),
    ])


def score_fn(name: str, clf, X_tr, y_tr, X_te, y_te) -> dict:
    clf.fit(X_tr, y_tr)
    pred = clf.predict(X_te)
    if hasattr(clf, "predict_proba"):
        scores = clf.predict_proba(X_te)[:, 1]
    else:
        scores = clf.decision_function(X_te)
    return {
        "model": name,
        "accuracy": round(float(accuracy_score(y_te, pred)), 4),
        "precision": round(float(precision_score(y_te, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_te, pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_te, pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_te, scores)), 4),
        "_pred": pred,
    }


def main() -> None:
    df = build_frame()
    X = df[["Review"] + SERVICE_COLS + LEN_COLS + CAT_COLS]
    y = df["y"]
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE)
    print(f"train={X_tr.shape} test={X_te.shape} pos_rate={y.mean():.3f}")

    pre = full_preprocess()
    results = [score_fn("dummy_stratified", make_pipeline(pre, DummyClassifier(strategy="stratified", random_state=RANDOM_STATE)), X_tr, y_tr, X_te, y_te)]
    print("dummy done")
    results.append(score_fn("logistic_regression",
        make_pipeline(full_preprocess(), LogisticRegression(max_iter=1000)), X_tr, y_tr, X_te, y_te))
    print("logreg done")
    results.append(score_fn("linear_svc",
        make_pipeline(full_preprocess(), LinearSVC()), X_tr, y_tr, X_te, y_te))
    print("svc done")
    nb = make_pipeline(make_tfidf(), ComplementNB())
    r_nb = score_fn("complement_nb_textonly", nb, X_tr["Review"], y_tr, X_te["Review"], y_te)
    results.append(r_nb)
    print("nb done")

    # Refit best by F1 on train, save
    best_name = max(results, key=lambda r: r["f1"])["model"]
    specs = {
        "logistic_regression": make_pipeline(full_preprocess(), LogisticRegression(max_iter=1000)),
        "linear_svc": make_pipeline(full_preprocess(), LinearSVC()),
        "complement_nb_textonly": make_pipeline(make_tfidf(), ComplementNB()),
    }
    best = specs[best_name]
    if best_name == "complement_nb_textonly":
        best.fit(X_tr["Review"], y_tr)
    else:
        best.fit(X_tr, y_tr)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": best, "model_name": best_name,
                 "service_cols": SERVICE_COLS, "cat_cols": CAT_COLS}, MODEL_PATH)

    metrics = [{k: v for k, v in r.items() if not k.startswith("_")} for r in results]
    METRICS_PATH.write_text(json.dumps({"best_model": best_name, "results": metrics,
        "leakage_excluded": ["OverallScore", "Title", "Slug", "unique_id", "DateFlown", "DatePub"],
        "note": "60/40 class split; F1 is the selection metric, not accuracy."}, indent=2))

    # Confusion matrix of best (from test preds recorded above)
    best_pred = next(r["_pred"] for r in results if r["model"] == best_name)
    cm = confusion_matrix(y_te, best_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(cm); ax.set_title(f"Confusion matrix — {best_name} (test)")
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="white", fontsize=12)
    fig.tight_layout(); fig.savefig(CM_PATH); plt.close(fig)

    REPORT_PATH.write_text(
        "# Recommended-prediction model (VERIFIED run)\n\n"
        f"Best by F1: **{best_name}**\n\n"
        + "\n".join(f"- {m['model']}: acc={m['accuracy']} prec={m['precision']} "
                    f"rec={m['recall']} F1={m['f1']} ROC-AUC={m['roc_auc']}" for m in metrics)
        + "\n\nTrade-offs: LinearSVC/LogReg use full features; ComplementNB is text-only "
          "(weaker but deployable on review text alone). Dummy shows the 60/40-majority floor. "
          "F1 chosen over accuracy because recommending correctly for the minority class matters "
          "and accuracy would reward majority-class bias.\n",
        encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"best={best_name} saved -> {MODEL_PATH}")


if __name__ == "__main__":
    main()
