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


@router.get("/send-greeting")
def send_greeting(user1_slack_id: str, user2_slack_id: str, common_point: str):
    try:
        # DMチャネルを開く
        response = client.conversations_open(users=[user1_slack_id, user2_slack_id])
        channel_id = response["channel"]["id"]

        user2_name = supabase.table("users").select("name").eq("slack_id", user2_slack_id).execute().data[0]["name"]

        # メッセージ内容
        message = f"こんにちは！あなたと{user2_name}さんには{common_point}の共通点があります。まずは挨拶してみましょう"

        # メッセージを送信
        client.chat_postMessage(channel=channel_id, text=message)
        
        return {"message": "メッセージが送信されました。", "channel_id": channel_id}

    except SlackApiError as e:
        return {"error": f"Slack APIエラー: {e.response['error']}"}


@router.get("/invite")
def invite_user_to_slack(user_id: str):
    # Supabase から `cluster_id` を取得
    response = supabase.table("users").select("cluster").eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")

    cluster_id = response.data[0]["cluster"]
    
    # クラスタ ID から Slack チャンネル ID を取得
    channel_id = CLUSTER_TO_CHANNEL.get(cluster_id)
    if not channel_id:
        raise HTTPException(status_code=400, detail="Cluster ID is not mapped to a Slack channel")

    # ユーザーの Slack ID を取得
    response = supabase.table("users").select("slack_id").eq("id", user_id).execute()
    if not response.data or not response.data[0]["slack_id"]:
        raise HTTPException(status_code=400, detail="Slack ID not found for user")

    slack_user_id = response.data[0]["slack_id"]

    # Slack API でチャンネルに招待
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    invite_response = requests.post(
        "https://slack.com/api/conversations.invite",
        headers=headers,
        json={"channel": channel_id, "users": slack_user_id}
    )

    invite_data = invite_response.json()
    if not invite_data.get("ok"):
        raise HTTPException(status_code=500, detail=f"Slack API error: {invite_data.get('error')}")

    # チャンネルのリンクを生成して返す
    invite_link = f"https://slack.com/app_redirect?channel={channel_id}"
    return {"channel_id": channel_id, "invite_link": invite_link}