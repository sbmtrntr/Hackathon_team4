from fastapi import APIRouter, HTTPException
from supabase_client import supabase
import requests
from config import SLACK_BOT_TOKEN

router = APIRouter()

def get_slack_users():
    url = "https://slack.com/api/users.list"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if not data.get("ok"):
        raise Exception("Slack API Error: " + str(data))

    # 全ユーザのメールアドレスとSlack_IDを取得
    user_emails = {user["profile"].get("email"): user["id"] for user in data["members"] if "email" in user["profile"]}
        
    return user_emails


@router.post("/check_email")
def check_email(email :str):
    slack_users = get_slack_users()

    if email not in slack_users:
        raise HTTPException(status_code=400, detail="このメールアドレスはSlackに登録されていません")

    return {"message": "登録を確認", "slack_id": slack_users[email]}