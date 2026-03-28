import streamlit as st
from dotenv import load_dotenv

# 外部モジュールの読み込み
import rag_bot
import proposal_bot

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(page_title="声が届く入試設計", layout="centered")

# サイドバー
st.sidebar.title("設定")
mode = st.sidebar.radio(
    "AIのモードを選択してください",
    ["質問モード", "提案モード"]
)
st.sidebar.markdown("---")
st.sidebar.write(f"現在のモード: **{mode}**")

# メインコンテンツ
st.title("声が届く入試設計")

doc_container = st.container(height=400, border=True)

with doc_container:
    st.markdown("""
    ### 1. 入試制度の全体像
    現在の日本の大学入試は、多様な背景や能力を持つ学習者を適切に評価するため、大きく分けて「3つの選抜方式」で構成されています。それぞれの方式が異なる評価軸を持ち、受験生は自身の強みや志望理由に合わせて方式を選択することができます。

    ### 2. 主な選抜方式

    #### ① 一般選抜
    主に学力検査（ペーパーテスト）の得点を重視して合否を判定する、最も受験者数が多い方式です。
    * **国公立大学**：原則として「大学入学共通テスト」を受験し、その後に各大学が実施する「個別学力検査（2次試験）」を受験して総合点で判定されます。
    * **私立大学**：各大学が独自に作成する試験を受験する方式や、共通テストの成績を利用して判定する方式など、多様なパターンが存在します。

    #### ② 総合型選抜（旧AO入試）
    大学が求める学生像（アドミッション・ポリシー）と、受験生の人物像や大学で学ぶ意欲が合致しているかを時間をかけて総合的に評価する方式です。
    * **評価方法**：書類審査（志望理由書、活動報告書など）、小論文、面接、プレゼンテーションなどを組み合わせて多角的に評価されます。近年は基礎学力を問うテストを併用する大学も増えています。

    #### ③ 学校推薦型選抜（旧推薦入試）
    出身高等学校の校長の推薦に基づき、高校時代の学業成績（評定平均）や課外活動の実績などを評価する方式です。
    * **指定校制**：大学が指定した特定の高校の生徒のみが出願できる方式です。
    * **公募制**：大学が定める出願条件を満たしていれば、全国どの高校からでも出願できる方式です。
    """)


# 画面下部チャットボットUI
st.markdown("<br><br>", unsafe_allow_html=True) # ドキュメントとボタンの間に余白を作る

if "messages" not in st.session_state:
    st.session_state.messages = []

# st.expanderを使ってチャット画面を開閉可能にする
expander_title = "AIに質問する / 提案する"
with st.expander(expander_title, expanded=False):
    
    # チャット履歴を表示するコンテナ
    chat_container = st.container(height=400, border=False)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # チャットの入力欄
    if user_input := st.chat_input("メッセージを入力..."):
        # ユーザー入力を表示
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)

        # ボットの応答処理
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("考え中..."):
                    
                    if mode == "質問モード":
                        # RAGで回答
                        answer = rag_bot.get_rag_response(user_input)
                        st.markdown(answer)
                        
                    elif mode == "提案モード":
                        # 提案処理とツール呼び出し
                        answer, saved_data = proposal_bot.get_proposal_response(user_input)
                        st.markdown(answer)
                        
                        # デバッグ・管理用: 裏側で抽出されたデータを画面に表示
                        if saved_data:
                            st.success(f"【裏側の処理】以下のデータがDBに送信されました:\n"
                                       f"- 対象: {saved_data.get('target_section')}\n"
                                       f"- 要約: {saved_data.get('proposal_summary')}\n"
                                       f"- 感情: {saved_data.get('sentiment')}", icon="💾")

        # ボットの回答を履歴に追加
        st.session_state.messages.append({"role": "assistant", "content": answer})