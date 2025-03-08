from supabase_client import supabase
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder

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
    mlb = MultiLabelBinarizer()
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
    X = df_processed.drop(["user_id", "preferences"], axis=1)  # user_id は除外

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
    
if __name__ == "__main__":
    update_clustering_result()