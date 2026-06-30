import streamlit as st
import httpx

API_URL = "http://localhost:8000/api/v1"

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        try:
            response = httpx.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state["token"] = token
                st.sidebar.success("Logged in successfully!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
        except Exception as e:
            st.sidebar.error(f"Error connecting to backend: {e}")

def check_auth():
    if "token" not in st.session_state:
        login()
        return False
    return True

def get_auth_headers():
    if "token" in st.session_state:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}
