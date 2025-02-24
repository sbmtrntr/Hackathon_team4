from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter()

@router.post("/matching_result")
def matching_result():
    return {"ここで最終的な":"マッチング結果を返す"}