# 関連ツイート取得API（AI APIコンテストにて「AI NOW賞」受賞）

## APIの説明

Twitterのデータから、指定したフレーズ（ワード）を含むツイートをするユーザーは他にどのようなツイートをしやすいか、（tf-idfとtermextractを用いた）重要度の強い順に500件json形式でレスポンスをするAPIになります。

[RakutenRapidAPI](https://api.rakuten.net/seven0525/api/related-tweet-words-api)にて公開済みですので、自由にお使いください。
  

#### アプリイメージ(ターミナルから直接実行する法法)

<img src="images/result_1.png" width=50%>
   
<img src="images/result_2.png" width=50%>

   

## 技術
- TwitterAPIを使って、該当ユーザー15人のツイートをそれぞれ100ツイートずつ直前のツイートを取得しています。  
- 取得したツイートを機械学習（[termextract](http://gensen.dl.itc.u-tokyo.ac.jp/pytermextract/)）によってその該当ユーザー特有のツイート傾向を評価値とともに算出しました。  
- 結果はFlaskとHerokuを使ってjson形式で返しています。
   

## 用途 
- SNSマーケティング  
- 広告（”転職したい”とツイートするであろう特定のユーザーに対してターゲティング広告を出すなど）   
- 医療（”病気になった”とツイートするであろう特定のユーザーに対して事前に処方を行う）  
- スクレイピング（特定のクラスタのツイッターユーザーを見つけることが容易になる）  
- リサーチ（単語同士の類似度を調べることはすでにできるが、フレーズ単位でできるようになる）  
  
   
## 使用方法 ターミナルから以下のように実行することもできます。
[RakutenRapidAPI](https://api.rakuten.net/seven0525/api/related-tweet-words-api)にて公開済みですので、自由にお使いください。


```
curl -X POST -H "Content-Type: application/json" -d '{"key_word":"転職したい"}' https://related-tweet-words-api.herokuapp.com/post
```

ローカルにクローンして実行する場合は、自身のTwitterAPIのTokenに値を書き換えてください。

## AI APIコンテストにて「AI NOW賞」を受賞させていただきました！（4/7更新）
記事にもなるそうなので、記事完成し次第追記します。

**Copyright © Taichi Watanabe. All Rights Reserved.**
