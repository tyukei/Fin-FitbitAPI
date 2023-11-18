# Sessionを使わず、import requestsでもOKです
import streamlit as st
from requests import Session
from pprint import pprint
import json
from fitbit_token import get_gss_value
from fitbit_token import update_access_token
from fitbit_token import update_refresh_token

session = Session()
uuid = 1
client_id, access_token, refresh_token = None, None, None 

def setupUser(uid):
    global uuid
    global client_id, access_token, refresh_token
    uuid = uid
    client_id, access_token, refresh_token = get_gss_value(uid=uid)
    print(f"client_id: {client_id}")
    print(f"access_token: {access_token}")
    print(f"refresh_token: {refresh_token}")

def bearer_header():
    """Bearer認証用ヘッダを取得する。

    Returns:
        dict: 認証用ヘッダ。

    Raises:
        ValueError: access_token が設定されていない場合に発生。
    """
    # access_token の取得方法を確認する
    # 例: 環境変数、設定ファイル、または Streamlit の secrets から取得

    if access_token is None:
        raise ValueError("アクセストークンが取得できません。")

    return {"Authorization": "Bearer " + access_token}


def refresh():
    """
    access_tokenを再取得し、conf.jsonを更新する。
    refresh_tokenは再取得に必要なので重要。
    is_expiredがTrueの時のみ呼ぶ。
    False時に呼んでも一式更新されるので、実害はない。
    """

    url = "https://api.fitbit.com/oauth2/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }

    # POST実行。 Body部はapplication/x-www-form-urlencoded。requestsならContent-Type不要。
    res = session.post(url, data=params)

    # responseをパース
    res_data = res.json()

    # errorあり
    if res_data.get("errors") is not None:
        emsg = res_data["errors"][0]
        print(emsg)
        return


    update_access_token(uid=uuid, access_token=res_data["access_token"])
    update_refresh_token(uid=uuid, refresh_token=res_data["refresh_token"])


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


def request(method, url, **kw):
    """
    sessionを通してリクエストを実行する関数。
    アクセストークンが8Hで失効するため、失効時は再取得し、
    リクエストを再実行する。
    レスポンスはパースしないので、呼ぶ側で.json()なり.text()なりすること。

    Args:
        method (function): session.get,session.post...等
        url (str): エンドポイント
        **kw: headers={},params={}を想定

    Returns:
        session.Response: レスポンス
    """

    # パラメタで受け取った関数を実行し、jsonでパース
    res = method(url, **kw)
    res_data = res.json()

    if is_expired(res_data):
        # 失効していしている場合、トークンを更新する
        refresh()
        # headersに設定されているトークンも
        # 新しい内容に更新して、methodを再実行
        kw["headers"] = bearer_header()
        res = method(url, **kw)
    # parseしていないほうを返す
    return res


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
    print(data)

    # Check if 'summary' key exists in the response
    if 'summary' in data:
        return data['summary']['steps']
    else:
        print(f"'summary' key not found in response for date {date}")
        return 0 

def get_user():
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/profile.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

def get_displayn_name():
    res = get_user()
    data = res.json()

    # Check if 'summary' key exists in the response
    if 'user' in data:
        return data['user']['displayName']
    else:
        return 0


def breath_summary():
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/profile.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

def hrv_summary(date: str = "today", period: str = "1d"):
    # パラメタを埋め込んでエンドポイント生成
    url = f"https://api.fitbit.com/1/user/-/hrv/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res

# 実行例
# res = heartbeat()
# res = activity_zone()
# res = activity_summary()
# res = breath_summary()
# res = hrv_summary()
# data = res.json()
# pprint(data)