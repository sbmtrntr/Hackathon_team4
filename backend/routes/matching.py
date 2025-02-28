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
    if target_user["hometown"] == other_user["hometown"]:
        match_scores["hometown"] += 1.0
    # 志望分野 (field) が一致したらmatch_scores["field"]加算する
    if target_user["field"] == other_user["field"]:
        match_scores["field"] += 1.0
    # 志望職種 (role) が一致したらmatch_scores["role"]に加算する
    if target_user["role"] == other_user["role"]:
        match_scores["role"] += 1.0
    # MBTI (mbti）の相性が良いまたは同じだったらmatch_scores["mbti"]に加算する
    mbti1 = target_user["mbti"]
    mbti2 = other_user["mbti"]
    
    #MBTIが完全一致なら+0.8、
    #相性が良い組み合わせなら+1.0。
    
    best_matches = {
        "INTJ": ["ESFJ", "ISFP", "INTP"],
        "INTP": ["ESFP", "ISFJ", "ENTJ"],
        "ENTJ": ["ISFJ", "INFP", "INTP"],
        "ENTP": ["ISFP", "ESTP", "ENFP"],
        "INFJ": ["ESTJ", "INFP", "ENFP"],
        "INFP": ["ESTP", "ENFJ", "INFJ"],
        "ENFJ": ["ISTJ", "INFP", "ESTP"],
        "ENFP": ["ISTP", "ESTJ", "INFJ"],
        "ISTJ": ["ENFJ", "ESTP", "ESFJ"],
        "ISFJ": ["ENTJ", "INTP", "INFP"],
        "ESTJ": ["INFJ", "ISFJ", "ESFJ"],
        "ESFJ": ["INTJ", "ENTP", "ISFP"],
        "ISTP": ["ENFP", "INFJ", "ESTJ"],
        "ISFP": ["ENTP", "INTJ", "ESFP"],
        "ESTP": ["INFP", "ENTP", "ESFJ"],
        "ESFP": ["INTP", "ENTJ", "ISFJ"],
    }
    
    if mbti1 == mbti2:
        match_scores["mbti"] += 0.8
    elif mbti2 in best_matches.get(mbti1, []):
        match_scores["mbti"] += 1.0
    else:
        match_scores["mbti"] += 0.0

    # 出身大学 (alma_mater) が一致したらmatch_scores["alma_mater"]に加算する
    if target_user["alma_mater"] == other_user["alma_mater"]:
        match_scores["alma_mater"] += 1.0    

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

    # 重み(何倍にするか)を設定
    # とりあえず一律で1.5倍
    # preferenceを選ぶ際に、押した回数分だけ重みを倍増させるようにしても面白いかもしれません
    preference_weights = {
        "hometown": 1.5,
        "field": 1.5,
        "role": 1.5,
        "mbti": 1.5,
        "alma_mater": 1.5,
        "hobbies": 1.5,
    }

    # target_user["preferences"]をリストにし、複数のpreferenceを選べることを想定
    target_user_preferences = target_user.get("preferences", [])
    # 文字列の場合、リスト化
    if isinstance(target_user_preferences, str):
        target_user_preferences = target_user_preferences.split(",")
    
    # target_user["preferences"]に指定された項目のスコアを重み付け
    for target_user_preference in target_user_preferences:
        if target_user_preference in match_scores:
            match_scores[target_user_preference] *= preference_weights.get(target_user_preference, 1)

    # スコアを合計
    score = round(sum(match_scores.values()), 2)

    return {"user_id": other_user["user_id"], "match_score": score}