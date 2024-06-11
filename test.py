import streamlit as st
from fill_blank import render_generate_fill_blank

st.title("Generate Fill-in-the-Blanks and MCQs")

# Text area for user to input story
story = st.text_area("Enter your story here", height=200)

if st.button("Generate Questions"):
    if story:
        render_generate_fill_blank(story)
    else:
        st.warning("Please enter some text to analyze.")
