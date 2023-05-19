import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import openai
from openai.error import APIError
from langchain.vectorstores import FAISS

# .envファイルからAPIキーを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# モデル定義
chatGPT = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

# 定数
CHUNK_SIZE = 1000
# csvファイルのヘッダ
HEADER = ["user_input", "assistant_reply", "timestamp"]

# PDFファイルの読み込み関数
def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    # 文書の分割
    text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    return texts

# Embeddings生成：ベクトルの集合データベースを返す
def create_embeddings(split_docs):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = FAISS.from_documents(split_docs, embeddings)

    return db

# ChatGPTへの入力処理
"""
    引数の説明
    file PDFファイルのパス
    query 指示
    chain_type
    k 参照するテキストチャンクの数
"""
def qa(file, query, chain_type, k):
    split_docs = load_pdf(file)
    vector_store = create_embeddings(split_docs)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    qa = RetrievalQA.from_chain_type(
        llm=chatGPT, chain_type=chain_type, retriever=retriever, return_source_documents=True
    )
    result = qa({"query": query})
    print(result['result'])
    return result

# OpenAIのChat completion APIを使用した関数
def create_chat_completion(
        messages: list,
        temperature: float,
        max_tokens=4000, 
        model="gpt-3.5-turbo", # デフォルトはChatGPT
) -> str:
    response = None
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    except APIError as e:
        pass

    return response.choices[0].message["content"]

# csv 書き込み
def write_data(file_path: str, row: list):
    # 使うライブラリをわかりやすくするため関数内でインポート
    import csv
    from datetime import datetime

    if os.path.exists(file_path):
        with open(file_path, 'a', newline='') as f:
            row.append(datetime.now()) # timestampを作成
            writer = csv.writer(f)
            writer.writerow(row)
    else:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            # ヘッダ書き込み
            writer.writerow(HEADER)
            row.append(datetime.now())
            writer.writerow(row)