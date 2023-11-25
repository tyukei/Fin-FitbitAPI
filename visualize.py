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
    st.sidebar.title('version 1.0.1')
    display_name = api.get_displayn_name()
    uid = st.sidebar.number_input('uid', min_value=1, max_value=100, value=1, step=1)
    

    setupUser(uid=uid)
    display_name = api.get_displayn_name()
    st.header(f"ようこそ{display_name}さん")

    date = st.sidebar.date_input("日付を選択")
    st.write('---')
    if date is not None:
        step=get_step(date=date.strftime("%Y-%m-%d"))
        st.write(f"{date.strftime('%Y-%m-%d')}の歩数は{step}歩です")

    st.write('---')
    st.write("データが取得できない場合は、再読み込みボタンを押してください")
    if st.button('再読み込み'):
        st.rerun()


    st.write('---')
    st.write("データ取得ボタンを押すと、json形式でデータが表示されます")
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

