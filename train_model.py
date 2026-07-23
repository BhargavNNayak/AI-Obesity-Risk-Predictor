import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Dataset
df = pd.read_csv("data/obesity.csv")

print(df.head())

# Encode categorical columns

from sklearn.preprocessing import LabelEncoder

label_encoders = {}

categorical_cols = df.select_dtypes(include=['object']).columns

for col in categorical_cols:

    le = LabelEncoder()

    df[col] = le.fit_transform(df[col].astype(str))

    label_encoders[col] = le
print(df.dtypes)
# Features and Target
X = df.drop("NObeyesdad", axis=1)
# Encode target labels

target_encoder = LabelEncoder()

y = target_encoder.fit_transform(
    df["NObeyesdad"]
)
# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Random Forest
rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)

print("\nRandom Forest Accuracy:", rf_accuracy)

# Gradient Boosting
gb_model = GradientBoostingClassifier()

gb_model.fit(X_train, y_train)

gb_pred = gb_model.predict(X_test)

gb_accuracy = accuracy_score(y_test, gb_pred)

print("\nGradient Boosting Accuracy:", gb_accuracy)

# Select Best Model
best_model = rf_model if rf_accuracy > gb_accuracy else gb_model

# Save model
joblib.dump(best_model, "models/obesity_model.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

# Save encoders
joblib.dump(label_encoders, "models/label_encoders.pkl")

print("\nModel Saved Successfully!")

# Classification Report
print("\nClassification Report:\n")
print(classification_report(y_test, rf_pred))
import matplotlib.pyplot as plt

importance = rf_model.feature_importances_

features = X.columns

plt.figure(figsize=(10,6))

plt.barh(features, importance)

plt.xlabel("Importance")

plt.ylabel("Features")

plt.title("Feature Importance")

plt.show()
