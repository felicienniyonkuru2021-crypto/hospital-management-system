import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state for login status if it doesn't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Initialize Data Session States
if 'patients' not in st.session_state:
    st.session_state.patients = []
if 'appointments' not in st.session_state:
    st.session_state.appointments = []
if 'bills' not in st.session_state:
    st.session_state.bills = []

# Function to handle login verification
def login_screen():
    st.title("🏥 Hospital Portal - Login")
    st.markdown("Please enter your credentials to access the system.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")

# Check if user is logged in
if not st.session_state.logged_in:
    login_screen()
else:
    # Sidebar logout option
    st.sidebar.title("Hospital Portal")
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

    # --- HORIZONTAL TABS NAVIGATION ---
    tab_home, tab_reg, tab_appt, tab_doc, tab_bill = st.tabs([
        "Home", 
        "Patient Registration", 
        "Appointment Booking", 
        "Doctor Dashboard", 
        "Billing Module"
    ])

    # --- HOME / DASHBOARD ---
    with tab_home:
        st.title("Welcome to the Hospital Management System")
        st.write("Streamlining healthcare administrative operations with digital workflows.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Registered Patients", len(st.session_state.patients))
        col2.metric("Scheduled Appointments", len(st.session_state.appointments))
        col3.metric("Generated Bills", len(st.session_state.bills))

        st.info("Use the horizontal tabs above to navigate through different administrative modules.")

    # --- PATIENT REGISTRATION ---
    with tab_reg:
        st.header("👤 Patient Registration Module")

        with st.form("patient_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=0, max_value=120, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            phone = st.text_input("Phone Number")
            address = st.text_area("Address")
            submit_patient = st.form_submit_button("Register Patient")

            if submit_patient:
                if name and phone:
                    patient_id = f"PAT-{len(st.session_state.patients) + 1:03d}"
                    st.session_state.patients.append({
                        "ID": patient_id,
                        "Name": name,
                        "Age": age,
                        "Gender": gender,
                        "Phone": phone,
                        "Address": address
                    })
                    st.success(f"Patient {name} successfully registered with ID: {patient_id}")
                else:
                    st.error("Please fill in at least the Name and Phone Number.")

        if st.session_state.patients:
            st.subheader("Current Patient Records")
            st.dataframe(pd.DataFrame(st.session_state.patients))

    # --- APPOINTMENT BOOKING ---
    with tab_appt:
        st.header("📅 Appointment Booking Module")

        if not st.session_state.patients:
            st.warning("Please register at least one patient first.")
        else:
            patient_names = [p["Name"] for p in st.session_state.patients]

            with st.form("appointment_form"):
                selected_patient = st.selectbox("Select Patient", patient_names)
                doctor = st.selectbox("Assign Doctor",
                                     ["Dr. Smith (Cardiology)", "Dr. Jones (Pediatrics)", "Dr. Alice (General Medicine)"])
                date = st.date_input("Appointment Date", datetime.today())
                time = st.time_input("Appointment Time")
                submit_appt = st.form_submit_button("Book Appointment")

                if submit_appt:
                    st.session_state.appointments.append({
                        "Patient": selected_patient,
                        "Doctor": doctor,
                        "Date": str(date),
                        "Time": str(time),
                        "Status": "Confirmed"
                    })
                    st.success(f"Appointment booked successfully for {selected_patient} with {doctor}!")

        if st.session_state.appointments:
            st.subheader("Scheduled Appointments")
            st.dataframe(pd.DataFrame(st.session_state.appointments))

    # --- DOCTOR DASHBOARD ---
    with tab_doc:
        st.header("🩺 Doctor Dashboard")

        if not st.session_state.appointments:
            st.info("No appointments scheduled yet.")
        else:
            st.subheader("Today's Patient Queue")
            appt_df = pd.DataFrame(st.session_state.appointments)
            st.dataframe(appt_df)

            doc_selected = st.selectbox("Filter by Doctor", appt_df["Doctor"].unique())
            filtered_df = appt_df[appt_df["Doctor"] == doc_selected]
            st.write(f"Queue for {doc_selected}:")
            st.dataframe(filtered_df)

    # --- BILLING SYSTEM ---
    with tab_bill:
        st.header("💳 Billing & Payments Module")

        if not st.session_state.patients:
            st.warning("No patients available to bill.")
        else:
            patient_names = [p["Name"] for p in st.session_state.patients]

            with st.form("billing_form"):
                bill_patient = st.selectbox("Select Patient for Billing", patient_names)
                consultation_fee = st.number_input("Consultation Fee", min_value=0.0, value=50.0)
                lab_fee = st.number_input("Laboratory Charges", min_value=0.0, value=20.0)
                medication_fee = st.number_input("Medication Charges", min_value=0.0, value=15.0)
                currency = st.selectbox("Currency", ["USD ($)", "RWF (FRW)"])

                submit_bill = st.form_submit_button("Generate Bill")

                if submit_bill:
                    total = consultation_fee + lab_fee + medication_fee
                    st.session_state.bills.append({
                        "Patient": bill_patient,
                        "Consultation": consultation_fee,
                        "Lab": lab_fee,
                        "Medication": medication_fee,
                        "Total": total,
                        "Currency": currency.split()[0]
                    })
                    st.success(f"Bill generated successfully! Total amount: {total} {currency.split()[0]}")

        if st.session_state.bills:
            st.subheader("Generated Invoices")
            st.dataframe(pd.DataFrame(st.session_state.bills))
