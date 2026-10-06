import streamlit as st

# Configure page settings (page icon removed)
st.set_page_config(
    page_title="Hospital Management System - Portal", layout="centered"
)

# Custom CSS to force clean white background, dark text, blue buttons, and green Log Out button
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
        color: #2c3e50;
    }
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTimeInput label, .stTextArea label {
        color: #2c3e50 !important;
        font-weight: bold;
    }
    /* Style all regular and form submit buttons to be blue with white text by default */
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #3498db !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background-color: #2980b9 !important;
        color: white !important;
    }
    /* Style the Log Out button specifically to be green */
    div.stButton > button:has(p:contains("Log Out")), div.stButton > button:has(div:contains("Log Out")) {
        background-color: #2ecc71 !important;
    }
    div.stButton > button:has(p:contains("Log Out")):hover, div.stButton > button:has(div:contains("Log Out")):hover {
        background-color: #27ae60 !important;
    }
    /* Force light background and blue border for input fields */
    input, textarea, select {
        background-color: #f8f9fa !important;
        color: #2c3e50 !important;
        border: 1px solid #3498db !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

# Persistent database data across navigation (including Patient ID and address)
if "patients" not in st.session_state:
    st.session_state.patients = [
        {"id": "PAT-001", "name": "Alice Uwase", "age": 28, "gender": "Female", "phone": "0781234567", "address": "Kigali"},
        {"id": "PAT-002", "name": "Jean Bosco", "age": 42, "gender": "Male", "phone": "0729876543", "address": "Butare"}
    ]
if "appointments" not in st.session_state:
    st.session_state.appointments = [
        {"patient": "Alice Uwase", "doctor": "Dr. Smith", "date": "2026-10-07", "time": "09:00 AM", "status": "Confirmed"}
    ]
if "bills" not in st.session_state:
    st.session_state.bills = [
        {"patient": "Alice Uwase", "service": "Consultation", "amount": 15000, "status": "Paid"}
    ]

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
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Hospital Management System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7f8c8d;'>Please log in to your account</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("Username:", value="doctor", key="input_user")
        st.text_input("Password:", type="password", value="doc123", key="input_pass")

        if st.button("Login", use_container_width=True):
            handle_login()

        if st.button("Forgotten Password?", use_container_width=True):
            st.info("Password reset instructions have been sent to your registered email address.")

    st.markdown("<br><br><p style='text-align: center; color: #95a5a6; font-style: italic;'>DEVELOPED BY - FEYI GROUP LTD</p>", unsafe_allow_html=True)

# ---------------- MAIN DASHBOARD SCREEN ----------------
else:
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Hospital Management System</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #7f8c8d;'>Welcome, <b>{st.session_state.name}</b>!</p>", unsafe_allow_html=True)

    if st.session_state.current_module == "dashboard":
        st.markdown("<h3 style='text-align: center; color: #34495e;'>Select a section to open:</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏥 Patient Registration", use_container_width=True):
                st.session_state.current_module = "patient_registration"
                st.rerun()

            if st.button("📅 Appointment Booking", use_container_width=True):
                st.session_state.current_module = "appointment_booking"
                st.rerun()

            if st.button("🩺 Doctor Dashboard", use_container_width=True):
                st.session_state.current_module = "doctor_dashboard"
                st.rerun()

            if st.button("💳 Billing & Payment", use_container_width=True):
                st.session_state.current_module = "billing"
                st.rerun()

            if st.button("🚪 Log Out", use_container_width=True):
                logout()
                st.rerun()

    else:
        if st.button("⬅ Back to Main Menu"):
            st.session_state.current_module = "dashboard"
            st.rerun()

        st.markdown("---")

        # 1. PATIENT REGISTRATION MODULE
        if st.session_state.current_module == "patient_registration":
            st.subheader("🏥 Patient Registration Portal")
            st.write("Add and manage patient records in the system.")

            with st.form("reg_form"):
                patient_id = st.text_input("Patient ID", value=f"PAT-{len(st.session_state.patients)+1:03d}")
                c1, c2 = st.columns(2)
                with c1:
                    f_name = st.text_input("First Name")
                    age = st.number_input("Age", min_value=0, max_value=130, value=23)
                with c2:
                    l_name = st.text_input("Last Name")
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                
                phone = st.text_input("Phone Number")
                address = st.text_input("Residential Address")
                
                submitted = st.form_submit_button("Register Patient")
                if submitted:
                    if patient_id and f_name and l_name and phone and address:
                        full_name = f"{f_name} {l_name}"
                        st.session_state.patients.append({
                            "id": patient_id, 
                            "name": full_name, 
                            "age": age, 
                            "gender": gender, 
                            "phone": phone,
                            "address": address
                        })
                        st.success(f"Patient {full_name} (ID: {patient_id}) registered successfully!")
                    else:
                        st.error("Please fill in Patient ID, First Name, Last Name, Phone Number, and Address.")

            st.markdown("### 📋 Registered Patients Directory")
            if st.session_state.patients:
                st.dataframe(st.session_state.patients, use_container_width=True)
            else:
                st.info("No records found.")

        # 2. APPOINTMENT BOOKING MODULE
        elif st.session_state.current_module == "appointment_booking":
            st.subheader("📅 Appointment Booking Portal")
            st.write("Schedule doctor appointments for registered patients.")

            patient_names = [p["name"] for p in st.session_state.patients]
            if not patient_names:
                st.warning("Please register at least one patient first.")
            else:
                with st.form("appt_form"):
                    sel_patient = st.selectbox("Select Patient", patient_names)
                    sel_doctor = st.selectbox("Assign Doctor", ["Dr. Smith", "Dr. Jean Bosco", "Dr. Alice Mukamana"])
                    appt_date = st.date_input("Appointment Date")
                    appt_time = st.selectbox("Time Slot", ["09:00 AM", "10:30 AM", "02:00 PM", "04:00 PM"])

                    appt_submitted = st.form_submit_button("Confirm Booking")
                    if appt_submitted:
                        st.session_state.appointments.append({
                            "patient": sel_patient,
                            "doctor": sel_doctor,
                            "date": str(appt_date),
                            "time": appt_time,
                            "status": "Confirmed"
                        })
                        st.success(f"Appointment scheduled for {sel_patient} with {sel_doctor}!")

            st.markdown("### 📋 Scheduled Appointments")
            if st.session_state.appointments:
                st.dataframe(st.session_state.appointments, use_container_width=True)
            else:
                st.info("No scheduled appointments.")

        # 3. DOCTOR DASHBOARD MODULE
        elif st.session_state.current_module == "doctor_dashboard":
            st.subheader("🩺 Doctor Dashboard Portal")
            st.write(f"Consultation workspace for **{st.session_state.name}**.")

            st.markdown("### 📋 Patient Queue")
            doc_appts = [a for a in st.session_state.appointments if a['doctor'] == st.session_state.name or st.session_state.username == 'admin']
            if doc_appts:
                st.dataframe(doc_appts, use_container_width=True)
            else:
                st.info("No active queue entries.")

            st.markdown("### 📝 Diagnosis & Prescription Form")
            pat_list = [p["name"] for p in st.session_state.patients] if st.session_state.patients else []
            if pat_list:
                chosen_pat = st.selectbox("Select Patient", pat_list)
                diagnosis = st.text_area("Medical Diagnosis")
                prescription = st.text_area("Prescribed Medications & Notes")
                if st.button("Save Medical Record"):
                    st.success(f"Medical notes saved successfully for {chosen_pat}!")
            else:
                st.info("No patients available for diagnosis.")

        # 4. BILLING & PAYMENT MODULE
        elif st.session_state.current_module == "billing":
            st.subheader("💳 Billing & Payment Portal")
            st.write("Generate bills and check payment processing statuses.")

            pat_list = [p["name"] for p in st.session_state.patients]
            if not pat_list:
                st.warning("No patients available for billing.")
            else:
                with st.form("bill_form"):
                    b_patient = st.selectbox("Select Patient", pat_list)
                    service = st.selectbox("Service Type", ["Consultation Fee", "Laboratory Tests", "Pharmacy / Medication", "Ward Admission"])
                    amount = st.number_input("Amount (RWF)", min_value=0, value=10000, step=1000)
                    status = st.selectbox("Payment Status", ["Paid", "Pending"])

                    bill_submitted = st.form_submit_button("Generate Bill")
                    if bill_submitted:
                        st.session_state.bills.append({
                            "patient": b_patient,
                            "service": service,
                            "
