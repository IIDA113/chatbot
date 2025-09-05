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

        # セッション状態の初期化
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 直近3件のみ保持するように履歴を制限
        st.session_state.messages = st.session_state.messages[-3:]

        with st.chat_message("user"):
            st.markdown(prompt)


        # Lambda に送信するペイロード（修正後）
        payload = {
            "text": prompt  # 入力されたテキストのみを送信
        }

        try:
            # Lambda API に POST リクエストを送信
            response = requests.post(api_gateway_url, json=payload)
            response.raise_for_status()
            response_json = response.json()
            # 各フィールドを取得
            assistant_reply = response_json.get("input_text", "")
            image_url = response_json.get("image_url", None)
        except Exception as e:
            assistant_reply = f"エラーが発生しました: {e}"

        # 応答を表示・保存
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
            if image_url:
                st.image(image_url)
                #markdown(f'<a href="{image_url}" target="_blank">画像を表示</a>', unsafe_allow_html=True)
            else:
                st.error("画像のURLが取得できませんでした。")

