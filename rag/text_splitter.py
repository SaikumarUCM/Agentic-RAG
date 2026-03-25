from langchain_community.document_loaders import SeleniumURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def text_splitter(urls=(), chunk_size=1000, chunk_overlap=200):
    if isinstance(urls, str):
        urls = (urls,)

    loader = SeleniumURLLoader(urls=list(urls))
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)
