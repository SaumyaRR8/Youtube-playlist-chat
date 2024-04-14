import os
import streamlit as st
import requests
from dotenv import load_dotenv
import ytlinkfetch as yt
import gettranscript as gt

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "api")
api_port = int(os.environ.get("PORT", 8080))


# Streamlit UI elements
st.title("Youtube Playlist ai chat")

yt_url = st.text_input("Enter youtube playlist link")

question = st.text_input(
    "Search for something",
    placeholder="What data are looking for?"
)

if yt_url:
    video_urls=yt.fetch_video_urls(yt_url)
    gt.get_transcript(video_urls)

if question:

    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(f"Failed to send data to Pathway API. Status code: {response.status_code}")
