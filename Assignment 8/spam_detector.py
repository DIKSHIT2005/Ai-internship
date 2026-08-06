import argparse
import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


TEXT_COL = "text"
LABEL_COL = "label"


def clean_text(text: str) -> str:
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {LABEL_COL, TEXT_COL}
    if not required.issubset(df.columns):
        raise ValueError(f"Dataset must contain columns: {required}")
    df = df[[LABEL_COL, TEXT_COL]].dropna()
    df[TEXT_COL] = df[TEXT_COL].apply(clean_text)
    df[LABEL_COL] = df[LABEL_COL].str.lower().str.strip()
    df = df[df[LABEL_COL].isin(["spam", "ham"])]
    if df.empty:
        raise ValueError("No valid rows found. Labels must be 'spam' or 'ham'.")
    return df


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1),
            ),
            ("classifier", MultinomialNB()),
        ]
    )


def train_model(data_path: str, model_path: str, test_size: float = 0.2) -> None:
    df = load_data(data_path)

    x_train, x_test, y_train, y_test = train_test_split(
        df[TEXT_COL],
        df[LABEL_COL],
        test_size=test_size,
        random_state=42,
        stratify=df[LABEL_COL],
    )

    model = build_pipeline()
    model.fit(x_train, y_train)
    preds = model.predict(x_test)

    print("\nModel Evaluation")
    print("=" * 40)
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, preds, digits=4))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, preds))

    model_file = Path(model_path)
    model_file.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_file)
    print(f"\nSaved trained model to: {model_file}")


def predict_email(model_path: str, text: str) -> None:
    model = joblib.load(model_path)
    cleaned = clean_text(text)
    pred = model.predict([cleaned])[0]
    prob = model.predict_proba([cleaned])[0]
    classes = list(model.classes_)
    confidence = prob[classes.index(pred)]

    print("\nPrediction")
    print("=" * 40)
    print(f"Email text: {text}")
    print(f"Predicted label: {pred.upper()}")
    print(f"Confidence: {confidence:.2%}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Email spam detection using machine learning")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train and evaluate the model")
    train_parser.add_argument(
        "--data",
        default="sample_emails.csv",
        help="Path to CSV dataset with columns: label,text",
    )
    train_parser.add_argument(
        "--model-path",
        default="model/spam_model.joblib",
        help="Where to save the trained model",
    )
    train_parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Test split ratio (default: 0.2)",
    )

    predict_parser = subparsers.add_parser("predict", help="Predict whether a message is spam")
    predict_parser.add_argument(
        "--model-path",
        default="model/spam_model.joblib",
        help="Path to the trained model",
    )
    predict_parser.add_argument("--text", required=True, help="Email content to classify")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "train":
        train_model(args.data, args.model_path, args.test_size)
    elif args.command == "predict":
        predict_email(args.model_path, args.text)


if __name__ == "__main__":
    main()
