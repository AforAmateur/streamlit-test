import os
import sys
from pathlib import Path

# Create tmp directories
tmp_base = Path("/tmp/docling_tmp")
tmp_base.mkdir(parents=True, exist_ok=True)
models_dir = tmp_base / "models"
models_dir.mkdir(parents=True, exist_ok=True)
uploads_dir = tmp_base / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)

# Try to force deepsearch_glm to use our directory
# os.environ["DEEPSEARCH_GLM_HOME"] = str(models_dir)
os.environ["DOCLING_MODEL_PATH"] = str(models_dir)

# Now import the required packages
import streamlit as st
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

# Configure the converter
pipeline_options = PdfPipelineOptions(artifacts_path=str(models_dir))
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

st.set_page_config(   
    layout="wide",
    page_title="Test App"
)

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
            try:
                if input_url:
                    source = input_url 
                else:                    
                    # Save uploaded file to tmp directory
                    file_path = uploads_dir / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())                 
                    source = str(file_path)                  
                print(source)
                try:
                    result = converter.convert(source)
                except Exception as e:
                    st.write(e)
                    print(e)
                    result = None
                
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
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                st.error("Detailed error information:")
                import traceback
                st.code(traceback.format_exc())
