from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 環境変数の読み込み
load_dotenv()

def build_and_save_vector_store():
    print("SFCの公式サイトを読み込んでいます...")
    urls = [
        "https://www.sfc.keio.ac.jp/admissions/"
    ]
    
    # ドキュメントの読み込みと分割
    loader = WebBaseLoader(urls)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)
    
    # ベクトル化してFAISSに保存
    print("ベクトルデータベースを構築中...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    
    # ローカルに保存
    vectorstore.save_local("faiss_index")
    print("完了しました！ 'faiss_index' フォルダが作成されました。")

if __name__ == "__main__":
    build_and_save_vector_store()