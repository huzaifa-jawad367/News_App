import os
import json
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
import faiss
import numpy as np
import getpass
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

def load_json_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                all_data.extend(data)
    return all_data

def split_text(data, text_splitter):
    split_documents = []
    for text in data:
        documents = [Document(page_content=text)]
        split_docs = text_splitter.split_documents(documents)
        split_documents.extend(split_docs)
    return split_documents

# Load the data
directory = 'data/nela-gt-2021/newsdata/train'
data = load_json_files(directory)

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')

texts = [item['content'] for item in data]

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

split_documents = split_text(texts, text_splitter)

# print(split_documents)

db = FAISS.from_documents(split_documents, OpenAIEmbeddings())

query = "Pfizer to boost production"
docs = db.similarity_search(query)
print(docs[0].page_content)
