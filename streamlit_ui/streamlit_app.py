import streamlit as st
import pandas as pd
import sys, os

# Add the project root to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now your imports should work
from app.routers import fax, ifax

# Configure the Streamlit page
st.set_page_config(page_title="Veritas One", layout="wide")

# Sidebar Navigation with all pages
pages = [
    "Welcome",
    "About Us",
    "Create Account",
    "Login",
    "Dashboard (User Profile)",
    "Encounter Record",
    "Settings & Privacy",
    "Notifications",
    "Search",
    "FAQs & Support",
    "Security & Privacy Disclosures"
]
selected_page = st.sidebar.selectbox("Navigation", pages)

# ----- Welcome Page -----
if selected_page == "Welcome":
    st.title("Welcome to Veritas One")
    st.image("logo.png", width=200)  # Ensure you have a logo image file named 'logo.png'
    st.subheader("Your Personal Health Record & Data Empowerment")
    st.write(
        """
        At Veritas One, we provide you with a free, unified electronic health record (EMR)—a single place where all your medical data is securely stored, always available, and completely under your control.

        But that’s just the beginning. Unlike other platforms, we empower you to take control of your health data, allowing you to monetize it on your own terms while contributing to groundbreaking medical research and industry innovation.

        We believe your health data is one of your most valuable assets—and you should be the one to control it.

        Most hospitals, insurance companies, and tech companies already collect and use your patient data—but they do it behind closed doors, without compensating you.

        We’re different. We put you in control, allowing you to:

        - **Improve Your Own Healthcare:** Faster, better care – doctors make better decisions when they see your full medical history.
        - **Easier Second Opinions:** No more faxing records or re-explaining your history.
        - **Avoid Duplicate Tests & Procedures:** Save time, money, and unnecessary treatments.
        - **Advance Medicine & Improve Patient Care (If You Choose To):** Help researchers discover new treatments and improve existing ones.
        - **Earn Money From Your Data (Only If You Opt In):** Receive a portion of the profits generated from your data.

        At Veritas One, you own your health data, you control its use, and you benefit from it.
        """
    )
    with st.expander("How Your Health Data is Stored & Used"):
        st.write(
            """
            At Veritas One, we use a three-database system to keep your identifiable and de-identified data separate. This ensures your privacy while still allowing you to benefit from data sharing.

            **Your Personal Health Record (Your Unified EMR - Secure & Private)**
            - **What it includes:**
              - Your entire medical history—lab results, imaging, medications, provider notes, and more.
              - Data from all your past providers, hospitals, and clinics, even across different systems.
              - Ongoing updates—whenever you visit a doctor, your records are automatically updated.
            - **How it helps you:**
              - No more scrambling to track down old records.
              - No more repeating tests because one hospital can’t see what another ordered.
              - A single, comprehensive record helps you get better care.
            - **How it’s used:**
              - For personal use—access, manage, and share your records anytime.
              - For your medical care—share records instantly with doctors or family.
              - For optional personalized opportunities—if you opt in, we can match you with clinical trials, new medications, or exclusive savings.

            **Your De-Identified Data (For Research & Medical Advancements - Always Anonymous)**
            - **What it includes:**
              - Medical conditions, treatments, lab values, and imaging findings (all personal identifiers removed).
            - **Why it matters:**
              - Helps researchers identify trends in diseases and treatment effectiveness.
              - Supports public health efforts.

            **Limited Identifiable Dataset**
            - Your data is already being monetized by others—unlike them, you control your identifiable data and decide whether to opt in for personalized opportunities.
            """
        )
        # Define the table data for sharing options
        table_data = {
            "Sharing Option": [
                "Strict Privacy Mode (No Sharing)",
                "De-Identified Research Only",
                "Full Data Sharing (Research + Ads)"
            ],
            "How Your Data is Used": [
                "Your data is stored for your personal use only.",
                "Your anonymous health data is used to improve medicine and public health.",
                "Your de-identified data is used for research, AND if you opt in, limited identifiable data (such as medications) can be used for personalized health offers."
            ],
            "Compensation": [
                "No compensation.",
                "You receive 5% of research profits.",
                "You receive 15% of total profits."
            ]
        }
        df = pd.DataFrame(table_data)
        st.table(df)

# ----- About Us Page -----
elif selected_page == "About Us":
    st.title("About Veritas One")
    st.subheader("Empowering Patients Through Transparent Data Management")
    st.write(
        """
        At Veritas One, our vision is to empower patients by putting control of their healthcare data directly in their hands.
        Founded by Dr. Brandon Thomas Gaston MD—a resident physician at Massachusetts General Hospital & Harvard Medical School—we are on a mission to revolutionize how medical records and imaging data are managed and shared.

        Our free, unified electronic health record (EMR) platform consolidates your medical data from every provider and hospital into one secure, patient-centered repository. By integrating advanced technologies—from real-time FHIR API connections to secure DICOM imaging retrieval—Veritas One ensures that your complete medical history is always accessible, streamlining care, reducing repetitive tests, and enabling more informed clinical decisions.

        What sets us apart is our ethical, patient-first approach to data sharing. You decide how your information is used with three customizable sharing modes:
        - **Strict Privacy Mode:** Your data is for your eyes only.
        - **De-Identified Research Only:** Contribute anonymously to research while earning a share of the profits.
        - **Full Data Sharing (Research + Ads):** Opt in for personalized health offers and greater rewards.

        Join us on our journey to redefine the future of healthcare—where your data, your decisions, and your health truly come first.

        For inquiries, please reach out at: bgaston@mgh.harvard.edu
        """
    )

# ----- Create Account Page -----
elif selected_page == "Create Account":
    st.title("Create Account")
    st.write("Fill out the form below to create your account.")
    with st.form("create_account_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        email = st.text_input("Email")
        st.write("Digital Health Record Release Agreement")
        agree = st.checkbox("I agree to the digital health record release.")
        st.write("Select your data sharing option:")
        sharing_option = st.radio(
            "Data Sharing Options",
            (
                "Strict Privacy Mode (No Sharing)",
                "De-Identified Research Only (5% of research profits)",
                "Full Data Sharing (Research + Ads) (15% of total profits)",
            )
        )
        # Define the table data for sharing options
        table_data = {
            "Sharing Option": [
                "Strict Privacy Mode (No Sharing)",
                "De-Identified Research Only",
                "Full Data Sharing (Research + Ads)"
            ],
            "How Your Data is Used": [
                "Your data is stored for your personal use only.",
                "Your anonymous health data is used to improve medicine and public health.",
                "Your de-identified data is used for research, AND if you opt in, limited identifiable data (such as medications) can be used for personalized health offers."
            ],
            "Compensation": [
                "No compensation.",
                "You receive 5% of research profits.",
                "You receive 15% of total profits."
            ]
        }
        df = pd.DataFrame(table_data)
        st.table(df)
        submitted = st.form_submit_button("Create Account")
        if submitted:
            st.success("Account created successfully!")
            st.write(f"Welcome, {first_name} {last_name}!")

# ----- Login Page -----
elif selected_page == "Login":
    st.title("Login")
    st.write("Enter your credentials to log in.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.success("Logged in successfully!")

# ----- Dashboard (User Profile) -----
elif selected_page == "Dashboard (User Profile)":
    st.title("User Dashboard - Joe Smith")
    st.write(
        """
        **Joe Smith**  
        67-year-old male, former smoker (quit 2018), with a history of coronary artery disease (4 vessel CABG in 2018), COPD, and Type 2 Diabetes.  
        Family history: Lung cancer in his father.
        """
    )
    st.subheader("Recent Healthcare Visits")
    visits_data = {
        "Date": ["2023-01-15", "2023-03-22", "2023-06-10"],
        "Doctor": ["Dr. Adams", "Dr. Baker", "Dr. Clark"],
        "Facility": ["General Hospital", "Specialty Clinic", "City Medical Center"],
        "Diagnosis/Procedure": ["Checkup", "Cardiac Stress Test", "Follow-up"],
    }
    visits_df = pd.DataFrame(visits_data)
    st.table(visits_df)
    st.write("Click on a visit for full details.")

# ----- Encounter Record Page -----
elif selected_page == "Encounter Record":
    st.title("Encounter Record Detail")
    st.subheader("Discharge Summary")
    st.write("Detailed summary of the patient’s hospital encounter.")
    st.subheader("Procedure/Operative Notes")
    st.write("Notes on procedures performed during the encounter.")
    st.subheader("Consult Notes & H&P")
    st.write("Consultation notes and History & Physical details.")
    st.subheader("Daily Progress Notes")
    st.write("Daily progress notes from the hospital stay.")
    st.subheader("Labs")
    st.write("Lab results:")
    with st.expander("View Labs"):
        lab_data = {
            "Test": ["CBC", "Metabolic Panel", "Lipid Panel"],
            "Result": ["Normal", "Abnormal", "Borderline"],
            "Date": ["2023-01-10", "2023-01-10", "2023-01-10"],
        }
        lab_df = pd.DataFrame(lab_data)
        st.table(lab_df)

# ----- Settings & Privacy Center -----
elif selected_page == "Settings & Privacy":
    st.title("Settings & Privacy Center")
    st.write("Manage your data sharing preferences and view your compensation details.")
    st.subheader("Adjust Sharing Preferences")
    sharing_pref = st.radio(
        "Select your preferred data sharing mode:",
        (
            "Strict Privacy Mode (No Sharing)",
            "De-Identified Research Only (5% of research profits)",
            "Full Data Sharing (Research + Ads) (15% of advertising profits)",
        ),
    )
    st.subheader("Notification Preferences")
    notifications_pref = st.multiselect(
        "Select notification types:",
        ["Clinical trial invites", "Compensation updates"],
    )
    st.subheader("Compensation Overview")
    st.write("You have earned $50 from data sharing this month!")

# ----- Notifications Panel -----
elif selected_page == "Notifications":
    st.title("Notifications")
    st.write("Your latest notifications:")
    st.write(
        """
        - **Clinical Trial Invite:** You have been invited to participate in a trial.
        - **Compensation Update:** Your earnings have been updated.
        - **Record Access Request:** A provider has requested access to your records.
        """
    )

# ----- Search Functionality -----
elif selected_page == "Search":
    st.title("Search Health Records")
    search_query = st.text_input("Search for visits, labs, procedures, or medications:")
    if st.button("Search"):
        st.write(f"Showing results for: {search_query}")
        st.write("Search results would appear here.")

# ----- FAQs & Support -----
elif selected_page == "FAQs & Support":
    st.title("FAQs & Support")
    st.write(
        """
        **FAQs**
        - **How is my data protected?**
          Your data is secured using industry-standard encryption and stored in a HIPAA-compliant environment.
        - **Can I change my data sharing preferences?**
          Yes, you can adjust your preferences in the Settings & Privacy Center.
        - **How do I contact support?**
          Email us at support@veritasone.com.
        """
    )

# ----- Security & Privacy Disclosures -----
elif selected_page == "Security & Privacy Disclosures":
    st.title("Security & Privacy Disclosures")
    st.write(
        """
        **Our Commitment to Security**
        - HIPAA-compliant data storage and handling.
        - End-to-end encryption for data transmission.
        - Regular security audits and updates.
        """
    )