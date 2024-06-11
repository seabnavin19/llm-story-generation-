import streamlit as st

# Set page configuration
st.set_page_config(layout="wide")

from diffusers import DiffusionPipeline
from PIL import Image
import numpy as np
from langchain_community.llms import Ollama
import time
import re
from utils import TextCleaner
from st_click_detector import click_detector
from features.fill_blank import render_generate_fill_blank
from features.network_graph import extract_and_visualize
from features.nltk_dowload import download_nltk_data

download_nltk_data()


# Load the diffusion pipeline model (memoized with st.cache)
@st.cache_resource()
def load_diffusion_pipeline():
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to("mps")
    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()
    return pipe

# Load the language model (memoized with st.cache)
@st.cache_resource()
def load_language_model():
    llm = Ollama(model="llama2")
    return llm

pipe = load_diffusion_pipeline()
llm = load_language_model()
text_cleaner = TextCleaner()

# Function to generate story
def generate_story(prompt):
    prompt = f''' '{prompt}' 
    1. generate short story with 200 words. 
    2. generate 5 MCQs with options and answer .'''
    story = llm.invoke(prompt)
    story, questions, answers = text_cleaner.clean_story(story=story)
    return story , questions, answers



# Streamlit UI
st.title('Story Generation')
prompt_story = st.text_area("Enter your prompt:", max_chars=200, height=100)
generate_story_button = st.button("Generate Story")

if "use_to_generate" not in st.session_state:
    st.session_state.use_to_generate = False
    st.session_state.content = []
    st.session_state.story = []
    st.session_state.questions = []
    st.session_state.answers = []


content = []
story   = []


if generate_story_button:
    st.session_state.use_to_generate = True
    with st.spinner("Generating story and images..."):
        if prompt_story:
                story, questions, answers = generate_story(prompt_story)
                st.session_state.story = story
                st.session_state.questions = questions
                st.session_state.answers = answers

                for index,sen in enumerate(story):
                    content.append(f"<div style='max-width: 800px; overflow-wrap: break-word;'><a href='#' style='color: white;' id='{index}'>{sen}</a></div>")
                st.session_state.content = content
        else:
            st.warning("Please enter a prompt.")



col1, col2 = st.columns(2)
with col1:
    with st.spinner("Generating story..."):
        st.write("### Generated Story:")
        clicked = click_detector("<br>".join(st.session_state.content))
        




if st.session_state.use_to_generate:
    story_text="\n".join(st.session_state.story)
    st.write("### Questions:")
    tabs = st.tabs(["Questions", "Fill in the Blanks", "Visualization"])

    with tabs[0]:
        st.write("### Questions:")
        for i, question in enumerate(st.session_state.questions):
            st.text(question)
            with st.expander("See Answer"):
                st.write(f"Answer: {st.session_state.answers[i]}")


    with tabs[1]:
        st.write("### Fill in the Blanks:")
        render_generate_fill_blank(story_text)
    
    with tabs[2]:
        st.write("### Story Visualization:")
        extract_and_visualize(story_text)

with col2:
    st.write("### Image:")
    text_desc = st.session_state.story[int(clicked)] if clicked != "" else ""
    st.markdown(f"**{text_desc} **")
    if text_desc!="":
        with st.spinner("Generating image..."):
            image = pipe(text_desc +"In 2d animation style ").images[0]
            st.image(image, width=300)