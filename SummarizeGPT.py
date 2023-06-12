# py -m pip install -r requirements.txt

# This Python file uses the following encoding: utf-8
from googletrans import Translator
import streamlit as st
import streamlit.components.v1 as components

from youtube_transcript_api import YouTubeTranscriptApi

import openai
import os

import pandas as pd

import time


# openai.api_key = 'api here'

sumsum=''
def summerize(paragraph,language,api):
    openai.api_key = api

    if '=' in paragraph:
        paragraph=paragraph.split('=')
        paragraph = (paragraph[1])
    else:
        paragraph=paragraph.split('/')
        paragraph=paragraph[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(paragraph,languages=['en', 'ar'])

        txtlist = []
        for i in transcript:
            outtxt = (i['text'])
            txtlist.append(outtxt)
        txtlist = ' '.join(txtlist)
        transcript_length = len(txtlist)
        # for t in range(0,int(transcript_length/10000)):
        #     text = txtlist[t:t+10000]
        text=txtlist[:3000]



        # translator = Translator()
        # translated = translator.translate(summery, src='en', dest='ar')

        def get_completion(prompt, model="gpt-3.5-turbo"):

            messages = [{"role": "user", "content": prompt}]

            response = openai.ChatCompletion.create(

                model='gpt-3.5-turbo',

                messages=messages,

                temperature=0,

            )

            return response.choices[0].message["content"]

        # prompt = f"You are tasked with summerizing what the following podcast content is about briefly, Please summarize the following text in arabic,:{text}"

        if language == 'Arabic':
            lang='arabic'
        else:
            lang='english'

        prompt = f"you are tasked with summarizing a segment in the following video, Please summarize the following text in {lang} briefly, and say what type of video is it:{text}"

        response = get_completion(prompt)
        return response




    except Exception as e: print(e)

        # return "This video can't be summarized because it has no captions"






langs=['Arabic','English']
st.title("NOBTHAH")
form = st.form(key="user_settings")
with form:
    para_input = st.text_input("URL", key = "link_input")
    api_input = st.text_input("API KEY", key = "api_input")
    lang = st.selectbox('Language',options=langs)
    generate_button = form.form_submit_button("Summarize")
    if generate_button:
        sumsum = summerize(para_input,lang,api_input)
        st.write(sumsum)

