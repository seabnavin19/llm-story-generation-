import streamlit as st

# Set page configuration
st.set_page_config(layout="wide")

from diffusers import DiffusionPipeline
from PIL import Image
import numpy as np
from langchain_community.llms import Ollama
import time
import re

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

# Function to generate story
def generate_story(prompt):
    answers = []
    prompt = f''' '{prompt}' 
    1.give short story with 200 words 
    2. give 3 image description ideas to generate images for this story
    3. generate 5 MCQs with options and answer '''
    story = llm.invoke(prompt)
    print(story+"\n")
    story = story+"\n"
    story , photoes, mcq = re.split(':\n+1', story)
    
    mcq = "1." + mcq
    story = "\n".join(story.split("\n")[:-1])
    # Define the regex pattern
    pattern = r'Answer:\s*[A-Za-z]\) .*\n'

    questions = re.split(pattern, mcq)

    matches = re.findall(pattern, mcq)
    for match in matches:
        answers.append(match.split("Answer: ")[1].strip())

    questions = questions[:-1]


    return story,  questions, answers ,photoes
def generate_image_description(story):
    para = story.split("\n")
    para = [p for p in para if "." in p]
    first_desc, second_desc, third_desc = "cartoon style of "+para[0],"cartoon style of " + para[1].replace('2.',""),para[2].replace('3.',"")

    return first_desc, second_desc, third_desc


# Streamlit UI
st.title('Story Generation')
prompt_story = st.text_area("Enter your prompt:", max_chars=200, height=100)
generate_story_button = st.button("Generate Story")


if generate_story_button:
    with st.spinner("Generating story and images..."):
        if prompt_story:
            story, questions, answers, photoes = generate_story(prompt_story)
            st.write("### Generated Story:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div style='max-width: 800px; overflow-wrap: break-word;'>{story}</div>", unsafe_allow_html=True)
            with col2:
                first_desc, second_desc, third_desc = generate_image_description(photoes)
                print(first_desc, second_desc, third_desc)
                ccol1, ccol2 = col2.columns(2)
                with ccol1:
                    with st.spinner("Generating Image 1..."):
                        image1 = pipe(first_desc).images[0]
                        st.image(image1, width=300)
                    with st.spinner("Generating Image 2..."):
                        image2 = pipe(second_desc).images[0]
                        st.image(image2, width=300)
                with ccol2:
                    with st.spinner("Generating Image 3..."):
                        image3 = pipe(second_desc).images[0]
                        st.image(image3, width=300)

            st.write("### Questions:")
            for i, question in enumerate(questions):
                st.text(question)
                with st.expander("See Answer"):
                    st.write(f"Answer: {answers[i]}")

        else:
            st.warning("Please enter a prompt.")
    st.success("Story and images generated successfully!")



