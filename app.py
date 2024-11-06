import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
import tempfile



uploaded_file = st.file_uploader("Upload your file", type=["pdf"])
if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    # Load the PDF using PyMuPDFLoader
    loader = PyMuPDFLoader(temp_file_path)
    docs = loader.load()

    # Display the content of the first document
    st.write(docs[0])
