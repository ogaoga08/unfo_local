# 目次
1. 概要
1. 使用技術
1. 機能一覧
1. デモンストレーション
1. 解説
    1. デザイン面
    1. コード面
1. 反省
1. 補足

# 概要
Githubリポジトリ : https://github.com/ogaoga08/unfo_local
大学2年生に授業で作成したWebアプリケーションです。(ローカル環境にて作成)
大学受験での経験から欲しかった、忘却曲線ベースの単語帳アプリを作成しました。
既存のアプリよりも視覚的見やすさ、多機能さを実装することを意識しました。
　(名前はunforgettableから。ロゴを考えるのが好きなので授業課題外でロゴタイプも作成しました)
![ポートフォリオ_小笠原慎_ページ_1.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3774078/ee319386-8428-96b8-d1c8-4914f50a23b4.jpeg)

>後述しますが、このアプリケーションは授業開始時に配布された簡単なブログアプリの雛形から作成したものです。インフラ部分は全て配布されたものです。

# 使用技術
<p>
  <img src="https://img.shields.io/badge/-Html5-444444.svg?logo=html5&style=popout-square" height="40">
  <img src="https://img.shields.io/badge/-Css3-1572B6.svg?logo=css3&style=popout-square" height="40">
  <img src="https://img.shields.io/badge/-Bootstrap-563D7C.svg?logo=bootstrap&style=popout-square" height="40">
  <img src="https://img.shields.io/badge/-Javascript-ffffff.svg?logo=javascript&style=popout-square" height="40">
  <img src="https://img.shields.io/badge/-FastAPI-ffffff.svg?logo=fastapi&style=popout-square" height="40">
  <img src="https://img.shields.io/badge/-Docker-ffffff.svg?logo=docker&style=popout-square" height="40">
  <img src="https://img.shields.io/badge/-Mysql-ffa500.svg?logo=mysql&style=popout-square" height="40">
</p>

# 機能一覧
- ユーザー登録、ログイン機能(授業にて雛形配布)
- ヘッダー、ナビゲーションバー、その他UIデザイン(Bootstrap)
- ホーム画面
  - 単語カードのOK,NG機能
  - 単語カードのフリップ機能(JavaScript)
  - クイズカードの正解判定(JavaScript)
  - タグ検索機能(MySQL)
- カード登録画面
  - クイズの選択肢数選択(JavaScript)

# デモンストレーション
https://www.youtube.com/embed/OmOXHVjJsmA?si=cEO3qqwZjzOL-p93

# 解説
### デザイン面
既存のアプリケーションよりも視覚的に見やすくするため、ライトモードの背景にした。また基本的にアプリ操作部分に緑、カード(単語帳)部分に赤を描画することで操作タスクを視覚的にわかりやすく工夫した。
そしてカード下部には進捗を表すプログレスバーを設置することによりあと何回で学習が終了するのかを視覚的にわかりやすく設計した。

<img width="309" alt="unfo_ホーム画面" src="https://github.com/ogaoga08/unfo_local/assets/131137413/c53b89a6-c4a7-45cf-8351-4f57acbec717">

### 　コード面
ログイン機能やディレクトリの構成は授業のTAさんが作成してくれたため、ある程度の雛形は用意されている状態(REST APIを利用した簡単なブログ投稿アプリ)から作成した。モデルとコントローラーをパイソンで書いているため、初心者でも作りやすかった。
FastAPIでのテンプレートエンジンの記法を理解することが難しく、エラーになることが多かったため、chatGPTにコードを投げて修正していった。

# 反省点
初めてということもあり非常に可読性が低いコードばかりになってしまった。
画面に表示する単語カードの条件を全て　SQL文で指定しているため、今ならもっとフロント側で処理できる気がする。
現在(2024/6/3)はReactで開発をしているので、コンポーネント化して再利用できる機能が多いと感じた。
今後モバイルアプリに移行する予定なので、そのときにリファクタリングしたいと思う。

# 補足
1年ほど前に作成したこのアプリについて、作成のプロセス・使用技術について思い出すため、またポートフォリオ作成の勉強のために書きました。
このアプリケーションはそもそもある程度の雛形が用意されたものであること、基礎的なコーディング方法を学んでいなかったため、とんでもなく可読性の低いコードであることなどツッコミどころが満載ですが一記録として見ていただけたら幸いです。

