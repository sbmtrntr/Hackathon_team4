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


def get_channel_id():
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    
    # Slack APIでチャンネルリストを取得
    response = requests.get(
        "https://slack.com/api/conversations.list",
        headers=headers
    )
    
    # Slack APIのレスポンスが正常か確認
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Slack API request failed")

    data = response.json()
    
    # チャンネルが正常に取得できたか確認
    if not data.get("ok"):
        raise HTTPException(status_code=500, detail="Failed to retrieve channels from Slack")

    channel_name2id = {}
    # チャンネルリストをループして指定されたチャンネル名を探す
    for channel in data.get("channels", []):
        channel_name2id[channel["name"]] = channel["id"]

    return channel_name2id


@router.get("/invite")
def invite_user_to_slack(user_id: str):
    # Supabase から `cluster_id` を取得
    response = supabase.table("users").select("cluster").eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")

    cluster_id = str(response.data[0]["cluster"])
    
    # クラスタ ID から Slack チャンネル ID を取得
    channel_name2id = get_channel_id()
    print(channel_name2id)
    channel_id = channel_name2id[cluster_id]
    if not channel_id:
        raise HTTPException(status_code=400, detail="Cluster ID is not mapped to a Slack channel")

    # チャンネルのリンクを生成して返す
    invite_link = f"https://slack.com/app_redirect?channel={channel_id}"
    return {"URL": invite_link}


@router.get("/join_slack_bot")
def join_slack_bot(id: str, common_point: str):
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    
    # チャンネル名を指定してチャンネルIDを取得
    channel_id = get_channel_id()[id]  # チャンネル名 "general" を使用（変更可能）
    
    # チャンネルに参加
    join_response = requests.post(
        "https://slack.com/api/conversations.join",
        headers=headers,
        json={"channel": channel_id}
    )
    
    # 参加できたか確認
    if not join_response.json().get("ok"):
        raise HTTPException(status_code=500, detail="Failed to join the channel")

    # メッセージを送信
    message_payload = {
        "channel": channel_id,
        "text": f"""
        こんにちは！このグループには{common_point}の似ている人が集まっています。
まずはお互いに挨拶してみましょう！
        """
    }
    
    send_message_response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        json=message_payload
    )
    
    # メッセージ送信が成功したか確認
    if not send_message_response.json().get("ok"):
        raise HTTPException(status_code=500, detail="Failed to send message to the channel")

    return {"status": "success", "message": "Bot joined the channel and sent a message"}