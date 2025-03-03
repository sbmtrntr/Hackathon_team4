from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter()

# 各テーブルの作成クエリ

# ユーザの個人情報を格納するテーブル
# 使用目的：ユーザーの個人情報を保存し、ログイン認証やSlack誘導の際に利用する。
CREATE_USERS_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    slack_id VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATE NOT NULL
);
"""

# ユーザの属性情報を格納するテーブル
# 使用目的：ユーザーの属性情報を保存し、マッチングの際に利用する。
CREATE_USER_ATTRIBUTES_SQL = """
CREATE TABLE IF NOT EXISTS user_attributes (
    user_id UUID PRIMARY KEY,
    hobbies TEXT NOT NULL,
    hometown VARCHAR(50),
    field VARCHAR(10) CHECK (field IN ('公共', '法人', '金融', 'TC&S', '技統本')) NOT NULL,
    role VARCHAR(10) CHECK (role IN ('SE', '営業', 'コンサル', 'スタッフ')) NOT NULL,
    mbti VARCHAR(4) CHECK (mbti IN ('INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP')) NOT NULL,
    alma_mater VARCHAR(100) NOT NULL,
    preferences VARCHAR(10) CHECK (preferences IN ('hobbies', 'hometown', 'field', 'role', 'mbti', 'alma_mater')) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# ユーザのいいね履歴を格納するテーブル
# 使用目的：ユーザーが相手に「いいね」した記録を保存し、マッチングの成立を判定する。
CREATE_LIKES_SQL = """
    CREATE TABLE likes (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES users(id) ON DELETE CASCADE,
        target_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, target_user_id) -- 1人につき1回だけ「いいね」できる
    );
"""

# ユーザのマッチング履歴を格納するテーブル
# 使用目的：双方が「いいね」したらマッチングが成立し、それを保存する。
CREATE_MATCHES_SQL = """
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user1_id UUID REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID REFERENCES users(id) ON DELETE CASCADE,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user1_id, user2_id) -- 重複マッチを防ぐ
);
"""


# 各テーブルの削除クエリ

DROP_USERS_SQL = "DROP TABLE IF EXISTS users CASCADE;"
DROP_USER_ATTRIBUTES_SQL = "DROP TABLE IF EXISTS user_attributes CASCADE;"
DROP_LIKES_SQL = "DROP TABLE IF EXISTS likes CASCADE;"
DROP_MATCHES_SQL = "DROP TABLE IF EXISTS matches CASCADE;"

# 各テーブルの架空データ挿入クエリ
INSERT_USERS_SQL = """
INSERT INTO users (name, email, slack_id, password_hash, created_at) VALUES
('田中 太郎', 'tanaka.taro@example.com', 'U12345678', crypt('securepassword1', gen_salt('bf')), '2023-05-01'),
('佐藤 花子', 'sato.hanako@example.com', 'U87654321', crypt('securepassword2', gen_salt('bf')), '2023-05-02'),
('鈴木 一郎', 'suzuki.ichiro@example.com', 'U23456789', crypt('securepassword3', gen_salt('bf')), '2023-05-03'),
('高橋 次郎', 'takahashi.jiro@example.com', 'U34567890', crypt('securepassword4', gen_salt('bf')), '2023-05-04'),
('山本 三郎', 'yamamoto.saburo@example.com', 'U45678901', crypt('securepassword5', gen_salt('bf')), '2023-05-05'),
('中村 四郎', 'nakamura.shiro@example.com', 'U56789012', crypt('securepassword6', gen_salt('bf')), '2023-05-06'),
('小林 五子', 'kobayashi.goko@example.com', 'U67890123', crypt('securepassword7', gen_salt('bf')), '2023-05-07'),
('加藤 六太', 'kato.rokuta@example.com', 'U78901234', crypt('securepassword8', gen_salt('bf')), '2023-05-08'),
('伊藤 七美', 'ito.nanami@example.com', 'U89012345', crypt('securepassword9', gen_salt('bf')), '2023-05-09'),
('渡辺 八郎', 'watanabe.hachiro@example.com', 'U90123456', crypt('securepassword10', gen_salt('bf')), '2023-05-10'),
('松本 九兵衛', 'matsumoto.kyube@example.com', 'U01234567', crypt('securepassword11', gen_salt('bf')), '2023-05-11'),
('林 十一', 'hayashi.juichi@example.com', 'U11223344', crypt('securepassword12', gen_salt('bf')), '2023-05-12'),
('清水 京子', 'shimizu.kyoko@example.com', 'U22334455', crypt('securepassword13', gen_salt('bf')), '2023-05-13'),
('山田 一子', 'yamada.kazuko@example.com', 'U33445566', crypt('securepassword14', gen_salt('bf')), '2023-05-14'),
('藤田 光', 'fujita.hikaru@example.com', 'U44556677', crypt('securepassword15', gen_salt('bf')), '2023-05-15'),
('岡本 真', 'okamoto.makoto@example.com', 'U55667788', crypt('securepassword16', gen_salt('bf')), '2023-05-16'),
('島田 空', 'shimada.sora@example.com', 'U66778899', crypt('securepassword17', gen_salt('bf')), '2023-05-17'),
('原田 瞳', 'harada.hitomi@example.com', 'U77889900', crypt('securepassword18', gen_salt('bf')), '2023-05-18'),
('三浦 蓮', 'miura.ren@example.com', 'U88990011', crypt('securepassword19', gen_salt('bf')), '2023-05-19'),
('石井 風', 'ishii.kaze@example.com', 'U99001122', crypt('securepassword20', gen_salt('bf')), '2023-05-20');

"""

INSERT_USER_ATTRIBUTES_SQL = """
INSERT INTO user_attributes (user_id, hobbies, hometown, field, role, mbti, alma_mater, preferences) VALUES
((SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), '読書, 旅行, 映画鑑賞', '東京都', '公共', 'SE', 'INTJ', '東京大学', 'hometown'),
((SELECT id FROM users WHERE email = 'sato.hanako@example.com'), '料理, ボードゲーム, カメラ', '大阪府', '法人', '営業', 'ENTP', '京都大学', 'field'),
((SELECT id FROM users WHERE email = 'suzuki.ichiro@example.com'), '登山, スポーツ観戦, 音楽', '愛知県', '金融', 'コンサル', 'INFJ', '一橋大学', 'role'),
((SELECT id FROM users WHERE email = 'takahashi.jiro@example.com'), 'ゲーム, プログラミング, カフェ', '福岡県', 'TC&S', 'SE', 'ISTP', '大阪大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'yamamoto.saburo@example.com'), '映画鑑賞, 読書, キャンプ', '北海道', '技統本', 'スタッフ', 'ENFP', '東北大学', 'mbti'),
((SELECT id FROM users WHERE email = 'nakamura.shiro@example.com'), '釣り, 旅行, DIY', '京都府', '公共', '営業', 'ESTJ', '名古屋大学', 'alma_mater'),
((SELECT id FROM users WHERE email = 'kobayashi.goko@example.com'), '登山, スポーツ観戦, 料理', '兵庫県', '法人', 'コンサル', 'ISFJ', '東京大学', 'hometown'),
((SELECT id FROM users WHERE email = 'kato.rokuta@example.com'), 'DIY, 読書, 筋トレ', '広島県', '金融', 'スタッフ', 'ENTJ', '京都大学', 'field'),
((SELECT id FROM users WHERE email = 'ito.nanami@example.com'), 'アニメ, ゲーム, 映画鑑賞', '宮城県', 'TC&S', 'SE', 'INFP', '東北大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'watanabe.hachiro@example.com'), 'カメラ, 旅行, 読書', '長野県', '技統本', '営業', 'ESFP', '大阪大学', 'mbti'),
((SELECT id FROM users WHERE email = 'matsumoto.kyube@example.com'), 'キャンプ, バスケットボール, 料理', '新潟県', '公共', 'コンサル', 'ISTJ', '東京大学', 'alma_mater'),
((SELECT id FROM users WHERE email = 'hayashi.juichi@example.com'), '映画鑑賞, 音楽, 読書', '岡山県', '法人', 'スタッフ', 'ISFP', '京都大学', 'hometown'),
((SELECT id FROM users WHERE email = 'shimizu.kyoko@example.com'), '釣り, スポーツ観戦, 旅行', '茨城県', '金融', 'SE', 'ENFJ', '一橋大学', 'field'),
((SELECT id FROM users WHERE email = 'yamada.kazuko@example.com'), 'ガーデニング, カフェ, ボードゲーム', '栃木県', 'TC&S', '営業', 'ESTP', '東北大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'fujita.hikaru@example.com'), '筋トレ, 読書, 音楽', '群馬県', '技統本', 'コンサル', 'INTP', '京都大学', 'role'),
((SELECT id FROM users WHERE email = 'okamoto.makoto@example.com'), 'ランニング, 料理, 登山', '静岡県', '公共', 'スタッフ', 'ESFJ', '名古屋大学', 'role'),
((SELECT id FROM users WHERE email = 'shimada.sora@example.com'), '映画鑑賞, ゲーム, プログラミング', '熊本県', '法人', 'SE', 'INFJ', '大阪大学', 'hometown'),
((SELECT id FROM users WHERE email = 'harada.hitomi@example.com'), 'キャンプ, 旅行, 読書', '山形県', '金融', '営業', 'ISTP', '一橋大学', 'mbti'),
((SELECT id FROM users WHERE email = 'miura.ren@example.com'), 'ランニング, 登山, 読書', '滋賀県', 'TC&S', 'コンサル', 'ENTP', '東京大学', 'alma_mater'),
((SELECT id FROM users WHERE email = 'ishii.kaze@example.com'), '音楽, ダンス, 料理', '奈良県', '技統本', 'スタッフ', 'INTJ', '東北大学', 'mbti');
"""

INSERT_LIKES_SQL = """
INSERT INTO likes (id, user_id, target_user_id, created_at) VALUES
('b1f94672-4c23-4a8e-b5c5-61b4f3f5e7a1', 'bcc6f8ab-38cd-46b2-bd61-ac3d38546798', 'bfbc7642-091b-4d98-bce8-07aa4a7516e3', '2025-03-03 12:00:00'),
('c2e58a6b-2d1f-48f6-b871-9a362b4f5d3e', 'bcc6f8ab-38cd-46b2-bd61-ac3d38546798', 'da74a3f9-79f2-44ee-b962-d031cc3886a1', '2025-03-03 12:05:00'),
('d3c74e9c-4b47-4d2f-bacf-61a57d3f5a9e', '5c1399ce-5d64-4b9e-a93d-1139fceaf86c', '08014313-7b76-48cc-8dd3-dfa9914d6813', '2025-03-03 12:10:00'),
('e4fda75d-5b92-4c83-987a-1b34e4a91b6c', '5c1399ce-5d64-4b9e-a93d-1139fceaf86c', 'b9d4b038-8f59-4502-853c-e53dbca2a015', '2025-03-03 12:15:00'),
('f5e86b9c-3e7a-4094-bf8e-3f7b95f0e5a6', 'f209de1e-7162-4995-a6c7-f8a8a6de0dd4', '67ee4f6a-22d1-4d13-8d0d-ac7e205d9d06', '2025-03-03 12:20:00')
"""

# 汎用的な関数
def execute_sql(query: str):
    """execute_sql を呼び出して任意のSQLを実行"""
    try:
        response = supabase.rpc("execute_sql", {"sql": query}).execute()
        return {"message": "Query executed successfully", "response": response.data}
    except Exception as e:
        return {"error": str(e)}

# 各テーブルの作成API
@router.post("/create-users")
def create_users():
    return execute_sql(CREATE_USERS_SQL)

@router.post("/create-user-attributes")
def create_user_attributes():
    return execute_sql(CREATE_USER_ATTRIBUTES_SQL)

@router.post("/create-likes")
def create_likes():
    return execute_sql(CREATE_LIKES_SQL)

@router.post("/create-matches")
def create_matches():
    return execute_sql(CREATE_MATCHES_SQL)


# 各テーブルの削除API
@router.post("/drop-users")
def drop_users():
    return execute_sql(DROP_USERS_SQL)

@router.post("/drop-user-attributes")
def drop_user_attributes():
    return execute_sql(DROP_USER_ATTRIBUTES_SQL)

@router.post("/drop-likes")
def drop_likes():
    return execute_sql(DROP_LIKES_SQL)

@router.post("/drop-matches")
def drop_matches():
    return execute_sql(DROP_MATCHES_SQL)

# 各テーブルの架空データ挿入API
@router.post("/insert-users")
def insert_users():
    return execute_sql(INSERT_USERS_SQL)

@router.post("/insert-user-attributes")
def insert_user_attributes():
    return execute_sql(INSERT_USER_ATTRIBUTES_SQL)

@router.post("/insert-likes")
def insert_likes():
    return execute_sql(INSERT_LIKES_SQL)