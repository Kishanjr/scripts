import streamlit as st

st.set_page_config(
    page_title="Custom Themed App",
    layout="wide",
    initial_sidebar_state="expanded",
    theme={
        "base": "dark",  # Switch to a dark theme
        "primaryColor": "#E91E63",  # Pink primary color
        "backgroundColor": "#212121",  # Dark background
        "secondaryBackgroundColor": "#424242",  # Secondary dark background
        "textColor": "#FFFFFF",  # White text
    },
)

# Content
st.title("Custom Theme Programmatically Applied")
st.write("This app uses Streamlit's built-in theming options!")
