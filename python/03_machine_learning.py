"""
NETFLIX CONTENT ANALYSIS PROJECT
Step 5: Machine Learning – Predict Movie vs TV Show
File: 03_machine_learning.py

Target: Predict 'type' (Movie=1 / TV Show=0)
Algorithm: Random Forest Classifier (~95% accuracy)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, roc_auc_score, roc_curve)
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

os.makedirs('outputs/ml', exist_ok=True)

NETFLIX_RED  = '#E50914'
NETFLIX_DARK = '#141414'
plt.rcParams['figure.dpi'] = 150

# ── Load Data ─────────────────────────────────────────────────────────────────
df = pd.read_csv('data/netflix_cleaned.csv')
print(f"Dataset shape: {df.shape}")

# ── Feature Engineering ────────────────────────────────────────────────────────
# Encode categorical features
le_rating  = LabelEncoder()
le_country = LabelEncoder()
le_genre   = LabelEncoder()

df['rating_encoded']  = le_rating.fit_transform(df['rating'].fillna('Not Rated'))
df['country_encoded'] = le_country.fit_transform(df['primary_country'].fillna('Unknown'))
df['genre_encoded']   = le_genre.fit_transform(df['primary_genre'].fillna('Unknown'))

# Binary: has director, has cast
df['has_director'] = (df['director'] != 'Unknown').astype(int)
df['has_cast']     = (df['cast'] != 'Unknown').astype(int)

# Feature set
FEATURES = [
    'release_year',
    'duration_value',
    'content_age',
    'year_added',
    'month_added',
    'rating_encoded',
    'country_encoded',
    'genre_encoded',
    'has_director',
    'has_cast',
]

TARGET = 'type_encoded'   # 1 = Movie, 0 = TV Show

# ── Prepare X, y ──────────────────────────────────────────────────────────────
X = df[FEATURES].copy()
y = df[TARGET].copy()

# Impute missing numeric values
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)
X = pd.DataFrame(X_imputed, columns=FEATURES)

print(f"\nFeatures: {FEATURES}")
print(f"Class distribution:\n{y.value_counts()}")

# ── Train / Test Split ────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain size: {len(X_train):,}  |  Test size: {len(X_test):,}")

# ── Train Random Forest ───────────────────────────────────────────────────────
print("\nTraining Random Forest...")
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────────────────────
y_pred   = rf.predict(X_test)
y_prob   = rf.predict_proba(X_test)[:, 1]
acc      = accuracy_score(y_test, y_pred)
auc      = roc_auc_score(y_test, y_prob)
cv_scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')

print("\n" + "=" * 50)
print("MODEL PERFORMANCE RESULTS")
print("=" * 50)
print(f"Accuracy      : {acc:.4f}  ({acc*100:.2f}%)")
print(f"ROC-AUC       : {auc:.4f}")
print(f"CV Mean Acc   : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['TV Show', 'Movie']))

# ── PLOT 1: Confusion Matrix ──────────────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(7, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',
            xticklabels=['TV Show', 'Movie'],
            yticklabels=['TV Show', 'Movie'],
            ax=ax, linewidths=1, cbar=False,
            annot_kws={'size': 16, 'color': 'white'})

ax.set_xlabel('Predicted', color='white', fontsize=13)
ax.set_ylabel('Actual', color='white', fontsize=13)
ax.set_title(f'Confusion Matrix\nAccuracy: {acc*100:.2f}%', color='white',
             fontsize=14, fontweight='bold')
ax.tick_params(colors='white')

plt.tight_layout()
plt.savefig('outputs/ml/confusion_matrix.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("\n✅ Confusion matrix saved.")

# ── PLOT 2: Feature Importance ────────────────────────────────────────────────
importances = pd.Series(rf.feature_importances_, index=FEATURES).sort_values()

fig, ax = plt.subplots(figsize=(10, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

colors = [NETFLIX_RED if v == importances.max() else '#831010' for v in importances]
ax.barh(importances.index, importances.values, color=colors, edgecolor='none')
ax.set_title('Feature Importances – Random Forest', color='white',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Importance', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/ml/feature_importance.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ Feature importance chart saved.")

# ── PLOT 3: ROC Curve ─────────────────────────────────────────────────────────
fpr, tpr, _ = roc_curve(y_test, y_prob)

fig, ax = plt.subplots(figsize=(8, 6), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

ax.plot(fpr, tpr, color=NETFLIX_RED, linewidth=2.5,
        label=f'Random Forest (AUC = {auc:.3f})')
ax.plot([0, 1], [0, 1], 'white', linestyle='--', linewidth=1, label='Random')

ax.set_title('ROC Curve – Content Type Prediction', color='white',
             fontsize=14, fontweight='bold')
ax.set_xlabel('False Positive Rate', color='white', fontsize=12)
ax.set_ylabel('True Positive Rate', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.legend(facecolor='#333', labelcolor='white', fontsize=11)
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/ml/roc_curve.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ ROC curve saved.")

# ── PLOT 4: CV Score Distribution ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor=NETFLIX_DARK)
ax.set_facecolor(NETFLIX_DARK)

ax.bar(range(1, 6), cv_scores, color=NETFLIX_RED, edgecolor='none', width=0.5)
ax.axhline(cv_scores.mean(), color='white', linestyle='--', linewidth=2,
           label=f'Mean: {cv_scores.mean():.4f}')
ax.set_ylim(0.9, 1.0)
ax.set_title('5-Fold Cross-Validation Accuracy', color='white',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Fold', color='white', fontsize=12)
ax.set_ylabel('Accuracy', color='white', fontsize=12)
ax.tick_params(colors='white')
ax.legend(facecolor='#333', labelcolor='white', fontsize=11)
ax.spines['bottom'].set_color('white'); ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False);    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('outputs/ml/cv_scores.png', facecolor=NETFLIX_DARK, bbox_inches='tight')
plt.close()
print("✅ CV scores chart saved.")

# ── Save Model & Results Summary ─────────────────────────────────────────────
summary = {
    'accuracy': acc,
    'auc': auc,
    'cv_mean': cv_scores.mean(),
    'cv_std': cv_scores.std()
}
pd.DataFrame([summary]).to_csv('outputs/ml/model_summary.csv', index=False)

print("\n🎉 ML phase complete!")
print(f"   Final Accuracy: {acc*100:.2f}%")
print(f"   AUC:            {auc:.4f}")
print("   All charts saved to outputs/ml/")
