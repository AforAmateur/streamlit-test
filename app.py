import streamlit as st
# from PIL import Image

# st.logo(
#     "https://dscvryai.com/assets/images/logos/logo-nobg-darktext.webp",
#     link="https://dscvryai.com/",
#     icon_image="https://dscvryai.com/assets/images/logos/favicon.ico",
# )


# Load favicon and set page config
# im = Image.open("favicon.ico")
st.set_page_config(
    # page_icon=im,
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

st.subheader(":rainbow[Test]")
t1,t2,t3 = st.tabs(
    [":material/info: Sign-Up", ":material/info: About", ":material/play_arrow: Playground"])

