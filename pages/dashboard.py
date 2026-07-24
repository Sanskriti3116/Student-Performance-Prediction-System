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

st.title("📊 Dashboard")

# ==========================
# LOAD DATA
# ==========================

data = get_dashboard_data(
    st.session_state.user_id
)

if not data:
    st.warning(
        "No daily updates found. Please submit some daily updates first."
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

# Convert Date column
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d/%m/%Y"
)

# Sort by date
df = df.sort_values("Date")

# ==========================
# BASIC CALCULATIONS
# ==========================

total_study_hours = df["Study Hours"].sum()

average_sleep_hours = round(
    df["Sleep Hours"].mean(),
    2
)

attendance_percentage = round(
    (df["Attendance"] == "Present").mean() * 100,
    2
)

total_updates = len(df)

# ==========================
# STUDY STREAK
# ==========================

streak = 0

dates = list(df["Date"])

for i in range(len(dates) - 1):

    difference = (
        dates[i + 1] - dates[i]
    ).days

    if difference == 1:
        streak += 1

if len(dates) > 0:
    streak += 1

# ==========================
# BEST STUDY DAY
# ==========================

best_day_row = df.loc[
    df["Study Hours"].idxmax()
]

best_day = best_day_row["Date"].strftime(
    "%d/%m/%Y"
)

best_hours = best_day_row["Study Hours"]

# ==========================
# ATTENDANCE STATUS
# ==========================

if attendance_percentage >= 90:
    attendance_status = "Excellent"

elif attendance_percentage >= 75:
    attendance_status = "Good"

else:
    attendance_status = "Needs Improvement"

# ==========================
# DASHBOARD CARDS
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Total Study Hours",
        f"{total_study_hours:.1f}"
    )

with col2:
    st.metric(
        "😴 Avg Sleep Hours",
        average_sleep_hours
    )

with col3:
    st.metric(
        "📅 Attendance %",
        f"{attendance_percentage}%"
    )

with col4:
    st.metric(
        "📝 Total Updates",
        total_updates
    )

st.divider()

# ==========================
# ADVANCED CARDS
# ==========================

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"🔥 Current Study Streak\n\n{streak} Days"
    )

with col2:
    st.info(
        f"🏆 Best Study Day\n\n{best_day}\n\n{best_hours} Hours"
    )

with col3:
    st.warning(
        f"📊 Attendance Status\n\n{attendance_status}"
    )

# ==========================
# LAST 30 DAYS
# ==========================

last_30_days = df.tail(30)

# ==========================
# STUDY HOURS GRAPH
# ==========================

st.divider()

st.subheader("📈 Study Hours Trend (Last 30 Records)")

study_chart = last_30_days[
    ["Date", "Study Hours"]
].set_index("Date")

st.line_chart(study_chart)

# ==========================
# SLEEP GRAPH
# ==========================

st.divider()

st.subheader("😴 Sleep Hours Trend (Last 30 Records)")

sleep_chart = last_30_days[
    ["Date", "Sleep Hours"]
].set_index("Date")

st.line_chart(sleep_chart)

# ==========================
# WEEKLY AVERAGE
# ==========================

st.divider()

st.subheader("📅 Weekly Average Study Hours")

weekly_avg = (
    df
    .set_index("Date")
    .resample("W")["Study Hours"]
    .mean()
)

st.bar_chart(weekly_avg)

# ==========================
# MOOD DISTRIBUTION
# ==========================

st.divider()

st.subheader("😊 Mood Distribution")

mood_counts = df["Mood"].value_counts()

st.bar_chart(mood_counts)

# ==========================
# PERFORMANCE INSIGHTS
# ==========================

st.divider()

st.subheader("🤖 AI Performance Insights")

if len(df) >= 2:

    recent = df.tail(7)

    previous = df.head(
        max(
            len(df) - len(recent),
            1
        )
    )

    recent_study = recent[
        "Study Hours"
    ].mean()

    previous_study = previous[
        "Study Hours"
    ].mean()

    recent_sleep = recent[
        "Sleep Hours"
    ].mean()

    previous_sleep = previous[
        "Sleep Hours"
    ].mean()

    if recent_study > previous_study:

        increase = round(
            (
                (recent_study - previous_study)
                / previous_study
            ) * 100,
            1
        )

        st.success(
            f"✅ Study hours increased by {increase}%."
        )

    elif recent_study < previous_study:

        st.warning(
            "⚠️ Study hours have decreased recently."
        )

    if recent_sleep < previous_sleep:

        st.warning(
            "⚠️ Sleep hours decreased in recent days."
        )

    else:

        st.success(
            "😴 Sleep pattern is stable."
        )

else:

    st.info(
        "Add more daily updates to generate AI insights."
    )