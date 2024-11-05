import streamlit as st

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

st.subheader(":rainbow[Test]")
t1,t2,t3 = st.tabs(
    [":material/info: Sign-Up", ":material/info: About", ":material/play_arrow: Playground"])

