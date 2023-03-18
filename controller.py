import subprocess
import datetime as dt
import jpbizday
from src.utils import timer, create_dir


if __name__ == "__main__":
    """
    https://jpx.gitbook.io/j-quants-api/api-reference/data-spec API仕様書
    https://github.com/J-Quants/jquants-api-client-python APIクライアント仕様書
    当日の24:30ごろ更新されるデータもあるので、毎日深夜に実行して前日分のデータを取得するのがよさそう
    * 銘柄情報（listed_info）:日次更新, 24:00
    * 業種情報:不変
    * 株価情報（prices_daily_quotes）:日次更新, 18:30
    * 指数情報（index_price）:日次更新, 21:00
    * 財務情報（fin_statement）:当日分の速報を18:30, 確定分を24:30
    * 投資部門別売買状況（trade_info）:毎週第4営業日, 18:00
    * 決算発表予定（fin_announcement）:https://www.jpx.co.jp/listing/event-schedules/financial-announcement/index.html に更新があった場合のみ, 19:00
    """
    previous_date = dt.datetime.now() - dt.timedelta(days=1)

    # 営業日でかつ12/31でないなら処理 （⇔ 土日、祝日、12/31,1/1～1/3はスキップ）
    if jpbizday.is_bizday(previous_date) and (previous_date.month, previous_date.day) != (12,31):
        pass
    else:
        exit()

    # ディレクトリ作成
    create_dir()

    # APIからデータを取得
    # historical_listed_info_loader 以外は全期間のデータを一括取得して,既存ファイルを上書きする
    # historical_listed_info_loader は2017-01-04以降のデータを差分取得(既存ファイルを破壊しない)する
    for script in ['src/trade_info_loader.py', 'src/index_price_loader.py', 
                   'src/fin_announcement_loader.py', 'src/prices_daily_quotes_loader.py', 
                   'src/fin_statement_loader.py', 'src/historical_listed_info_loader.py']: 
        with timer(script):
            result = subprocess.run(['python', script])
        if result.returncode != 0:
            raise ValueError(f'{script} failed')
    
    # detaにアップロード
    with timer('deta_uploader.py'):
        result = subprocess.run(['python', 'deta_uploader.py'])
    if result.returncode != 0:
        raise ValueError('deta_uploader.py failed')
