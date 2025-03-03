import gensim
import numpy as np

# Word2Vecモデルの読み込み(https://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/)
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('./entity_vector.model.bin', binary=True)

# 確認する趣味の単語リスト
hobbies = [
    "サッカー", "バスケットボール", "野球", "ランニング", "旅行", "映画鑑賞", "アニメ", "漫画", "ゲーム", "カフェ", 
    "読書", "音楽", "カメラ", "キャンプ", "筋トレ", "料理", "プログラミング", "ボードゲーム", "ダンス", "登山", 
    "ランニング", "釣り", "DIY", "ガーデニング", "スポーツ観戦", "イラスト", "手芸", "ラーメン", "居酒屋", "ボランティア"
]

# 単語ベクトルを取得し、辞書に格納
vectors = {}
for word in hobbies:
    if word in word2vec_model:
        vectors[word] = word2vec_model[word]
    else:
        print(f'"{word}" はモデルに含まれていません。')

# ベクトルを圧縮保存
np.savez_compressed("hobby_vectors.npz", **vectors)