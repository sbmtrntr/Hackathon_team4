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
    cluster INTEGER, -- クラスタリングのための列
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
    self_introductions TEXT NOT NULL, -- 「自己紹介文」の列
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
        reasons TEXT NOT NULL, -- 「いいねの理由」の列
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
('田中 太郎', 'tanaka.taro@example.com', 'U12345671', crypt('securepassword1', gen_salt('bf')), NULL, '2023-05-01'),
('佐藤 花子', 'sato.hanako@example.com', 'U87654321', crypt('securepassword2', gen_salt('bf')), NULL, '2023-05-02'),
('鈴木 一郎', 'suzuki.ichiro@example.com', 'U23456189', crypt('securepassword3', gen_salt('bf')), NULL, '2023-05-03'),
('高橋 次郎', 'takahashi.jiro@example.com', 'U34567890', crypt('securepassword4', gen_salt('bf')), NULL, '2023-05-04'),
('井上 美咲', 'inoue.misaki@example.com', 'U45678901', crypt('securepassword5', gen_salt('bf')), NULL, '2023-05-05'),
('山本 健太', 'yamamoto.kenta@example.com', 'U56789012', crypt('securepassword6', gen_salt('bf')), NULL, '2023-05-06'),
('中村 桃子', 'nakamura.momoko@example.com', 'U67890123', crypt('securepassword7', gen_salt('bf')), NULL, '2023-05-07'),
('小林 太一', 'kobayashi.taichi@example.com', 'U78901234', crypt('securepassword8', gen_salt('bf')), NULL, '2023-05-08'),
('加藤 春菜', 'kato.haruna@example.com', 'U89012345', crypt('securepassword9', gen_salt('bf')), NULL, '2023-05-09'),
('吉田 和夫', 'yoshida.kazu@example.com', 'U90123456', crypt('securepassword10', gen_salt('bf')), NULL, '2023-05-10'),
('山田 涼太', 'yamada.ryota@example.com', 'U01234567', crypt('securepassword11', gen_salt('bf')), NULL, '2023-05-11'),
('佐々木 美咲', 'sasaki.misaki@example.com', 'U12345678', crypt('securepassword12', gen_salt('bf')), NULL, '2023-05-12'),
('森田 拓也', 'morita.takuya@example.com', 'U23456789', crypt('securepassword13', gen_salt('bf')), NULL, '2023-05-13'),
('大島 結衣', 'oshima.yui@example.com', 'U34567891', crypt('securepassword14', gen_salt('bf')), NULL, '2023-05-14'),
('松本 裕樹', 'matsumoto.yuki@example.com', 'U45678902', crypt('securepassword15', gen_salt('bf')), NULL, '2023-05-15'),
('藤田 千夏', 'fujita.chinatsu@example.com', 'U56789023', crypt('securepassword16', gen_salt('bf')), NULL, '2023-05-16'),
('渡辺 大輝', 'watanabe.daiki@example.com', 'U67890134', crypt('securepassword17', gen_salt('bf')), NULL, '2023-05-17'),
('石井 彩花', 'ishii.ayaka@example.com', 'U78901245', crypt('securepassword18', gen_salt('bf')), NULL, '2023-05-18'),
('清水 優太', 'shimizu.yuta@example.com', 'U89012356', crypt('securepassword19', gen_salt('bf')), NULL, '2023-05-19'),
('長谷川 結衣', 'hasegawa.yui@example.com', 'U90123467', crypt('securepassword20', gen_salt('bf')), NULL, '2023-05-20'),
('田村 陽介', 'tamura.yosuke@example.com', 'U01234568', crypt('securepassword21', gen_salt('bf')), NULL, '2023-05-21'),
('松井 恵理', 'matsui.eri@example.com', 'U12345679', crypt('securepassword22', gen_salt('bf')), NULL, '2023-05-22'),
('近藤 真一', 'kondo.shinichi@example.com', 'U23456790', crypt('securepassword23', gen_salt('bf')), NULL, '2023-05-23'),
('橋本 奈々', 'hashimoto.nana@example.com', 'U34567891', crypt('securepassword24', gen_salt('bf')), NULL, '2023-05-24'),
('小川 亮太', 'ogawa.ryota@example.com', 'U45678902', crypt('securepassword25', gen_salt('bf')), NULL, '2023-05-25'),
('遠藤 美月', 'endo.mizuki@example.com', 'U56789023', crypt('securepassword26', gen_salt('bf')), NULL, '2023-05-26'),
('三浦 大翔', 'miura.daito@example.com', 'U67890134', crypt('securepassword27', gen_salt('bf')), NULL, '2023-05-27'),
('永田 結菜', 'nagata.yuna@example.com', 'U78901245', crypt('securepassword28', gen_salt('bf')), NULL, '2023-05-28'),
('石川 一真', 'ishikawa.kazuma@example.com', 'U89012356', crypt('securepassword29', gen_salt('bf')), NULL, '2023-05-29'),
('岡田 知恵', 'okada.chie@example.com', 'U90123467', crypt('securepassword30', gen_salt('bf')), NULL, '2023-05-30'),
('坂井 大志', 'sakai.taishi@example.com', 'U01234571', crypt('securepassword31', gen_salt('bf')), NULL, '2023-06-10'),
('平田 真紀', 'hirata.maki@example.com', 'U12345682', crypt('securepassword32', gen_salt('bf')), NULL, '2023-06-11'),
('中田 健太', 'nakata.kenta@example.com', 'U23456793', crypt('securepassword33', gen_salt('bf')), NULL, '2023-06-12'),
('加藤 美月', 'kato.mizuki@example.com', 'U34567894', crypt('securepassword34', gen_salt('bf')), NULL, '2023-06-13'),
('佐々木 明日香', 'sasaki.asuka@example.com', 'U45678904', crypt('securepassword35', gen_salt('bf')), NULL, '2023-06-14'),
('中村 翼', 'nakamura.tsubasa@example.com', 'U56789035', crypt('securepassword36', gen_salt('bf')), NULL, '2023-06-15'),
('藤田 翼', 'fujita.tsubasa@example.com', 'U67890156', crypt('securepassword37', gen_salt('bf')), NULL, '2023-06-16'),
('坂本 愛', 'sakamoto.ai@example.com', 'U78901267', crypt('securepassword38', gen_salt('bf')), NULL, '2023-06-17'),
('原田 大輝', 'harada.daiki@example.com', 'U89012378', crypt('securepassword39', gen_salt('bf')), NULL, '2023-06-18'),
('吉岡 千晶', 'yoshioka.chiaki@example.com', 'U90123489', crypt('securepassword40', gen_salt('bf')), NULL, '2023-06-19'),
('林 大地', 'hayashi.daichi@example.com', 'U01234570', crypt('securepassword41', gen_salt('bf')), NULL, '2023-06-20'),
('小川 茉莉', 'ogawa.mari@example.com', 'U12345681', crypt('securepassword42', gen_salt('bf')), NULL, '2023-06-21'),
('木村 崇', 'kimura.takashi@example.com', 'U23456792', crypt('securepassword43', gen_salt('bf')), NULL, '2023-06-22'),
('加藤 美月', 'kato.mizuki@example.com', 'U34567893', crypt('securepassword44', gen_salt('bf')), NULL, '2023-06-23'),
('佐々木 明日香', 'sasaki.asuka@example.com', 'U45678904', crypt('securepassword45', gen_salt('bf')), NULL, '2023-06-24'),
('中村 翼', 'nakamura.tsubasa@example.com', 'U56789035', crypt('securepassword46', gen_salt('bf')), NULL, '2023-06-25'),
('藤田 翼', 'fujita.tsubasa@example.com', 'U67890156', crypt('securepassword47', gen_salt('bf')), NULL, '2023-06-26'),
('坂本 愛', 'sakamoto.ai@example.com', 'U78901267', crypt('securepassword48', gen_salt('bf')), NULL, '2023-06-27'),
('原田 大輝', 'harada.daiki@example.com', 'U89012378', crypt('securepassword49', gen_salt('bf')), NULL, '2023-06-28'),
('吉岡 千晶', 'yoshioka.chiaki@example.com', 'U90123489', crypt('securepassword50', gen_salt('bf')), NULL, '2023-06-29'),
('坂井 大志', 'sakai.taishi@example.com', 'U01234571', crypt('securepassword51', gen_salt('bf')), NULL, '2023-06-20'),
('平田 真紀', 'hirata.maki@example.com', 'U12345682', crypt('securepassword52', gen_salt('bf')), NULL, '2023-06-21'),
('中田 健太', 'nakata.kenta@example.com', 'U23456793', crypt('securepassword53', gen_salt('bf')), NULL, '2023-06-22'),
('加藤 美月', 'kato.mizuki@example.com', 'U34567893', crypt('securepassword54', gen_salt('bf')), NULL, '2023-06-23'),
('佐々木 明日香', 'sasaki.asuka@example.com', 'U45678904', crypt('securepassword55', gen_salt('bf')), NULL, '2023-06-24'),
('中村 翼', 'nakamura.tsubasa@example.com', 'U56789035', crypt('securepassword56', gen_salt('bf')), NULL, '2023-06-25'),
('藤田 翼', 'fujita.tsubasa@example.com', 'U67890156', crypt('securepassword57', gen_salt('bf')), NULL, '2023-06-26'),
('坂本 愛', 'sakamoto.ai@example.com', 'U78901267', crypt('securepassword58', gen_salt('bf')), NULL, '2023-06-27'),
('原田 大輝', 'harada.daiki@example.com', 'U89012378', crypt('securepassword59', gen_salt('bf')), NULL, '2023-06-28'),
('吉岡 千晶', 'yoshioka.chiaki@example.com', 'U90123489', crypt('securepassword60', gen_salt('bf')), NULL, '2023-06-29'),
('長井 健太', 'nagai.kenta@example.com', 'U01234572', crypt('securepassword61', gen_salt('bf')), NULL, '2023-06-30'),
('松下 愛', 'matsushita.ai@example.com', 'U12345683', crypt('securepassword62', gen_salt('bf')), NULL, '2023-07-01'),
('岡本 里奈', 'okamoto.rina@example.com', 'U23456794', crypt('securepassword63', gen_salt('bf')), NULL, '2023-07-02'),
('堀江 翼', 'horie.tsubasa@example.com', 'U34567895', crypt('securepassword64', gen_salt('bf')), NULL, '2023-07-03'),
('小泉 一成', 'koizumi.issei@example.com', 'U45678906', crypt('securepassword65', gen_salt('bf')), NULL, '2023-07-04'),
('木下 雅人', 'kinoshita.masato@example.com', 'U56789047', crypt('securepassword66', gen_salt('bf')), NULL, '2023-07-05'),
('佐野 美香', 'sano.mika@example.com', 'U67890178', crypt('securepassword67', gen_salt('bf')), NULL, '2023-07-06'),
('渡辺 寛之', 'watanabe.hiroyuki@example.com', 'U78901289', crypt('securepassword68', gen_salt('bf')), NULL, '2023-07-07'),
('石井 未来', 'ishii.mirai@example.com', 'U89012390', crypt('securepassword69', gen_salt('bf')), NULL, '2023-07-08'),
('前川 恵美', 'maekawa.emi@example.com', 'U90123491', crypt('securepassword70', gen_salt('bf')), NULL, '2023-07-09'),
('山田 海斗', 'yamada.kaito@example.com', 'U01234573', crypt('securepassword71', gen_salt('bf')), NULL, '2023-07-10'),
('石田 一輝', 'ishida.kazuki@example.com', 'U12345684', crypt('securepassword72', gen_salt('bf')), NULL, '2023-07-11'),
('岡村 智也', 'okamura.tomoya@example.com', 'U23456795', crypt('securepassword73', gen_salt('bf')), NULL, '2023-07-12'),
('林 沙耶', 'hayashi.saya@example.com', 'U34567896', crypt('securepassword74', gen_salt('bf')), NULL, '2023-07-13'),
('田村 龍之介', 'tamura.ryunosuke@example.com', 'U45678907', crypt('securepassword75', gen_salt('bf')), NULL, '2023-07-14'),
('森本 理沙', 'morimoto.risa@example.com', 'U56789048', crypt('securepassword76', gen_salt('bf')), NULL, '2023-07-15'),
('山本 菜々子', 'yamamoto.nanako@example.com', 'U67890179', crypt('securepassword77', gen_salt('bf')), NULL, '2023-07-16'),
('井上 慶太', 'inoue.keita@example.com', 'U78901290', crypt('securepassword78', gen_salt('bf')), NULL, '2023-07-17'),
('佐藤 萌', 'sato.moe@example.com', 'U89012391', crypt('securepassword79', gen_salt('bf')), NULL, '2023-07-18'),
('加藤 瑠璃', 'kato.ruri@example.com', 'U90123492', crypt('securepassword80', gen_salt('bf')), NULL, '2023-07-19'),
('高橋 光', 'takahashi.hikaru@example.com', 'U01234574', crypt('securepassword81', gen_salt('bf')), NULL, '2023-07-20'),
('佐藤 歩', 'sato.ayumu@example.com', 'U12345685', crypt('securepassword82', gen_salt('bf')), NULL, '2023-07-21'),
('鈴木 風花', 'suzuki.fuka@example.com', 'U23456796', crypt('securepassword83', gen_salt('bf')), NULL, '2023-07-22'),
('吉田 仁美', 'yoshida.hitomi@example.com', 'U34567897', crypt('securepassword84', gen_salt('bf')), NULL, '2023-07-23'),
('野村 美優', 'nomura.miyu@example.com', 'U45678908', crypt('securepassword85', gen_salt('bf')), NULL, '2023-07-24'),
('伊藤 竜也', 'ito.tatsuya@example.com', 'U56789049', crypt('securepassword86', gen_salt('bf')), NULL, '2023-07-25'),
('田村 あすか', 'tamura.asuka@example.com', 'U67890180', crypt('securepassword87', gen_salt('bf')), NULL, '2023-07-26'),
('中田 恵理', 'nakata.eri@example.com', 'U78901291', crypt('securepassword88', gen_salt('bf')), NULL, '2023-07-27'),
('岩田 幸雄', 'iwata.yukio@example.com', 'U89012392', crypt('securepassword89', gen_salt('bf')), NULL, '2023-07-28'),
('佐々木 希', 'sasaki.nozomi@example.com', 'U90123493', crypt('securepassword90', gen_salt('bf')), NULL, '2023-07-29'),
('橋本 涼', 'hashimoto.ryo@example.com', 'U01234575', crypt('securepassword91', gen_salt('bf')), NULL, '2023-07-30'),
('宮本 結菜', 'miyamoto.yuna@example.com', 'U12345686', crypt('securepassword92', gen_salt('bf')), NULL, '2023-07-31'),
('斉藤 陽子', 'saito.yoko@example.com', 'U23456797', crypt('securepassword93', gen_salt('bf')), NULL, '2023-08-01'),
('加藤 優', 'kato.yu@example.com', 'U34567898', crypt('securepassword94', gen_salt('bf')), NULL, '2023-08-02'),
('伊藤 亮', 'ito.ryo@example.com', 'U45678909', crypt('securepassword95', gen_salt('bf')), NULL, '2023-08-03'),
('北村 真由', 'kitamura.mayu@example.com', 'U56789050', crypt('securepassword96', gen_salt('bf')), NULL, '2023-08-04'),
('田中 理恵', 'tanaka.rie@example.com', 'U67890181', crypt('securepassword97', gen_salt('bf')), NULL, '2023-08-05'),
('柳田 優希', 'yanagida.yuki@example.com', 'U78901292', crypt('securepassword98', gen_salt('bf')), NULL, '2023-08-06'),
('山崎 翔太', 'yamazaki.shota@example.com', 'U89012393', crypt('securepassword99', gen_salt('bf')), NULL, '2023-08-07'),
('中村 優太', 'nakamura.yuta@example.com', 'U90123494', crypt('securepassword100', gen_salt('bf')), NULL, '2023-08-08');
"""

INSERT_USER_ATTRIBUTES_SQL = """
INSERT INTO user_attributes (user_id, hobbies, hometown, field, role, mbti, alma_mater, preferences, self_introductions) VALUES
((SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), '読書, 旅行, 映画鑑賞', '東京都', '公共', 'SE', 'INTJ', '東京大学', 'hobbies', 'こんにちは。読書と映画鑑賞が大好きで、静かな時間を大切にしています。穏やかな会話ができる友人を探しています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'sato.hanako@example.com'), '料理, ボードゲーム, カメラ', '大阪府', '法人', '営業', 'ENTP', '京都大学', 'hometown', '初めまして！料理やボードゲームが好きで、週末はよくボドゲカフェに行きます。写真撮影も趣味ですので、一緒に楽しんでくれる関西の方を募集しています！'),
((SELECT id FROM users WHERE email = 'suzuki.ichiro@example.com'), 'ゲーム, 釣り, 音楽', '愛知県', '金融', 'コンサル', 'ENFP', '名古屋大学', 'field', 'こんにちは！ゲームや釣りが大好きで、アウトドア派です。音楽もよく聴くので、音楽の話ができる友達を作りたいと思っています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'takahashi.jiro@example.com'), 'サッカー, バスケットボール, ダンス', '北海道', 'TC&S', 'スタッフ', 'INTP', '北海道大学', 'role', '初めまして。サッカーやバスケットボールなどのスポーツが大好きで、ダンスも楽しんでいます。友達と活動的な時間を過ごしたいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'inoue.misaki@example.com'), '旅行, カフェ, プログラミング', '神奈川県', '法人', 'SE', 'ISFJ', '早稲田大学', 'field', 'こんにちは！旅行とカフェ巡りが好きで、プログラミングも得意です。穏やかな会話ができる友達を探しています。気軽に声をかけてくださいね！'),
((SELECT id FROM users WHERE email = 'yamamoto.kenta@example.com'), '映画鑑賞, ランニング, アニメ', '福岡県', '技統本', '営業', 'ENFJ', '九州大学', 'role', '初めまして！映画鑑賞とランニングが趣味です。最近はアニメにもハマっています。アクティブに過ごすことが好きな友達と仲良くなりたいです！'),
((SELECT id FROM users WHERE email = 'nakamura.momoko@example.com'), '登山, 温泉, DIY', '京都府', '金融', 'スタッフ', 'ISFP', '大阪大学', 'field', 'こんにちは！登山や温泉巡りが大好きで、DIYにも挑戦しています。自然を愛する友達と一緒に新しいことを始めたいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'kobayashi.taichi@example.com'), '音楽, 筋トレ, 読書', '東京都', '公共', 'SE', 'ISTJ', '東京工業大学', 'hobbies', 'こんにちは！音楽を聴きながら筋トレするのが日課で、読書も好きです。静かな時間を大切にしつつも、積極的に新しい人と出会いたいと思っています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'kato.haruna@example.com'), 'カメラ, 旅行, スポーツ観戦', '埼玉県', '法人', 'コンサル', 'INFJ', '早稲田大学', 'role', '初めまして！カメラを持って旅行をするのが好きで、スポーツ観戦もよく行きます。新しい経験を一緒に楽しんでくれる友達を探しています！'),
((SELECT id FROM users WHERE email = 'yoshida.kazu@example.com'), 'ボードゲーム, サッカー, 釣り', '大阪府', 'TC&S', 'スタッフ', 'ESTP', '大阪大学', 'hometown', 'こんにちは！ボードゲームやサッカーが好きで、釣りにもよく行きます。気軽に遊べる友達と一緒に過ごしたいと思っています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'yamada.ryota@example.com'), '音楽, 筋トレ, ランニング', '東京都', '公共', '営業', 'ISTP', '東京大学', 'role', 'こんにちは！音楽を聴きながら筋トレするのが日課で、ランニングも楽しんでいます。新しいことに挑戦できる友達を探しています。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'sasaki.misaki@example.com'), 'カフェ, 旅行, ボードゲーム', '北海道', '法人', 'スタッフ', 'ISFJ', '東北大学', 'field', '初めまして！カフェ巡りと旅行が好きで、週末はよくボードゲームを楽しみます。穏やかで落ち着いた友達ができたら嬉しいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'morita.takuya@example.com'), '映画鑑賞, ダンス, 旅行', '福岡県', '金融', 'SE', 'ENFJ', '九州大学', 'hobbies', '映画鑑賞とダンスが趣味で、旅行も好きです。新しい経験を一緒に楽しめる友達を探しています！気軽に声をかけてください。'),
((SELECT id FROM users WHERE email = 'oshima.yui@example.com'), '読書, キャンプ, サッカー', '兵庫県', 'TC&S', 'コンサル', 'INTJ', '神戸大学', 'role', 'こんにちは！読書やキャンプ、サッカーが大好きで、友達と一緒に楽しい時間を過ごすことが楽しみです。仲良くしていただけると嬉しいです！'),
((SELECT id FROM users WHERE email = 'matsumoto.yuki@example.com'), 'プログラミング, ゲーム, 読書', '東京都', '法人', 'SE', 'ENFP', '早稲田大学', 'hobbies', 'こんにちは！プログラミングやゲームを楽しんでいます。読書も好きで、静かな時間を大切にしています。気軽にお話しできる友達を探しています！'),
((SELECT id FROM users WHERE email = 'fujita.chinatsu@example.com'), 'カメラ, 料理, アニメ', '大阪府', '技統本', 'スタッフ', 'INTP', '大阪大学', 'field', '初めまして！カメラを持って新しい場所を訪れるのが好きです。アニメも好きで、一緒に楽しんでくれる方と仲良くなりたいです！'),
((SELECT id FROM users WHERE email = 'watanabe.daiki@example.com'), '映画鑑賞, 登山, アニメ', '神奈川県', '金融', '営業', 'ISTJ', '慶應義塾大学', 'hobbies', 'こんにちは！映画やアニメを見ながらリラックスするのが好きです。登山もよく行きますので、アウトドア活動に興味のある方と仲良くなりたいです！'),
((SELECT id FROM users WHERE email = 'ishii.ayaka@example.com'), 'スポーツ観戦, 料理, 旅行', '埼玉県', '公共', 'コンサル', 'INFJ', '早稲田大学', 'field', '初めまして！スポーツ観戦と旅行が大好きです。料理も得意なので、一緒に料理したり、楽しい時間を過ごせる友達を探しています！'),
((SELECT id FROM users WHERE email = 'shimizu.yuta@example.com'), 'ランニング, 音楽, ゲーム', '千葉県', '法人', 'SE', 'ENFP', '東京工業大学', 'role', 'こんにちは！ランニングと音楽を楽しんでいます。ゲームも好きで、一緒に過ごせる友達を探しています。気軽にお話しできる方がいれば嬉しいです！'),
((SELECT id FROM users WHERE email = 'hasegawa.yui@example.com'), 'ダンス, プログラミング, カフェ', '愛知県', '技統本', 'スタッフ', 'ENTP', '名古屋大学', 'hobbies', '初めまして！ダンスとプログラミングが好きで、カフェ巡りも楽しんでいます。新しいことに挑戦できる友達を探しています！よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'tamura.yosuke@example.com'), 'ボードゲーム, プログラミング, 読書', '東京都', '金融', '営業', 'ISTP', '東京大学', 'role', 'こんにちは！ボードゲームやプログラミングが好きで、読書も大切にしています。静かな時間を楽しみたい方と友達になりたいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'matsui.eri@example.com'), '映画鑑賞, サッカー, 旅行', '大阪府', '公共', 'スタッフ', 'INTJ', '京都大学', 'hobbies', '映画鑑賞やサッカーを楽しんでいます。旅行にもよく行くので、一緒に色々な場所を訪れる友達を探しています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'kondo.shinichi@example.com'), 'カフェ, 料理, ランニング', '神奈川県', 'TC&S', 'SE', 'ENFP', '慶應義塾大学', 'field', 'こんにちは！カフェ巡りと料理が趣味で、ランニングも好きです。アクティブで楽しい時間を過ごせる友達を探しています。気軽にお声かけください！'),
((SELECT id FROM users WHERE email = 'hashimoto.nana@example.com'), '読書, キャンプ, サッカー', '兵庫県', '金融', '営業', 'INFJ', '神戸大学', 'hobbies', '読書やキャンプが大好きで、サッカーもよく観戦します。新しい友達と静かな時間を過ごすことが楽しみです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'ogawa.ryota@example.com'), 'ダンス, 登山, スポーツ観戦', '埼玉県', '法人', '営業', 'ENFJ', '早稲田大学', 'role', 'こんにちは！ダンスや登山が好きで、スポーツ観戦もよくします。アウトドア活動や楽しい会話を楽しめる友達を探しています！'),
((SELECT id FROM users WHERE email = 'endo.mizuki@example.com'), 'カメラ, 料理, アニメ', '大阪府', '技統本', 'スタッフ', 'INTP', '大阪大学', 'field', 'こんにちは！カメラを持って新しい場所を訪れるのが好きです。アニメや料理も好きなので、共通の趣味を持つ方と仲良くなりたいです！'),
((SELECT id FROM users WHERE email = 'miura.daito@example.com'), 'ランニング, 筋トレ, ボードゲーム', '大阪府', '法人', '営業', 'ISTJ', '名古屋大学', 'field', 'ランニングと筋トレが日課です。ボードゲームも楽しんでいるので、一緒に活動的な時間を過ごせる友達を探しています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'nagata.yuna@example.com'), 'カメラ, 音楽, 旅行', '神奈川県', '技統本', 'スタッフ', 'ISFP', '名古屋大学', 'role', 'こんにちは！カメラを持って旅行するのが大好きです。音楽にも興味があるので、一緒に楽しめる友達を探しています。気軽にお声かけください！'),
((SELECT id FROM users WHERE email = 'ishikawa.kazuma@example.com'), 'プログラミング, ボードゲーム, 旅行', '千葉県', '金融', 'スタッフ', 'ENTP', '東京大学', 'hobbies', 'プログラミングが得意で、ボードゲームや旅行も楽しんでいます。新しいことに挑戦できる友達を探しています。気軽に話しかけてください！'),
((SELECT id FROM users WHERE email = 'okada.chie@example.com'), '料理, サッカー, 旅行', '大阪府', '法人', 'SE', 'ESTJ', '早稲田大学', 'field', 'こんにちは！料理とサッカーが好きで、旅行にもよく行きます。一緒に色々な経験を楽しんでくれる友達を探しています！よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'sakai.taishi@example.com'), 'ゲーム, 旅行, 読書', '愛知県', '法人', 'スタッフ', 'INTP', '名古屋大学', 'role', 'こんにちは！ゲームが大好きで、旅行もよく行きます。読書も好きで、静かな時間を過ごせる友達を探しています。気軽にお声かけください！'),
((SELECT id FROM users WHERE email = 'hirata.maki@example.com'), 'ダンス, プログラミング, ボードゲーム', '福岡県', '技統本', '営業', 'INFJ', '九州大学', 'hobbies', 'ダンスとプログラミングが得意で、ボードゲームも楽しんでいます。新しい友達と一緒に活動的な時間を過ごしたいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'nakata.kenta@example.com'), '音楽, 映画鑑賞, サッカー', '東京都', '公共', 'コンサル', 'ENFJ', '東京大学', 'field', '音楽と映画鑑賞が趣味で、サッカーも好きです。友達と楽しい時間を過ごしながら、新しい経験を一緒に楽しめる方を探しています！'),
((SELECT id FROM users WHERE email = 'kato.mizuki@example.com'), 'ランニング, 筋トレ, 登山', '愛知県', '金融', 'スタッフ', 'INTJ', '名古屋大学', 'role', 'ランニングや筋トレ、登山が好きで、アクティブな友達と一緒に活動的な時間を過ごしたいです。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'sasaki.asuka@example.com'), 'カメラ, 旅行, サッカー', '東京都', '法人', '営業', 'ESTJ', '早稲田大学', 'field', 'カメラで新しい場所を撮影するのが好きで、旅行にもよく行きます。サッカーも観戦しますので、共通の趣味を持つ友達を探しています！'),
((SELECT id FROM users WHERE email = 'nakamura.tsubasa@example.com'), 'ゲーム, 音楽, 料理', '埼玉県', '金融', 'コンサル', 'ENFP', '慶應義塾大学', 'hobbies', 'ゲームと音楽が大好きで、料理も得意です。一緒に新しいことに挑戦できる友達を探しています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'fujita.tsubasa@example.com'), '旅行, アニメ, 音楽', '東京都', '法人', 'スタッフ', 'ISFP', '大阪大学', 'role', '旅行やアニメ、音楽が好きで、リラックスできる友達と過ごしたいです。共通の趣味を持っている方と仲良くなりたいです！'),
((SELECT id FROM users WHERE email = 'sakamoto.ai@example.com'), 'スポーツ観戦, プログラミング, ダンス', '京都府', '金融', '営業', 'ISTJ', '早稲田大学', 'field', 'スポーツ観戦やプログラミングが趣味で、ダンスも楽しんでいます。友達と一緒に楽しい時間を過ごしたいです！'),
((SELECT id FROM users WHERE email = 'harada.daiki@example.com'), '音楽, 旅行, 読書', '大阪府', '法人', '営業', 'ENFJ', '慶應義塾大学', 'hobbies', '音楽と旅行が大好きで、読書もよくします。穏やかな会話を楽しみながら、新しい友達を作りたいと思っています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'yoshioka.chiaki@example.com'), 'ダンス, 旅行, サッカー', '愛知県', '技統本', 'SE', 'INTP', '早稲田大学', 'hobbies', 'ダンスやサッカーが好きで、旅行にもよく行きます。新しい友達と一緒に楽しい時間を過ごしたいです。気軽にお話しできる方がいれば嬉しいです！'),
((SELECT id FROM users WHERE email = 'hayashi.daichi@example.com'), 'ゲーム, 旅行, 読書', '愛知県', '法人', 'スタッフ', 'INTP', '名古屋大学', 'role', 'こんにちは！ゲームが大好きで、旅行もよく行きます。読書も好きで、静かな時間を過ごせる友達を探しています。気軽にお声かけください！'),
((SELECT id FROM users WHERE email = 'ogawa.mari@example.com'), 'ダンス, プログラミング, ボードゲーム', '福岡県', '技統本', '営業', 'INFJ', '九州大学', 'hobbies', 'ダンスとプログラミングが得意で、ボードゲームも楽しんでいます。新しい友達と一緒に活動的な時間を過ごしたいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'kimura.takashi@example.com'), 'カフェ, 料理, ランニング', '神奈川県', 'TC&S', 'SE', 'ENFP', '慶應義塾大学', 'field', 'こんにちは！カフェ巡りと料理が趣味で、ランニングも好きです。アクティブで楽しい時間を過ごせる友達を探しています。気軽にお声かけください！'),
((SELECT id FROM users WHERE email = 'kato.mizuki@example.com'), '音楽, 映画鑑賞, サッカー', '東京都', '法人', '営業', 'INFJ', '名古屋大学', 'role', '音楽と映画鑑賞が趣味で、サッカーも好きです。友達と楽しい時間を過ごしながら、新しい経験を一緒に楽しめる方を探しています！'),
((SELECT id FROM users WHERE email = 'sasaki.asuka@example.com'), 'カメラ, 旅行, サッカー', '東京都', '法人', '営業', 'ESTJ', '早稲田大学', 'field', 'カメラで新しい場所を撮影するのが好きで、旅行にもよく行きます。サッカーも観戦しますので、共通の趣味を持つ友達を探しています！'),
((SELECT id FROM users WHERE email = 'nakamura.tsubasa@example.com'), 'ランニング, 筋トレ, 登山', '愛知県', '金融', 'スタッフ', 'INTJ', '名古屋大学', 'role', 'ランニングや筋トレ、登山が好きで、アクティブな友達と一緒に活動的な時間を過ごしたいです。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'fujita.tsubasa@example.com'), 'カメラ, 音楽, 旅行', '埼玉県', '金融', 'コンサル', 'ISFP', '慶應義塾大学', 'field', 'カメラを持って新しい場所を訪れるのが好きです。音楽にも興味があり、旅行も好きなので、共通の趣味を持つ友達を探しています！'),
((SELECT id FROM users WHERE email = 'sakamoto.ai@example.com'), 'スポーツ観戦, プログラミング, ダンス', '京都府', '金融', '営業', 'ISTJ', '早稲田大学', 'hobbies', 'スポーツ観戦やプログラミングが趣味で、ダンスも楽しんでいます。友達と一緒に楽しい時間を過ごしたいです！'),
((SELECT id FROM users WHERE email = 'harada.daiki@example.com'), '音楽, 旅行, 読書', '大阪府', '法人', '営業', 'ENFJ', '慶應義塾大学', 'field', '音楽と旅行が大好きで、読書もよくします。穏やかな会話を楽しみながら、新しい友達を作りたいと思っています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'yoshioka.chiaki@example.com'), 'ダンス, 旅行, サッカー', '愛知県', '技統本', 'SE', 'INTP', '早稲田大学', 'hobbies', 'ダンスやサッカーが好きで、旅行にもよく行きます。新しい友達と一緒に楽しい時間を過ごしたいです。気軽にお話しできる方がいれば嬉しいです！'),
((SELECT id FROM users WHERE email = 'sakai.taishi@example.com'), 'ゲーム, 旅行, 読書', '愛知県', '法人', 'スタッフ', 'INTP', '名古屋大学', 'role', 'こんにちは！ゲームが大好きで、旅行もよく行きます。読書も好きで、静かな時間を過ごせる友達を探しています。気軽にお声かけください！'),
((SELECT id FROM users WHERE email = 'hirata.maki@example.com'), 'ダンス, プログラミング, ボードゲーム', '福岡県', '技統本', '営業', 'INFJ', '九州大学', 'hobbies', 'ダンスとプログラミングが得意で、ボードゲームも楽しんでいます。新しい友達と一緒に活動的な時間を過ごしたいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'nakata.kenta@example.com'), '音楽, 映画鑑賞, サッカー', '東京都', '公共', 'コンサル', 'ENFJ', '東京大学', 'field', '音楽と映画鑑賞が趣味で、サッカーも好きです。友達と楽しい時間を過ごしながら、新しい経験を一緒に楽しめる方を探しています！'),
((SELECT id FROM users WHERE email = 'kato.mizuki@example.com'), 'ランニング, 筋トレ, 登山', '愛知県', '金融', 'スタッフ', 'INTJ', '名古屋大学', 'role', 'ランニングや筋トレ、登山が好きで、アクティブな友達と一緒に活動的な時間を過ごしたいです。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'sasaki.asuka@example.com'), 'カメラ, 旅行, サッカー', '東京都', '法人', '営業', 'ESTJ', '早稲田大学', 'field', 'カメラで新しい場所を撮影するのが好きで、旅行にもよく行きます。サッカーも観戦しますので、共通の趣味を持つ友達を探しています！'),
((SELECT id FROM users WHERE email = 'nakamura.tsubasa@example.com'), 'ランニング, 筋トレ, 登山', '愛知県', '金融', 'スタッフ', 'INTJ', '名古屋大学', 'role', 'ランニングや筋トレ、登山が好きで、アクティブな友達と一緒に活動的な時間を過ごしたいです。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'fujita.tsubasa@example.com'), 'カメラ, 音楽, 旅行', '埼玉県', '金融', 'コンサル', 'ISFP', '慶應義塾大学', 'field', 'カメラを持って新しい場所を訪れるのが好きです。音楽にも興味があり、旅行も好きなので、共通の趣味を持つ友達を探しています！'),
((SELECT id FROM users WHERE email = 'sakamoto.ai@example.com'), 'スポーツ観戦, プログラミング, ダンス', '京都府', '金融', '営業', 'ISTJ', '早稲田大学', 'hobbies', 'スポーツ観戦やプログラミングが趣味で、ダンスも楽しんでいます。友達と一緒に楽しい時間を過ごしたいです！'),
((SELECT id FROM users WHERE email = 'harada.daiki@example.com'), '音楽, 旅行, 読書', '大阪府', '法人', '営業', 'ENFJ', '慶應義塾大学', 'field', '音楽と旅行が大好きで、読書もよくします。穏やかな会話を楽しみながら、新しい友達を作りたいと思っています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'yoshioka.chiaki@example.com'), 'ダンス, 旅行, サッカー', '愛知県', '技統本', 'SE', 'INTP', '早稲田大学', 'hobbies', 'ダンスやサッカーが好きで、旅行にもよく行きます。新しい友達と一緒に楽しい時間を過ごしたいです。気軽にお話しできる方がいれば嬉しいです！'),
((SELECT id FROM users WHERE email = 'nagai.kenta@example.com'), 'ダンス, サッカー, 釣り', '北海道', '公共', '営業', 'ISFP', '北海道大学', 'role', 'こんにちは！ダンスやサッカーが好きで、釣りも楽しんでいます。アクティブな時間を過ごせる友達を探しています。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'matsushita.ai@example.com'), '音楽, キャンプ, ボードゲーム', '大阪府', '法人', 'SE', 'INFJ', '大阪大学', 'hobbies', '音楽を聴きながらキャンプやボードゲームを楽しむのが好きです。共通の趣味を持つ友達と一緒に過ごしたいと思っています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'okamoto.rina@example.com'), 'プログラミング, 旅行, 映画鑑賞', '東京都', '技統本', 'スタッフ', 'INTP', '東京工業大学', 'field', 'プログラミングが得意で、旅行と映画鑑賞も楽しんでいます。新しい経験を一緒に楽しめる友達を探しています！'),
((SELECT id FROM users WHERE email = 'horie.tsubasa@example.com'), 'ランニング, 筋トレ, 料理', '愛知県', '法人', '営業', 'ENFJ', '名古屋大学', 'hobbies', 'ランニングと筋トレが好きで、料理も得意です。友達と楽しい時間を過ごしながら、新しいことに挑戦したいです！'),
((SELECT id FROM users WHERE email = 'koizumi.issei@example.com'), '音楽, ボードゲーム, 読書', '福岡県', '金融', 'スタッフ', 'ISTJ', '九州大学', 'field', '音楽を聴きながらボードゲームや読書を楽しむのが好きです。穏やかな時間を大切にできる友達を探しています。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'kinoshita.masato@example.com'), '映画鑑賞, ダンス, キャンプ', '埼玉県', '法人', '営業', 'ESTP', '慶應義塾大学', 'hobbies', '映画鑑賞やダンスが好きで、キャンプにもよく行きます。アクティブで楽しい時間を過ごせる友達を探しています！'),
((SELECT id FROM users WHERE email = 'sano.mika@example.com'), 'サッカー, ボードゲーム, 旅行', '神奈川県', '公共', 'SE', 'ENFP', '慶應義塾大学', 'field', 'サッカーやボードゲームが好きで、旅行にもよく行きます。共通の趣味を持つ友達と一緒に過ごしたいです。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'watanabe.hiroyuki@example.com'), 'ダンス, 映画鑑賞, 旅行', '京都府', '技統本', 'コンサル', 'ISTJ', '京都大学', 'hobbies', 'ダンスや映画鑑賞が好きで、旅行にもよく行きます。新しい友達と楽しい時間を過ごすことが楽しみです！'),
((SELECT id FROM users WHERE email = 'ishii.mirai@example.com'), '音楽, 読書, 釣り', '大阪府', '金融', 'スタッフ', 'INFJ', '大阪大学', 'role', '音楽を聴きながら読書や釣りを楽しんでいます。穏やかな会話ができる友達を探しています。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'maekawa.emi@example.com'), '旅行, ボードゲーム, サッカー', '東京都', '法人', '営業', 'ENFP', '早稲田大学', 'hobbies', '旅行とボードゲームが好きで、サッカー観戦も楽しんでいます。共通の趣味を持つ友達と一緒に過ごす時間を楽しみにしています！'),
((SELECT id FROM users WHERE email = 'yamada.kaito@example.com'), '音楽, ゲーム, プログラミング', '東京都', '法人', 'SE', 'ENTP', '東京大学', 'hobbies', 'ゲームや音楽が大好きです。プログラミングも得意で、新しい技術に挑戦することが好きです。一緒に楽しめる友達を探しています！'),
((SELECT id FROM users WHERE email = 'ishida.kazuki@example.com'), '読書, 筋トレ, 旅行', '福岡県', '技統本', 'スタッフ', 'ISFJ', '慶應義塾大学', 'hobbies', '読書と筋トレが趣味で、旅行にもよく行きます。静かな時間を楽しむのが好きで、穏やかな友達を探しています！'),
((SELECT id FROM users WHERE email = 'okamura.tomoya@example.com'), '映画鑑賞, カフェ, 旅行', '東京都', '法人', '営業', 'INFJ', '早稲田大学', 'role', '映画鑑賞とカフェ巡りが大好きです。旅行にもよく行くので、一緒にいろんな場所を訪れたい友達を探しています！'),
((SELECT id FROM users WHERE email = 'hayashi.saya@example.com'), 'ランニング, 旅行, 釣り', '大阪府', '金融', '営業', 'INTJ', '名古屋大学', 'hobbies', 'ランニングと旅行が好きで、釣りにもよく行きます。新しい体験を共有できる友達と仲良くなりたいです！'),
((SELECT id FROM users WHERE email = 'tamura.ryunosuke@example.com'), 'ボードゲーム, 音楽, 旅行', '神奈川県', '法人', 'コンサル', 'ENFJ', '名古屋大学', 'field', 'ボードゲームや音楽が好きで、旅行にもよく行きます。友達と一緒に新しい経験を楽しみたいです！'),
((SELECT id FROM users WHERE email = 'morimoto.risa@example.com'), 'ダンス, 料理, アニメ', '大阪府', '技統本', 'スタッフ', 'ENFP', '早稲田大学', 'hobbies', 'ダンスや料理が得意で、アニメも大好きです。一緒に楽しい時間を過ごせる友達を探しています！'),
((SELECT id FROM users WHERE email = 'yamamoto.nanako@example.com'), 'サッカー, 読書, 音楽', '愛知県', '金融', 'スタッフ', 'ISTJ', '名古屋大学', 'role', 'サッカーと読書が好きで、音楽にも興味があります。静かな時間も楽しみながら、新しい友達を作りたいです！'),
((SELECT id FROM users WHERE email = 'inoue.keita@example.com'), 'ゲーム, 映画鑑賞, 旅行', '東京都', '法人', '営業', 'ESTP', '早稲田大学', 'field', 'ゲームや映画鑑賞が趣味で、旅行にもよく行きます。新しい友達と一緒に楽しむ時間を過ごしたいです！'),
((SELECT id FROM users WHERE email = 'sato.moe@example.com'), '音楽, ダンス, 旅行', '神奈川県', '法人', '営業', 'ENFJ', '慶應義塾大学', 'role', '音楽とダンスが好きで、旅行もよく行きます。楽しく過ごせる友達と一緒に新しい体験をしたいです！'),
((SELECT id FROM users WHERE email = 'kato.ruri@example.com'), 'プログラミング, 筋トレ, 読書', '東京都', '技統本', 'コンサル', 'INTP', '名古屋大学', 'field', 'プログラミングや筋トレが得意で、読書も大好きです。新しい技術に挑戦しながら、友達と学び合いたいです！'),
((SELECT id FROM users WHERE email = 'takahashi.hikaru@example.com'), 'ゲーム, 音楽, 映画鑑賞', '東京都', '金融', 'コンサル', 'INTJ', '慶應義塾大学', 'hobbies', 'ゲームと音楽が大好きです。映画鑑賞も楽しんでおり、リラックスできる友達と過ごしたいです。新しい友達を作りたいと思っています！'),
((SELECT id FROM users WHERE email = 'sato.ayumu@example.com'), 'カフェ, 旅行, プログラミング', '大阪府', '法人', 'SE', 'ISFJ', '東京大学', 'field', 'カフェ巡りと旅行が好きで、プログラミングも得意です。共通の趣味を持つ友達を作りたいと思っています！よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'suzuki.fuka@example.com'), 'ダンス, 登山, ボードゲーム', '福岡県', '技統本', 'スタッフ', 'ENFP', '名古屋大学', 'role', 'ダンスや登山が好きで、ボードゲームも楽しんでいます。アクティブに過ごす時間を一緒に楽しんでくれる友達を探しています！'),
((SELECT id FROM users WHERE email = 'yoshida.hitomi@example.com'), '映画鑑賞, 音楽, 旅行', '神奈川県', '金融', '営業', 'ISTP', '早稲田大学', 'hobbies', '映画鑑賞と音楽を楽しんでいます。旅行にもよく行くので、同じようにアクティブな友達と仲良くなりたいです！'),
((SELECT id FROM users WHERE email = 'nomura.miyu@example.com'), 'カメラ, 旅行, 料理', '大阪府', '法人', 'コンサル', 'INFP', '京都大学', 'field', 'カメラで風景を撮影したり、旅行を楽しんでいます。料理も得意なので、一緒に楽しめる友達を探しています！'),
((SELECT id FROM users WHERE email = 'ito.tatsuya@example.com'), 'ボードゲーム, 音楽, プログラミング', '東京都', '法人', 'スタッフ', 'ISTJ', '慶應義塾大学', 'hobbies', 'ボードゲームと音楽が好きで、プログラミングにも興味があります。新しいことを一緒に学びながら過ごせる友達を探しています！'),
((SELECT id FROM users WHERE email = 'tamura.asuka@example.com'), '旅行, ダンス, サッカー', '愛知県', '金融', 'SE', 'INTP', '早稲田大学', 'hobbies', '旅行やダンスが好きで、サッカー観戦も楽しんでいます。楽しい時間を一緒に過ごせる友達を探しています！'),
((SELECT id FROM users WHERE email = 'nakata.eri@example.com'), '音楽, 映画鑑賞, 読書', '神奈川県', '法人', '営業', 'INFJ', '慶應義塾大学', 'role', '音楽や映画鑑賞、読書が好きです。穏やかな会話ができる友達と一緒に過ごしたいです。気軽に声をかけてください！'),
((SELECT id FROM users WHERE email = 'iwata.yukio@example.com'), 'ボードゲーム, 旅行, 筋トレ', '埼玉県', '技統本', 'スタッフ', 'ISFP', '早稲田大学', 'field', 'ボードゲームや旅行が好きで、筋トレも日課です。新しい経験を一緒に楽しめる友達を探しています！'),
((SELECT id FROM users WHERE email = 'sasaki.nozomi@example.com'), '映画鑑賞, 音楽, 旅行', '東京都', '法人', 'SE', 'INTP', '慶應義塾大学', 'hobbies', '映画鑑賞と音楽が趣味で、旅行も好きです。新しい友達とリラックスできる時間を過ごしたいです！'),
((SELECT id FROM users WHERE email = 'hashimoto.ryo@example.com'), 'サッカー, 映画鑑賞, 旅行', '大阪府', '金融', '営業', 'ENFJ', '大阪大学', 'role', 'サッカーと映画鑑賞が好きで、旅行にもよく行きます。新しい友達と一緒に楽しい時間を過ごせたら嬉しいです！'),
((SELECT id FROM users WHERE email = 'miyamoto.yuna@example.com'), '読書, 音楽, ボードゲーム', '福岡県', '法人', 'SE', 'ISTJ', '東京大学', 'hobbies', '読書や音楽を楽しんでいます。ボードゲームもよくやりますので、静かな時間を一緒に過ごす友達を探しています！'),
((SELECT id FROM users WHERE email = 'saito.yoko@example.com'), 'プログラミング, ランニング, 映画鑑賞', '神奈川県', '技統本', 'スタッフ', 'INTP', '慶應義塾大学', 'field', 'プログラミングとランニングが好きです。映画も大好きで、共通の趣味を持つ友達と過ごしたいです！'),
((SELECT id FROM users WHERE email = 'kato.yu@example.com'), 'カメラ, 旅行, サッカー', '埼玉県', '金融', 'スタッフ', 'ENFP', '名古屋大学', 'role', 'カメラを持って旅行するのが大好きで、サッカーも観戦します。新しい経験を一緒に楽しめる友達を探しています！'),
((SELECT id FROM users WHERE email = 'ito.ryo@example.com'), '音楽, ボードゲーム, 筋トレ', '千葉県', '法人', '営業', 'ESTJ', '早稲田大学', 'hobbies', '音楽とボードゲームが好きで、筋トレも楽しんでいます。新しい友達と共にアクティブな時間を過ごしたいです！'),
((SELECT id FROM users WHERE email = 'kitamura.mayu@example.com'), 'ダンス, 旅行, 料理', '東京都', '金融', 'SE', 'INFJ', '東京大学', 'field', 'ダンスと旅行が好きで、料理にも挑戦しています。友達と楽しく過ごせる時間を一緒に楽しみたいです！'),
((SELECT id FROM users WHERE email = 'tanaka.rie@example.com'), '音楽, 読書, サッカー', '大阪府', '法人', 'コンサル', 'ISFP', '名古屋大学', 'role', '音楽や読書が好きで、サッカーも楽しんでいます。穏やかな会話をしながら、新しい友達を作りたいです！'),
((SELECT id FROM users WHERE email = 'yanagida.yuki@example.com'), 'カメラ, 旅行, ボードゲーム', '東京都', '技統本', 'スタッフ', 'ENFJ', '東京工業大学', 'hobbies', 'カメラを持って旅行するのが大好きです。ボードゲームも楽しんでおり、共通の趣味を持つ友達を探しています！'),
((SELECT id FROM users WHERE email = 'yamazaki.shota@example.com'), 'サッカー, 音楽, 旅行', '京都府', '法人', '営業', 'ISFP', '早稲田大学', 'role', 'サッカーと音楽を楽しんでいます。旅行にも行くのが好きなので、新しい友達と素晴らしい体験を共有したいです！'),
((SELECT id FROM users WHERE email = 'nakamura.yuta@example.com'), 'プログラミング, ゲーム, 旅行', '東京都', '金融', 'コンサル', 'ESTP', '慶應義塾大学', 'hobbies', 'プログラミングとゲームが好きで、旅行にもよく行きます。共通の興味を持つ友達を作りたいです！');
"""

INSERT_LIKES_SQL = """
INSERT INTO likes (id, user_id, target_user_id, reasons, created_at) VALUES
('b1f94672-4c23-4a8e-b5c5-61b4f3f5e7a1', (SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), (SELECT id FROM users WHERE email = 'sato.hanako@example.com'), '最近ボードゲームの楽しさを知ったので、一緒にボードゲームしたいです。', '2025-03-03 12:00:00'),
('c2e58a6b-2d1f-48f6-b871-9a362b4f5d3e', (SELECT id FROM users WHERE email = 'sato.hanako@example.com'), (SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), '東京詳しくないので、東京の観光地など教えて欲しいです。', '2025-03-03 12:05:00'),
('d3c74e9c-4b47-4d2f-bacf-61a57d3f5a9e', (SELECT id FROM users WHERE email = 'sato.hanako@example.com'), (SELECT id FROM users WHERE email = 'suzuki.ichiro@example.com'), 'MBTIが同じだったので、気が合うかもと思い、いいねしました。', '2025-03-03 12:10:00');
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