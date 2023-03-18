# JQuants APIを用いでデータ取得します
* 基本的には `poetry shell` で仮想環境に入った後は `python controller.py` を毎日実行するのみ.   
* また,取得データをDeta（https://deta.space）というクラウドサービスに保存（バックアップ）する処理が `controller.py` の最終フェーズに存在するが, 利用しない場合はコメントアウトすればOK.

## requirement
* `token.json` をREADMEと同じディレクトリに配置する必要がある. jsonファイルのキーは `mail`, `password`, `deta` の4つを想定している.  
`mail` : JQuants API登録時のメールアドレス.  
`password` : JQuants API登録時のパスワード.  
`deta` : detaのアクセスキー. detaを利用しない場合は無くても問題なし.
* `src/utils.py` のFILE_PATHという変数は自分の作業環境に合わせて修正してください.