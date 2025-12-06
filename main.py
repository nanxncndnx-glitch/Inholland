import os.path
from dotenv import load_dotenv

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import altair as alt

import sqlite3 as sql

import yaml
from yaml.loader import SafeLoader

import smtplib
from email.message import EmailMessage

from Plugins import app

load_dotenv()
alt.themes.enable("dark")

#Page config =>
st.set_page_config(
    page_title = "Dashboard",
    layout = "wide"
)

#Opening the yaml file =>
with open('./Data/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

#Loadin and Connecting to the Database =>
BASE_DIR = os.getenv("DB_path")
db_user = os.path.join(BASE_DIR, "Storage.db")
conn = sql.connect(db_user)
c = conn.cursor()

def yaml2db(username, user_info, conn, c):
    #extract info from Dict value =>
    email, FirstName, LastName, password = user_info["email"], user_info["first_name"], user_info["last_name"], user_info["password"]
    c.execute(f"""INSERT INTO USERS(username, Email, FirstName, LastName, Password) VALUES('{username}', '{email}', '{FirstName}', '{LastName}', '{password}');""")
    conn.commit()

#Authenticate Configuration =>
def authentication_yaml(user_info):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    return authenticator

#SQLite database into dictionaries =>
def sql_to_dict(conn, c):
    #function for get columns and values = > 
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    conn.row_factory = dict_factory
    c = conn.cursor()

    Dict1 = { }
    Dict2 = { }
    res = c.execute(""" SELECT * FROM USERS """)
    res = res.fetchone()
    username = res["username"]
    Dict1[username] = res
    Dict2["usernames"] = Dict1

    return Dict2

if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False

@st.dialog("Additional Information")
#PopUp function =>
def popup_form(username, conn, c):
    st.write("Please provide the following information:")
    
    gymname = st.text_input("Your Gym Name")
    city = st.text_input("City", placeholder="Amsterdam, ...")
    
    if st.button("Submit", type="primary"):
        if gymname and city:
            c.execute(f""" UPDATE USERS SET City = '{city}', GymName = '{gymname}' WHERE username = '{username}'; """)

            st.session_state.show_popup = False
            st.success("Information saved Now you can Login to Your Account!")
        else:
            st.error("Please fill in both fields")


#User Registration Form =>
def register_user(authenticator, conn, c):
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user()
        if email_of_registered_user:
            #inser user info to yaml file =>
            with open('./Data/config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success('User registered successfully')

            #extract info from yaml format value =>
            username = username_of_registered_user
            for user in config['credentials'].items():
                user_info = user[1][username]

            yaml2db(username , user_info, conn, c)
            popup_form(username, conn, c)
    except Exception as e:
        st.error(e)

#Login Form =>
def Login(authenticator):
    authenticator.login()
    if st.session_state["authentication_status"]:
        name = st.session_state["name"]
        username = st.session_state["username"]
        app.createPage(username, name)

    elif st.session_state["authentication_status"] is False:
        st.error('Username or password is incorrect')

    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

#Navigation for changing the pages Login/Register and ...
navbar = option_menu(None, ["Register", "Login", "Forget Password", "About Us", "Logout"], 
    icons=['person-fill-add', 'person-fill-check', 'key', 'info-lg', 'person-fill-dash'], 
    default_index=0, orientation="horizontal",
    styles={
    "container": {"padding": "important", "background-color": "#0F161E", "border-radius" : "15px"},
    "icon": {"color": "white", "font-size": "15px"}, 
    "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "transparent", "border-radius" : "20px"},
    "nav-link-selected": {"background-color": "#CF9AC4"},
    }
)

if navbar == "Register":
    user_info = sql_to_dict(conn , c)
    authenticator = authentication_yaml(user_info)
    register_user(authenticator, conn , c)

if navbar == "Login":
    user_info = sql_to_dict(conn , c)
    authenticator = authentication_yaml(user_info)
    Login(authenticator)

if navbar == "Logout":
    if st.session_state["authentication_status"]:
        user_info = sql_to_dict(conn , c)
        authenticator = authentication_yaml(user_info)
        authenticator.logout()

#I'm gonna hard code the forget password part without using any extra lib ... =>
if navbar == "Forget Password":
    st.write("Please enter your account email here.")
    origin_email = st.text_input("Email", placeholder="asdfgh@gmail.com")

    #email configuration =>
    information = EmailMessage()
    information["Subject"] = ""
    
    if st.button("Submit", type="primary"):
        pass
