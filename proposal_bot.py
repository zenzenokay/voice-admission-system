from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
import json

# AIが呼び出す「提案保存関数（モック）」を定義
@tool
def save_proposal_to_db(target_section: str, proposal_summary: str, sentiment: str) -> str:
    """
    ユーザーからの提案や改善案をデータベースに保存します。
    ユーザーが「〜を改善してほしい」「〜のほうがいい」と発言した際に呼び出してください。
    
    Args:
        target_section: 提案の対象となっている箇所（例: "AO入試の評価基準", "WebサイトのUI"など）
        proposal_summary: 提案内容の簡潔な要約
        sentiment: 提案のニュアンス（"positive", "negative", "neutral" のいずれか）
    """
    # 実際はここでSupabase等のDBに保存する処理を書きます
    proposal_data = {
        "target": target_section,
        "summary": proposal_summary,
        "sentiment": sentiment
    }
    return f"システム: 提案（{json.dumps(proposal_data, ensure_ascii=False)}）の保存に成功しました。"

def get_proposal_response(user_input: str):
    """提案を受け付け、必要に応じてツールを呼び出す"""
    
    # 提案抽出用のLLM（ツールをバインド）
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    llm_with_tools = llm.bind_tools([save_proposal_to_db])
    
    # ユーザー入力を評価
    ai_msg = llm_with_tools.invoke(user_input)
    
    # ツール（関数）を呼び出すべきとAIが判断した場合
    if ai_msg.tool_calls:
        tool_call = ai_msg.tool_calls[0]
        args = tool_call["args"]
        
        # ツールの実行（DB保存のモック）
        tool_result = save_proposal_to_db.invoke(args)
        
        # 保存完了後、ユーザーへのお礼メッセージを生成
        final_resp = llm.invoke(
            f"ユーザーの入力: {user_input}\n"
            f"システム処理結果: {tool_result}\n"
            "上記を踏まえ、提案を受け付けたことを感謝とともにユーザーへ短く伝えてください。"
        )
        return final_resp.content, args
    
    # 関数呼び出しが不要な（単なる雑談などの）場合
    else:
        return ai_msg.content, None