import pathway as pw
import os
from dotenv import load_dotenv
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt
from pathway.stdlib.ml.index import KNNIndex
from pathway.xpacks.llm.parsers import ParseUnstructured
from pathway.xpacks.llm.splitters import TokenCountSplitter
from pathway.xpacks.llm.embedders import OpenAIEmbedder
from pathway.xpacks.llm.llms import OpenAIChat, prompt_chat_single_qa
load_dotenv()

embedder = OpenAIEmbedder(
    api_key=os.getenv("OPENAI_API_TOKEN"),
    model=os.getenv("EMBEDDER_LOCATOR"),
    retry_strategy=pw.asynchronous.FixedDelayRetryStrategy(),
    cache_strategy=pw.asynchronous.DefaultCache(),
)

model = OpenAIChat(
        api_key=os.getenv("OPENAI_API_TOKEN"),
        model=os.getenv("EMBEDDER_LOCATOR"),
        temperature=os.getenv("TEMPERATURE"),
        max_tokens=os.getenv("MAX_TOKENS"),
        retry_strategy=pw.asynchronous.FixedDelayRetryStrategy(),
        cache_strategy=pw.asynchronous.DefaultCache(),
    )


class QueryInputSchema(pw.Schema):
    query: str



def run(host, port):
    # Given a user search query
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )
    
    # Real-time data coming from external unstructured data sources like a PDF file

    input_data = pw.io.fs.read(
        "./docs/",
        mode="streaming",
        format="binary",
        autocommit_duration_ms=50,
    )
    
    
    # Chunk input data into smaller documents
    parser = ParseUnstructured()
    documents = input_data.select(texts=parser(pw.this.data))
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
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()


