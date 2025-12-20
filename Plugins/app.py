import os
import sqlite3 as sql
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu

from .styles import (
    GLASS_SIDEBAR_CSS,
    MENU_STYLES,
    get_profile_card_html,
    GLASS_DIVIDER_HTML,
    GLASS_FOOTER_STATS_HTML,
    GLASS_VERSION_BADGE_HTML
)

from . import Detector

# Apply CSS
st.markdown(GLASS_SIDEBAR_CSS, unsafe_allow_html=True)

def createPage(username, first_name):
    #loadin data from .env and connecting database =>
    load_dotenv()
    BASE_DIR = os.getenv("DB_path")
    db_user = os.path.join(BASE_DIR, "Storage.db")
    conn = sql.connect(db_user)
    c = conn.cursor()

    #Extracting name of the gym =>
    gymname = c.execute(f""" SELECT GymName FROM USERS WHERE username = '{username}'; """)

    with st.sidebar:
        # Profile Card
        st.markdown(get_profile_card_html(first_name), unsafe_allow_html=True)
    
        # Navigation Menu
        selected = option_menu(
            menu_title=None,
            options=['Home', 'Detector', 'Analytics', 'Settings'], 
            icons=['house-fill', 'robot', 'bar-chart-fill', 'gear-fill'], 
            default_index=0,
            styles=MENU_STYLES
        )

        # Glass Divider
        st.markdown(GLASS_DIVIDER_HTML, unsafe_allow_html=True)
    
        # Glass Footer Stats
        st.markdown(GLASS_FOOTER_STATS_HTML, unsafe_allow_html=True)
    
        # Glass Version Badge
        st.markdown(GLASS_VERSION_BADGE_HTML, unsafe_allow_html=True)

    if selected == "Detector":
        Detector.Model()
