import streamlit as st
import os
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

# Create a local directory for models in a writable location
local_dir = Path("./local_models")  # Using current directory
local_dir.mkdir(parents=True, exist_ok=True)

# First download models to the local directory
artifacts_path = StandardPdfPipeline.download_models_hf(local_dir)

# Set up the converter with the local path
pipeline_options = PdfPipelineOptions(artifacts_path=str(local_dir))
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

st.set_page_config(   
    layout="wide",
    page_title="Test App"
)

# Custom CSS
css = '''
<style>
    [data-testid="stMainBlockContainer"] {
        padding-top: 3rem!important;
    }
    [data-testid="stSidebarNavLink"] {
        font-size: small;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# Directory where PDF files will be saved
SAVE_DIR = "static"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.subheader(":rainbow[Test]")
t1,t2,t3 = st.tabs(
    [":material/info: Sign-Up", ":material/info: About", ":material/play_arrow: Playground"])

with t3:
    uploaded_file = st.file_uploader("Upload your file", type=["pdf", "docx", "pptx", "png", "jpg", "jpeg", "html"])
    input_url = st.text_input("OR enter a URL:")
    
    if input_url or uploaded_file:
        if input_url and uploaded_file:
            st.error("Please provide only one input: either a URL or a file.")
        else:
            if input_url:
                source = input_url 
            else:
                file_path = os.path.join(SAVE_DIR, uploaded_file.name)                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())                 
                source = f"{SAVE_DIR}/{uploaded_file.name}"   
            
            result = converter.convert(source)
            
            o1,o2,o3 = st.tabs(
                [":material/info: Text", ":material/apps: JSON", ":material/play_arrow: Token"])
            
            with o1:
                st.text_area("Output", result.document.export_to_markdown(), height=800)
            
            with o2:
                data = result.document.export_to_dict()
                if "schema_name" in data and data["schema_name"] == "DoclingDocument":
                    data["schema_name"] = "StructurifyDocument"
                st.json(data)
            
            with o3:
                st.text_area("Output", result.document.export_to_document_tokens(), height=800)
