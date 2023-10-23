
from dataIngester import index
from sentence_transformers import SentenceTransformer
import pinecone
import openai
import streamlit as st
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import keys

# Load credentials from JSON file
with open('token.json') as json_file:
    credentials = json.load(json_file)

oauth_credentials = Credentials.from_authorized_user_info(credentials)

service = build('gmail', 'v1', credentials=oauth_credentials)

openai.api_key = keys.OPENAI_KEY
model = SentenceTransformer('all-MiniLM-L6-v2')

pinecone.init(api_key=keys.PINECONE_KEY, environment='us-east4-gcp')
index = pinecone.Index('langchain-chatbot')



def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=5, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']+result['matches'][2]['metadata']['text']+result['matches'][3]['metadata']['text']+result['matches'][4]['metadata']['text']

def getResponse(query):
    return "hello"+query




# docs = split_docs(documents)
# print(len(docs))