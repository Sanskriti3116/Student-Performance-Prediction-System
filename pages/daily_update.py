import streamlit as st
from utils.sidebar import show_sidebar

show_sidebar()
import pandas as pd
from datetime import date

from utils.db import (
    add_daily_update,
    daily_update_exists,
    get_daily_updates
)


if "logged_in" not in st.session_state:
    st.error("Please login first.")
    st.stop()

if not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

# ==========================
# SESSION STATE
# ==========================

if "update_saved" not in st.session_state:
    st.session_state.update_saved = False

# ==========================
# PAGE TITLE
# ==========================

st.title("📝 Daily Update")

if st.session_state.update_saved:
    st.success("Daily Update Saved Successfully!")
    st.session_state.update_saved = False

st.subheader("Enter Today's Progress")

# ==========================
# FORM
# ==========================

selected_date = st.date_input(
    "Date",
    value=date.today(),
    format="DD/MM/YYYY",
    max_value=date.today()
)

study_hours = st.number_input(
    "Study Hours Today",
    min_value=0.0,
    max_value=24.0,
    step=0.5,
    value=5.0
)

attendance = st.selectbox(
    "Attendance",
    ["Present", "Absent"]
)

sleep_hours = st.number_input(
    "Sleep Hours Last Night",
    min_value=0.0,
    max_value=24.0,
    step=0.5,
    value=8.0
)

mood = st.selectbox(
    "Mood",
    ["Good", "Average", "Bad"]
)

# ==========================
# SAVE DATA
# ==========================

if st.button("Submit Daily Update"):

    formatted_date = selected_date.strftime("%d/%m/%Y")

    if daily_update_exists(
        st.session_state.user_id,
        formatted_date
    ):

        st.error(
            "You have already submitted an update for this date."
        )

    else:

        try:

            add_daily_update(
                st.session_state.user_id,
                formatted_date,
                study_hours,
                attendance,
                sleep_hours,
                0,
                0,
                mood,
                0,
                0,
                ""
            )

            st.session_state.update_saved = True
            st.rerun()

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

# ==========================
# HISTORY
# ==========================

st.divider()

with st.expander(
    "📊 View Previous Daily Updates",
    expanded=False
):

    history = get_daily_updates(
        st.session_state.user_id
    )

    if history:

        df = pd.DataFrame(
            history,
            columns=[
                "Date",
                "Study Hours",
                "Attendance",
                "Sleep Hours",
                "Mood"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No daily updates found."
        )