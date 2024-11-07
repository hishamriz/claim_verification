import streamlit as st
from input_layer import InputLayer
from nlp_engine import NLPEngine
from verification_layer import ClaimVerifier

# Initialize components
input_layer = InputLayer()
nlp_engine = NLPEngine()
verifier = ClaimVerifier()

# Streamlit UI
st.title("Claim Verification System")

# File upload
uploaded_file = st.file_uploader("Upload a document (PDF, Image, URL)")
file_type = st.selectbox("Select file type", options=["pdf", "image", "url"])

if uploaded_file:
    extracted_text = input_layer.handle_input(file_type, uploaded_file)
    st.write("Extracted Text:", extracted_text)
    
    # Extract claims using NLP
    claims = nlp_engine.extract_claims(extracted_text)
    entities = nlp_engine.extract_entities(extracted_text)
    
    st.write("Extracted Claims:", claims)
    st.write("Entities:", entities)
    
    # Verify claims
    for claim in claims:
        is_verified = verifier.verify_claim(claim)
        st.write(f"Claim: {claim}, Verified: {is_verified}")
