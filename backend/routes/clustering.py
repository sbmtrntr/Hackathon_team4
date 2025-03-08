from fastapi import APIRouter
from supabase_client import supabase
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
from sklearn.neighbors import NearestCentroid

router = APIRouter()

def fetch_user_attributes():
    """user_attributes テーブルのデータを取得して DataFrame に変換"""
    user_attributes = supabase.table("user_attributes").select("*").execute()

    if not user_attributes:
        return {"error": "User not found"}

    # Supabase からのレスポンスを Pandas DataFrame に変換
    data = user_attributes.data
    df = pd.DataFrame(data)

    return df

def clustering(df_user_attributes):
    """ユーザー属性データをクラスタリング"""
    # データの前処理
    # ラベルエンコーディング
    mlb = MultiLabelBinarizer()
    df_user_attributes["hobbies"] = df_user_attributes["hobbies"].apply(lambda x: x.split(", "))
    hobby_features = pd.DataFrame(mlb.fit_transform(df_user_attributes["hobbies"]), columns=mlb.classes_)
    df_processed = pd.concat([df_user_attributes.drop("hobbies", axis=1), hobby_features], axis=1)

    # One-hot エンコーディングを適用するカラム
    categorical_columns = ["hometown", "field", "role", "mbti", "alma_mater"]
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = pd.DataFrame(encoder.fit_transform(df_processed[categorical_columns]), 
                                    columns=encoder.get_feature_names_out(categorical_columns))

    # 元のデータと統合
    df_processed = pd.concat([df_processed.drop(categorical_columns, axis=1), encoded_features], axis=1)

    # クラスタリング
    # クラスタリングに使用する特徴量
    X = df_processed.drop(["user_id", "preferences", "self_introductions"], axis=1)  # user_id は除外

    # K-means クラスタリング
    kmeans = KMeans(n_clusters=len(df_processed)//3, random_state=42)
    df_processed["cluster"] = kmeans.fit_predict(X)

    return df_processed

def update_clustering_result():
    # ユーザー属性データを取得
    df_user_attributes = fetch_user_attributes()

    # クラスタリング
    df_clustered = clustering(df_user_attributes)

    try:
        # クラスタリング結果を Supabase に保存
        for index, row in df_clustered.iterrows():
            update_query = f"UPDATE users SET cluster = {row['cluster']} WHERE id = '{row['user_id']}';"
            response = supabase.rpc("execute_sql", {"sql": update_query}).execute()

        return {"message": "Clustering completed"}
    
    except Exception as e:
        return {"error": str(e)}
    

# 新規ユーザーのクラスタリング結果を取得
@router.get("/assign_new_user_to_cluster")
def assign_new_user_to_cluster(user_id: str):
    """新規ユーザーを最も近いクラスタに追加し、Slack チャンネルに招待"""

    # 既存ユーザー情報を取得
    df_users = supabase.table("users").select("id", "cluster").execute()
    df_users = pd.DataFrame(df_users.data)
    df_users.dropna(subset=["cluster"], inplace=True)

    # ユーザー属性情報を取得
    df_user_attributes = supabase.table("user_attributes").select('*').neq("user_id", user_id).execute()
    df_user_attributes = pd.DataFrame(df_user_attributes.data)
    df_user_attributes.dropna(inplace=True)

    # usersテーブルとuser_attributesテーブルを結合
    df_users = df_users.merge(df_user_attributes, left_on="id", right_on="user_id", how="left")

    # 新規ユーザーの情報を取得
    new_user_data = supabase.table("user_attributes").select("*").eq("user_id", user_id).execute()
    new_user = pd.DataFrame(new_user_data.data)

    # 特徴量の前処理
    categorical_columns = ["hometown", "field", "role", "mbti", "alma_mater"]

    # Hobbies の MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    df_users["hobbies"] = df_users["hobbies"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])
    hobby_features = pd.DataFrame(mlb.fit_transform(df_users["hobbies"]), columns=mlb.classes_)

    # One-Hot Encoding
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded_features = pd.DataFrame(encoder.fit_transform(df_users[categorical_columns]), 
                                    columns=encoder.get_feature_names_out(categorical_columns))

    df_processed = pd.concat([df_users.drop(["hobbies"] + categorical_columns, axis=1, errors='ignore'), 
                              hobby_features, encoded_features], axis=1)
    
    # クラスタの重心を計算
    # クラスタリング用の特徴量を作成（id, user_id, cluster, preferences, self_introductions は削除）
    X = df_processed.drop(["id", "user_id", "cluster", "preferences", "self_introductions"], axis=1)
    y = df_users["cluster"]

    # 既存のクラスタ中心を計算
    clf = NearestCentroid()
    clf.fit(X, y)

    # 新規ユーザーの特徴量変換（同じエンコーダを使用）
    new_user["hobbies"] = new_user["hobbies"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])
    new_hobby_features = pd.DataFrame(mlb.transform(new_user["hobbies"]), columns=mlb.classes_)
    new_encoded_features = pd.DataFrame(encoder.transform(new_user[categorical_columns]), 
                                        columns=encoder.get_feature_names_out(categorical_columns))

    new_processed = pd.concat([new_user.drop(["hobbies"] + categorical_columns, axis=1, errors='ignore'),
                               new_hobby_features, new_encoded_features], axis=1)
    
    # 新規ユーザーの特徴量をCSVに保存
    new_processed.to_csv(f"new_user.csv", index=False)

    # 近いクラスタを予測
    new_user_features = new_processed.drop(["user_id", "preferences", "self_introductions"], axis=1, errors='ignore')
    assigned_cluster = int(clf.predict(new_user_features)[0])

    # データベースを更新
    supabase.table("users").update({"cluster": assigned_cluster}).eq("id", user_id).execute()

    return {"message": "User assigned to cluster", "cluster_id": assigned_cluster}