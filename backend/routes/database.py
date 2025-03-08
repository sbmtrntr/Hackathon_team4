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
    preferences TEXT NOT NULL,
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


# 各テーブルの架空データ挿入クエリ
INSERT_USERS_SQL = """
INSERT INTO users (name, email, slack_id, password_hash, cluster, created_at) VALUES
('鈴木 一郎', 'suzuki.ichiro@example.com', 'U11111111', crypt('securepassword1', gen_salt('bf')), NULL, '2023-03-01'),
('高橋 美咲', 'takahashi.misaki@example.com', 'U22222222', crypt('securepassword2', gen_salt('bf')), NULL, '2023-03-02'),
('佐藤 大輔', 'sato.daisuke@example.com', 'U33333333', crypt('securepassword3', gen_salt('bf')), NULL, '2023-03-03'),
('田中 直樹', 'tanaka.naoki@example.com', 'U44444444', crypt('securepassword4', gen_salt('bf')), NULL, '2023-03-04'),
('中村 由美', 'nakamura.yumi@example.com', 'U55555555', crypt('securepassword5', gen_salt('bf')), NULL, '2023-03-05'),
('山本 翔太', 'yamamoto.shota@example.com', 'U66666666', crypt('securepassword6', gen_salt('bf')), NULL, '2023-03-06'),
('小林 仁美', 'kobayashi.hitomi@example.com', 'U77777777', crypt('securepassword7', gen_salt('bf')), NULL, '2023-03-07'),
('加藤 健太', 'kato.kenta@example.com', 'U88888888', crypt('securepassword8', gen_salt('bf')), NULL, '2023-03-08'),
('松本 綾子', 'matsumoto.ayako@example.com', 'U99999999', crypt('securepassword9', gen_salt('bf')), NULL, '2023-03-09'),
('石井 佳子', 'ishii.keiko@example.com', 'U10101010', crypt('securepassword10', gen_salt('bf')), NULL, '2023-03-10'),
('岡田 翔太', 'okada.shota@example.com', 'U11121314', crypt('securepassword11', gen_salt('bf')), NULL, '2023-03-11'),
('吉田 美由紀', 'yoshida.miyuki@example.com', 'U22232425', crypt('securepassword12', gen_salt('bf')), NULL, '2023-03-12'),
('井上 雄一', 'inoue.yuichi@example.com', 'U33343536', crypt('securepassword13', gen_salt('bf')), NULL, '2023-03-13'),
('橋本 真由美', 'hashimoto.mayumi@example.com', 'U44454647', crypt('securepassword14', gen_salt('bf')), NULL, '2023-03-14'),
('山田 俊輔', 'yamada.shunsuke@example.com', 'U55565758', crypt('securepassword15', gen_salt('bf')), NULL, '2023-03-15'),
('藤田 玲奈', 'fujita.reina@example.com', 'U66676869', crypt('securepassword16', gen_salt('bf')), NULL, '2023-03-16'),
('松田 悠介', 'matsuda.yusuke@example.com', 'U77787980', crypt('securepassword17', gen_salt('bf')), NULL, '2023-03-17'),
('黒田 由香', 'kuroda.yuka@example.com', 'U88899091', crypt('securepassword18', gen_salt('bf')), NULL, '2023-03-18'),
('小松 美奈子', 'komatsu.minako@example.com', 'U99910102', crypt('securepassword19', gen_salt('bf')), NULL, '2023-03-19'),
('三浦 正博', 'miura.masahiro@example.com', 'U10111213', crypt('securepassword20', gen_salt('bf')), NULL, '2023-03-20'),
('田村 宗一郎', 'tamura.souichiro@example.com', 'U11121415', crypt('securepassword21', gen_salt('bf')), NULL, '2023-03-21'),
('遠藤 愛子', 'endo.aiko@example.com', 'U22232526', crypt('securepassword22', gen_salt('bf')), NULL, '2023-03-22'),
('小野 芳樹', 'ono.yoshiki@example.com', 'U33343637', crypt('securepassword23', gen_salt('bf')), NULL, '2023-03-23'),
('西村 雅彦', 'nishimura.masahiko@example.com', 'U44454748', crypt('securepassword24', gen_salt('bf')), NULL, '2023-03-24'),
('高田 美月', 'takada.mizuki@example.com', 'U55565859', crypt('securepassword25', gen_salt('bf')), NULL, '2023-03-25'),
('岩崎 真治', 'iwasaki.shinji@example.com', 'U66676970', crypt('securepassword26', gen_salt('bf')), NULL, '2023-03-26'),
('村上 加奈子', 'murakami.kanako@example.com', 'U77788081', crypt('securepassword27', gen_salt('bf')), NULL, '2023-03-27'),
('原田 結衣', 'harada.yui@example.com', 'U88899102', crypt('securepassword28', gen_salt('bf')), NULL, '2023-03-28'),
('木村 渚', 'kimura.nagisa@example.com', 'U99910203', crypt('securepassword29', gen_salt('bf')), NULL, '2023-03-29'),
('藤原 理恵', 'fujiwara.rie@example.com', 'U10121314', crypt('securepassword30', gen_salt('bf')), NULL, '2023-03-30'),
('佐々木 啓太', 'sasaki.keita@example.com', 'U11121315', crypt('securepassword31', gen_salt('bf')), NULL, '2023-03-31'),
('宮崎 寿美子', 'miyazaki.sumiko@example.com', 'U22232427', crypt('securepassword32', gen_salt('bf')), NULL, '2023-04-01'),
('林 哲也', 'hayashi.tetsuya@example.com', 'U33343639', crypt('securepassword33', gen_salt('bf')), NULL, '2023-04-02'),
('小川 彩花', 'ogawa.ayaka@example.com', 'U44454750', crypt('securepassword34', gen_salt('bf')), NULL, '2023-04-03'),
('村田 由紀', 'murata.yuki@example.com', 'U55565861', crypt('securepassword35', gen_salt('bf')), NULL, '2023-04-04'),
('高木 美沙子', 'takagi.misako@example.com', 'U66676972', crypt('securepassword36', gen_salt('bf')), NULL, '2023-04-05'),
('石田 健一', 'ishida.kenichi@example.com', 'U77788083', crypt('securepassword37', gen_salt('bf')), NULL, '2023-04-06'),
('坂本 涼', 'sakamoto.ryo@example.com', 'U88899104', crypt('securepassword38', gen_salt('bf')), NULL, '2023-04-07'),
('金子 美咲', 'kaneko.misaki@example.com', 'U99910206', crypt('securepassword39', gen_salt('bf')), NULL, '2023-04-08'),
('渡辺 順子', 'watanabe.junko@example.com', 'U10121316', crypt('securepassword40', gen_salt('bf')), NULL, '2023-04-09'),
('木下 陽子', 'kinoshita.youko@example.com', 'U11121317', crypt('securepassword41', gen_salt('bf')), NULL, '2023-04-10'),
('森本 誠', 'morimoto.makoto@example.com', 'U22232429', crypt('securepassword42', gen_salt('bf')), NULL, '2023-04-11'),
('斉藤 聡', 'saito.satoshi@example.com', 'U33343641', crypt('securepassword43', gen_salt('bf')), NULL, '2023-04-12'),
('藤井 朋子', 'fujii.tomoko@example.com', 'U44454752', crypt('securepassword44', gen_salt('bf')), NULL, '2023-04-13'),
('高橋 直人', 'takahashi.naoto@example.com', 'U55565863', crypt('securepassword45', gen_salt('bf')), NULL, '2023-04-14'),
('長谷川 佳奈', 'hasegawa.kenna@example.com', 'U66676974', crypt('securepassword46', gen_salt('bf')), NULL, '2023-04-15'),
('吉村 亮', 'yoshimura.ryo@example.com', 'U77788085', crypt('securepassword47', gen_salt('bf')), NULL, '2023-04-16'),
('中川 佐代', 'nakagawa.sayo@example.com', 'U88899106', crypt('securepassword48', gen_salt('bf')), NULL, '2023-04-17'),
('橋本 瞳', 'hashimoto.hitomi@example.com', 'U99910208', crypt('securepassword49', gen_salt('bf')), NULL, '2023-04-18'),
('本田 裕子', 'honda.yuko@example.com', 'U10121318', crypt('securepassword50', gen_salt('bf')), NULL, '2023-04-19'),
('坂口 優希', 'sakaguchi.yuki@example.com', 'U11121319', crypt('securepassword51', gen_salt('bf')), NULL, '2023-04-20'),
('加藤 里奈', 'kato.rina@example.com', 'U22232431', crypt('securepassword52', gen_salt('bf')), NULL, '2023-04-21'),
('大島 博樹', 'oshima.hiroki@example.com', 'U33343643', crypt('securepassword53', gen_salt('bf')), NULL, '2023-04-22'),
('佐野 美穂', 'sano.miho@example.com', 'U44454754', crypt('securepassword54', gen_salt('bf')), NULL, '2023-04-23'),
('木村 勝彦', 'kimura.katsuhiko@example.com', 'U55565865', crypt('securepassword55', gen_salt('bf')), NULL, '2023-04-24'),
('井上 大輔', 'inoue.daisuke@example.com', 'U66676976', crypt('securepassword56', gen_salt('bf')), NULL, '2023-04-25'),
('永田 奈々', 'nagata.nana@example.com', 'U77788087', crypt('securepassword57', gen_salt('bf')), NULL, '2023-04-26'),
('松井 優香', 'matsui.yuka@example.com', 'U88899108', crypt('securepassword58', gen_salt('bf')), NULL, '2023-04-27'),
('高山 恵理', 'takayama.eri@example.com', 'U99910210', crypt('securepassword59', gen_salt('bf')), NULL, '2023-04-28'),
('鈴木 昌樹', 'suzuki.masaki1@example.com', 'U10121320', crypt('securepassword60', gen_salt('bf')), NULL, '2023-04-29'),
('井口 聡子', 'iguchi.satoko@example.com', 'U11121321', crypt('securepassword61', gen_salt('bf')), NULL, '2023-04-30'),
('原田 翔', 'harada.sho@example.com', 'U22232433', crypt('securepassword62', gen_salt('bf')), NULL, '2023-05-01'),
('加藤 智子', 'kato.tomoko@example.com', 'U33343645', crypt('securepassword63', gen_salt('bf')), NULL, '2023-05-02'),
('渡辺 尚子', 'watanabe.naoko@example.com', 'U44454756', crypt('securepassword64', gen_salt('bf')), NULL, '2023-05-03'),
('佐々木 愛', 'sasaki.ai@example.com', 'U55565867', crypt('securepassword65', gen_salt('bf')), NULL, '2023-05-04'),
('野村 亮介', 'nomura.ryosuke@example.com', 'U66676978', crypt('securepassword66', gen_salt('bf')), NULL, '2023-05-05'),
('今井 和也', 'imai.kazuya@example.com', 'U77788089', crypt('securepassword67', gen_salt('bf')), NULL, '2023-05-06'),
('島田 裕子', 'shimada.yuko@example.com', 'U88899110', crypt('securepassword68', gen_salt('bf')), NULL, '2023-05-07'),
('小川 優斗', 'ogawa.yuto@example.com', 'U99910212', crypt('securepassword69', gen_salt('bf')), NULL, '2023-05-08'),
('加藤 裕子', 'kato.hiroko@example.com', 'U10121322', crypt('securepassword70', gen_salt('bf')), NULL, '2023-05-09'),
('山下 亜美', 'yamashita.ami@example.com', 'U11121323', crypt('securepassword71', gen_salt('bf')), NULL, '2023-05-10'),
('松本 卓也', 'matsumoto.takuya@example.com', 'U22232435', crypt('securepassword72', gen_salt('bf')), NULL, '2023-05-11'),
('村田 秀一', 'murata.shuichi@example.com', 'U33343647', crypt('securepassword73', gen_salt('bf')), NULL, '2023-05-12'),
('高木 亜紀', 'takagi.aki@example.com', 'U44454758', crypt('securepassword74', gen_salt('bf')), NULL, '2023-05-13'),
('福田 芳子', 'fukuda.yoshiko@example.com', 'U55565870', crypt('securepassword75', gen_salt('bf')), NULL, '2023-05-14'),
('吉田 和也', 'yoshida.kazuya@example.com', 'U66676980', crypt('securepassword76', gen_salt('bf')), NULL, '2023-05-15'),
('佐藤 玲', 'sato.rei@example.com', 'U77788091', crypt('securepassword77', gen_salt('bf')), NULL, '2023-05-16'),
('加藤 美樹', 'kato.miki@example.com', 'U88899112', crypt('securepassword78', gen_salt('bf')), NULL, '2023-05-17'),
('石井 健', 'ishii.ken@example.com', 'U99910214', crypt('securepassword79', gen_salt('bf')), NULL, '2023-05-18'),
('小林 里奈', 'kobayashi.rina@example.com', 'U10121324', crypt('securepassword80', gen_salt('bf')), NULL, '2023-05-19'),
('田中 友香', 'tanaka.tomoka@example.com', 'U11121326', crypt('securepassword81', gen_salt('bf')), NULL, '2023-05-20'),
('川口 賢治', 'kawaguchi.kenji@example.com', 'U22232438', crypt('securepassword82', gen_salt('bf')), NULL, '2023-05-21'),
('田村 華子', 'tamura.hanako@example.com', 'U33343649', crypt('securepassword83', gen_salt('bf')), NULL, '2023-05-22'),
('鈴木 正樹', 'suzuki.masaki@example.com', 'U44454760', crypt('securepassword84', gen_salt('bf')), NULL, '2023-05-23'),
('山本 志保', 'yamamoto.shiho@example.com', 'U55565872', crypt('securepassword85', gen_salt('bf')), NULL, '2023-05-24'),
('松田 悠人', 'matsuda.yuto@example.com', 'U66676983', crypt('securepassword86', gen_salt('bf')), NULL, '2023-05-25'),
('斉藤 一樹', 'saito.kazuki@example.com', 'U77788094', crypt('securepassword87', gen_salt('bf')), NULL, '2023-05-26'),
('三浦 薫', 'miura.kaoru@example.com', 'U88899116', crypt('securepassword88', gen_salt('bf')), NULL, '2023-05-27'),
('木村 由香', 'kimura.yuka@example.com', 'U99910218', crypt('securepassword89', gen_salt('bf')), NULL, '2023-05-28'),
('高橋 俊介', 'takahashi.shunsuke@example.com', 'U10121328', crypt('securepassword90', gen_salt('bf')), NULL, '2023-05-29'),
('西村 浩二', 'nishimura.koji@example.com', 'U11121330', crypt('securepassword91', gen_salt('bf')), NULL, '2023-05-30'),
('田村 浩子', 'tamura.hiroko@example.com', 'U22232440', crypt('securepassword92', gen_salt('bf')), NULL, '2023-05-31'),
('小林 結衣', 'kobayashi.yui@example.com', 'U33343651', crypt('securepassword93', gen_salt('bf')), NULL, '2023-06-01'),
('松本 信也', 'matsumoto.shinya@example.com', 'U44454762', crypt('securepassword94', gen_salt('bf')), NULL, '2023-06-02'),
('池田 美咲', 'ikeda.misaki@example.com', 'U55565874', crypt('securepassword95', gen_salt('bf')), NULL, '2023-06-03'),
('木下 知幸', 'kinoshita.tomoyuki@example.com', 'U66676985', crypt('securepassword96', gen_salt('bf')), NULL, '2023-06-04'),
('田中 実', 'tanaka.minoru@example.com', 'U77788096', crypt('securepassword97', gen_salt('bf')), NULL, '2023-06-05'),
('永井 優', 'nagai.yu@example.com', 'U88899118', crypt('securepassword98', gen_salt('bf')), NULL, '2023-06-06'),
('川口 美穂', 'kawaguchi.miho@example.com', 'U99910220', crypt('securepassword99', gen_salt('bf')), NULL, '2023-06-07'),
('石井 哲也', 'ishii.tetsuya@example.com', 'U10121332', crypt('securepassword100', gen_salt('bf')), NULL, '2023-06-08');
"""

INSERT_USER_ATTRIBUTES_SQL = """
INSERT INTO user_attributes (user_id, hobbies, hometown, field, role, mbti, alma_mater, preferences, self_introductions) VALUES
((SELECT id FROM users WHERE email = 'suzuki.ichiro@example.com'), 'サッカー, 旅行, 映画鑑賞', '東京都', '公共', 'SE', 'INTJ', '早稲田大学', 'hobbies, mbti', '初めまして、鈴木一郎です。旅行と映画鑑賞が大好きで、静かな時間を楽しんでいます。共通の趣味を持つ方とお話しできることを楽しみにしています！'),
((SELECT id FROM users WHERE email = 'takahashi.misaki@example.com'), '読書, 映画鑑賞, カフェ', '神奈川県', '金融', '営業', 'INFJ', '慶應義塾大学', 'hobbies, field', '映画や読書が趣味の高橋美咲です。カフェ巡りが好きで、ゆっくりとした時間を大切にしています。金融業界に興味があり、理想的な仲間を探しています。'),
((SELECT id FROM users WHERE email = 'sato.daisuke@example.com'), 'バスケットボール, 音楽, 旅行', '大阪府', '法人', 'SE', '京都大学', 'role, alma_mater', 'こんにちは、佐藤大輔です！音楽とバスケットボールが大好きで、旅行にもよく行きます。技術的な挑戦が好きなので、SEとして働いている方とお話ししたいです！'),
((SELECT id FROM users WHERE email = 'tanaka.naoki@example.com'), 'プログラミング, 筋トレ, ゲーム', '北海道', '技統本', 'スタッフ', 'ENTP', '東京大学', 'hobbies, role', 'プログラミングが大好きで、筋トレも趣味です。ゲームを通じてリラックスするのが好きで、エンタープライズ系の技術職に興味があります。新しい技術に挑戦したいです。'),
((SELECT id FROM users WHERE email = 'nakamura.yumi@example.com'), '読書, カメラ, 映画鑑賞', '愛知県', '法人', 'SE', 'INFP', '名古屋大学', 'field', '初めまして、ナカムラユミです。カメラと映画が趣味で、週末は写真を撮りながら散歩しています。法人分野に興味があり、ビジネスを学びたいと思っています。どうぞよろしくお願いします！'),
((SELECT id FROM users WHERE email = 'yamamoto.shota@example.com'), '音楽, ゲーム, キャンプ', '大阪府', '公共', 'SE', 'ISTJ', '大阪大学', 'field, hobbies', '音楽やゲームが好きな山本翔太です。自然の中で過ごすことが好きで、キャンプもよく行きます。公共分野に関心があり、社会に貢献できる仕事を目指しています。'),
((SELECT id FROM users WHERE email = 'kobayashi.hitomi@example.com'), '映画鑑賞, ラーメン, スポーツ観戦', '京都府', '金融', '営業', 'ESFP', '立命館大学', 'hobbies', '映画とラーメンが大好きな小林仁美です。友達と映画を観ることが多いですが、スポーツ観戦も欠かせません。共通の趣味がある方とお友達になりたいです！'),
((SELECT id FROM users WHERE email = 'kato.kenta@example.com'), '料理, 旅行, ボードゲーム', '福岡県', '法人', 'コンサル', '九州大学', 'role', 'こんにちは、加藤健太です。料理とボードゲームが好きで、特に友達との集まりが楽しみです。コンサルティング分野に興味があり、成長できる環境を求めています！'),
((SELECT id FROM users WHERE email = 'matsumoto.ayako@example.com'), 'カフェ, 読書, 音楽', '東京都', '金融', 'コンサル', 'ISTP', '早稲田大学', 'hobbies', '松本綾子です。カフェでゆっくり過ごしながら読書を楽しんでいます。音楽も欠かせません。金融業界に興味があり、新しい挑戦に一緒に取り組める仲間を探しています。'),
((SELECT id FROM users WHERE email = 'ishii.keiko@example.com'), 'スポーツ観戦, 映画鑑賞, サッカー', '千葉県', 'TC&S', 'SE', 'ENFJ', '明治大学', 'mbti, role', '石井佳子です！スポーツ観戦が好きで、特にサッカーに情熱を注いでいます。映画鑑賞も趣味で、ポジティブなエネルギーを持った方々と一緒に働きたいです。よろしくお願いします！'),
((SELECT id FROM users WHERE email = 'okada.shota@example.com'), 'プログラミング, 筋トレ, 音楽', '東京都', '技統本', 'SE', 'INTP', '東京工業大学', 'hobbies, field', '岡田翔太です！筋トレが趣味で、プログラミングも大好きです。理系の道を進みながら、テクノロジーに関する新しい発見を共有できる仲間を探しています。'),
((SELECT id FROM users WHERE email = 'yoshida.miyuki@example.com'), '旅行, サッカー, カフェ', '神奈川県', '金融', '営業', 'ISFJ', '早稲田大学', 'hobbies, role', '吉田美由紀です！旅行とサッカーが大好きで、カフェ巡りも楽しんでいます。金融分野に関心があり、柔軟で協力的な方と一緒に働きたいです。'),
((SELECT id FROM users WHERE email = 'inoue.yuichi@example.com'), '映画鑑賞, 音楽, バスケットボール', '大阪府', '法人', 'スタッフ',  'ENFP', '大阪大学', 'field, alma_mater', '映画と音楽が大好きな井上雄一です。バスケットボールをしてリフレッシュするのが日課です。法人分野に挑戦したいと思っています！'),
((SELECT id FROM users WHERE email = 'hashimoto.mayumi@example.com'), '読書, ゲーム, 筋トレ', '兵庫県', 'TC&S', '営業',  'ISTJ', '京都大学', 'role', '橋本真由美です。読書とゲームが趣味で、筋トレにも力を入れています。私自身、技術的な問題解決を追求したいと思っています！'),
((SELECT id FROM users WHERE email = 'yamada.shunsuke@example.com'), 'ランニング, サッカー, 旅行', '福岡県', '法人', 'SE', 'ESTP', '早稲田大学', 'hobbies', 'ランニングとサッカーが好きな山田俊輔です。旅行を通じて新しい場所を探索するのが楽しみです。人と関わることが好きなので、みんなで活動できる環境を探しています。'),
((SELECT id FROM users WHERE email = 'fujita.reina@example.com'), '映画鑑賞, カメラ, 料理', '千葉県', '金融', 'SE', 'ISFP', '慶應義塾大学', 'mbti', '藤田玲奈です！映画鑑賞とカメラが趣味で、週末はよく料理も楽しんでいます。金融分野でのキャリアを築きたいと思っています。新しい出会いを楽しみにしています！'),
((SELECT id FROM users WHERE email = 'matsuda.yusuke@example.com'), '旅行, 音楽, スポーツ観戦', '東京都', '公共', '営業', 'ENTJ', '東京大学', 'hobbies', '松田悠介です。旅行や音楽が大好きで、スポーツ観戦も欠かせません。社会貢献に興味があり、公共の分野で活動する仲間を探しています。'),
((SELECT id FROM users WHERE email = 'kuroda.yuka@example.com'), 'ダンス, 映画鑑賞, キャンプ', '愛知県', '技統本', 'SE', 'ENFJ', '名古屋大学', 'role, alma_mater', 'こんにちは、黒田由香です！ダンスと映画鑑賞が好きで、キャンプにも行くことが多いです。技術的な分野に興味があり、成長できる環境で活躍したいと思っています。'),
((SELECT id FROM users WHERE email = 'komatsu.minako@example.com'), 'バスケットボール, 旅行, 音楽', '大阪府', '金融', 'スタッフ', 'ISFJ', '立命館大学', 'field', '小松美奈子です！バスケットボールが趣味で、旅行にもよく出かけます。音楽が生活の一部で、金融業界でキャリアを築いていきたいと思っています。'),
((SELECT id FROM users WHERE email = 'miura.masahiro@example.com'), 'カメラ, 料理, 音楽', '北海道', '法人', '営業', 'ISTP', '北海道大学', 'field, alma_mater, role', '三浦正博です。カメラと料理が好きで、音楽も大切にしています。法人でのビジネス展開に興味があり、新しい経験を得たいと考えています。'),
((SELECT id FROM users WHERE email = 'tamura.souichiro@example.com'), '旅行, カフェ, 音楽', '東京都', '金融', '営業', 'ENTP', '早稲田大学', 'role, alma_mater', '田村宗一郎です！旅行が趣味で、カフェ巡りも大好きです。音楽は日々の癒しです。営業職として、効果的なコミュニケーションを取りながら新しいビジネスを広げていきたいと考えています。'),
((SELECT id FROM users WHERE email = 'endo.aiko@example.com'), '読書, 映画鑑賞, サッカー', '大阪府', '法人', 'SE', 'INFJ', '京都大学', 'hobbies, mbti', '遠藤愛子です。読書や映画鑑賞が大好きで、サッカーを観ることも趣味です。静かな時間を大切にしており、論理的な会話ができる方とお話ししたいと思っています。'),
((SELECT id FROM users WHERE email = 'ono.yoshiki@example.com'), '音楽, 旅行, プログラミング', '福岡県', '技統本', 'SE', 'ISFP', '東京大学', 'hobbies', '小野芳樹です！音楽とプログラミングが好きで、旅行も大好きです。新しい技術や方法論を学び、他の技術者と協力できる環境を求めています。'),
((SELECT id FROM users WHERE email = 'nishimura.masahiko@example.com'), '映画鑑賞, ダンス, バスケットボール', '東京都', '公共', 'スタッフ', 'ESTJ', '慶應義塾大学', 'hobbies', '西村雅彦です！映画鑑賞とダンスが趣味で、バスケットボールも楽しんでいます。公共の分野での成長に興味があり、責任感のあるポジションを求めています。'),
((SELECT id FROM users WHERE email = 'takada.mizuki@example.com'), 'カメラ, 旅行, 筋トレ', '京都府', '法人', 'コンサル', 'ISTP', '大阪大学', 'field, role', '高田美月です！カメラと旅行が趣味で、筋トレをして体を鍛えています。法人分野で成長し、戦略的な考え方を活かした仕事ができれば嬉しいです！'),
((SELECT id FROM users WHERE email = 'iwasaki.shinji@example.com'), 'サッカー, 音楽, 読書', '北海道', '金融', 'SE', 'INTJ', '北海道大学', 'mbti', '岩崎真治です。サッカーと音楽が趣味で、読書も欠かせません。論理的な思考を重視し、金融の分野で成長したいと思っています。'),
((SELECT id FROM users WHERE email = 'murakami.kanako@example.com'), '旅行, カフェ, ボードゲーム', '神奈川県', '法人', 'SE', 'ISFJ', '明治大学', 'role', '村上加奈子です！旅行とカフェ巡りが好きで、友達とボードゲームをするのが楽しみです。法人でのキャリアを積んで、人とのつながりを大切にしたいです。'),
((SELECT id FROM users WHERE email = 'harada.yui@example.com'), '料理, 音楽, 旅行', '千葉県', '金融', '営業', 'ENFJ', '立命館大学', 'mbti, role', '原田結衣です！料理と音楽が好きで、旅行もよく行きます。人とのつながりを大切にし、金融業界で積極的に成長していきたいです。'),
((SELECT id FROM users WHERE email = 'kimura.nagisa@example.com'), 'サッカー, 映画鑑賞, バスケットボール', '茨城県', '技統本', 'SE', 'ESTJ', '早稲田大学', 'hobbies', '木村渚です！サッカーとバスケットボールが好きで、映画鑑賞も楽しんでいます。技術的な分野で、チームワークを活かして成果を出していきたいと思っています。'),
((SELECT id FROM users WHERE email = 'fujiwara.rie@example.com'), 'ボードゲーム, 旅行, カメラ', '大阪府', '法人', 'SE', 'INFP', '関西大学', 'role', '藤原理恵です！ボードゲームが大好きで、旅行に出かけることが趣味です。法人の分野で、クリエイティブなアイディアを形にしていきたいです。'),
((SELECT id FROM users WHERE email = 'sasaki.keita@example.com'), 'サッカー, 音楽, 映画鑑賞', '東京都', '金融', '営業', 'ESTP', '慶應義塾大学', 'hobbies, role', '佐々木啓太です！サッカーや音楽が大好きで、映画鑑賞も趣味の一つです。営業職に興味があり、アクティブな環境で成長したいと思っています！'),
((SELECT id FROM users WHERE email = 'miyazaki.sumiko@example.com'), '旅行, 料理, 読書', '京都府', '法人', 'INFP', '京都大学', 'field, hobbies', '宮崎寿美子です！旅行と料理が趣味で、読書もよくします。法人分野で新しい挑戦をし、人とのつながりを深められる環境を探しています。'),
((SELECT id FROM users WHERE email = 'hayashi.tetsuya@example.com'), 'バスケットボール, カメラ, 音楽', '大阪府', '技統本', 'INTJ', '大阪大学', 'hobbies, mbti', '林哲也です。バスケットボールやカメラが趣味で、音楽も日常の一部です。論理的な思考を大切にし、技術分野での深い知識を身につけたいと考えています。'),
((SELECT id FROM users WHERE email = 'ogawa.ayaka@example.com'), '料理, 読書, 映画鑑賞', '兵庫県', '金融', 'ESFJ', '関西大学', 'role', '小川彩花です！料理や読書が好きで、映画鑑賞も楽しんでいます。金融分野でキャリアを築き、ビジネスの成長に貢献したいと思っています。'),
((SELECT id FROM users WHERE email = 'murata.yuki@example.com'), '音楽, キャンプ, ボードゲーム', '神奈川県', '法人', 'ISTJ', '早稲田大学', 'hobbies', '村田由紀です！音楽とキャンプが大好きで、ボードゲームを友達と楽しんでいます。法人分野でビジネスの展開を学び、成長していきたいと思っています。'),
((SELECT id FROM users WHERE email = 'takagi.misako@example.com'), 'バスケットボール, 映画鑑賞, 旅行', '千葉県', '公共', 'ISFP', '明治大学', 'mbti, field, hobbies', '高木美沙子です！バスケットボールと映画鑑賞が趣味で、旅行も大好きです。公共の分野で貢献できる仕事に携わりたいと考えています。'),
((SELECT id FROM users WHERE email = 'ishida.kenichi@example.com'), 'サッカー, 旅行, プログラミング', '福岡県', '技統本', 'ENTJ', '東京大学', 'hobbies', '石田健一です！サッカーや旅行が好きで、プログラミングに興味があります。技術分野でリーダーシップを発揮し、組織を導く役割を担いたいと思っています。'),
((SELECT id FROM users WHERE email = 'sakamoto.ryo@example.com'), '料理, 音楽, キャンプ', '北海道', '金融', 'INTP', '北海道大学', 'field', '坂本涼です！料理や音楽が趣味で、キャンプも楽しんでいます。金融業界における新たな挑戦を求めており、理論的かつ戦略的に取り組みたいです。'),
((SELECT id FROM users WHERE email = 'kaneko.misaki@example.com'), '旅行, サッカー, 釣り', '東京都', '法人', 'ISTP', '慶應義塾大学', 'role', '金子美咲です！旅行とサッカーが大好きで、釣りも趣味の一つです。法人分野でチームを率いてプロジェクトを成功させることに興味があります。'),
((SELECT id FROM users WHERE email = 'watanabe.junko@example.com'), '映画鑑賞, ダンス, 読書', '神奈川県', '公共', 'ESFJ', '立命館大学', 'hobbies', '渡辺順子です！映画鑑賞とダンスが趣味で、読書も楽しんでいます。社会的な貢献を目指して公共の分野で成長したいと思っています。'),
((SELECT id FROM users WHERE email = 'kinoshita.youko@example.com'), 'カメラ, 旅行, 読書', '東京都', '法人', 'コンサル', 'INFJ', '早稲田大学', 'hobbies, role', '木下陽子です！カメラと旅行が好きで、読書をよくします。コンサルティングの分野で他の人々と協力し、新しい問題に取り組みたいと思っています。'),
((SELECT id FROM users WHERE email = 'morimoto.makoto@example.com'), 'プログラミング, 音楽, バスケットボール', '大阪府', '金融', '営業', 'ENTP', '京都大学', 'field', '森本誠です！プログラミングと音楽が好きで、バスケットボールも楽しんでいます。金融分野に興味があり、データ分析や戦略的思考に挑戦したいです。'),
((SELECT id FROM users WHERE email = 'saito.satoshi@example.com'), '映画鑑賞, ラーメン, 読書', '北海道', '技統本', '営業', 'INTJ', '北海道大学', 'hobbies, role', '斉藤聡です！映画鑑賞とラーメンが趣味で、読書も大好きです。技術の分野で専門性を高め、新しい挑戦に取り組みたいと考えています。'),
((SELECT id FROM users WHERE email = 'fujii.tomoko@example.com'), '旅行, 音楽, 料理', '神奈川県', '法人', 'コンサル', 'ISFJ', '明治大学', 'role', '藤井朋子です！旅行と音楽が趣味で、料理も楽しんでいます。法人分野でのキャリアを築きたいと思っており、責任ある役割を果たしたいです。'),
((SELECT id FROM users WHERE email = 'takahashi.naoto@example.com'), 'スポーツ観戦, バスケットボール, 料理', '東京都', '公共', 'SE', 'ENFP', '慶應義塾大学', 'hobbies', '高橋直人です！スポーツ観戦とバスケットボールが好きで、料理も得意です。公共分野に関心があり、社会的な問題を解決したいと思っています。'),
((SELECT id FROM users WHERE email = 'hasegawa.kenna@example.com'), 'カフェ, 音楽, 旅行', '大阪府', '金融', 'SE', 'ENFJ', '大阪大学', 'hobbies', '長谷川佳奈です！カフェ巡りや音楽が大好きで、旅行も楽しんでいます。金融業界で働き、柔軟でリーダーシップを持つ環境で成長したいです。'),
((SELECT id FROM users WHERE email = 'yoshimura.ryo@example.com'), '音楽, バスケットボール, ゲーム', '愛知県', '技統本', 'SE', 'ISTP', '名古屋大学', 'field, mbti', '吉村亮です！音楽とバスケットボールが好きで、ゲームも趣味です。技術分野に興味があり、問題解決能力を高めたいと思っています。'),
((SELECT id FROM users WHERE email = 'nakagawa.sayo@example.com'), '映画鑑賞, ダンス, 料理', '京都府', '金融', 'SE', 'ISFP', '立命館大学', 'role', '中川佐代です！映画鑑賞やダンスが趣味で、料理も大好きです。金融業界に興味があり、人と協力しながら成長したいと考えています。'),
((SELECT id FROM users WHERE email = 'hashimoto.hitomi@example.com'), '読書, ボードゲーム, カフェ', '東京都', '法人', 'コンサル', 'INTP', '早稲田大学', 'hobbies', '橋本瞳です！読書やボードゲームが好きで、カフェでゆっくり過ごすのが楽しみです。法人分野で働き、ビジネスに関する知識を深めていきたいです。'),
((SELECT id FROM users WHERE email = 'honda.yuko@example.com'), 'サッカー, ラーメン, 旅行', '千葉県', '法人', '営業', 'ENTP', '東京大学', 'field', '本田裕子です！サッカーやラーメンが大好きで、旅行にもよく行きます。法人分野で活躍し、より多くのチャンスに挑戦したいと考えています。'),
((SELECT id FROM users WHERE email = 'sakaguchi.yuki@example.com'), '音楽, 映画鑑賞, 読書', '東京都', '金融', '営業', 'ISTJ', '早稲田大学', 'hobbies, role', '坂口優希です！音楽や映画鑑賞、読書が大好きです。営業職として他の人々とのコミュニケーションを大切にしています。金融業界で成長できる仲間を求めています。'),
((SELECT id FROM users WHERE email = 'kato.rina@example.com'), 'カメラ, 旅行, プログラミング', '大阪府', '技統本', 'コンサル', 'INTP', '慶應義塾大学', 'alma_mater', '加藤里奈です！カメラと旅行が趣味で、プログラミングにも取り組んでいます。技術分野で新しい挑戦を求めており、問題解決能力を伸ばしていきたいです。'),
((SELECT id FROM users WHERE email = 'oshima.hiroki@example.com'), 'スポーツ観戦, 音楽, キャンプ', '福岡県', '法人', 'コンサル', 'ISFJ', '北海道大学', 'hobbies', '大島博樹です！スポーツ観戦と音楽が大好きで、キャンプもよく楽しんでいます。法人分野で活躍し、チームワークを大切にしたいと考えています。'),
((SELECT id FROM users WHERE email = 'sano.miho@example.com'), '読書, バスケットボール, ダンス', '神奈川県', '公共', 'コンサル', 'ISFP', '東京大学', 'field', '佐野美穂です！読書とバスケットボールが趣味で、ダンスも楽しんでいます。公共分野で人々に貢献できる仕事をしたいと考えています。'),
((SELECT id FROM users WHERE email = 'kimura.katsuhiko@example.com'), '映画鑑賞, ボードゲーム, 音楽', '大阪府', '法人', 'コンサル', 'ENTP', '立命館大学', 'hobbies', '木村勝彦です！映画鑑賞と音楽が好きで、ボードゲームも友達と楽しんでいます。法人分野で新しいチャレンジをして、ビジネススキルを高めたいと考えています。'),
((SELECT id FROM users WHERE email = 'inoue.daisuke@example.com'), 'サッカー, 音楽, プログラミング', '東京都', '技統本', '営業', 'ESTP', '早稲田大学', 'hobbies, mbti', '井上大輔です！サッカーと音楽が大好きで、プログラミングにも興味があります。技術的な問題解決に挑戦し、スキルを高めていきたいです。'),
((SELECT id FROM users WHERE email = 'nagata.nana@example.com'), 'ダンス, サッカー, 旅行', '愛知県', '金融', 'SE', 'INFJ', '名古屋大学', 'role', '永田奈々です！ダンスやサッカーが好きで、旅行にもよく行きます。金融業界で、人と関わりながら成長したいと思っています。'),
((SELECT id FROM users WHERE email = 'matsui.yuka@example.com'), 'カメラ, 料理, 旅行', '東京都', '法人', '営業', 'ESFJ', '慶應義塾大学', 'hobbies', '松井優香です！カメラと料理が趣味で、旅行を通じて世界を広げています。法人分野でのキャリアを築き、人々に貢献する仕事をしたいです。'),
((SELECT id FROM users WHERE email = 'takayama.eri@example.com'), '音楽, 映画鑑賞, ボードゲーム', '神奈川県', '技統本', '営業', 'INTJ', '東京大学', 'hobbies', '高山恵理です！音楽と映画鑑賞が好きで、ボードゲームを友達とよくします。技術の分野で問題解決を行い、革新的なアイデアを形にしていきたいです。'),
((SELECT id FROM users WHERE email = 'suzuki.masaki1@example.com'), '料理, バスケットボール, 音楽', '大阪府', '法人', 'SE', 'ENTJ', '立命館大学', 'field', '鈴木昌樹です！料理やバスケットボールが好きで、音楽を聴くことが日課です。法人分野で戦略的な思考を活かし、リーダーシップを発揮したいと考えています。'),
((SELECT id FROM users WHERE email = 'iguchi.satoko@example.com'), '音楽, 映画鑑賞, 旅行', '京都府', '金融', '営業', 'ISFJ', '慶應義塾大学', 'hobbies', '井口聡子です！音楽と映画鑑賞が大好きで、旅行も楽しんでいます。営業職として人々と関わりながら成長していきたいと思っています。'),
((SELECT id FROM users WHERE email = 'harada.sho@example.com'), 'プログラミング, 映画鑑賞, バスケットボール', '大阪府', '技統本', 'コンサル', 'ENTP', '東京大学', 'hobbies, field', '原田翔です！プログラミングと映画鑑賞が趣味で、バスケットボールを楽しんでいます。技術分野で成長し、社会に貢献できる仕事をしたいです。'),
((SELECT id FROM users WHERE email = 'kato.tomoko@example.com'), '読書, 料理, ボードゲーム', '東京都', '法人', 'SE', 'ISTP', '名古屋大学', 'role, hobbies', '加藤智子です！読書と料理が趣味で、ボードゲームも楽しんでいます。法人分野で仕事を学び、成長したいと考えています。'),
((SELECT id FROM users WHERE email = 'watanabe.naoko@example.com'), '音楽, サッカー, キャンプ', '神奈川県', '法人', 'ENFJ', '立命館大学', 'hobbies', '渡辺尚子です！音楽やサッカーが好きで、キャンプもよく楽しんでいます。法人分野で新しい挑戦をしていきたいです。'),
((SELECT id FROM users WHERE email = 'sasaki.ai@example.com'), '映画鑑賞, 音楽, 旅行', '大阪府', '金融', 'INFJ', '慶應義塾大学', 'field', '佐々木愛です！映画鑑賞と音楽が大好きで、旅行にもよく行きます。金融分野でキャリアを積んで、社会に貢献したいと思っています。'),
((SELECT id FROM users WHERE email = 'nomura.ryosuke@example.com'), 'ダンス, バスケットボール, サッカー', '愛知県', '公共', 'ISFP', '名古屋大学', 'role', '野村亮介です！ダンスやバスケットボールが好きで、サッカーもよく観戦します。公共の分野で人々に貢献できる仕事をしたいと考えています。'),
((SELECT id FROM users WHERE email = 'imai.kazuya@example.com'), 'プログラミング, ゲーム, 映画鑑賞', '千葉県', '技統本', 'INTP', '東京工業大学', 'hobbies', '今井和也です！プログラミングとゲームが好きで、映画鑑賞も楽しんでいます。技術分野で新しい挑戦をしたいと考えています。'),
((SELECT id FROM users WHERE email = 'shimada.yuko@example.com'), '音楽, サッカー, 読書', '北海道', '法人', 'ESFJ', '立命館大学', 'field', '島田裕子です！音楽とサッカーが好きで、読書も楽しんでいます。法人分野で働き、人々に貢献したいと思っています。'),
((SELECT id FROM users WHERE email = 'ogawa.yuto@example.com'), 'ゲーム, サッカー, 料理', '東京都', '金融', 'ISTJ', '早稲田大学', 'field, hobbies', '小川優斗です！ゲームとサッカーが趣味で、料理も好きです。金融業界で働き、戦略的なキャリアを築いていきたいと思っています。'),
((SELECT id FROM users WHERE email = 'kato.hiroko@example.com'), '映画鑑賞, 音楽, 旅行', '大阪府', '法人', 'ESFP', '慶應義塾大学', 'role', '加藤裕子です！映画鑑賞と音楽が好きで、旅行にもよく行きます。法人分野でリーダーシップを発揮し、チームと一緒に成果を出していきたいと思っています。'),
((SELECT id FROM users WHERE email = 'yamashita.ami@example.com'), '映画鑑賞, 料理, 旅行', '東京都', '金融', '営業', 'INFJ', '早稲田大学', 'hobbies, field', '山下亜美です！映画鑑賞と料理が趣味で、旅行にもよく行きます。金融業界で営業として人々に貢献したいと思っています。'),
((SELECT id FROM users WHERE email = 'matsumoto.takuya@example.com'), 'サッカー, バスケットボール, 音楽', '大阪府', '法人', 'ESTP', '慶應義塾大学', 'role', '松本卓也です！サッカーやバスケットボールが好きで、音楽を楽しんでいます。法人分野で新たなチャレンジをしたいと思っています。'),
((SELECT id FROM users WHERE email = 'murata.shuichi@example.com'), '読書, 料理, ボードゲーム', '福岡県', '公共', 'ISFJ', '名古屋大学', 'role', '村田秀一です！読書と料理が好きで、ボードゲームを友達と楽しんでいます。公共分野で社会貢献できる仕事をしたいと思っています。'),
((SELECT id FROM users WHERE email = 'takagi.aki@example.com'), '音楽, キャンプ, バスケットボール', '千葉県', '技統本', 'ISTP', '東京大学', 'hobbies', '高木亜紀です！音楽とキャンプが好きで、バスケットボールも楽しんでいます。技術分野で新しいアイデアを生み出したいと思っています。'),
((SELECT id FROM users WHERE email = 'fukuda.yoshiko@example.com'), '映画鑑賞, サッカー, ダンス', '北海道', '金融', 'INTJ', '慶應義塾大学', 'alma_mater', '福田芳子です！映画鑑賞とサッカーが好きで、ダンスも楽しんでいます。金融分野で新たな挑戦をしていきたいです。'),
((SELECT id FROM users WHERE email = 'yoshida.kazuya@example.com'), 'カメラ, 読書, ボードゲーム', '愛知県', '法人', 'ISTJ', '大阪大学', 'field', '吉田和也です！カメラと読書が趣味で、ボードゲームも楽しんでいます。法人分野での成長を目指し、貢献できる環境を探しています。'),
((SELECT id FROM users WHERE email = 'sato.rei@example.com'), '音楽, サッカー, 映画鑑賞', '神奈川県', '技統本', 'ENFP', '早稲田大学', 'hobbies', '佐藤玲です！音楽とサッカーが大好きで、映画鑑賞も楽しんでいます。技術分野で新しい挑戦をしたいと考えています。'),
((SELECT id FROM users WHERE email = 'kato.miki@example.com'), '旅行, 料理, ボードゲーム', '東京都', '金融', 'ISFP', '立命館大学', 'alma_mater', '加藤美樹です！旅行と料理が好きで、ボードゲームも楽しんでいます。金融業界で働きながら、成長できる環境を探しています。'),
((SELECT id FROM users WHERE email = 'ishii.ken@example.com'), 'ゲーム, バスケットボール, 旅行', '大阪府', '法人', 'ENTJ', '東京大学', 'role', '石井健です！ゲームとバスケットボールが趣味で、旅行にもよく出かけます。法人分野でリーダーシップを発揮し、チームを牽引したいと思っています。'),
((SELECT id FROM users WHERE email = 'kobayashi.rina@example.com'), '音楽, 映画鑑賞, カフェ', '北海道', '技統本', 'INTP', '北海道大学', 'hobbies', '小林里奈です！音楽と映画鑑賞が大好きで、カフェでゆっくり過ごすのが楽しみです。技術分野で深い知識を身につけ、新しい発見をしたいと考えています。'),
((SELECT id FROM users WHERE email = 'tanaka.tomoka@example.com'), '旅行, 音楽, 読書', '大阪府', '法人', 'SE', 'INFP', '早稲田大学', 'hobbies, field', '田中友香です！旅行と音楽が大好きで、読書も楽しんでいます。SEとして、システム開発の分野で貢献できる仕事をしたいです。'),
((SELECT id FROM users WHERE email = 'kawaguchi.kenji@example.com'), '映画鑑賞, サッカー, ダンス', '東京都', '金融', 'ISTJ', '慶應義塾大学', 'role', '川口賢治です！映画鑑賞とサッカーが趣味で、ダンスも楽しんでいます。金融業界でキャリアを築き、成長できるチャンスを求めています。'),
((SELECT id FROM users WHERE email = 'tamura.hanako@example.com'), 'プログラミング, カメラ, 旅行', '千葉県', '技統本', 'INTP', '東京大学', 'hobbies', '田村華子です！プログラミングとカメラが好きで、旅行も楽しんでいます。技術の分野で新しい挑戦をし、成長したいと思っています。'),
((SELECT id FROM users WHERE email = 'suzuki.masaki@example.com'), '料理, 音楽, ボードゲーム', '神奈川県', '法人', 'ENTJ', '立命館大学', 'role, alma_mater', '鈴木正樹です！料理や音楽が好きで、ボードゲームを友達と楽しんでいます。法人分野でリーダーシップを発揮し、成果を上げたいと考えています。'),
((SELECT id FROM users WHERE email = 'yamamoto.shiho@example.com'), '映画鑑賞, バスケットボール, サッカー', '大阪府', '公共', 'ISFJ', '慶應義塾大学', 'field', '山本志保です！映画鑑賞とバスケットボールが趣味で、サッカーも好きです。公共の分野で活躍し、社会に貢献したいと思っています。'),
((SELECT id FROM users WHERE email = 'matsuda.yuto@example.com'), '音楽, サッカー, ゲーム', '福岡県', '金融', 'ENFJ', '明治大学', 'hobbies', '松田悠人です！音楽とサッカーが大好きで、ゲームも趣味の一つです。金融業界で柔軟に対応しながら成長していきたいと思っています。'),
((SELECT id FROM users WHERE email = 'saito.kazuki@example.com'), 'ダンス, バスケットボール, 読書', '東京都', '法人', 'ESTJ', '早稲田大学', 'filed, alma_mater', '斉藤一樹です！ダンスやバスケットボールが好きで、読書も楽しんでいます。法人分野でリーダーシップを発揮し、積極的に挑戦していきたいです。'),
((SELECT id FROM users WHERE email = 'miura.kaoru@example.com'), '音楽, 旅行, サッカー', '愛知県', '技統本', 'INTJ', '名古屋大学', 'field', '三浦薫です！音楽と旅行が大好きで、サッカーも趣味です。技術の分野で成長し、新しい技術を身につけたいと考えています。'),
((SELECT id FROM users WHERE email = 'kimura.yuka@example.com'), 'カメラ, 料理, 読書', '神奈川県', '金融', 'ISFP', '慶應義塾大学', 'role', '木村由香です！カメラと料理が趣味で、読書も好きです。金融業界で働きながら、スキルアップを目指しています。'),
((SELECT id FROM users WHERE email = 'takahashi.shunsuke@example.com'), '映画鑑賞, ダンス, ラーメン', '大阪府', '法人', 'ENTP', '立命館大学', 'filed, hobbies', '高橋俊介です！映画鑑賞やダンスが好きで、ラーメンを食べ歩くことが楽しみです。法人分野で新しい価値を創出し、ビジネスの成長に貢献したいと思っています。'),
((SELECT id FROM users WHERE email = 'nishimura.koji@example.com'), 'サッカー, 音楽, ダンス', '愛知県', '金融', '営業', 'ESTJ', '慶應義塾大学', 'role', '西村浩二です！サッカーや音楽が好きで、ダンスも楽しんでいます。営業職として、他の人々と信頼関係を築いていきたいと思っています。'),
((SELECT id FROM users WHERE email = 'tamura.hiroko@example.com'), '映画鑑賞, 読書, 旅行', '東京都', '法人', 'INFJ', '早稲田大学', 'hobbies', '田村浩子です！映画鑑賞と読書が趣味で、旅行にもよく出かけます。法人分野で新しいプロジェクトに関わり、成長していきたいと思っています。'),
((SELECT id FROM users WHERE email = 'kobayashi.yui@example.com'), '音楽, 旅行, バスケットボール', '大阪府', '金融', 'ISTP', '京都大学', 'alma_mater', '小林結衣です！音楽と旅行が大好きで、バスケットボールも趣味の一つです。金融業界で新しい挑戦をし、キャリアを築いていきたいと思っています。'),
((SELECT id FROM users WHERE email = 'matsumoto.shinya@example.com'), 'プログラミング, サッカー, 料理', '神奈川県', '技統本', 'INTJ', '東京大学', 'hobbies', '松本信也です！プログラミングとサッカーが好きで、料理も得意です。技術分野で新しい挑戦をしたいと考えています。'),
((SELECT id FROM users WHERE email = 'ikeda.misaki@example.com'), '音楽, カメラ, 映画鑑賞', '北海道', '法人', 'ENTP', '慶應義塾大学', 'role', '池田美咲です！音楽とカメラが趣味で、映画鑑賞も楽しんでいます。法人分野で新しい価値を創造し、活躍したいと考えています。'),
((SELECT id FROM users WHERE email = 'kinoshita.tomoyuki@example.com'), '旅行, サッカー, 音楽', '大阪府', '金融', 'INFP', '名古屋大学', 'hobbies, alma_mater', '木下知幸です！旅行とサッカーが好きで、音楽も日常の一部です。金融業界で積極的に学び、成長したいと思っています。'),
((SELECT id FROM users WHERE email = 'tanaka.minoru@example.com'), '映画鑑賞, ボードゲーム, 音楽', '福岡県', '法人', 'ESTP', '東京大学', 'hobbies', '田中実です！映画鑑賞やボードゲームが趣味で、音楽を聴くことが大好きです。法人分野で働き、新しい挑戦に取り組みたいと思っています。'),
((SELECT id FROM users WHERE email = 'nagai.yu@example.com'), 'スポーツ観戦, サッカー, 音楽', '東京都', '技統本', 'ISFJ', '早稲田大学', 'field', '永井優です！スポーツ観戦とサッカーが大好きで、音楽も欠かせません。技術分野で成長し、新しいプロジェクトに関わりたいと思っています。'),
((SELECT id FROM users WHERE email = 'kawaguchi.miho@example.com'), '読書, バスケットボール, 音楽', '大阪府', '金融', 'INFP', '慶應義塾大学', 'hobbies', '川口美穂です！読書とバスケットボールが趣味で、音楽を聴くことも楽しんでいます。金融分野で働き、将来的に多くの人と協力していきたいと思っています。'),
((SELECT id FROM users WHERE email = 'ishii.tetsuya@example.com'), '旅行, 音楽, ゲーム', '東京都', '法人', 'ISTJ', '名古屋大学', 'role', '石井哲也です！旅行や音楽が好きで、ゲームも楽しんでいます。法人分野でリーダーシップを発揮し、成長していきたいと思っています。');
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