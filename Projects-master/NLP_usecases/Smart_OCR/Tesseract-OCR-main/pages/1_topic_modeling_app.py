import gensim
import streamlit as st
import pyLDAvis.gensim_models
import streamlit.components.v1 as components
from pprint import pprint
from pages.OCR_multipage import ocr
from utils import *
from pages.OCR_multipage import file_uploader

def topicModeling(corpus,id2word,num_topics):
    # number of topics
    # num_topics = 10

    # Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics)

    # Print the Keyword in the 10 topics
    pprint(lda_model.print_topics())
    # doc_lda = lda_model[corpus]
    return lda_model


# if __name__ =='__main__':
st.markdown("# Topic modeling")
st.sidebar.header("Ploting Topic Modeling")


# uploaded_file = st.file_uploader(label='Upload PDF', type='pdf')
uploaded_file=file_uploader()

if uploaded_file:
    filename = uploaded_file.name
    filename = './input_pdf/' + filename

    no_of_topics = st.number_input('Enter the no of topics', min_value=1, max_value=10, step=1)

    if no_of_topics:
        if st.button('topicModeling'):
            text = ocr(filename,0)
            clean_text = preprocess(text)
            id2word, corpus = corpus(clean_text)
            lda_model = topicModeling(corpus, id2word,num_topics=no_of_topics)
            vis = pyLDAvis.gensim_models.prepare(topic_model=lda_model,
                                                 corpus=corpus,
                                                 dictionary=id2word)
            py_lda_vis_html = pyLDAvis.prepared_data_to_html(vis)
            components.html(py_lda_vis_html, width=1300, height=800)
