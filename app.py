# coding:utf-8
import json
from flask import Flask, jsonify, make_response, request, Response
from requests_oauthlib import OAuth1Session
from twitter import Twitter, OAuth
from janome.tokenizer import Tokenizer
import collections
import re
from collections import Counter, defaultdict
import collections
import sys
import japanese_plaintext
import core
import emoji
import collections as cl


CONSUMER_KEY =  'kbIE5ZLubgsSDL1T73SQXH63J'
CONSUMER_SECRET = 'fCO2y2zwcHXgceNNWkE2DLSgy9rf53pOKS7E36YAA5PAKIQkXU'
ACCESS_TOKEN = '2811495061-3vMWEm62DhMuY2blPMgE7tEO4zRd7jdA0Z55XiQ'
ACCESS_SECRET = '3XzJUVD0bAV2WCoLUgpFd2hyDHguvfxGCfbGF3YfUJeMZ'

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
url = "https://api.twitter.com/1.1/search/tweets.json"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

ignore_words = ['今日','日本','本日','💕\u3000','👋😆✨☀️','昨日','・・・','日本人','チョロ','u3000','～´∇｀ﾉ','日本国民','事無','毎日','一松','時間','中国','～♪','大事','今年','阪神','年月日', '本当','元気','可愛','松兄','仕事',
    '写真','本気出','\u3000日本人','韓国','最後','・・・今日','女性','年前','～今日','👋😃☀️','自分','明日','本日時','線開業周年','\u3000・',
 '一日','・・・・・','本日分','ˊᵕˋ','全文','カラ','大人','日本食','⁾⁾','👋😆✨☀️\u3000','\u3000思','トド','犯人',
 '女神チョロ','開業','食事券','本年','名様','沢山','気持','山本','日本酒','投稿','★今日','発生','今度','応援','反日','一体',
 '～～～','日本韓国','日本侵略','彼氏','日本語','男性','～毎日','〜♪','〜♪今日','日本以外','円分','小学生','日目','配信中','普通','女子','記事','♪昨日','😆💕✨今日','今日富山','無理','子供','動画','～´∇｀ﾉ今日','出会','人気','酒会',
 '当然','一昨日','十四松','富山','先生','本物','開催中','意味','毎日チャレンジ','美味','先生様','コメント','本文','是非','画像','阪神電車','様～🤗今日','最高','返信',
 '本機','今日付','誕生日','・・・僕','先日','今月分','・・・†','月日金～月日木',
 '国外国人','👋😆✨☀️\u3000昨日','悪松','年間生','誕生月位\u3000月\u3000♔位\u3000月位\u3000月位\u3000月位\u3000月位\u3000月位\u3000月位\u3000月位\u3000月位\u3000月位\u3000月位\u3000月相性一覧対',
 '・・・顔','🎶今日','💓🤗','一人称','子人','大人気','日本一星','無事','〜♪本来','一緒','決定','仕事終','貴方','人時間','一歩','今後','海外日本','最終日','米日','～´∇｀ﾉ気',
 '\u3000見','平成最後','実行中今','更新','全力','組長','来月','今日出勤','明後日','朝日','体調悪','生物','用事','人気高','´∀｀','俺達','年間','本格','平均','一日横','今日ムリ','仕事中',
 '～´∇｀ﾉ\u3000可愛','物事','花粉症','\u3000何','友達','姿日本国民','～～💓∀','記念','事実','配下民日本','日旅','制限',
 '山間部','店員','今回','国会','時元気','手前\u3000','毎日楽','極主夫道話','車出','今夜','本企画本当','人・付',
 '漫画','有名日本料理店','元気出','人達','～ビーエルトリプルサンド','ｷｬｯ','山行','～～💓´艸｀','夜中','♪主役','年寄','世界','恋愛','期間中毎日名様','野生','小学校',
 '💖誕生日','大音量','目線','火事','一理','シコメモ','仕方','´・ω・｀コークオン','最強','神様','出来','記念日','電気','久々','小生','漫画\u3000','二日目',
 '相変','部屋','日間連続','連中','ｼｴﾘｲｪｯｽｼｴﾘｲｪｯｽ','電話','⁾⁾大分元気','物理的','💖〃','Σ・∀・','正直者','今投','体育館','❤️🤗',
 '未来','生放送中','手伝','生中継','組当','昨日同様','愛車','中心','素敵','国連','仕上','同人誌','💕\u3000可愛','生産','今年初','～´∇｀ﾉ\u3000綾夏','👋😆✨☀️\u3000真依','作品','次郎',
 '日本人Ｎｏ給料', '息子','～♪深夜限定★派生ＢＬ松',
 '日本地図～マルコポーロ', '外出', '健康', '法学部生', '聖歌トド', '国民', '阪神電車乗車中', '笑笑', '毎日万名様', '恋人', '小学生男子', '車以外', '当時', '安定', '文字中', 'ｱｰｰｰｰｰｰｰｰｰｰｰ', '手術中', '開業周年', '様子', '理由', '平気','心配',
 '画面', '食欲', '昨日仕事休', '現実', '機材', '大会', '相談', '西武', '一部平野部', '今日彩矢', '暴力', '一見', '♪深夜限定★派生ＢＬ松', '新車', '💓\u3000凛子', '一度', '問題', '〜♪深夜限定★派生ＢＬ松', '遠距離恋愛', '名前', '距離感', '外食行', '充実', '機内','～凛子',
 '誕生日ロレックス', '神父カラ', '\u3000最終話', '視聴率日本', '線開業周年犯人', '後者', '一歩踏', '和歌山来', '前者', 'ＢＬ松', '子達', '流行', '配信中只今', '総勢名様', '〜♪♪♪ハァハアオカズ', '発言', '実行', '一体何', '食中毒分', '深夜限定★派生ＢＬ松', '手間', '交通情報アナ', '💖中々会', '車高調', '乗車','犬様',
 '以前', '修悦体', '女子力高', '年間知', '出発', '来場', '二人', '行動', '和歌山', '生放送', '数時間', '食事券円分', '×台', '注意下', '下車', '何故', '年金', '用途', '国内有数', '精気', '今週', '今朝', '一人暮', '💖気','人・常識',
 '精神', '内田', '週間限定', '一切無', '公文', '頭痛', '面白', '～職場', '生制作', '彼女出来', 'ﾀﾞｧ', 'ヽ´∀｀ﾉ', '\u3000誰', '実際', '通勤', '🎶✨😆✨🎶','万人',
 '長女', '〜地元和歌山', '⁾⁾未成年', '我々', '今トド', '始動\u3000新線力', '乗客', '毎日挑戦', '～～💓´艸｀即保存', '強制使用料徴収日本', '子供用', '△深夜限定★派生ＢＬ松', '土曜日久々', '本抜', '写真出', 'フォロー', '選挙', '生息', '京急', '畜生', '悪用', '小見出', '♪美味', '花粉', '自信','不満',
 '口内炎', '丁度年前', '王様', '神父', '実施', '名乗', '悪徳人', '月一パンク', '富山市中央通', '実質無料', '有名', '愛情', '来場者数', '\u3000甘', '自転車', '校内', '和歌山市', '埼玉', '時期', '仮面ライダー', '年充電', '一言', '乗車中コメント', '♪僕', '全然', '攻達磨', '伊豆大島', '在庫本', '砂防', '育児中', '西洋人','時以外トド',
 '阪神乗', '子供達', '画像送', '記事完成後', '食中毒続出中キムチ', '西洋古版日本地図', '恋愛相性', '必要', '以上', '富山県内気象情報', '会計無料', '心理', '富山駅', '今後スマホ', '君元気', '有名漫画', 'ε´∀｀ﾎｯ', '時〜環水公園内', '長女小学校', '睡眠時間', '見当', '機長', '新生活応援', '警部犯人', '状態', '近鉄特急', '同級生','共産党',
 '公園', '街頭演説', '文字', '暴動事件', '文字以下', '相手', '一時預', '♪▽', '位俺', '元黒部市長', 'メディア', '作者', '解放', '車勝手', '長男', '学校', '❤︎', '政府', '単調減少日本語腐', '〜時頃食', 'ＧＯ\u3000電車・バス', '達成毎', '～笑顔', '様ｂ\u3000褒美', '有効活用出来', '黒部円',
 '来館', '体調良', '〜♪牛乳', '多分信', '加越能加賀・越中・能生買', '～ギシギシ', '氷見', '最近', '是非来', '時代', '反日メディア', '富富富', '導入', '受信料', '―中国メディア', '保護者会', '丁呂介', '鎧武外伝\u3000公式', '死神', '⁾⁾期待', '中止', '丸今回', '🥖今回', '予定通', '〜♪全然イイ', '車内表示',
 '開催', '映画', '中継信号', '俳人', '上手', '～💕😴', '一足先', '報道', '👋😃☀️頑張', '制作決定', '年素敵', '会話', '富山県美術館', '卒園式明日', '生乳使用牛乳', '人食器棚', '米子', '⁾⁾暇', '一刻', '集金日回ノイローゼ', 'ヾ◎´∀｀◎ﾉ', '通話', '優雅', '久保田悠来','黒部市',
 '頭気温', '今シーズン', '開催中🍖', '飛行機', '食器', '新酒', '下手', '貴様', '一件以来ルノー', '気圧', '♪ＢＬＴサンド', '大切', '勿体無', '名前挙', '～チキンタツタ', '～ブレーキローター', '活発', '車両', '同行', '店長', '野球部', '保育園', '自転車付', '〜♪モーニングセット', 'ツイート', '時半', '体勢', 'ティッシュ', '餓死寸前・最後', '限定パッケージ', '年―', '夢中', '信号無視', '公約者', '･ω･',
 '店来始', '来週', '最初', '恋愛相談乗', '人フォロバ', '廃人', '肉食', '試験中', '♪ギシギシ', '感謝', '正解', '解決', '駅前', '高貴', '♪力任', '建物沢山', '彼女', '何度', '無防備','線全駅','地酒横丁～','限界','理性失','平山郁夫画伯','和歌山サイクリングフェスタエイド','和歌山サイクリングフェスタ','時起','無自覚','妖精界','無限ループ','一途','一杯','予定','仕事疲','本音有給年間＾ω＾｀ｩ､ｩ､騙','過去',
 '関連性','有料道路使','有機水銀','⁾⁾ステッカー','百田尚樹氏外国人','時々忘','連投','迷子','俺様','知識','美久','国民アンケート','不正留学者',
 '政治家','無敵','全駅','授乳中','必要無','筋肉痛','性格受','黒部川','部屋化','暴動','真優','韓国ナチス','韓国傾','幼稚園土曜日','方法','体験','映画館','地酒','見直',
 '雰囲気出','★☆稽古場通信①☆★','想像以上','大変','一時停止','攻撃行動','開始','長野県','ヶ月','糖分','⸝元々明','二人暮','会計終','平和','無関係写真',
 '阪神西宮ｴﾋﾞｽﾀ西宮前','過去最高','〜条件〜・平均キル','機内アナウンス','個性','水発売','〜→','重度','素直','堕天','激怒','昼食後','人以上左翼','久保田悠来仮面ライダー','性格重視','病気',
 '寒気','五千円～','小沢一郎早','画像添付','有終','男女差','大千秋楽公演','会社','解説','多分','電話越','心理的','単体','初回放送','不正','回言','距離','受信料問題',
 '朝起','裏切','入店','堀内康男氏','一番好','一足早','情報解禁','否定',"頑張","スマホ", "男子", "フォロー"]

remove_words = ["〜", "ｗ", "・", "🥺", "♡", "☆", "♪", "笑", "※"]

userTweets = []


def get_userstweets(user_id, tweet_id):
    t = Twitter(auth=OAuth(
        ACCESS_TOKEN,
        ACCESS_SECRET,
        CONSUMER_KEY,
        CONSUMER_SECRET
    ))

    remain = True
    max_id = tweet_id
    remainNum = 0
    numberOfTweets = 100
    count = 50
    while remain:
        aTimeLine = t.statuses.user_timeline(user_id = user_id, count=count, max_id=max_id)
        for tweet in aTimeLine:
            userTweets.append(tweet['text'])
        max_id = aTimeLine[-1]['id']-1
        remainNum = numberOfTweets - len(userTweets)
        count = remainNum
        if len(userTweets)+1 > numberOfTweets:
            #print(userTweets)
            remain = False



@app.route('/')
def index():
    return 'Hello World!'

@app.route('/post', methods=['POST'])
def post_json():
    req_json = request.get_json()  # Get POST JSON
    key_word = req_json['key_word']

    params = {'q' : key_word, 'count' : 15}
    req = twitter.get(url, params = params)
    
    if req.status_code == 200:
        search_timeline = json.loads(req.text)
        for tweet in search_timeline['statuses']:
            user_id = tweet["user"]["id"]
            tweet_id = tweet["id"]
            get_userstweets(user_id,tweet_id)

    # 複合語をつくる
    texts = ','.join(userTweets)
    texts=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", texts)
    texts=re.sub('RT', "", texts)
    texts=re.sub('お気に入り', "", texts)
    texts=re.sub('まとめ', "", texts)
    texts=re.sub(r'[!-~]', "", texts)#半角記号,数字,英字
    texts=re.sub(r'[︰-＠]', "", texts)#全角記号
    texts=re.sub('\n', "", texts)#改行文字
    texts = ''.join(c for c in texts if c not in emoji.UNICODE_EMOJI) #絵文字の除去
    texts = ''.join(c for c in texts if c not in remove_words) #remove_wordsを除去

    # 複合語を抽出し、重要度を算出
    frequency = japanese_plaintext.cmp_noun_dict(texts)
    LR = core.score_lr(frequency,
            ignore_words=japanese_plaintext.IGNORE_WORDS,
            lr_mode=1, average_rate=0.1
        )
    term_imp = core.term_importance(frequency, LR)

    # 重要度が高い順に並べ替えて出力
    important_words = []
    important_score = []
    data_collection = collections.Counter(term_imp)
    for cmp_noun, value in data_collection.most_common():
        if value > 10000000:
            if core.modify_agglutinative_lang(cmp_noun) in ignore_words:
                continue
            else:
                important_words.append(core.modify_agglutinative_lang(cmp_noun))
                important_score.append(value)
                
    #json形式化して出力
    # ys = cl.OrderedDict()
    ys = {}
    for i in range(500):
        #data = cl.OrderedDict()
        data = {}
        data["ID"] = i
        data["importance"] = important_score[i]
        ys[important_words[i]] = data

    result_json = json.dumps(ys, ensure_ascii=False, indent=4)
    return result_json


if __name__ == "__main__":
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
