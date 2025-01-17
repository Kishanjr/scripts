import streamlit as st
import datetime

# Title of the app
st.title("Streamlit App with Scoped CSS for Buttons")

# Custom HTML and CSS for side-by-side buttons
st.markdown("""
    <div class="button-container">
        <style>
        .button-container div.stButton > button {
            display: inline-block;
            margin: 0 5px;  /* Adjust spacing between buttons */
        }
        </style>
        <div>
            <button class="stButton">Say Hello</button>
        </div>
    </div>
""", unsafe_allow_html=True)

if st.button("Say Hello"):
    st.write("Hello! How are you?")

if st.button("Show Current Time"):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"The current time is: {current_time}")


