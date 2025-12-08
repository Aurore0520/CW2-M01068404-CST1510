import streamlit as st
import pandas as pd
import os
from app.services.user_service import register_user, login_user

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

#__Initialise session state__
if "users" not in st.session_state:
    users = {}
    if os.path.exists("users.txt"):
       with open("users.txt", "r") as f:
           for line in f:
                line = line.strip()
                if line:
                 username, password = line.split(",", 1)
                 users[username.strip()] = password.strip() 
    st.session_state.users = users 

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
   st.session_role = ""

st.title(" Welcome")

#__LOGIN TAB__
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
      role = login_user(login_username, login_password) #returns role if valid

      if role:
          st.session_state.logged_in = True
          st.session_state.username = login_username
          st.success("Login successful")
          st.rerun()
      else: 
          st.error("Invalid username or password")

#__Register tab__
with tab_register: 
  st.subheader("Register")

  new_username = st.text_input("Choose a username", key="register_username")
  new_password =st.text_input("Choose a password", key="register_password")
  confirm_password = st.text_input("Confirm password",type="password", key="register_confirm")
  role = st.selectbox("Role", ["data_scientist", "analyst", "admin"])

  if st.button("Register", key="register_button"):
     if new_password != confirm_password:
        st.error("Passwords don't match")
     elif new_username in st.session_state.users:
        st.error("Username already exists")
     else:
        register_user(new_username, new_password, role)
        st.success("Registration successful! You can now log in.")

        with open("users.txt", "a") as f:
          f.write(f"{new_username}, {new_password}\n")
        st.success("Registration successful! You can now log in.")

#If already logged in, go straight to dashboard
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username} ** ")
    if st.button("Go to dashboard"):
        #Use the official navigation API to switch pages
        st.switch_page("Pages/1_Dashboard.py")

    #Don't show login/Register again
    st.stop() 
    




