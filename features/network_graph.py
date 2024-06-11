import streamlit as st
import nltk
import networkx as nx
import matplotlib.pyplot as plt
from nltk import pos_tag
from nltk.chunk import RegexpParser



def extract_and_visualize(text):
    def extract_noun_phrases(text):
        noun_phrases = []
        relationships = []
        sentences = nltk.sent_tokenize(text)

        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tagged_words = pos_tag(words)

            grammar = r"""
                NP: {<DT|JJ|JJR|JJS|RB|RBR|RBS|CD>*<NN|NNS|NNP|NNPS>}
                REL: {<IN|VBG|VBN>}
            """

            cp = RegexpParser(grammar)
            tree = cp.parse(tagged_words)

            current_relations = []

            for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP' or t.label() == 'REL'):
                for leaf in subtree.leaves():
                    word, tag = leaf
                    if tag in ["IN", "VBG", "VBN"]:
                        current_relations.append(word)
                if subtree.label() == 'NP':
                    noun_phrase = ' '.join([word for word, tag in subtree.leaves()])
                    noun_phrases.append(noun_phrase)
                    relationships.append(current_relations)
                    current_relations = []

        return noun_phrases, relationships

    noun_phrases, relations = extract_noun_phrases(text)


    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes for noun phrases
    G.add_nodes_from(noun_phrases)

    # Add edges based on relationships
    for i in range(len(noun_phrases) - 1):
        source = noun_phrases[i]
        target = noun_phrases[i + 1]

        # Check if source and target noun phrases exist in the text
        if source in text and target in text:
            # Check the POS tags of words between source and target
            words_between = text.split(source)[1].split(target)[0].strip().split()
            words_between_tags = pos_tag(words_between)
            relations_between = [word for word, tag in words_between_tags if tag in ["IN", "VBG", "VBN"]]
            relation = ', '.join(relations_between) if relations_between else ""

            edge_color = 'red' if relation else 'blue'

            G.add_edge(source, target, relation=relation, color=edge_color)

    # Visualize the graph
    pos = nx.spring_layout(G, seed=42)  # Adding seed for reproducibility
    labels = nx.get_edge_attributes(G, "relation")
    edge_colors = [G[source][target]['color'] for source, target in G.edges]

    plt.figure(figsize=(10, 8))  # Adjust the figure size for better visibility
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=10, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    st.pyplot(plt)
