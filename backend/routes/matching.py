from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter()

@router.get("/matching_result")
def get_matching_result(user_id: str):
    # リクエストされたユーザー情報を取得
    target_user_data = supabase.table("user_attributes").select("*").eq("user_id", user_id).single().execute()
    if not target_user_data:
        return {"error": "User not found"}

    target_user = target_user_data.data

    # その人以外の全ユーザーを取得
    other_users_data = supabase.table("user_attributes").select("*").neq("user_id", user_id).execute()
    other_users = other_users_data.data

    # すべてのユーザーとマッチ度を計算
    match_results = [calculate_match_score(target_user, other_user) for other_user in other_users]
    print(match_results)

    # スコア順にソート
    match_results = sorted(match_results, key=lambda x: x["match_score"], reverse=True)

    # 上位5人を返す
    return {"matches": match_results[:5]}


# マッチ度計算用の関数
def calculate_match_score(target_user, other_user):
    match_scores = {
        "hometown": 0.0,
        "field": 0.0,
        "role": 0.0,
        "mbti": 0.0,
        "alma_mater": 0.0,
        "hobbies": 0.0,
    }

    # ここから担当（さやチュウ）
    # 出身地 (hometown) が一致したらmatch_scores["hometown"]に加算する
    
    # 志望分野 (field) が一致したらmatch_scores["field"]加算する

    # 志望職種 (role) が一致したらmatch_scores["role"]に加算する

    # MBTI (mbti) が一致したらmatch_scores["mbti"]に加算する（できれば一致だけでなく、相性がいいmbti同士でも加算したい）

    # 出身大学 (alma_mater) が一致したらmatch_scores["alma_mater"]に加算する


    # 趣味のマッチ度を計算(担当：shibarin)
    target_hobbies = target_user["hobbies"].split(",")
    other_hobbies = other_user["hobbies"].split(",")
    for target_hobby in target_hobbies:
        for other_hobby in other_hobbies:
            if target_hobby == other_hobby:
                match_scores["hobbies"] += 1.0
    if len(target_hobbies) > 0:
        match_scores["hobbies"] /= len(target_hobbies) # 0~1に正規化
    
    """
    単語からベクトルにして類似度を計算する方法
    from gensim.models import Word2Vec
    model = Word2Vec.load('routes/content/ja.bin')
    target_user_hobbies = target_user["hobbies"].split(",")
    other_user_hobbies = other_user["hobbies"].split(",")

    hobby_similarity = 0
    count = 0
    for tuh in target_user_hobbies:
        for ouh in other_user_hobbies:
            if tuh in model.wv and ouh in model.wv:
                print(tuh, ouh, model.wv.similarity(tuh, ouh))
                hobby_similarity += model.wv.similarity(tuh, ouh)
                count += 1
    if count > 0:
        hobby_similarity /= count # 0~1に正規化

    match_scores["hobbies"] += hobby_similarity
    """

    # preference（重視する点）を考慮し、該当項目のスコアに重みをつける（担当：しんや）
    # 例：target_userが「hometown」を重視している場合（つまり target_user["preferences"] == hometown"）、match_scores["hometown"]に重みをつける
    
    # スコアを合計
    score = round(sum(match_scores.values()), 2)

    return {"user_id": other_user["user_id"], "match_score": score}