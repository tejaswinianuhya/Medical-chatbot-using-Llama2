from flask import Flask, render_template, jsonify, request
from langchain import PromptTemplate
from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.llms import CTransformers
from dotenv import load_dotenv
import os
from src.prompt import *

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

embeddings = download_hugging_face_embeddings()

index_name = "testing"

docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)

PROMPT = PromptTemplate(template = prompt_template, input_variables=["context", "question"])
chain_type_kwargs={"prompt": PROMPT}

# from langchain.vectorstores.base import VectorStoreRetriever
llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})

qa = RetrievalQA.from_chain_type(  
    llm=llm,  
    chain_type="stuff",  
    retriever=docsearch.as_retriever(    
        search_type="similarity",
        search_kwargs={"k": 3}),
    chain_type_kwargs=chain_type_kwargs 
) 

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get', methods=['GET', 'POST'])
def chat():
    msg = request.form['msg']
    input = msg.strip()
    print(input)
    result = qa({"query": input})
    print("Response:", result['result'])
    return str(result['result'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080, debug=True)

