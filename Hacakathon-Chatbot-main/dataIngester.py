import pinecone 
from langchain.vectorstores import Pinecone

from langchain.document_loaders import DirectoryLoader
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import JSONLoader
import json
from pathlib import Path
from pprint import pprint
import keys



from langchain.document_loaders import DirectoryLoader




directory = 'data'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs (directory)
print(len(documents))

from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(documents,chunk_size=500,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)
print(len(docs))

print(docs[1].page_content)
from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

import pinecone 
from langchain.vectorstores import Pinecone
# initialize pinecone
pinecone.init(
    api_key=keys.PINECONE_KEY,  # find at app.pinecone.io
    environment="us-east4-gcp"  # next to api key in console
)

index_name = "langchain-chatbot"

index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# documents = load_docs(directory)
# len(documents)

def get_similiar_docs(query,k=1,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

print("ANSWER:\n")
query = "What are the team get togethers"
similar_docs = get_similiar_docs(query)
print(similar_docs)