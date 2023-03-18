# JQuants APIを用いでデータ取得します
* 基本的には `poetry shell` で仮想環境に入った後は `python controller.py` を毎日実行するのみ.  
* 注意事項としては,初回実行時のみとても時間がかかる. これは,過去の上場情報の取得に時間がかかっているからである. 2回目以降は差分処理となるため時間は短縮される.  
* また,取得データをDeta（https://deta.space）というクラウドサービスに保存（バックアップ）する処理が `controller.py` の最終フェーズに存在するが, 利用しない場合はコメントアウトすればOK.

## requirement
* `token.json` をディレクトリに配置する必要がある. jsonファイルのキーは `jquants`, `mail`, `password`, `deta` の4つを想定している.  
`jquants`: JQuants API時のリフレッシュトークン. 無くてもOKだと思う.  
`mail` : JQuants API登録時のメールアドレス.  
`password` : JQuants API登録時のパスワード.  
`deta` : 無くてもOKだと思う. detaのアクセスキー.
* `src/utils.py` のFILE_PATHという変数は自分の作業環境に合わせて修正してください.