from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter()

# 各テーブルの作成クエリ
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

CREATE_USER_ATTRIBUTES_SQL = """
CREATE TABLE IF NOT EXISTS user_attributes (
    user_id UUID PRIMARY KEY,
    hobbies TEXT NOT NULL,
    hometown VARCHAR(50) NOT NULL,
    field VARCHAR(10) CHECK (field IN ('公共', '法人', '金融', 'TC&S', '技統本')) NOT NULL,
    role VARCHAR(10) CHECK (role IN ('SE', '営業', 'コンサル', 'スタッフ')) NOT NULL,
    preferences VARCHAR(10) CHECK (preferences IN ('hobbies', 'hometown', 'field', 'role')) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

CREATE_MATCHING_HISTORY_SQL = """
CREATE TABLE IF NOT EXISTS matching_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user1_id UUID REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID REFERENCES users(id) ON DELETE CASCADE,
    score FLOAT CHECK (score BETWEEN 0 AND 1),
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_SLACK_CHANNELS_SQL = """
CREATE TABLE IF NOT EXISTS slack_channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user1_id UUID REFERENCES users(id) ON DELETE CASCADE,
    user2_id UUID REFERENCES users(id) ON DELETE CASCADE,
    channel_id VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# 各テーブルの削除クエリ
DROP_USERS_SQL = "DROP TABLE IF EXISTS users CASCADE;"
DROP_USER_ATTRIBUTES_SQL = "DROP TABLE IF EXISTS user_attributes CASCADE;"
DROP_MATCHING_HISTORY_SQL = "DROP TABLE IF EXISTS matching_history CASCADE;"
DROP_SLACK_CHANNELS_SQL = "DROP TABLE IF EXISTS slack_channels CASCADE;"

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
INSERT INTO user_attributes (user_id, hobbies, hometown, field, role, preferences) VALUES
((SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), '読書, 旅行, 映画鑑賞', '東京都', '公共', 'SE', 'hometown'),
((SELECT id FROM users WHERE email = 'sato.hanako@example.com'), '料理, ヨガ, 写真', '大阪府', '法人', '営業', 'field'),
((SELECT id FROM users WHERE email = 'suzuki.ichiro@example.com'), '登山, スポーツ, 音楽', '愛知県', '金融', 'コンサル', 'role'),
((SELECT id FROM users WHERE email = 'takahashi.jiro@example.com'), 'ゲーム, プログラミング, カフェ巡り', '福岡県', 'TC&S', 'SE', 'hobbies'),
((SELECT id FROM users WHERE email = 'yamamoto.saburo@example.com'), '映画, 読書, アウトドア', '北海道', '技統本', 'スタッフ', 'hobbies'),
((SELECT id FROM users WHERE email = 'nakamura.shiro@example.com'), 'ドライブ, 旅行, 温泉巡り', '京都府', '公共', '営業', 'role'),
((SELECT id FROM users WHERE email = 'kobayashi.goko@example.com'), 'ハイキング, スポーツ観戦, 料理', '兵庫県', '法人', 'コンサル', 'hometown'),
((SELECT id FROM users WHERE email = 'kato.rokuta@example.com'), 'DIY, 読書, 筋トレ', '広島県', '金融', 'スタッフ', 'field'),
((SELECT id FROM users WHERE email = 'ito.nanami@example.com'), 'アニメ, ゲーム, 映画', '宮城県', 'TC&S', 'SE', 'hobbies'),
((SELECT id FROM users WHERE email = 'watanabe.hachiro@example.com'), '写真, 旅行, サイクリング', '長野県', '技統本', '営業', 'field'),
((SELECT id FROM users WHERE email = 'matsumoto.kyube@example.com'), 'アウトドア, バイク, 料理', '新潟県', '公共', 'コンサル', 'role'),
((SELECT id FROM users WHERE email = 'hayashi.juichi@example.com'), '映画, 音楽, 読書', '岡山県', '法人', 'スタッフ', 'hometown'),
((SELECT id FROM users WHERE email = 'shimizu.kyoko@example.com'), '釣り, スポーツ, 旅行', '茨城県', '金融', 'SE', 'field'),
((SELECT id FROM users WHERE email = 'yamada.kazuko@example.com'), 'ヨガ, ガーデニング, カフェ巡り', '栃木県', 'TC&S', '営業', 'hobbies'),
((SELECT id FROM users WHERE email = 'fujita.hikaru@example.com'), '筋トレ, 読書, 音楽鑑賞', '群馬県', '技統本', 'コンサル', 'role'),
((SELECT id FROM users WHERE email = 'okamoto.makoto@example.com'), 'ジョギング, 料理, 登山', '静岡県', '公共', 'スタッフ', 'role'),
((SELECT id FROM users WHERE email = 'shimada.sora@example.com'), '映画, ゲーム, プログラミング', '熊本県', '法人', 'SE', 'hometown'),
((SELECT id FROM users WHERE email = 'harada.hitomi@example.com'), '温泉巡り, 旅行, 写真', '山形県', '金融', '営業', 'field'),
((SELECT id FROM users WHERE email = 'miura.ren@example.com'), 'ランニング, ハイキング, 読書', '滋賀県', 'TC&S', 'コンサル', 'hobbies'),
((SELECT id FROM users WHERE email = 'ishii.kaze@example.com'), '音楽, ダンス, 料理', '奈良県', '技統本', 'スタッフ', 'hometown');
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

@router.post("/create-matching-history")
def create_matching_history():
    return execute_sql(CREATE_MATCHING_HISTORY_SQL)

@router.post("/create-slack-channels")
def create_slack_channels():
    return execute_sql(CREATE_SLACK_CHANNELS_SQL)

# 各テーブルの削除API
@router.post("/drop-users")
def drop_users():
    return execute_sql(DROP_USERS_SQL)

@router.post("/drop-user-attributes")
def drop_user_attributes():
    return execute_sql(DROP_USER_ATTRIBUTES_SQL)

@router.post("/drop-matching-history")
def drop_matching_history():
    return execute_sql(DROP_MATCHING_HISTORY_SQL)

@router.post("/drop-slack-channels")
def drop_slack_channels():
    return execute_sql(DROP_SLACK_CHANNELS_SQL)

# 各テーブルの架空データ挿入API
@router.post("/insert-users")
def insert_users():
    return execute_sql(INSERT_USERS_SQL)

@router.post("/insert-user-attributes")
def insert_user_attributes():
    return execute_sql(INSERT_USER_ATTRIBUTES_SQL)