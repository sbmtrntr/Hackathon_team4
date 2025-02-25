from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter()

@router.get("/users")
def users():
    response = supabase.table("users").select("*").execute()
    return response

@router.get("/user_attributes")
def user_attributes():
    response = supabase.table("user_attributes").select("*").execute()
    return response