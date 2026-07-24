import streamlit as st
from utils.sidebar import show_sidebar

show_sidebar()
import pandas as pd

from utils.db import (
    get_student,
    get_dashboard_data
)

from utils.pdf_generator import generate_report_pdf



# ==========================
# LOGIN CHECK
# ==========================

if "logged_in" not in st.session_state:
    st.stop()

if not st.session_state.logged_in:
    st.stop()

# ==========================
# LOAD DATA
# ==========================

student = get_student(
    st.session_state.user_id
)

data = get_dashboard_data(
    st.session_state.user_id
)

if not data:

    st.warning(
        "No data available."
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

total_study_hours = round(
    df["Study Hours"].sum(),
    2
)

avg_sleep = round(
    df["Sleep Hours"].mean(),
    2
)

attendance_percent = round(
    (df["Attendance"] == "Present").mean() * 100,
    2
)

avg_study = round(
    df["Study Hours"].mean(),
    2
)

# ==========================
# PERFORMANCE SCORE
# ==========================

score = round(
    (
        avg_study * 5
        + attendance_percent * 0.4
        + avg_sleep * 3
    ),
    0
)

if score > 100:
    score = 100

# ==========================
# RISK LEVEL
# ==========================

if score >= 80:

    level = "Excellent"
    risk = "Low Risk"

elif score >= 60:

    level = "Good"
    risk = "Moderate Risk"

elif score >= 40:

    level = "Average"
    risk = "High Risk"

else:

    level = "Poor"
    risk = "Critical Risk"

# ==========================
# REPORT PAGE
# ==========================

st.title("📄 Student Performance Report")

# ==========================
# STUDENT INFO
# ==========================

st.subheader("👨‍🎓 Student Information")

st.write(
    f"**Name:** {student[1]}"
)

st.write(
    f"**Email:** {student[2]}"
)

st.write(
    f"**Department:** {student[4]}"
)

st.write(
    f"**Semester:** {student[5]}"
)

# ==========================
# ACADEMIC SUMMARY
# ==========================

st.divider()

st.subheader("📊 Academic Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Study Hours",
        total_study_hours
    )

with c2:

    st.metric(
        "Attendance %",
        attendance_percent
    )

with c3:

    st.metric(
        "Performance Score",
        score
    )

with c4:

    st.metric(
        "Risk Level",
        risk
    )

# ==========================
# RECOMMENDATIONS
# ==========================

st.divider()

st.subheader("💡 Recommendations")

if avg_study < 6:

    st.warning(
        "📚 Increase study hours."
    )

else:

    st.success(
        "📚 Study hours are good."
    )

if attendance_percent < 90:

    st.warning(
        "📅 Improve attendance."
    )

else:

    st.success(
        "📅 Attendance is excellent."
    )

if avg_sleep < 7:

    st.warning(
        "😴 Increase sleep duration."
    )

else:

    st.success(
        "😴 Healthy sleep pattern."
    )

# ==========================
# PDF DOWNLOAD
# ==========================

st.divider()

st.subheader("📄 Download Report")


if st.button("Generate PDF Report"):

    generate_report_pdf(
        "Student_Report.pdf",
        student[1],
        student[2],
        student[4],
        student[5],
        attendance_percent,
        total_study_hours,
        score,
        risk,
        score,
        score,
        score,
        level
    )

    with open(
        "Student_Report.pdf",
        "rb"
    ) as pdf_file:

        st.download_button(
            label="⬇ Download PDF",
            data=pdf_file,
            file_name="Student_Report.pdf",
            mime="application/pdf"
        )


# ==========================
# DAILY RECORDS
# ==========================

st.divider()

st.subheader("📋 Daily Update Records")

st.dataframe(
    df,
    use_container_width=True
)