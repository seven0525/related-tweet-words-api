# 関連ツイート取得API

## APIの説明

Twitterのデータから、指定したフレーズ（ワード）を含むツイートをするユーザーは他にどのようなツイートをしやすいか、（tf-idfとtermextractを用いた）重要度の強い順に500件json形式でレスポンスをするAPIになります。

[RakutenRapidAPI](https://api.rakuten.net/seven0525/api/related-tweet-words-api)にて公開済みですので、自由にお使いください。

#### アプリイメージ(ターミナルから直接実行する法法)
![](readme_images/flask-web1.png)

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

**Copyright © Taichi Watanabe. All Rights Reserved.**
