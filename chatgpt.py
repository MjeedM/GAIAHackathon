# This Python file uses the following encoding: utf-8
import cohere
from googletrans import Translator
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import os

import pandas as pd

import time

openai.api_key = put API here

link = input()
if '=' in link:
    link = link.split('=')
    link = (link[1])
else:
    link = link.split('/')
    link = link[-1]
transcript = YouTubeTranscriptApi.get_transcript(link)
txtlist=[]
for i in transcript:
    outtxt = (i['text'])
    txtlist.append(outtxt)

txtlist = ' '.join(txtlist)
text = txtlist[:3000]

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model='gpt-3.5-turbo',

    messages=messages,

    temperature=0,

    )

    return response.choices[0].message["content"]


prompt = f"you are tasked with summarizing a segment in the following podcast, Please summarize the following text in arabic briefly,:{text}"


response = get_completion(prompt)

print(response)


