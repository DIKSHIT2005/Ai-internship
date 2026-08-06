# Email Spam Detection (Machine Learning)

A beginner-friendly machine learning project to classify emails as **spam** or **ham** using a TF-IDF + Naive Bayes pipeline.

## Project Structure

```text
Assignment 8/
├── spam_detector.py
├── sample_emails.csv
├── requirements.txt
└── model/
```

## Setup

```bash
cd "Assignment 8"
pip install -r requirements.txt
```

## Train the Model

```bash
python spam_detector.py train --data sample_emails.csv --model-path model/spam_model.joblib
```

This command:
- Loads and cleans the dataset
- Splits data into train/test sets
- Trains a TF-IDF + Multinomial Naive Bayes model
- Prints evaluation metrics
- Saves the trained model

## Predict New Emails

```bash
python spam_detector.py predict --model-path model/spam_model.joblib --text "Win a free iPhone now"
```

Output includes predicted label and confidence score.

## Dataset Format

Use a CSV with these columns:
- `label` (`spam` or `ham`)
- `text` (email content)
