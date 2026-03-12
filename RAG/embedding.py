from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from .text_splitter import text_splitter


embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, api_key=api_key)


vector_store = Chroma(
    collection_name="my_collection", 
    embedding_function=embeddings,
    persist_directory="db/chroma_db"
    )