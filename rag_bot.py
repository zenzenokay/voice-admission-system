from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def get_rag_response(user_input: str) -> str:
    """保存されたベクトルDBを読み込み、質問に回答する"""
    
    # ベクトルDBの読み込み
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    
    # LLMとプロンプトの設定
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
    以下の文脈を踏まえて質問に答えてください。
    文脈: {context}
    質問: {input}
    """)
    
    # チェーンの構築と実行
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    response = rag_chain.invoke({"input": user_input})
    return response["answer"]