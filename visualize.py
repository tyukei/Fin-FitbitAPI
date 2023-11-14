import streamlit as st
from api import heartbeat  
from api import activity_zone   
from api import activity_summary
from api import breath_summary
from api import hrv_summary
from api import get_step

def init_ui():

    st.title('Fitbit Data Viewer')
    st.write('今日の歩数')

    # 日付選択ウィジェット
    date = st.sidebar.date_input("日付を選択")
    if date is not None:
        with st.spinner('Loading...'):
            step=get_step()
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

def main():
    init_ui()

