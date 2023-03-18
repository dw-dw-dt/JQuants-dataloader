import subprocess
import pathlib
import datetime as dt
import jpbizday
from src.utils import FILE_PATH, timer


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
    target_date = dt.datetime.now() - dt.timedelta(days=1)
    yyyymmdd = target_date.strftime('%Y%m%d')

    # 営業日でかつ12/31でないなら処理 （⇔ 土日、祝日、12/31,1/1～1/3はスキップ）
    if jpbizday.is_bizday(target_date) and (target_date.month, target_date.day) != (12,31):
        pass
    else:
        exit()

    # ディレクトリ作成
    for dir in ['listed_info', 'trade_info', 'index_price', 'fin_announcement', 'prices_daily_quotes', 'fin_statement/cache']:
        p = pathlib.Path(f'{FILE_PATH}/{dir}')
        p.mkdir(parents=True, exist_ok=True)

    # script実行
    for script in ['src/trade_info_loader.py', 'src/index_price_loader.py', 'src/fin_announcement_loader.py',
                   'src/prices_daily_quotes_loader.py', 'src/fin_statement_loader.py']:
        with timer(script):
            res = subprocess.run(['python', script])
    
    for script in ['src/listed_info_loader.py']:
        with timer(script):
            res = subprocess.run(['python', script, yyyymmdd])
