


import pinecone
from dotenv import load_dotenv
import os,time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_huggingface import HuggingFaceEmbeddings
vector_store=None


def init_pinecone():
    global vector_store
    #load_dotenv()
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    index_name = "medconnect"  

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
      pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

    index = pc.Index(index_name)
    
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    #example_vector = embeddings.embed_query("example text")
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    print("Pinecone initialized")


def get_vector_store():
    return vector_store
