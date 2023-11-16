import os
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import toml
import json

load_dotenv()

# 環境変数の設定
GSS_TEMP_KEY = st.secrets["GSS_TEMP_KEY"]


# worksheetの情報を返す関数
def get_gss_worksheet(gss_name, gss_sheet_name):
    # jsonファイルを使って認証情報を取得
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # st.secretsから認証情報を取得し、辞書に変換
    credentials = dict(st.secrets["google_credentials"])

    # 辞書を使って認証情報のオブジェクトを作成
    c = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)

    # 認証情報を使ってスプレッドシートの操作権を取得
    gs = gspread.authorize(c)

    # スプレッドシート名をもとに、キーを設定
    if gss_name == "FitbitKey":
        spreadsheet_key = GSS_TEMP_KEY  # このGSS_TEMP_KEYは適切に定義してください

    # 共有したスプレッドシートのキーを使ってシートの情報を取得
    worksheet = gs.open_by_key(spreadsheet_key).worksheet(gss_sheet_name)

    return worksheet

def get_gss_value(uid):
    # スプレッドシートを定義
    worksheet = get_gss_worksheet(gss_name='FitbitKey', gss_sheet_name='シート1')

    client_id_cell = 'B' + str(uid)
    # スプレッドシートを読み込み
    client_id = worksheet.acell(client_id_cell).value

    access_token_cell = 'C' + str(uid)
    access_token = worksheet.acell(access_token_cell).value

    refresh_token_cell = 'D' + str(uid)
    refresh_token = worksheet.acell(refresh_token_cell).value

    list = [client_id, access_token, refresh_token]
    return list

def update_client_id(uid, client_id):
    worksheet = get_gss_worksheet(gss_name='FitbitKey', gss_sheet_name='シート1')
    gss_cell = 'B' + str(uid)
    worksheet.update_acell(gss_cell, client_id)

def update_access_token(uid, access_token):
    worksheet = get_gss_worksheet(gss_name='FitbitKey', gss_sheet_name='シート1')
    gss_cell = 'C' + str(uid)
    worksheet.update_acell(gss_cell, access_token)

def update_refresh_token(uid, refresh_token):
    worksheet = get_gss_worksheet(gss_name='FitbitKey', gss_sheet_name='シート1')
    gss_cell = 'D' + str(uid)
    worksheet.update_acell(gss_cell, refresh_token)

