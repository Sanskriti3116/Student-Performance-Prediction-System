import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor

# ==========================
# RANDOM SEED
# ==========================

np.random.seed(42)

# ==========================
# DATASET SIZE
# ==========================

rows = 1000

# ==========================
# GENERATE FEATURES
# ==========================

study_hours = np.random.randint(
    1,
    11,
    rows
)

attendance = np.random.randint(
    50,
    101,
    rows
)

sleep_hours = np.random.randint(
    4,
    11,
    rows
)

mood = np.random.choice(
    [0, 1, 2],  # Bad, Average, Good
    rows
)

# ==========================
# REALISTIC PERFORMANCE SCORE
# ==========================

performance_score = (
    study_hours * 4 +
    attendance * 0.3 +
    sleep_hours * 2 +
    mood * 5
)

# Add randomness

performance_score += np.random.randint(
    -10,
    11,
    rows
)

# Limit range

performance_score = np.clip(
    performance_score,
    20,
    100
)

# ==========================
# DATAFRAME
# ==========================

df = pd.DataFrame({
    "StudyHours": study_hours,
    "Attendance": attendance,
    "SleepHours": sleep_hours,
    "Mood": mood,
    "PerformanceScore": performance_score
})

# ==========================
# FEATURES / TARGET
# ==========================

X = df[
    [
        "StudyHours",
        "Attendance",
        "SleepHours",
        "Mood"
    ]
]

y = df["PerformanceScore"]

# ==========================
# MODEL
# ==========================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

# ==========================
# TRAIN
# ==========================

model.fit(X, y)

# ==========================
# SAVE MODEL
# ==========================

joblib.dump(
    model,
    "models/student_model.pkl"
)

print("\n✅ Model Trained Successfully!")
print("✅ student_model.pkl created")
print(f"Dataset Size: {rows} Students")