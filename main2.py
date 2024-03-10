import streamlit as st
import ytlinkfetch as yt
import gettranscript as gt
import pathway as pw
from pathway.xpacks.llm.parsers import ParseUnstructured
from pathway.xpacks.llm.splitters import TokenCountSplitter
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt
import json
import requests
from pathway.stdlib.ml.index import KNNIndex
from pathway.xpacks.llm.embedders import OpenAIEmbedder
from pathway.xpacks.llm.llms import OpenAIChat, prompt_chat_single_qa

st.title("Youtube video chatgpt")
user_input = st.text_input("Enter youtube playlist link")
question = st.text_input("Enter question")

class InputSchema(pw.Schema):
    transcript: str

class QueryInputSchema(pw.Schema):
    query: str



if st.button("Submit"):
#    urls=yt.fetch_video_urls(user_input)
#    gt.get_transcript(urls)

    
    # Convert string to JSON line
    que_json = json.dumps({"query": question})
    
    input_data = pw.io.jsonlines.read("transcript.jsonl", schema=InputSchema, mode="static")

    que = pw.io.jsonlines.read(que_json, schema=QueryInputSchema, mode="static")

    query, response_writer = pw.io.http.rest_connector(
        host='172.17.251.194',
        port=8501,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    parser = ParseUnstructured()
    documents = input_data.select(texts=parser(pw.this.transcript))
    documents = documents.flatten(pw.this.texts)
    documents = documents.select(texts=pw.this.texts[0])

    splitter = TokenCountSplitter()
    documents = documents.select(chunks=splitter(pw.this.texts))
    documents = documents.flatten(pw.this.chunks)
    documents = documents.select(chunk=pw.this.chunks[0])

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=documents, data_to_embed=pw.this.chunk)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=que, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    print(responses)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)
    st.success(f"{question}\n  {responses} \n{response_writer}")