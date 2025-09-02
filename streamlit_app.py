import streamlit as st
import requests

# タイトルと説明
st.title("売上分析bot")
st.write(
    "分析したいことを入力してください"
)


# Lambda API のエンドポイント URL（コード内で直接指定）
api_gateway_url = "https://bok2c0gsbl.execute-api.ap-northeast-1.amazonaws.com/default/lambda1_FY25_MDS"

if not api_gateway_url:
    st.info("Lambda API のエンドポイント URL を入力してください。", icon="🔗")
else:
    # セッション状態の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 過去のメッセージ表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力受付
    if prompt := st.chat_input("メッセージを入力してください"):
        # ユーザーのメッセージを保存・表示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lambda に送信するペイロード
        payload = {
            "messages": st.session_state.messages
        }

        try:
            # Lambda API に POST リクエストを送信
            response = requests.post("https://bok2c0gsbl.execute-api.ap-northeast-1.amazonaws.com/default/lambda1_FY25_MDS", json=payload)
            response.raise_for_status()
            assistant_reply = response.json().get("reply", "（応答が取得できませんでした）")
        except Exception as e:
            assistant_reply = f"エラーが発生しました: {e}"

        # 応答を表示・保存
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
