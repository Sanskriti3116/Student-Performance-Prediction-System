import streamlit as st


def show_sidebar():

    st.markdown("""
    <style>

    [data-testid="stSidebarNav"] {
        display: none;
    }

    section[data-testid="stSidebar"] {
        background-color: #F5F7FA;
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        border-radius: 12px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("## 📌 Navigation")

    st.sidebar.page_link(
        "app.py",
        label="🏠 Home"
    )

    st.sidebar.page_link(
        "pages/daily_update.py",
        label="📝 Daily Update"
    )

    st.sidebar.page_link(
        "pages/dashboard.py",
        label="📊 Dashboard"
    )

    st.sidebar.page_link(
        "pages/prediction.py",
        label="🤖 Prediction"
    )

    st.sidebar.page_link(
        "pages/report.py",
        label="📄 Report"
    )

    st.sidebar.markdown("---")

    if (
        "logged_in" in st.session_state
        and st.session_state.logged_in
    ):

        st.sidebar.markdown(
            f"### 👤 {st.session_state.user_name}"
        )

        st.sidebar.markdown("")

        if st.sidebar.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_name = ""

            st.rerun()