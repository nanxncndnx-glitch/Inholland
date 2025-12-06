import os
import sqlite3 as sql
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu

from . import Detector

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
        st.header(f"Welcome :violet[{first_name}]", divider = "grey")

        selected = option_menu("DashBoard", ['Home', 'Detector', 'A', 'Settings'], 
            icons=['house', 'robot', 'microsoft-teams', 'gear'], default_index=1,
                styles={
        "container": {"padding": "important", "background-color": "#0F161E", "border-radius" : "10px"},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"10px", "--hover-color": "transparent", "border-radius" : "10px"},
        "nav-link-selected": {"background-color": "#CF9AC4"},
        }
    )

    if selected == "Detector":
        Detector.Model()
