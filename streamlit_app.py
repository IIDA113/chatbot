import streamlit as st
import requests

# ユーザー情報
users = {
    "lion": "Roar88!",
    "elephant":"Trunk9$",
    "wolf":"W01fRun!",
    "eagle":"FlyEye#",
    "fox":"F0xJump$",
    "dolphin":"Swim@25",
    "owl":"Wis3Owl!",
    "cat":"Me0w#77",
    "ant":"AntWork!",
    "panda":"B4mboo$"
}

# ログイン状態の初期化
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ログインしていない場合のみログイン画面を表示
if not st.session_state.logged_in:
    st.title("Salesight")
    st.write("こちらは売上分析エージェント、Salesightの社内ログイン画面です。")
    st.write("⚠ 関係者限りです。それ以外の方はこの画面をクローズしてください。")
    st.write("⚠ 管理者はFY25_DE新入社員です。何かありましたらご連絡ください。")

    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("ログイン成功！")
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが間違っています")

# ログイン後の画面
if st.session_state.logged_in:
    st.title("Salesight")
    st.write("こちらは売上分析エージェントです。分析したいことを入力してください！")
    st.write("⚠ 管理者はFY25_DE新入社員です。何かありましたらご連絡ください。")
    st.write("⚠ 傷つきやすいから、丁寧にやさしく教えてね。")

    api_gateway_url = "https://bok2c0gsbl.execute-api.ap-northeast-1.amazonaws.com/default/lambda1_FY25_MDS"

    if not api_gateway_url:
        st.info("Lambda API のエンドポイント URL を入力してください。", icon="🔗")
    else:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("メッセージを入力してください"):
            st.session_state.messages = st.session_state.messages[-3:]

            with st.chat_message("user"):
                st.markdown(prompt)

            payload = {
                "text": prompt
            }
            try:
                response = requests.post(api_gateway_url, json=payload)
                response.raise_for_status()
                response_json = response.json()
                
                if isinstance(response_json, dict):
                    assistant_reply = response_json.get("input_text", "")
                    image_url = response_json.get("image_url", None)
                else:
                    assistant_reply = "Lambdaからの応答形式が不正です。"
                    image_url = None
            except Exception as e:
                assistant_reply = f"エラーが発生しました。運用担当者に連絡してください。" # エラー詳細: {e}"
                image_url = None

            with st.chat_message("assistant"):
                if image_url:
                    st.image(image_url)
                else:
                    st.text(assistant_reply)
                    st.error("画像のURLが取得できませんでした。")
