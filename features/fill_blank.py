import streamlit as st
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import RegexpParser
from random import sample

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define the grammar for fill-in-the-blanks
fill_in_the_blanks_grammar = r"""
    Nodes: {<DT|JJ|JJR|JJS|RB|RBR|RBS|CD>*<NN.*>+}
"""

# Function to generate fill-in-the-blanks text
def generate_fill_in_the_blanks(parsed_tokens):
    blanks = []
    for subtree in parsed_tokens.subtrees():
        if subtree.label() == 'Nodes':
            blank = ' '.join(word for word, tag in subtree.leaves())
            blanks.append(blank)
    return blanks

# Function to generate multiple-choice questions
def generate_mcqs(sentences):
    mcqs = []
    for sentence in sentences:
        # Randomly select a keyword from the sentence
        words = word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)
        keywords = [word for word, pos in tagged_words if pos.startswith('NN')]
        if keywords:
            keyword = sample(keywords, 1)[0]
            # Formulate a question with the selected keyword
            question = sentence.replace(keyword, "______")
            # Generate options
            options = [keyword]
            other_keywords = list(set(keywords) - {keyword})
            
            # Ensure that we have at least 3 additional options
            if len(other_keywords) >= 3:
                additional_options = sample(other_keywords, 3)
            else:
                additional_options = other_keywords
                while len(additional_options) < 3:
                    additional_options.append("dummy_option_" + str(len(additional_options) + 1))

            options.extend(additional_options)
            # Shuffle options
            options = sample(options, len(options))
            mcqs.append((question, options))
    return mcqs


def generate_questions(story):
    # Tokenize the story into sentences
    sentences = sent_tokenize(story)

    # Tokenize the story
    tokens = word_tokenize(story)

    # Perform part-of-speech tagging
    tagged_tokens = nltk.pos_tag(tokens)

    # Initialize the parser with the defined grammar for fill-in-the-blanks
    parser = RegexpParser(fill_in_the_blanks_grammar)

    # Parse the tagged tokens using the defined grammar
    parsed_tokens = parser.parse(tagged_tokens)

    # Generate fill-in-the-blanks text
    fill_in_the_blanks = generate_fill_in_the_blanks(parsed_tokens)

    # Generate MCQs
    mcqs = generate_mcqs(sentences)

    return fill_in_the_blanks, mcqs

def render_generate_fill_blank(story):
    fill_in_the_blanks, mcqs = generate_questions(story)
    

    filled_story = story
    for blank in fill_in_the_blanks:
        filled_story = filled_story.replace(blank, "__________")
    st.write(filled_story)
    
    st.subheader("Multiple Choice Questions (MCQs)")
    for i, (question, options) in enumerate(mcqs, start=1):
        st.write(f"MCQ {i}: {question}")
        for j, option in enumerate(options, start=1):
            st.write(f"{j}. {option}")

