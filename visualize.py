import streamlit as st
from api import heartbeat  
from api import activity_zone   
from api import activity_summary
from api import breath_summary
from api import hrv_summary
from api import get_step
from api import setupUser
from api import get_user
import api

def init_ui():

    st.title('Fitbit Data Viewer')
    display_name = api.get_displayn_name()
    header = st.header(f"ようこそ{display_name}さん")
    uid = st.sidebar.number_input('uid', min_value=1, max_value=100, value=1, step=1)

    setupUser(uid+1)
    display_name = api.get_displayn_name()
    header.header(f"ようこそ{display_name}さん")

    # 日付選択ウィジェット

    date = st.sidebar.date_input("日付を選択")
    if date is not None:
        step=get_step(date=date.strftime("%Y-%m-%d"))
        st.write(f"{date.strftime('%Y-%m-%d')}の歩数は{step}歩です")



    # データ取得ボタン
    if st.button('heartrate data'):
        response = heartbeat(date=date.strftime("%Y-%m-%d"))
        data = response.json()
        st.json(data) 

    if st.button('activity zone data'):
        response = activity_zone(date=date.strftime("%Y-%m-%d"))
        data = response.json()
        st.json(data) 

    if st.button('activity summary data'):
        response = activity_summary(date=date.strftime("%Y-%m-%d"))
        data = response.json()
        st.json(data)

    if st.button('breath summary data'):
        response = breath_summary(date=date.strftime("%Y-%m-%d"))
        data = response.json()
        st.json(data)
        
    if st.button('hrv summary data'):
        response = hrv_summary(date=date.strftime("%Y-%m-%d"))
        data = response.json()
        st.json(data)

    if st.button('user'):
        response = get_user()
        data = response.json()
        st.json(data)

def main():
    init_ui()

