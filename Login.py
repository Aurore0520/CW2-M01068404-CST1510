import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

#__Initialise session state__
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
   st.session_role = ""

#Initialize database and auth manager
db = DatabaseManager("database/intelligence_plaform.db")
auth = AuthManager(db)

st.title(" Welcome")

#__LOGIN TAB__
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
      user = auth.login_user(login_username, login_password) #returns role if valid

      if user is None:
        st.error("Invalid username or password")
          
      else: 
          st.session_state.logged_in = True
          st.session_state.username = user.get_username()
          st.session_state.role = user.get_role()
          st.success(f"Login successful for **{user.get_username()}**")
          st.rerun()

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
     elif auth.user_exists(new_username):
        st.error("Username already exists")
     else:
        auth.register_user(new_username, new_password, role)
        st.success("Registration successful! You can now log in.")

#If already logged in, go straight to dashboard
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username} ** ")
    if st.button("Go to dashboard"):
        #Use the official navigation API to switch pages
        st.switch_page("Pages/Dataset_metadata.py")

    #Don't show login/Register again
    st.stop() 
    




