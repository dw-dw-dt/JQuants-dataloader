import subprocess
import os
import datetime as dt
import jpbizday
import jquantsapi
from src.utils import *


if __name__ == "__main__":
    """
    https://jpx.gitbook.io/j-quants-api/api-reference/data-spec API仕様書
    https://github.com/J-Quants/jquants-api-client-python APIクライアント仕様書
    当日の24:30ごろ更新されるデータもあるので、毎日深夜に実行して前日分のデータを取得するのがよさそう
    * 投資部門別売買状況（trade_info）:毎週第4営業日, 18:00
    * 株価情報（prices_daily_quotes）:日次更新, 18:30
    * 決算発表予定（fin_announcement）:更新があった場合のみ, 19:00
    * 指数情報（index_price）:日次更新, 21:00
    * 銘柄情報（listed_info）:日次更新, 24:00
    * 財務情報（fin_statement）:当日分の速報を18:30, 確定分を24:30
    """
    MAX_WORKERS = int(os.cpu_count()*0.8)
    target_date = dt.datetime.now() - dt.timedelta(days=1)

    # 営業日でかつ12/31でないなら処理 （⇔ 土日、祝日、12/31,1/1～1/3はスキップ）
    if jpbizday.is_bizday(target_date) and (target_date.month, target_date.day) != (12,31):
        pass
    else:
        print(f'{target_date} is not bizday. bye!')
        exit()

    # ディレクトリ作成
    create_dir()

    # APIからデータを取得
    cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
    cli.MAX_WORKERS = MAX_WORKERS
    for func in [trade_info_loader, prices_daily_quotes_loader, fin_announcement_loader, index_price_loader, fin_statement_loader]:
        with timer(func.__name__): func(cli)
    del cli
    
    script = 'src/historical_listed_info_loader.py'  # いい感じのAPIがなかったので自力実装. from_date = 2017-01-04がhard codingされているので注意.
    with timer(script):
        result = subprocess.run(['python', script, str(MAX_WORKERS)])
    if result.returncode != 0:
        raise ValueError(f'{script} failed')
    
    # detaにアップロード
    for func in [deta_upload]:
        with timer(func.__name__): func()
