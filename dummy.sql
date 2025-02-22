-- ユーザー情報テーブルを作成
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    slack_id VARCHAR(50) UNIQUE NOT NULL,
    created_at DATE NOT NULL
);

-- ユーザー属性テーブルを作成
CREATE TABLE user_attributes (
    user_id INT PRIMARY KEY,
    hobbies TEXT NOT NULL,
    hometown VARCHAR(50) NOT NULL,
    field VARCHAR(10) CHECK (field IN ('公共', '法人', '金融', 'TC&S', '技統本')) NOT NULL,
    role VARCHAR(10) CHECK (role IN ('SE', '営業', 'コンサル', 'スタッフ')) NOT NULL,
    preferences VARCHAR(10) CHECK (preferences IN ('user_id', 'hobbies', 'hometown', 'field', 'role')) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 架空のユーザーデータを挿入
INSERT INTO users (name, email, slack_id, created_at) VALUES
('田中 太郎', 'tanaka.taro@example.com', 'U12345678', '2023-05-01'),
('佐藤 花子', 'sato.hanako@example.com', 'U87654321', '2023-05-02'),
('鈴木 一郎', 'suzuki.ichiro@example.com', 'U23456789', '2023-05-03'),
('高橋 次郎', 'takahashi.jiro@example.com', 'U34567890', '2023-05-04'),
('山本 三郎', 'yamamoto.saburo@example.com', 'U45678901', '2023-05-05'),
('中村 四郎', 'nakamura.shiro@example.com', 'U56789012', '2023-05-06'),
('小林 五子', 'kobayashi.goko@example.com', 'U67890123', '2023-05-07'),
('加藤 六太', 'kato.rokuta@example.com', 'U78901234', '2023-05-08'),
('伊藤 七美', 'ito.nanami@example.com', 'U89012345', '2023-05-09'),
('渡辺 八郎', 'watanabe.hachiro@example.com', 'U90123456', '2023-05-10'),
('松本 九兵衛', 'matsumoto.kyube@example.com', 'U01234567', '2023-05-11'),
('林 十一', 'hayashi.juichi@example.com', 'U11223344', '2023-05-12'),
('清水 京子', 'shimizu.kyoko@example.com', 'U22334455', '2023-05-13'),
('山田 一子', 'yamada.kazuko@example.com', 'U33445566', '2023-05-14'),
('藤田 光', 'fujita.hikaru@example.com', 'U44556677', '2023-05-15'),
('岡本 真', 'okamoto.makoto@example.com', 'U55667788', '2023-05-16'),
('島田 空', 'shimada.sora@example.com', 'U66778899', '2023-05-17'),
('原田 瞳', 'harada.hitomi@example.com', 'U77889900', '2023-05-18'),
('三浦 蓮', 'miura.ren@example.com', 'U88990011', '2023-05-19'),
('石井 風', 'ishii.kaze@example.com', 'U99001122', '2023-05-20');

-- ユーザー属性データを挿入
INSERT INTO user_attributes (user_id, hobbies, hometown, field, role, preferences) VALUES
(1, '読書, 旅行, 映画鑑賞', '東京都', '公共', 'SE', 'hometown'),
(2, '料理, ヨガ, 写真', '大阪府', '法人', '営業', 'field'),
(3, '登山, スポーツ, 音楽', '愛知県', '金融', 'コンサル', 'role'),
(4, 'ゲーム, プログラミング, カフェ巡り', '福岡県', 'TC&S', 'SE', 'user_id'),
(5, '映画, 読書, アウトドア', '北海道', '技統本', 'スタッフ', 'hobbies'),
(6, 'ドライブ, 旅行, 温泉巡り', '京都府', '公共', '営業', 'role'),
(7, 'ハイキング, スポーツ観戦, 料理', '兵庫県', '法人', 'コンサル', 'hometown'),
(8, 'DIY, 読書, 筋トレ', '広島県', '金融', 'スタッフ', 'field'),
(9, 'アニメ, ゲーム, 映画', '宮城県', 'TC&S', 'SE', 'hobbies'),
(10, '写真, 旅行, サイクリング', '長野県', '技統本', '営業', 'user_id'),
(11, 'アウトドア, バイク, 料理', '新潟県', '公共', 'コンサル', 'role'),
(12, '映画, 音楽, 読書', '岡山県', '法人', 'スタッフ', 'hometown'),
(13, '釣り, スポーツ, 旅行', '茨城県', '金融', 'SE', 'field'),
(14, 'ヨガ, ガーデニング, カフェ巡り', '栃木県', 'TC&S', '営業', 'hobbies'),
(15, '筋トレ, 読書, 音楽鑑賞', '群馬県', '技統本', 'コンサル', 'user_id'),
(16, 'ジョギング, 料理, 登山', '静岡県', '公共', 'スタッフ', 'role'),
(17, '映画, ゲーム, プログラミング', '熊本県', '法人', 'SE', 'hometown'),
(18, '温泉巡り, 旅行, 写真', '山形県', '金融', '営業', 'field'),
(19, 'ランニング, ハイキング, 読書', '滋賀県', 'TC&S', 'コンサル', 'hobbies'),
(20, '音楽, ダンス, 料理', '奈良県', '技統本', 'スタッフ', 'user_id');
