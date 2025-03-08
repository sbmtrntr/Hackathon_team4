from fastapi import APIRouter, HTTPException
from supabase_client import supabase
import requests
from urllib.parse import urlencode
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_BOT_TOKEN

router = APIRouter()
client = WebClient(token=SLACK_BOT_TOKEN)

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


def create_slack_channel(channel_name):
    """Slackのプライベートチャンネルを作成"""
    try:
        response = client.conversations_create(name=channel_name, is_private=True)
        return response["channel"]["id"]
    except SlackApiError as e:
        print(f"Error creating channel: {e.response['error']}")
        return None
    

def invite_users_to_channel(channel_id, user_ids):
    """Slackチャンネルにユーザーを招待"""
    try:
        client.conversations_invite(channel=channel_id, users=user_ids)
        print(f"Invited users {user_ids} to channel {channel_id}")
    except SlackApiError as e:
        print(f"Error inviting users: {e.response['error']}")


# クラスタごとに Slack チャンネルを作成し、ユーザーを追加
for cluster_id, group in df_processed.groupby("cluster"):
    channel_name = f"group_{cluster_id}"
    channel_id = create_slack_channel(channel_name)
    
    if channel_id:
        user_ids = group["user_id"].tolist()  # Supabase の user_id を Slack のユーザーID に変換する処理が必要
        invite_users_to_channel(channel_id, user_ids)