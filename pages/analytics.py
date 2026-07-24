import streamlit as st
from utils.sidebar import show_sidebar

show_sidebar()
import pandas as pd

from utils.db import get_dashboard_data

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

st.title("📈 Analytics")

# ==========================
# LOAD DATA
# ==========================

data = get_dashboard_data(
    st.session_state.user_id
)

if not data:
    st.warning(
        "No data available. Please submit daily updates first."
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

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d/%m/%Y"
)

# ==========================
# ATTENDANCE ANALYSIS
# ==========================

st.subheader("🗓️ Attendance Analysis")

present_days = (
    df["Attendance"] == "Present"
).sum()

absent_days = (
    df["Attendance"] == "Absent"
).sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Present Days",
        present_days
    )

with col2:
    st.metric(
        "Absent Days",
        absent_days
    )

attendance_counts = (
    df["Attendance"]
    .value_counts()
)

st.bar_chart(
    attendance_counts
)

# ==========================
# MOOD ANALYSIS
# ==========================

st.divider()

st.subheader("😊 Mood Analysis")

mood_analysis = (
    df.groupby("Mood")["Study Hours"]
    .mean()
    .round(2)
)

st.bar_chart(
    mood_analysis
)

st.dataframe(
    mood_analysis.reset_index().rename(
        columns={
            "Study Hours":
            "Average Study Hours"
        }
    ),
    use_container_width=True,
    hide_index=True
)

# ==========================
# STUDY VS SLEEP
# ==========================

st.divider()

st.subheader(
    "📊 Study Hours vs Sleep Hours"
)

comparison_df = pd.DataFrame({
    "Sleep Hours":
    df["Sleep Hours"],

    "Study Hours":
    df["Study Hours"]
})

st.line_chart(
    comparison_df
)

# ==========================
# WEEKLY PERFORMANCE
# ==========================

st.divider()

st.subheader(
    "📚 Weekly Performance"
)

weekly_df = (
    df
    .resample(
        "W",
        on="Date"
    )
    .agg({
        "Study Hours": "mean",
        "Sleep Hours": "mean"
    })
    .round(2)
)

weekly_df = weekly_df.reset_index()

weekly_df["Date"] = weekly_df["Date"].dt.strftime(
    "%d-%b-%Y"
)

weekly_df = weekly_df.rename(
    columns={
        "Date": "Week Ending"
    }
)

st.dataframe(
    weekly_df,
    use_container_width=True,
    hide_index=True
)

# ==========================
# MONTHLY REPORT
# ==========================

st.divider()

st.subheader(
    "🗓️ Monthly Report"
)

total_study = round(
    df["Study Hours"].sum(),
    2
)

avg_sleep = round(
    df["Sleep Hours"].mean(),
    2
)

attendance_percent = round(
    (
        (df["Attendance"] == "Present")
        .mean()
    ) * 100,
    2
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Study Hours",
        total_study
    )

with c2:
    st.metric(
        "Average Sleep",
        avg_sleep
    )

with c3:
    st.metric(
        "Attendance %",
        f"{attendance_percent}%"
    )

# ==========================
# ANALYTICS INSIGHTS
# ==========================

st.divider()

st.subheader(
    "🧐 Analytics Insights"
)

best_mood = (
    df.groupby("Mood")["Study Hours"]
    .mean()
    .idxmax()
)

st.success(
    f"🏆 You study best when your mood is '{best_mood}'."
)

if attendance_percent >= 90:
    st.info(
        "👍 Excellent attendance record."
    )

elif attendance_percent >= 75:
    st.info(
        "👍 Good attendance record."
    )

else:
    st.warning(
        "⚠️ Attendance needs improvement."
    )

if avg_sleep >= 7:
    st.success(
        "😴 Healthy sleep pattern detected."
    )

else:
    st.warning(
        "⚠️ Sleep duration is below recommended levels."
    )