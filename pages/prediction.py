import streamlit as st
from utils.sidebar import show_sidebar

show_sidebar()
import pandas as pd

from utils.db import get_dashboard_data
from utils.predictor import predict_performance

# ==========================
# LOGIN CHECK
# ==========================

if "logged_in" not in st.session_state:
    st.error("Please login first.")
    st.stop()

if not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

# ==========================
# PAGE TITLE
# ==========================

st.title("🎯 Performance Prediction")

# ==========================
# LOAD DATA
# ==========================

data = get_dashboard_data(
    st.session_state.user_id
)

if not data:
    st.warning(
        "No daily updates available. Please submit data first."
    )
    st.stop()

# ==========================
# DATAFRAME
# ==========================

df = pd.DataFrame(
    data,
    columns=[
        "Date",
        "Study Hours",
        "Attendance",
        "Sleep Hours",
        "Mood"
    ]
)

# ==========================
# CALCULATIONS
# ==========================

avg_study = df["Study Hours"].mean()

avg_sleep = df["Sleep Hours"].mean()

attendance_percent = (
    (df["Attendance"] == "Present").mean()
) * 100

most_common_mood = (
    df["Mood"].mode()[0]
)

# ==========================
# RULE-BASED SCORING
# ==========================

if avg_study >= 8:
    study_score = 40

elif avg_study >= 6:
    study_score = 30

elif avg_study >= 4:
    study_score = 20

else:
    study_score = 10

# Attendance Score

if attendance_percent >= 90:
    attendance_score = 30

elif attendance_percent >= 75:
    attendance_score = 20

elif attendance_percent >= 60:
    attendance_score = 10

else:
    attendance_score = 5

# Sleep Score

if 7 <= avg_sleep <= 9:
    sleep_score = 20

elif avg_sleep >= 6:
    sleep_score = 15

else:
    sleep_score = 5

# Mood Score

if most_common_mood == "Good":
    mood_score = 10

elif most_common_mood == "Average":
    mood_score = 7

else:
    mood_score = 3

# ==========================
# RULE-BASED SCORE
# ==========================

prediction_score = (
    study_score +
    attendance_score +
    sleep_score +
    mood_score
)

# ==========================
# ML PREDICTION
# ==========================

ml_score = predict_performance(
    avg_study,
    attendance_percent,
    avg_sleep,
    most_common_mood
)

# ==========================
# FINAL AI SCORE
# ==========================

final_score = round(
    (prediction_score + ml_score) / 2,
    2
)

# ==========================
# PERFORMANCE CATEGORY
# ==========================

if final_score >= 85:

    category = "🟢 Excellent"
    risk = "🟢 Low Risk"

elif final_score >= 70:

    category = "🔵 Good"
    risk = "🟡 Moderate Risk"

elif final_score >= 50:

    category = "🟡 Average"
    risk = "🟠 High Risk"

else:

    category = "🔴 Poor"
    risk = "🔴 Critical Risk"

# ==========================
# SCORE DISPLAY
# ==========================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "Rule-Based Score",
        f"{prediction_score}/100"
    )

with col2:

    st.metric(
        "ML Prediction",
        f"{ml_score}/100"
    )

with col3:

    st.metric(
        "Final AI Score",
        f"{final_score}/100"
    )

with col4:

    st.metric(
        "Performance Level",
        category
    )

with col5:

    st.metric(
        "Risk Level",
        risk
    )

# ==========================
# FACTORS
# ==========================

st.divider()

st.subheader("📊 Prediction Factors")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Avg Study Hours",
        round(avg_study, 2)
    )

with c2:

    st.metric(
        "Attendance %",
        round(attendance_percent, 2)
    )

with c3:

    st.metric(
        "Avg Sleep",
        round(avg_sleep, 2)
    )

with c4:

    st.metric(
        "Mood",
        most_common_mood
    )

# ==========================
# RECOMMENDATIONS
# ==========================

st.divider()

st.subheader("💡 Recommendations")

if avg_study < 6:

    st.warning(
        "📚 Increase study hours to at least 6 hours per day."
    )

else:

    st.success(
        "📚 Good study consistency maintained."
    )

if attendance_percent < 90:

    st.warning(
        "📅 Improve attendance to above 90%."
    )

else:

    st.success(
        "📅 Excellent attendance record."
    )

if avg_sleep < 7:

    st.warning(
        "😴 Sleep at least 7-8 hours daily."
    )

else:

    st.success(
        "😴 Healthy sleep pattern detected."
    )

if most_common_mood != "Good":

    st.warning(
        "😊 Maintain positive mood for better academic performance."
    )

else:

    st.success(
        "😊 Positive mood trend detected."
    )

# ==========================
# AI SUMMARY
# ==========================

st.divider()

st.subheader("🤖 AI Prediction Summary")

st.info(
    f"""
📊 Rule-Based Score: {prediction_score}/100

🤖 ML Prediction Score: {ml_score}/100

🎯 Final AI Score: {final_score}/100

📈 Performance Level: {category}

⚠️ Risk Status: {risk}
"""
)

# ==========================
# FINAL VERDICT
# ==========================

st.divider()

st.subheader("🏆 Final Verdict")

if final_score >= 85:

    st.success(
        "Excellent academic performance predicted. Keep maintaining your current habits."
    )

elif final_score >= 70:

    st.info(
        "Good academic performance predicted. A little improvement in study consistency can further increase your score."
    )

elif final_score >= 50:

    st.warning(
        "Average performance predicted. Focus on improving study hours and attendance."
    )

else:

    st.error(
        "High academic risk detected. Immediate improvement in study habits is recommended."
    )