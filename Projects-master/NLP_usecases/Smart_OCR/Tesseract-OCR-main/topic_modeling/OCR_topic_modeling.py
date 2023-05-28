from topic_modeling.topic_modeling_app import corpus,topicModeling,preprocess
import pyLDAvis.gensim_models
from pages.OCR_multipage import *
import streamlit.components.v1 as components

uploaded_file = st.file_uploader(label='Upload PDF', type='pdf')

if uploaded_file:
    filename = uploaded_file.name
    filename = '../input_pdf/' + filename

    if st.button('topicModeling'):
        text = ocr(filename,0)
        clean_text = preprocess(text)
        id2word, corpus = corpus(clean_text)
        print(id2word, corpus)
        lda_model = topicModeling(corpus, id2word)
        vis = pyLDAvis.gensim_models.prepare(topic_model=lda_model,
                                         corpus=corpus,
                                         dictionary=id2word)

        py_lda_vis_html = pyLDAvis.prepared_data_to_html(vis)
        components.html(py_lda_vis_html, width=1300, height=800)
