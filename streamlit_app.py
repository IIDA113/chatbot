import streamlit as st
import requests


users = {
    "demotype": "fy25"
}

st.title("社内ログイン")

username = st.text_input("ユーザー名")
password = st.text_input("パスワード", type="password")


if st.button("ログイン"):
    if username in users and users[username] == password:
        st.success("ログイン成功！")

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

                    # 応答形式の確認と取得
                    if isinstance(response_json, dict):
                        assistant_reply = response_json.get("input_text", "")
                        image_url = response_json.get("image_url", None)
                    else:
                        assistant_reply = "Lambdaからの応答形式が不正です。"
                        image_url = None
                except Exception as e:
                    assistant_reply = f"エラーが発生しました。管理者に連絡してください。エラー詳細: {e}"

                # 応答を表示・保存
                with st.chat_message("assistant"):
                    st.text(assistant_reply)
                    if image_url:
                        st.image(image_url)
                        #markdown(f'<a href="{image_url}" target="_blank">画像を表示</a>', unsafe_allow_html=True)
                    else:
                        st.error("画像のURLが取得できませんでした。")
    else:
        st.error("ユーザー名またはパスワードが間違っています")

