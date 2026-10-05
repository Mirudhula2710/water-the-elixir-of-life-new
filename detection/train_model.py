import pandas as pd
import numpy as np
import json
import hashlib
import os
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(os.path.dirname(BASE_DIR), 'data', 'water_leak_sensor_dataset.csv')
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'model_artifacts')

def compute_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def get_feature_names(pipeline):
    """Extract feature names from the pipeline's ColumnTransformer"""
    col_trans = pipeline.named_steps['preprocessor']
    feature_names = []
    for name, trans, columns in col_trans.transformers_:
        if name == 'num':
            feature_names.extend(columns)
        elif name == 'cat':
            cats = trans.get_feature_names_out(columns)
            feature_names.extend(cats)
    return feature_names

def train_and_evaluate():
    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    n_rows = len(df)
    dataset_hash = compute_hash(DATA_FILE)
    
    # Drop columns per spec
    cols_to_drop = [
        'anomaly_type', 'deviation', 'deviation_pct', 
        'rolling_avg_deviation', 'rolling_std_deviation',
        'reading_index', 'zone_id', 'minutes_since_last_reading'
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
    
    X = df.drop(columns=['severity'])
    y = df['severity']
    
    # Define features
    numeric_features = ['hour', 'minute_of_day', 'tank_level', 'expected_level', 'rate_of_change']
    categorical_features = ['zone']
    
    # 80/20 stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    # Create preprocessing and modeling pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Train SVC (RBF) as requested
    svm_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', SVC(kernel='rbf', probability=True, random_state=42))
    ])
    
    print("Training SVM_RBF model...")
    svm_pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = svm_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Cross-validation
    print("Running 5-fold CV on full dataset...")
    cv_scores = cross_val_score(svm_pipeline, X, y, cv=5, scoring='f1_macro')
    print(f"5-fold CV Macro F1: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Five-model comparison for Viva
    print("\n--- Five-Model Comparison (Macro F1 on Test Set) ---")
    models = {
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'DecisionTree(max_depth=6)': DecisionTreeClassifier(max_depth=6, random_state=42),
        'RandomForest(100, max_depth=6)': RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        'SVC (RBF)': SVC(kernel='rbf', random_state=42),
        'MLP': MLPClassifier(max_iter=500, random_state=42)
    }
    
    for name, clf in models.items():
        pipe = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', clf)])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        f1 = f1_score(y_test, preds, average='macro')
        print(f"{name:30s} | F1: {f1:.4f}")
    
    # Save the selected SVM pipeline
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    model_path = os.path.join(ARTIFACTS_DIR, 'severity_model.pkl')
    joblib.dump(svm_pipeline, model_path)
    print(f"\nModel saved to {model_path}")
    
    # Write metadata
    feature_names = get_feature_names(svm_pipeline)
    
    metadata = {
        "model_name": "SVM_RBF_Pipeline",
        "features": feature_names,
        "base_features": numeric_features + categorical_features,
        "classes": list(svm_pipeline.classes_),
        "training_date": datetime.utcnow().isoformat() + "Z",
        "dataset_size": n_rows,
        "dataset_hash": dataset_hash,
        "split": "80/20 Stratified (random_state=42)",
        "metrics": {
            "test_accuracy": accuracy,
            "test_macro_f1": macro_f1,
            "cv_macro_f1_mean": cv_scores.mean(),
            "cv_macro_f1_std": cv_scores.std()
        },
        "sklearn_version": joblib.__version__, # joblib used for save, we will log sklearn in ml_model.py
        "note": "Trained on purely SYNTHETIC data. The dataset exhibits leakage where severity is a direct rule on deviation_pct, so the model largely learns a threshold rule on simulated data."
    }
    import sklearn
    metadata['sklearn_version'] = sklearn.__version__
    
    with open(os.path.join(ARTIFACTS_DIR, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    print("Metadata saved.")

if __name__ == '__main__':
    train_and_evaluate()
