


import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def text_splitter():

    loader= WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
    parse_only=bs4.SoupStrainer(
            class_= ("post-content", "post-title", "post-header")
            )
        ),
    )

    docs= loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_texts = text_splitter.split_documents(docs)

    return all_texts



