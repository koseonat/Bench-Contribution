import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc, classification_report
from sklearn.preprocessing import StandardScaler

def train_eval_models():
    print("\n🤖 Training ML Models (Logistic Regression & Random Forest)...")
    
    # 1. Load Data
    df = pd.read_csv("data/ml/playoff_matchups_labeled.csv")
    
    # Features: VORP Diff, BPM Diff, PPG Diff
    features = ['Diff_VORP', 'Diff_BPM', 'Diff_PPG']
    X = df[features]
    y = df['Target_Win']
    
    # 2. Split Data (Slide 26)
    # We use Chronological Split to simulate real forecasting
    # Train: 2010-2019 (History)
    # Test:  2020-2025 (Future/Recent)
    train_mask = df['Year'] <= 2019
    test_mask  = df['Year'] >= 2020
    
    X_train, y_train = X[train_mask], y[train_mask]
    X_test, y_test   = X[test_mask], y[test_mask]
    
    print(f"   Training Set: {len(X_train)} samples (2010-2019)")
    print(f"   Testing Set:  {len(X_test)} samples (2020-2025)")

    # 3. Standardization (Slide 46)
    # Essential for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # --- MODEL 1: LOGISTIC REGRESSION (Slide 32) ---
    print("\n🔹 Model 1: Logistic Regression")
    log_reg = LogisticRegression(random_state=42)
    log_reg.fit(X_train_scaled, y_train)
    
    y_pred_log = log_reg.predict(X_test_scaled)
    acc_log = accuracy_score(y_test, y_pred_log)
    print(f"   Accuracy: {acc_log:.4f}")
    
    # Coefficients (Slide 35)
    coef_df = pd.DataFrame({'Feature': features, 'Coefficient': log_reg.coef_[0]})
    print("   Coefficients (Impact of features):\n", coef_df)

    # --- MODEL 2: RANDOM FOREST (Slide 60) ---
    print("\n🌲 Model 2: Random Forest (Ensemble)")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    rf.fit(X_train, y_train)
    
    y_pred_rf = rf.predict(X_test)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]
    acc_rf = accuracy_score(y_test, y_pred_rf)
    print(f"   Accuracy: {acc_rf:.4f}")
    
    # Feature Importance (Slide 62)
    importances = pd.DataFrame({'Feature': features, 'Importance': rf.feature_importances_})
    print("   Feature Importance:\n", importances.sort_values(by='Importance', ascending=False))

    # --- EVALUATION ---
    # Confusion Matrix (Slide 39)
    cm = confusion_matrix(y_test, y_pred_rf)
    print("\n   Confusion Matrix (Random Forest):\n", cm)
    
    # ROC Curve (Slide 40)
    fpr, tpr, _ = roc_curve(y_test, y_prob_rf)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve (Random Forest)')
    plt.legend(loc="lower right")
    plt.savefig("notebooks/roc_curve_rf.png")
    print("   ✅ ROC Curve saved to notebooks/roc_curve_rf.png")

if __name__ == "__main__":
    train_eval_models()
