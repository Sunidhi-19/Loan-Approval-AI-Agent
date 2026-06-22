import streamlit as st
import requests
from datetime import datetime

# Base URL pointing to the decoupled FastAPI microservice
BACKEND_URL = "http://127.0.0.1:8000/loan_approval"  # FastAPI URL

st.set_page_config(page_title="Loan Underwriting Portal", page_icon="🏦", layout="centered")
st.title("🏦 Automated Loan Approval Portal")
st.markdown("Provide comprehensive profile parameters below to submit for approval.")
st.markdown("---")

# Generate the auto-populated timestamp
current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with st.form(key="loan_application_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Applicant Profile")  
        applicant_id = st.text_input("Applicant ID", placeholder="e.g., APP-98421")
        name = st.text_input("Full Name", placeholder="e.g., Jane Doe")
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        location = st.text_input("Location", placeholder="e.g., New York, NY")  
        
    with col2:
        st.subheader("📊 Financial Liabilities")
        employment_type = st.selectbox(
            "Employment Type",
            ("Full-Time", "Contract", "Freelancer")
        )
        income = st.number_input("Gross Annual Income", min_value=10000.0, value=75000.0, step=5000.0, format="%.2f")
        
        existing_liabilities = st.number_input(
            "Existing Liabilities", 
            min_value=0.0, 
            value=450.0,
            help="Monthly expenses, EMIs, credit card debts, etc."
        )
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=710)
        
    st.subheader("💰 Requested Loan Terms")
    term_col1, term_col2 = st.columns(2)
    with term_col1:
        loan_amount = st.number_input("Loan Amount", min_value=0.0, value=25000.0, step=1000.0)
    with term_col2:
        loan_duration = st.slider("Duration (Years)", min_value=1, max_value=30, value=5)

    # Display the non-editable auto-populated timestamp inside the form
    st.markdown(f"**Application Timestamp:** `{current_timestamp}`")

    submit = st.form_submit_button("Submit", type="primary")

# API POST Request Handling
if submit:
    # Package form data into a payload dictionary including the updated variable name
    payload = {
        "applicant_id": applicant_id,
        "name": name,
        "age": age,
        "employment_type": employment_type,
        "location": location,  
        "gross_annual_income": income,
        "existing_liabilities": existing_liabilities,  
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "loan_duration_years": loan_duration,
        "application_timestamp": current_timestamp  
    }
    
    with st.spinner("Processing..."):
        try:
            response = requests.post(BACKEND_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.success("Analysis Complete!")
                st.json(result)
            else:
                st.error(f"Backend error ({response.status_code}): {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to the backend at {BACKEND_URL}. Is your FastAPI server running?")