from fastapi import APIRouter, HTTPException
from supabase_client import supabase
import requests
from urllib.parse import urlencode
from config import SLACK_BOT_TOKEN

router = APIRouter()

@router.get("/check_email")
def check_email(email: str):
    url = "https://slack.com/api/users.list"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if not data.get("ok"):
        raise HTTPException(status_code=500, detail="Slack API Error: " + str(data))

    # 全ユーザのメールアドレスとSlack_IDを取得
    slack_users = {user["profile"].get("email"): user["id"] for user in data["members"] if "email" in user["profile"]}

    if email not in slack_users:
        raise HTTPException(status_code=400, detail="このメールアドレスはSlackに登録されていません")

    return {"message": "登録を確認", "slack_id": slack_users[email]}


@router.get("/connect_dm")
def connect_dm(slack_id1: str, slack_id2: str):
    url = "https://slack.com/api/conversations.open"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"users": [slack_id1, slack_id2]}
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if not data.get("ok"):
        raise HTTPException(status_code=500, detail=f"Slack API Error: {data.get('error')}")

    channel_id = data["channel"]["id"]
    slack_dm_url = f"https://slack.com/app_redirect?{urlencode({'channel': channel_id})}"

    return {"URL": slack_dm_url}