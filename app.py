import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Hospital Management System - Portal", page_icon="🏥", layout="centered"
)

# Initialize session state variables for login and navigation tracking
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "name" not in st.session_state:
  st.session_state.name = ""
if "current_module" not in st.session_state:
  st.session_state.current_module = "dashboard"

# User database including credentials
users = {
    "admin": {"password": "pass123", "name": "Hospital Admin"},
    "doctor": {"password": "doc123", "name": "Dr. Smith"},
    "reception": {"password": "rec123", "name": "Front Desk"},
}


def handle_login():
  username = st.session_state.input_user.strip().lower()
  password = st.session_state.input_pass.strip()

  if username in users and users[username]["password"] == password:
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.name = users[username]["name"]
    st.session_state.current_module = "dashboard"
  else:
    st.error("Invalid username or password. Please try again.")


def logout():
  st.session_state.logged_in = False
  st.session_state.username = ""
  st.session_state.name = ""
  st.session_state.current_module = "dashboard"


# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
  st.markdown(
      "<h1 style='text-align: center; color: #2c3e50;'>Hospital Management"
      " System</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #7f8c8d;'>Please log in to your"
      " account</p>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.text_input("Username:", value="doctor", key="input_user")
    st.text_input("Password:", type="password", value="doc123", key="input_pass")

    if st.button("Login", use_container_width=True):
      handle_login()

    if st.button("Forgotten Password?", use_container_width=True):
      st.info(
          "Password reset instructions have been sent to your registered email"
          " address."
      )

  st.markdown(
      "<br><br><p style='text-align: center; color: #95a5a6; font-style:"
      " italic;'>DEVELOPED BY - FEYI GROUP LTD</p>",
      unsafe_allow_html=True,
  )

# ---------------- MAIN DASHBOARD SCREEN ----------------
else:
  st.markdown(
      "<h1 style='text-align: center; color: #2c3e50;'>Hospital Management"
      " System</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      f"<p style='text-align: center; color: #7f8c8d;'>Welcome, "
      f"<b>{st.session_state.name}</b>!</p>",
      unsafe_allow_html=True,
  )

  if st.session_state.current_module == "dashboard":
    st.markdown(
        "<h3 style='text-align: center; color: #34495e;'>Select a section to"
        " open:</h3>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      if st.button(" Patient Registration", use_container_width=True):
        st.session_state.current_module = "patient_registration"
        st.rerun()

      if st.button(" Appointment Booking", use_container_width=True):
        st.session_state.current_module = "appointment_booking"
        st.rerun()

      if st.button(" Doctor Dashboard", use_container_width=True):
        st.session_state.current_module = "doctor_dashboard"
        st.rerun()

      if st.button(" Billing & Payment", use_container_width=True):
        st.session_state.current_module = "billing"
        st.rerun()

      if st.button("Log Out", use_container_width=True):
        logout()
        st.rerun()

  else:
    # Display selected module view
    module_titles = {
        "patient_registration": "Patient Registration Portal",
        "appointment_booking": "Appointment Booking Portal",
        "doctor_dashboard": "Doctor Dashboard Portal",
        "billing": "Billing & Payment Portal",
    }
    current_title = module_titles.get(
        st.session_state.current_module, "Section"
    )

    st.subheader(current_title)
    st.write(f"You are currently viewing the **{current_title}** section.")

    if st.button("⬅️ Back to Main Menu"):
      st.session_state.current_module = "dashboard"
      st.rerun()

  st.markdown(
      "<br><br><p style='text-align: center; color: #95a5a6; font-style:"
      " italic;'>FEYI GROUP LTD</p>",
      unsafe_allow_html=True,
  )
