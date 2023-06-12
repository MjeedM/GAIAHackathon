# py -m pip install -r requirements.txt
# This Python file uses the following encoding: utf-8
import cohere
from googletrans import Translator
import streamlit as st
import streamlit.components.v1 as components

from youtube_transcript_api import YouTubeTranscriptApi

CO_API_KEY = api here
co = cohere.Client(CO_API_KEY)  # This is your trial API key

sumsum = ''


def summerize(paragraph, creativity, language):
    if '=' in paragraph:
        paragraph = paragraph.split('=')
        paragraph = (paragraph[1])
    else:
        paragraph = paragraph.split('/')
        paragraph = paragraph[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(paragraph, languages=['en', 'ar'])

        txtlist = []
        for i in transcript:
            outtxt = (i['text'])
            txtlist.append(outtxt)
        txtlist = ' '.join(txtlist)
        transcript_length = len(txtlist)
        # for t in range(0,int(transcript_length/10000)):
        #     text = txtlist[t:t+10000]
        text = txtlist[:10000]

        response = co.summarize(
            text=text,
            length='long',
            format='paragraph',
            model='summarize-xlarge',
            additional_command='write it as a preview, very general, write it as a description, write it in third person',
            # additional_command='Write an introductory paragraph for a blog post about language models.',

            temperature=creativity / 10,
            extractiveness='auto', )
        summery = response.summary
        if language == 'Arabic':
            translator = Translator()
            translated = translator.translate(summery, src='en', dest='ar')
            summery = translated.text

        return (summery)




    except:
        return "This video can't be summarized because it has no captions"


langs = ['Arabic', 'English']
st.title("Podcast Summarizer")
form = st.form(key="user_settings")
with form:
    para_input = st.text_input("URL", key="link_input")
    # api_input = st.text_input("API KEY", key = "api_input")
    Creativity = st.slider('Creativity', min_value=1, max_value=10, value=3,
                           help='Indicates The Randomness of The Summarization', )
    lang = st.selectbox('Language', options=langs)
    generate_button = form.form_submit_button("Summarize")
    if generate_button:
        sumsum = summerize(para_input, Creativity, lang)
        st.write(sumsum)
    # st.components.v1.html((f'<a href="https://twitter.com/intent/tweet?text={sumsum}" class="twitter-share-button" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'), scrolling=False)
