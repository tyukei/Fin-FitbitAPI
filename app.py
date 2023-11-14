import streamlit as st
import visualize  

# 認証情報の設定
VALID_USERNAME = "fin"
VALID_PASSWORD = "123456"

# 認証状態を保持するセッション変数
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# ユーザー認証関数
def authenticate(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

# 認証フォームの表示
if not st.session_state['authenticated']:
    with st.form("login_form"):
        username = st.text_input("ユーザー名")
        password = st.text_input("パスワード", type="password")
        submit_button = st.form_submit_button("ログイン")

        if submit_button:
            if authenticate(username, password):
                st.session_state['authenticated'] = True
                st.experimental_rerun()
            else:
                st.error("ログイン失敗：ユーザー名またはパスワードが間違っています")


if st.session_state['authenticated']:
    visualize.main()


