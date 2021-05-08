"""
Description
This is a Natural Language Processing(NLP) Based App useful for basic NLP concepts such as follows;
+ Tokenization & Lemmatization using Spacy
+ Named Entity Recognition(NER) using SpaCy
+ Sentiment Analysis using TextBlob
+ Document/Text Summarization using Gensim/Sumy
This is built with Streamlit Framework, an awesome framework for building ML and NLP tools.

Purpose
To perform basic and useful NLP task with Streamlit,Spacy,Textblob and Gensim/Sumy

"""
# Core Pkgs
import streamlit as st
import os


# NLP Pkgs
from textblob import TextBlob
import spacy
from gensim.summarization.summarizer import summarize
import nltk
nltk.download('punkt')

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


# Function for Sumy Summarization
def sumy_summarizer(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

# Function to Analyse Tokens and Lemma
@st.cache
def text_analyzer(my_text):
	nlp = spacy.load('en_core_web_sm')
	docx = nlp(my_text)
	# tokens = [ token.text for token in docx]
	allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx ]
	return allData

# Function For Extracting Entities
@st.cache
def entity_analyzer(my_text):
	nlp = spacy.load('en_core_web_sm')
	docx = nlp(my_text)
	tokens = [ token.text for token in docx]
	entities = [(entity.text,entity.label_)for entity in docx.ents]
	allData = ['"Token":{},\n"Entities":{}'.format(tokens,entities)]
	return allData


def main():
	""" NLP Based App with Streamlit """

	# Title
	st.title("Ultimate NLP Application")
	st.subheader("Natural Language Processing for everyone")
	st.markdown("""
    	#### Description
    	+ This is a Natural Language Processing(NLP) Based App useful for basic NLP task
    	Tokenization , Lemmatization, Named Entity Recognition (NER), Sentiment Analysis, Text Summarization. Built for social good by [LekanAkin](https://github.com/lekanakin). Click any of the checkboxes to get started.
    	""")

	# Summarization
	if st.checkbox("Get the summary of your text"):
		st.subheader("Summarize Your Text")

		message = st.text_area("Enter Text","Type Here....")
		summary_options = st.selectbox("Choose Summarizer",['sumy','gensim'])
		if st.button("Summarize"):
			if summary_options == 'sumy':
				st.text("Using Sumy Summarizer ..")
				summary_result = sumy_summarizer(message)
			elif summary_options == 'gensim':
				st.text("Using Gensim Summarizer ..")
				summary_result = summarize(message)
			else:
				st.warning("Using Default Summarizer")
				st.text("Using Gensim Summarizer ..")
				summary_result = summarize(message)
			st.success(summary_result)

	# Sentiment Analysis
	if st.checkbox("Get the Sentiment Score of your text"):
		st.subheader("Identify Sentiment in your Text")

		message = st.text_area("Enter Text","Type Here...")
		if st.button("Analyze"):
			blob = TextBlob(message)
			result_sentiment = blob.sentiment
			st.success(result_sentiment)

	# Entity Extraction
	if st.checkbox("Get the Named Entities of your text"):
		st.subheader("Identify Entities in your text")

		message = st.text_area("Enter Text","Type Here..")
		if st.button("Extract"):
			entity_result = entity_analyzer(message)
			st.json(entity_result)

	# Tokenization
	if st.checkbox("Get the Tokens and Lemma of text"):
		st.subheader("Tokenize Your Text")

		message = st.text_area("Enter Text","Type Here.")
		if st.button("Analyze"):
			nlp_result = text_analyzer(message)
			st.json(nlp_result)





	st.sidebar.subheader("About App")
	st.sidebar.text("NLP for everyone.")
	st.sidebar.info("Use this tool to get the sentiment score, tokens , lemma, Named Entities and Summary of your text. It's the ultimate!")
	st.sidebar.subheader("Developed by")
	st.sidebar.text("Lekan Akinsande (Twitter: @Akinsande1)")




if __name__ == '__main__':
	main()
