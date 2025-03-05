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
('田中 太郎', 'tanaka.taro@example.com', 'U12355678', crypt('securepassword1', gen_salt('bf')), '2023-05-01'),
('佐藤 花子', 'sato.hanako@example.com', 'U87654321', crypt('securepassword2', gen_salt('bf')), '2023-05-02'),
('鈴木 一郎', 'suzuki.ichiro@example.com', 'U25456789', crypt('securepassword3', gen_salt('bf')), '2023-05-03'),
('高橋 次郎', 'takahashi.jiro@example.com', 'U54567890', crypt('securepassword4', gen_salt('bf')), '2023-05-04'),
('井上 美咲', 'inoue.misaki@example.com', 'U45578901', crypt('securepassword5', gen_salt('bf')), '2023-05-05'),
('山本 健太', 'yamamoto.kenta@example.com', 'U55789012', crypt('securepassword6', gen_salt('bf')), '2023-05-06'),
('中村 桃子', 'nakamura.momoko@example.com', 'U57890123', crypt('securepassword7', gen_salt('bf')), '2023-05-07'),
('小林 太一', 'kobayashi.taichi@example.com', 'U58901234', crypt('securepassword8', gen_salt('bf')), '2023-05-08'),
('加藤 春菜', 'kato.haruna@example.com', 'U89012545', crypt('securepassword9', gen_salt('bf')), '2023-05-09'),
('吉田 和夫', 'yoshida.kazu@example.com', 'U90125456', crypt('securepassword10', gen_salt('bf')), '2023-05-10'),
('山田 涼太', 'yamada.ryota@example.com', 'U01235567', crypt('securepassword11', gen_salt('bf')), '2023-05-11'),
('佐々木 美咲', 'sasaki.misaki@example.com', 'U15345678', crypt('securepassword12', gen_salt('bf')), '2023-05-12'),
('森田 拓也', 'morita.takuya@example.com', 'U23456789', crypt('securepassword13', gen_salt('bf')), '2023-05-13'),
('大島 結衣', 'oshima.yui@example.com', 'U34567890', crypt('securepassword14', gen_salt('bf')), '2023-05-14'),
('松本 裕樹', 'matsumoto.yuki@example.com', 'U45678901', crypt('securepassword15', gen_salt('bf')), '2023-05-15'),
('藤田 千夏', 'fujita.chinatsu@example.com', 'U56789012', crypt('securepassword16', gen_salt('bf')), '2023-05-16'),
('渡辺 大輝', 'watanabe.daiki@example.com', 'U67890123', crypt('securepassword17', gen_salt('bf')), '2023-05-17'),
('石井 彩花', 'ishii.ayaka@example.com', 'U78901234', crypt('securepassword18', gen_salt('bf')), '2023-05-18'),
('清水 優太', 'shimizu.yuta@example.com', 'U89012345', crypt('securepassword19', gen_salt('bf')), '2023-05-19'),
('長谷川 結衣', 'hasegawa.yui@example.com', 'U90123456', crypt('securepassword20', gen_salt('bf')), '2023-05-20'),
('田村 陽介', 'tamura.yosuke@example.com', 'U01234568', crypt('securepassword21', gen_salt('bf')), '2023-05-21'),
('松井 恵理', 'matsui.eri@example.com', 'U12345679', crypt('securepassword22', gen_salt('bf')), '2023-05-22'),
('近藤 真一', 'kondo.shinichi@example.com', 'U23456790', crypt('securepassword23', gen_salt('bf')), '2023-05-23'),
('橋本 奈々', 'hashimoto.nana@example.com', 'U34567891', crypt('securepassword24', gen_salt('bf')), '2023-05-24'),
('小川 亮太', 'ogawa.ryota@example.com', 'U45678902', crypt('securepassword25', gen_salt('bf')), '2023-05-25'),
('遠藤 美月', 'endo.mizuki@example.com', 'U56789023', crypt('securepassword26', gen_salt('bf')), '2023-05-26'),
('三浦 大翔', 'miura.daito@example.com', 'U67890134', crypt('securepassword27', gen_salt('bf')), '2023-05-27'),
('永田 結菜', 'nagata.yuna@example.com', 'U78901245', crypt('securepassword28', gen_salt('bf')), '2023-05-28'),
('石川 一真', 'ishikawa.kazuma@example.com', 'U89012356', crypt('securepassword29', gen_salt('bf')), '2023-05-29'),
('岡田 知恵', 'okada.chie@example.com', 'U90123467', crypt('securepassword30', gen_salt('bf')), '2023-05-30'),
('佐藤 智子', 'sato.tomoko@example.com', 'U01234569', crypt('securepassword31', gen_salt('bf')), '2023-05-31'),
('中島 剛', 'nakajima.tsuyoshi@example.com', 'U12345680', crypt('securepassword32', gen_salt('bf')), '2023-06-01'),
('藤井 綾香', 'fujii.ayaka@example.com', 'U23456791', crypt('securepassword33', gen_salt('bf')), '2023-06-02'),
('堀田 勇気', 'hotta.yuki@example.com', 'U34567892', crypt('securepassword34', gen_salt('bf')), '2023-06-03'),
('山下 奈々子', 'yamashita.nanako@example.com', 'U45678903', crypt('securepassword35', gen_salt('bf')), '2023-06-04'),
('池田 海斗', 'ikeda.kaito@example.com', 'U56789034', crypt('securepassword36', gen_salt('bf')), '2023-06-05'),
('小松 聡', 'komatsu.satoshi@example.com', 'U67890145', crypt('securepassword37', gen_salt('bf')), '2023-06-06'),
('永井 優子', 'nagai.yuko@example.com', 'U78901256', crypt('securepassword38', gen_salt('bf')), '2023-06-07'),
('村田 修一', 'murata.shuichi@example.com', 'U89012367', crypt('securepassword39', gen_salt('bf')), '2023-06-08'),
('川口 美穂', 'kawaguchi.miho@example.com', 'U90123478', crypt('securepassword40', gen_salt('bf')), '2023-06-09'),
('林 大地', 'hayashi.daichi@example.com', 'U01234570', crypt('securepassword41', gen_salt('bf')), '2023-06-10'),
('小川 茉莉', 'ogawa.mari@example.com', 'U12345681', crypt('securepassword42', gen_salt('bf')), '2023-06-11'),
('木村 崇', 'kimura.takashi@example.com', 'U23456792', crypt('securepassword43', gen_salt('bf')), '2023-06-12'),
('加藤 美月', 'kato.mizuki@example.com', 'U34567893', crypt('securepassword44', gen_salt('bf')), '2023-06-13'),
('佐々木 明日香', 'sasaki.asuka@example.com', 'U45678904', crypt('securepassword45', gen_salt('bf')), '2023-06-14'),
('中村 翼', 'nakamura.tsubasa@example.com', 'U56789035', crypt('securepassword46', gen_salt('bf')), '2023-06-15'),
('藤田 翼', 'fujita.tsubasa@example.com', 'U67890156', crypt('securepassword47', gen_salt('bf')), '2023-06-16'),
('坂本 愛', 'sakamoto.ai@example.com', 'U78901267', crypt('securepassword48', gen_salt('bf')), '2023-06-17'),
('原田 大輝', 'harada.daiki@example.com', 'U89012378', crypt('securepassword49', gen_salt('bf')), '2023-06-18'),
('吉岡 千晶', 'yoshioka.chiaki@example.com', 'U90123489', crypt('securepassword50', gen_salt('bf')), '2023-06-19'),
('坂井 大志', 'sakai.taishi@example.com', 'U01234571', crypt('securepassword51', gen_salt('bf')), '2023-06-20'),
('平田 真紀', 'hirata.maki@example.com', 'U12345682', crypt('securepassword52', gen_salt('bf')), '2023-06-21'),
('中田 健太', 'nakata.kenta@example.com', 'U23456793', crypt('securepassword53', gen_salt('bf')), '2023-06-22'),
('安藤 優菜', 'ando.yuna@example.com', 'U34567894', crypt('securepassword54', gen_salt('bf')), '2023-06-23'),
('前田 結子', 'maeda.yuko@example.com', 'U45678905', crypt('securepassword55', gen_salt('bf')), '2023-06-24'),
('小林 寛之', 'kobayashi.hiroyuki@example.com', 'U56789046', crypt('securepassword56', gen_salt('bf')), '2023-06-25'),
('村上 千尋', 'murakami.chihiro@example.com', 'U67890167', crypt('securepassword57', gen_salt('bf')), '2023-06-26'),
('高田 裕太', 'takada.yuta@example.com', 'U78901278', crypt('securepassword58', gen_salt('bf')), '2023-06-27'),
('清水 陽子', 'shimizu.yoko@example.com', 'U89012389', crypt('securepassword59', gen_salt('bf')), '2023-06-28'),
('大竹 拓海', 'otake.takumi@example.com', 'U90123490', crypt('securepassword60', gen_salt('bf')), '2023-06-29'),
('長井 健太', 'nagai.kenta@example.com', 'U01234572', crypt('securepassword61', gen_salt('bf')), '2023-06-30'),
('松下 愛', 'matsushita.ai@example.com', 'U12345683', crypt('securepassword62', gen_salt('bf')), '2023-07-01'),
('岡本 里奈', 'okamoto.rina@example.com', 'U23456794', crypt('securepassword63', gen_salt('bf')), '2023-07-02'),
('堀江 翼', 'horie.tsubasa@example.com', 'U34567895', crypt('securepassword64', gen_salt('bf')), '2023-07-03'),
('小泉 一成', 'koizumi.issei@example.com', 'U45678906', crypt('securepassword65', gen_salt('bf')), '2023-07-04'),
('木下 雅人', 'kinoshita.masato@example.com', 'U56789047', crypt('securepassword66', gen_salt('bf')), '2023-07-05'),
('佐野 美香', 'sano.mika@example.com', 'U67890178', crypt('securepassword67', gen_salt('bf')), '2023-07-06'),
('渡辺 寛之', 'watanabe.hiroyuki@example.com', 'U78901289', crypt('securepassword68', gen_salt('bf')), '2023-07-07'),
('石井 未来', 'ishii.mirai@example.com', 'U89012390', crypt('securepassword69', gen_salt('bf')), '2023-07-08'),
('前川 恵美', 'maekawa.emi@example.com', 'U90123491', crypt('securepassword70', gen_salt('bf')), '2023-07-09'),
('山田 海斗', 'yamada.kaito@example.com', 'U01234573', crypt('securepassword71', gen_salt('bf')), '2023-07-10'),
('石田 一輝', 'ishida.kazuki@example.com', 'U12345684', crypt('securepassword72', gen_salt('bf')), '2023-07-11'),
('岡村 智也', 'okamura.tomoya@example.com', 'U23456795', crypt('securepassword73', gen_salt('bf')), '2023-07-12'),
('林 沙耶', 'hayashi.saya@example.com', 'U34567896', crypt('securepassword74', gen_salt('bf')), '2023-07-13'),
('田村 龍之介', 'tamura.ryunosuke@example.com', 'U45678907', crypt('securepassword75', gen_salt('bf')), '2023-07-14'),
('森本 理沙', 'morimoto.risa@example.com', 'U56789048', crypt('securepassword76', gen_salt('bf')), '2023-07-15'),
('山本 菜々子', 'yamamoto.nanako@example.com', 'U67890179', crypt('securepassword77', gen_salt('bf')), '2023-07-16'),
('井上 慶太', 'inoue.keita@example.com', 'U78901290', crypt('securepassword78', gen_salt('bf')), '2023-07-17'),
('佐藤 萌', 'sato.moe@example.com', 'U89012391', crypt('securepassword79', gen_salt('bf')), '2023-07-18'),
('加藤 瑠璃', 'kato.ruri@example.com', 'U90123492', crypt('securepassword80', gen_salt('bf')), '2023-07-19'),
('高橋 光', 'takahashi.hikaru@example.com', 'U01234574', crypt('securepassword81', gen_salt('bf')), '2023-07-20'),
('佐藤 歩', 'sato.ayumu@example.com', 'U12345685', crypt('securepassword82', gen_salt('bf')), '2023-07-21'),
('鈴木 風花', 'suzuki.fuka@example.com', 'U23456796', crypt('securepassword83', gen_salt('bf')), '2023-07-22'),
('吉田 仁美', 'yoshida.hitomi@example.com', 'U34567897', crypt('securepassword84', gen_salt('bf')), '2023-07-23'),
('野村 美優', 'nomura.miyu@example.com', 'U45678908', crypt('securepassword85', gen_salt('bf')), '2023-07-24'),
('伊藤 竜也', 'ito.tatsuya@example.com', 'U56789049', crypt('securepassword86', gen_salt('bf')), '2023-07-25'),
('田村 あすか', 'tamura.asuka@example.com', 'U67890180', crypt('securepassword87', gen_salt('bf')), '2023-07-26'),
('中田 恵理', 'nakata.eri@example.com', 'U78901291', crypt('securepassword88', gen_salt('bf')), '2023-07-27'),
('岩田 幸雄', 'iwata.yukio@example.com', 'U89012392', crypt('securepassword89', gen_salt('bf')), '2023-07-28'),
('佐々木 希', 'sasaki.nozomi@example.com', 'U90123493', crypt('securepassword90', gen_salt('bf')), '2023-07-29'),
('橋本 涼', 'hashimoto.ryo@example.com', 'U01234575', crypt('securepassword91', gen_salt('bf')), '2023-07-30'),
('宮本 結菜', 'miyamoto.yuna@example.com', 'U12345686', crypt('securepassword92', gen_salt('bf')), '2023-07-31'),
('斉藤 陽子', 'saito.yoko@example.com', 'U23456797', crypt('securepassword93', gen_salt('bf')), '2023-08-01'),
('加藤 優', 'kato.yu@example.com', 'U34567898', crypt('securepassword94', gen_salt('bf')), '2023-08-02'),
('伊藤 亮', 'ito.ryo@example.com', 'U45678909', crypt('securepassword95', gen_salt('bf')), '2023-08-03'),
('北村 真由', 'kitamura.mayu@example.com', 'U56789050', crypt('securepassword96', gen_salt('bf')), '2023-08-04'),
('田中 理恵', 'tanaka.rie@example.com', 'U67890181', crypt('securepassword97', gen_salt('bf')), '2023-08-05'),
('柳田 優希', 'yanagida.yuki@example.com', 'U78901292', crypt('securepassword98', gen_salt('bf')), '2023-08-06'),
('山崎 翔太', 'yamazaki.shota@example.com', 'U89012393', crypt('securepassword99', gen_salt('bf')), '2023-08-07'),
('中村 優太', 'nakamura.yuta@example.com', 'U90123494', crypt('securepassword100', gen_salt('bf')), '2023-08-08'); -- 80人分のデータを追加済み
"""

INSERT_USER_ATTRIBUTES_SQL = """
INSERT INTO user_attributes (user_id, hobbies, hometown, field, role, mbti, alma_mater, preferences) VALUES
((SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), '読書, 旅行, 映画鑑賞', '東京都', '公共', 'SE', 'INTJ', '東京大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'sato.hanako@example.com'), '料理, ボードゲーム, カメラ', '大阪府', '法人', '営業', 'ENTP', '京都大学', 'hometown'),
((SELECT id FROM users WHERE email = 'suzuki.ichiro@example.com'), 'ゲーム, 釣り, 音楽', '愛知県', '金融', 'コンサル', 'ENFP', '名古屋大学', 'field'),
((SELECT id FROM users WHERE email = 'takahashi.jiro@example.com'), 'サッカー, バスケットボール, ダンス', '北海道', 'TC&S', 'スタッフ', 'INTP', '北海道大学', 'role'),
((SELECT id FROM users WHERE email = 'inoue.misaki@example.com'), '旅行, カフェ, プログラミング', '神奈川県', '法人', 'SE', 'ISFJ', '早稲田大学', 'field'),
((SELECT id FROM users WHERE email = 'yamamoto.kenta@example.com'), '映画鑑賞, ランニング, アニメ', '福岡県', '技統本', '営業', 'ENFJ', '九州大学', 'role'),
((SELECT id FROM users WHERE email = 'nakamura.momoko@example.com'), '登山, 温泉, DIY', '京都府', '金融', 'スタッフ', 'ISFP', '大阪大学', 'field'),
((SELECT id FROM users WHERE email = 'kobayashi.taichi@example.com'), '音楽, 筋トレ, 読書', '東京都', '公共', 'SE', 'ISTJ', '東京工業大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'kato.haruna@example.com'), 'カメラ, 旅行, スポーツ観戦', '埼玉県', '法人', 'コンサル', 'INFJ', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'yoshida.kazu@example.com'), 'ボードゲーム, サッカー, 釣り', '大阪府', 'TC&S', 'スタッフ', 'ESTP', '大阪大学', 'hometown'),
((SELECT id FROM users WHERE email = 'yamada.ryota@example.com'), '音楽, 筋トレ, ランニング', '東京都', '公共', '営業', 'ISTP', '東京大学', 'role'),
((SELECT id FROM users WHERE email = 'sasaki.misaki@example.com'), 'カフェ, 旅行, ボードゲーム', '北海道', '法人', 'スタッフ', 'ISFJ', '東北大学', 'field'),
((SELECT id FROM users WHERE email = 'morita.takuya@example.com'), '映画鑑賞, ダンス, 旅行', '福岡県', '金融', 'SE', 'ENFJ', '九州大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'oshima.yui@example.com'), '読書, キャンプ, サッカー', '兵庫県', 'TC&S', 'コンサル', 'INTJ', '神戸大学', 'role'),
((SELECT id FROM users WHERE email = 'matsumoto.yuki@example.com'), 'プログラミング, ゲーム, 読書', '東京都', '法人', 'SE', 'ENFP', '早稲田大学', 'hometown'),
((SELECT id FROM users WHERE email = 'fujita.chinatsu@example.com'), 'カメラ, ボードゲーム, 釣り', '大阪府', '技統本', 'スタッフ', 'INTP', '大阪大学', 'field'),
((SELECT id FROM users WHERE email = 'watanabe.daiki@example.com'), '映画鑑賞, 登山, アニメ', '神奈川県', '金融', '営業', 'ISTJ', '慶應義塾大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'ishii.ayaka@example.com'), 'スポーツ観戦, 料理, 旅行', '埼玉県', '公共', 'コンサル', 'INFJ', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'shimizu.yuta@example.com'), 'ランニング, 音楽, ゲーム', '千葉県', '法人', 'SE', 'ENFP', '東京工業大学', 'field'),
((SELECT id FROM users WHERE email = 'hasegawa.yui@example.com'), 'ダンス, プログラミング, カフェ', '愛知県', '技統本', 'スタッフ', 'ENTP', '名古屋大学', 'hometown'),
((SELECT id FROM users WHERE email = 'tamura.yosuke@example.com'), 'ボードゲーム, プログラミング, 読書', '東京都', '金融', '営業', 'ISTP', '東京大学', 'role'),
((SELECT id FROM users WHERE email = 'matsui.eri@example.com'), '映画鑑賞, サッカー, 旅行', '大阪府', '公共', 'スタッフ', 'INTJ', '京都大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'kondo.shinichi@example.com'), 'カフェ, 料理, ランニング', '神奈川県', 'TC&S', 'SE', 'ENFP', '慶應義塾大学', 'field'),
((SELECT id FROM users WHERE email = 'hashimoto.nana@example.com'), '旅行, ゲーム, 音楽', '福岡県', '金融', 'コンサル', 'INFJ', '九州大学', 'role'),
((SELECT id FROM users WHERE email = 'ogawa.ryota@example.com'), 'ダンス, 登山, スポーツ観戦', '埼玉県', '法人', '営業', 'ENFP', '早稲田大学', 'field'),
((SELECT id FROM users WHERE email = 'endo.mizuki@example.com'), 'カメラ, 料理, アニメ', '千葉県', '公共', 'SE', 'ISFJ', '東京工業大学', 'role'),
((SELECT id FROM users WHERE email = 'miura.daito@example.com'), 'ランニング, 筋トレ, ボードゲーム', '大阪府', 'TC&S', 'スタッフ', 'INTP', '大阪大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'nagata.yuna@example.com'), '旅行, 音楽, サッカー', '神奈川県', '金融', 'SE', 'ESTJ', '名古屋大学', 'field'),
((SELECT id FROM users WHERE email = 'ishikawa.kazuma@example.com'), 'プログラミング, キャンプ, ボランティア', '京都府', '法人', 'コンサル', 'INTJ', '京都大学', 'hometown'),
((SELECT id FROM users WHERE email = 'okada.chie@example.com'), '読書, ダンス, 旅行', '東京都', '技統本', 'スタッフ', 'INFJ', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'sato.tomoko@example.com'), '読書, 映画鑑賞, 旅行', '東京都', '公共', 'SE', 'ISTJ', '早稲田大学', 'field'),
((SELECT id FROM users WHERE email = 'nakajima.tsuyoshi@example.com'), 'ボードゲーム, サッカー, カフェ', '大阪府', '法人', '営業', 'INFJ', '東京大学', 'role'),
((SELECT id FROM users WHERE email = 'fujii.ayaka@example.com'), 'アニメ, 音楽, プログラミング', '神奈川県', '金融', 'スタッフ', 'INTP', '慶應義塾大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'hotta.yuki@example.com'), 'ランニング, 筋トレ, 登山', '北海道', '技統本', 'コンサル', 'ISFJ', '北海道大学', 'field'),
((SELECT id FROM users WHERE email = 'yamashita.nanako@example.com'), 'ゲーム, 旅行, キャンプ', '埼玉県', '法人', '営業', 'ENFJ', '東京工業大学', 'role'),
((SELECT id FROM users WHERE email = 'ikeda.kaito@example.com'), '映画鑑賞, ボードゲーム, 音楽', '福岡県', '金融', 'スタッフ', 'ISTP', '九州大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'komatsu.satoshi@example.com'), 'サッカー, ダンス, プログラミング', '千葉県', '公共', 'SE', 'ENFP', '大阪大学', 'role'),
((SELECT id FROM users WHERE email = 'nagai.yuko@example.com'), '読書, カフェ, 釣り', '東京都', '金融', '営業', 'ISTJ', '慶應義塾大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'murata.shuichi@example.com'), 'ボードゲーム, 音楽, 旅行', '愛知県', '法人', 'SE', 'INFP', '名古屋大学', 'hometown'),
((SELECT id FROM users WHERE email = 'kawaguchi.miho@example.com'), '読書, キャンプ, ダンス', '神奈川県', '技統本', 'コンサル', 'ENTJ', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'hayashi.daichi@example.com'), 'サッカー, 旅行, ダンス', '東京都', '金融', 'スタッフ', 'ENFJ', '東京大学', 'role'),
((SELECT id FROM users WHERE email = 'ogawa.mari@example.com'), '映画鑑賞, 音楽, 読書', '大阪府', '法人', '営業', 'INFP', '大阪大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'kimura.takashi@example.com'), 'プログラミング, スポーツ観戦, ボードゲーム', '北海道', '技統本', 'SE', 'INTP', '北海道大学', 'field'),
((SELECT id FROM users WHERE email = 'kato.mizuki@example.com'), 'カフェ, ランニング, 旅行', '愛知県', '金融', 'コンサル', 'ISFP', '名古屋大学', 'role'),
((SELECT id FROM users WHERE email = 'sasaki.asuka@example.com'), 'アニメ, カメラ, 登山', '東京都', '法人', '営業', 'ISTJ', '早稲田大学', 'field'),
((SELECT id FROM users WHERE email = 'nakamura.tsubasa@example.com'), 'ゲーム, 音楽, サッカー', '千葉県', '公共', 'SE', 'INTJ', '慶應義塾大学', 'role'),
((SELECT id FROM users WHERE email = 'fujita.tsubasa@example.com'), '読書, 釣り, キャンプ', '神奈川県', '金融', 'スタッフ', 'ESTJ', '東京大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'sakamoto.ai@example.com'), 'ランニング, ボードゲーム, プログラミング', '京都府', '法人', '営業', 'INFJ', '京都大学', 'field'),
((SELECT id FROM users WHERE email = 'harada.daiki@example.com'), 'ダンス, 映画鑑賞, 旅行', '大阪府', '金融', 'SE', 'ENFP', '大阪大学', 'role'),
((SELECT id FROM users WHERE email = 'yoshioka.chiaki@example.com'), 'スポーツ観戦, 読書, サッカー', '愛知県', '技統本', 'コンサル', 'ISTP', '名古屋大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'sakai.taishi@example.com'), 'ゲーム, 旅行, 読書', '愛知県', '法人', 'スタッフ', 'INTP', '名古屋大学', 'role'),
((SELECT id FROM users WHERE email = 'hirata.maki@example.com'), 'ダンス, プログラミング, ボードゲーム', '福岡県', '技統本', '営業', 'INFJ', '九州大学', 'field'),
((SELECT id FROM users WHERE email = 'nakata.kenta@example.com'), 'サッカー, 音楽, 映画鑑賞', '東京都', '公共', 'コンサル', 'ENFJ', '東京大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'ando.yuna@example.com'), '読書, カメラ, 温泉', '京都府', '金融', 'スタッフ', 'ISTJ', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'maeda.yuko@example.com'), '映画鑑賞, プログラミング, 筋トレ', '大阪府', '法人', '営業', 'ESTJ', '大阪大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'kobayashi.hiroyuki@example.com'), '音楽, カフェ, サッカー', '神奈川県', '技統本', 'SE', 'ENFP', '慶應義塾大学', 'field'),
((SELECT id FROM users WHERE email = 'murakami.chihiro@example.com'), 'ゲーム, スポーツ観戦, ダンス', '埼玉県', '金融', 'コンサル', 'ISFP', '東京工業大学', 'role'),
((SELECT id FROM users WHERE email = 'takada.yuta@example.com'), 'ボードゲーム, キャンプ, ランニング', '京都府', '法人', '営業', 'INTJ', '京都大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'shimizu.yoko@example.com'), '料理, 音楽, 旅行', '千葉県', '技統本', 'SE', 'ISFJ', '大阪大学', 'field'),
((SELECT id FROM users WHERE email = 'otake.takumi@example.com'), 'プログラミング, 読書, 登山', '神奈川県', '公共', 'スタッフ', 'ESTP', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'nagai.kenta@example.com'), 'ダンス, サッカー, 釣り', '北海道', '公共', '営業', 'ISFP', '北海道大学', 'role'),
((SELECT id FROM users WHERE email = 'matsushita.ai@example.com'), '音楽, キャンプ, ボードゲーム', '大阪府', '法人', 'SE', 'INFJ', '大阪大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'okamoto.rina@example.com'), 'プログラミング, 旅行, 映画鑑賞', '東京都', '技統本', 'スタッフ', 'INTP', '東京工業大学', 'field'),
((SELECT id FROM users WHERE email = 'horie.tsubasa@example.com'), 'ランニング, 筋トレ, 料理', '愛知県', '法人', 'コンサル', 'ENFJ', '名古屋大学', 'role'),
((SELECT id FROM users WHERE email = 'koizumi.issei@example.com'), '音楽, ボードゲーム, 読書', '福岡県', '金融', 'スタッフ', 'ISTJ', '九州大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'kinoshita.masato@example.com'), '映画鑑賞, ダンス, キャンプ', '埼玉県', '法人', '営業', 'ESTP', '早稲田大学', 'field'),
((SELECT id FROM users WHERE email = 'sano.mika@example.com'), 'サッカー, ボードゲーム, 旅行', '神奈川県', '公共', 'SE', 'ENFP', '慶應義塾大学', 'role'),
((SELECT id FROM users WHERE email = 'watanabe.hiroyuki@example.com'), 'ダンス, 旅行, 映画鑑賞', '京都府', '技統本', 'コンサル', 'ISTJ', '京都大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'ishii.mirai@example.com'), '読書, プログラミング, ランニング', '大阪府', '金融', 'SE', 'INFJ', '大阪大学', 'field'),
((SELECT id FROM users WHERE email = 'maekawa.emi@example.com'), '旅行, 音楽, サッカー', '千葉県', '法人', '営業', 'INTJ', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'yamada.kaito@example.com'), '音楽, ゲーム, プログラミング', '東京都', '法人', 'SE', 'ENTP', '東京大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'ishida.kazuki@example.com'), '読書, 筋トレ, 旅行', '福岡県', '技統本', 'スタッフ', 'ISFJ', '慶應義塾大学', 'field'),
((SELECT id FROM users WHERE email = 'okamura.tomoya@example.com'), '映画鑑賞, カフェ, 登山', '愛知県', '金融', 'コンサル', 'INTJ', '名古屋大学', 'role'),
((SELECT id FROM users WHERE email = 'hayashi.saya@example.com'), 'ランニング, 旅行, 釣り', '大阪府', '法人', '営業', 'ISFP', '早稲田大学', 'field'),
((SELECT id FROM users WHERE email = 'tamura.ryunosuke@example.com'), 'ボードゲーム, 音楽, 旅行', '神奈川県', '技統本', 'SE', 'ENFJ', '東京工業大学', 'role'),
((SELECT id FROM users WHERE email = 'morimoto.risa@example.com'), 'ダンス, ボードゲーム, カフェ', '埼玉県', '法人', 'スタッフ', 'ISTP', '名古屋大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'yamamoto.nanako@example.com'), 'サッカー, 旅行, 映画鑑賞', '千葉県', '金融', 'コンサル', 'INFJ', '東京大学', 'role'),
((SELECT id FROM users WHERE email = 'inoue.keita@example.com'), 'スポーツ観戦, 音楽, 料理', '東京都', '法人', '営業', 'ENFP', '慶應義塾大学', 'field'),
((SELECT id FROM users WHERE email = 'sato.moe@example.com'), '映画鑑賞, 旅行, サッカー', '大阪府', '公共', 'SE', 'ESTJ', '早稲田大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'kato.ruri@example.com'), 'プログラミング, 筋トレ, 読書', '京都府', '技統本', 'コンサル', 'ENTP', '大阪大学', 'field'),
((SELECT id FROM users WHERE email = 'takahashi.hikaru@example.com'), 'ゲーム, 音楽, 映画鑑賞', '東京都', '金融', 'コンサル', 'INTJ', '慶應義塾大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'sato.ayumu@example.com'), 'カフェ, 旅行, プログラミング', '大阪府', '法人', 'SE', 'ISFJ', '東京大学', 'field'),
((SELECT id FROM users WHERE email = 'suzuki.fuka@example.com'), 'ダンス, 登山, ボードゲーム', '福岡県', '技統本', 'スタッフ', 'ENFP', '九州大学', 'role'),
((SELECT id FROM users WHERE email = 'yoshida.hitomi@example.com'), '映画鑑賞, ランニング, 旅行', '神奈川県', '金融', 'SE', 'INTP', '早稲田大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'nomura.miyu@example.com'), 'カメラ, 料理, サッカー', '大阪府', '法人', '営業', 'ESTJ', '名古屋大学', 'field'),
((SELECT id FROM users WHERE email = 'ito.tatsuya@example.com'), 'ボードゲーム, 音楽, プログラミング', '東京都', '公共', 'コンサル', 'INFJ', '東京工業大学', 'role'),
((SELECT id FROM users WHERE email = 'tamura.asuka@example.com'), '旅行, ランニング, ボードゲーム', '愛知県', '金融', '営業', 'ENFP', '早稲田大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'nakata.eri@example.com'), 'ダンス, プログラミング, 旅行', '千葉県', '法人', 'スタッフ', 'ISFP', '慶應義塾大学', 'field'),
((SELECT id FROM users WHERE email = 'iwata.yukio@example.com'), '音楽, ゲーム, キャンプ', '神奈川県', '技統本', 'SE', 'INTJ', '東京大学', 'role'),
((SELECT id FROM users WHERE email = 'sasaki.nozomi@example.com'), '映画鑑賞, サッカー, ボードゲーム', '埼玉県', '金融', '営業', 'INFJ', '名古屋大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'hashimoto.ryo@example.com'), 'サッカー, 映画鑑賞, 旅行', '大阪府', '金融', '営業', 'ENFJ', '大阪大学', 'role'),
((SELECT id FROM users WHERE email = 'miyamoto.yuna@example.com'), '読書, 音楽, ボードゲーム', '福岡県', '法人', 'SE', 'ISTJ', '早稲田大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'saito.yoko@example.com'), 'プログラミング, ランニング, 料理', '神奈川県', '公共', 'コンサル', 'INTP', '慶應義塾大学', 'field'),
((SELECT id FROM users WHERE email = 'kato.yu@example.com'), 'カメラ, ダンス, 旅行', '埼玉県', '技統本', '営業', 'ISFP', '東京大学', 'role'),
((SELECT id FROM users WHERE email = 'ito.ryo@example.com'), '音楽, 読書, 釣り', '東京都', '法人', 'スタッフ', 'ENFP', '名古屋大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'kitamura.mayu@example.com'), 'ゲーム, キャンプ, ダンス', '大阪府', '金融', 'SE', 'INTJ', '慶應義塾大学', 'field'),
((SELECT id FROM users WHERE email = 'tanaka.rie@example.com'), '映画鑑賞, 旅行, 料理', '神奈川県', '法人', '営業', 'ISTJ', '早稲田大学', 'role'),
((SELECT id FROM users WHERE email = 'yanagida.yuki@example.com'), 'プログラミング, ボードゲーム, 音楽', '東京都', '技統本', 'コンサル', 'ENFP', '東京大学', 'hobbies'),
((SELECT id FROM users WHERE email = 'yamazaki.shota@example.com'), 'ボードゲーム, 旅行, スポーツ観戦', '愛知県', '金融', 'スタッフ', 'INTP', '名古屋大学', 'field'),
((SELECT id FROM users WHERE email = 'nakamura.yuta@example.com'), 'ランニング, ダンス, プログラミング', '千葉県', '法人', 'SE', 'INFJ', '早稲田大学', 'role'); -- 80人分のデータを追加済み
"""

INSERT_LIKES_SQL = """
INSERT INTO likes (id, user_id, target_user_id, created_at) VALUES
('b1f94672-4c23-4a8e-b5c5-61b4f3f5e7a1', (SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), (SELECT id FROM users WHERE email = 'sato.hanako@example.com'), '2025-03-03 12:00:00'),
('c2e58a6b-2d1f-48f6-b871-9a362b4f5d3e', (SELECT id FROM users WHERE email = 'sato.hanako@example.com'), (SELECT id FROM users WHERE email = 'tanaka.taro@example.com'), '2025-03-03 12:05:00'),
('d3c74e9c-4b47-4d2f-bacf-61a57d3f5a9e', (SELECT id FROM users WHERE email = 'sato.hanako@example.com'), (SELECT id FROM users WHERE email = 'suzuki.ichiro@example.com'), '2025-03-03 12:10:00');
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