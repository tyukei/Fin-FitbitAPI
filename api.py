# Sessionを使わず、import requestsでもOKです
import streamlit as st
from requests import Session
from pprint import pprint
import json

session = Session()

# with open("./test_conf.json", "r", encoding="utf-8") as f:
#     conf = json.load(f)

def bearer_header():
    """Bearer認証用ヘッダを作成する。
    Args:
        access_token (str): アクセストークン
    Returns:
        dict: 認証ヘッダ
    """
    new_access_token, new_refresh_token = refresh()
    if new_access_token and new_refresh_token:
        access_token = new_access_token
        return {"Authorization": "Bearer " + access_token}
    else:
        return None

def request(method, url, access_token, **kw):
    """
    ...
    Args:
        method (function): ...
        url (str): ...
        access_token (str): アクセストークン
        **kw: その他のキーワード引数
    Returns:
        session.Response: レスポンス
    """
    headers = bearer_header(access_token)
    res = method(url, headers=headers, **kw)
    # その他の処理
    return res


def refresh():
    """
    access_tokenを再取得する。
    新しいaccess_tokenとrefresh_tokenを返す。

    Args:
        refresh_token (str): 現在のリフレッシュトークン
        client_id (str): クライアントID

    Returns:
        tuple: 新しい(access_token, refresh_token)
    """
    refresh_token = st.secrets["refresh_token"]
    client_id = st.secrets["client_id"]

    url = "https://api.fitbit.com/oauth2/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }

    res = session.post(url, data=params)
    res_data = res.json()

    # エラーチェック
    if res_data.get("errors") is not None:
        emsg = res_data["errors"][0]
        print(emsg)
        return None, None

    return res_data["access_token"], res_data["refresh_token"]

# 使用例
# new_access_token, new_refresh_token = refresh(current_refresh_token, client_id)
# if new_access_token and new_refresh_token:
#     # 新しいトークンを使用する



def is_expired(resObj) -> bool:
    """
    Responseから、accesss-tokenが失効しているかチェックする。
    失効ならTrue、失効していなければFalse。Fitbit APIでは8時間が寿命。
    Args:
        reqObj (_type_): response.json()したもの

    Returns:
        boolean: 失効ならTrue、失効していなければFalse
    """

    errors = resObj.get("errors")

    # エラーなし。
    if errors is None:
        return False

    # エラーあり
    for err in errors:
        etype = err.get("errorType")
        if (etype is None):
            continue
        if etype == "expired_token":
            pprint("TOKEN_EXPIRED!!!")
            return True

    # 失効していないのでFalse。エラーありだが、ここでは制御しない。
    return False




def heartbeat(date: str = "today", period: str = "1d"):
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{date}/{period}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

def activity_zone(date: str = "today", period: str = "1d"):
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/activities/active-zone-minutes/date/{date}/{period}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

def activity_summary(date: str = "today", period: str = "1d"):
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/activities/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

def get_step(date: str = "today", period: str = "1d"):
    res = activity_summary(date=date, period=period)
    data = res.json()
    print(data['summary']['steps'])


def breath_summary(date: str = "today", period: str = "1d"):
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/br/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

def hrv_summary(date: str = "today", period: str = "1d"):
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/hrv/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

# get_step()

# 実行例
# res = heartbeat()
# res = activity_zone()
# res = activity_summary()
# res = breath_summary()
# res = hrv_summary()
# data = res.json()
# pprint(data)