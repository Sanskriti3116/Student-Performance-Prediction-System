import streamlit as st
from utils.auth import register_student, login_student
from utils.sidebar import show_sidebar
from utils.db import create_students_table, create_daily_updates_table

st.set_page_config(
    page_title="Student Performance Prediction System",
    page_icon="🎓",
    layout="wide"
)

show_sidebar()

# Create database tables if they don't exist
create_students_table()
create_daily_updates_table()

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None




# ==========================
# LOGGED IN USER
# ==========================

if st.session_state.logged_in:

    
    st.markdown(
        """
        <div style='text-align:center;padding-top:20px'>
            <h1>🎓 Student Performance Prediction System</h1>
            <h3 style='color:gray;'>
                Track academic performance and predict future results using AI
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "📚 Study Hours\n\nMonitor daily study activity"
        )

    with col2:
        st.success(
            "🗓️ Attendance\n\nTrack attendance percentage"
        )

    with col3:
        st.warning(
            "😴 Sleep & Mood\n\nAnalyze health habits"
        )

    st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.success(
            "🤖 AI Prediction\n\nPredict performance score"
        )

    with col5:
        st.info(
            "📈 Analytics\n\nView charts and trends"
        )

    with col6:
        st.success(
            "📄 PDF Reports\n\nDownload performance reports"
        )

    st.divider()



    st.markdown("""
### 🚀 Quick Start

1. Go to Daily Update

2. Add study hours, attendance, sleep and mood

3. Open Dashboard for insights

4. Open Prediction for AI score

5. Download report from Report Page
""")

# ==========================
# NOT LOGGED IN
# ==========================

else:

    st.markdown(
        """
        <div style='text-align:center;padding-top:20px'>
            <h1>🎓 Student Performance Prediction System</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.radio(
        "Select Option",
        ["Login", "Register"],
        horizontal=True
    )

    if menu == "Register":

        st.subheader("Student Registration")

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )
        department = st.text_input("Department")
        semester = st.text_input("Semester")

        if st.button("Register"):

            try:
                register_student(
                    name,
                    email,
                    password,
                    department,
                    semester
                )

                st.success(
                    "Registration Successful!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    if menu == "Login":

        st.subheader("Student Login")

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_student(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.user_name = user[1]

                st.rerun()

            else:

                st.error(
                    "Invalid Email or Password"
                )