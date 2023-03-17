import subprocess
import time
import pathlib
from tqdm import tqdm
import pandas as pd
import datetime as dt
import jpbizday
from src.utils import FILE_PATH, timer


def load_financial_statement(yyyymmdd, overwrite=False):
    p = pathlib.Path(f'{FILE_PATH}/fin_statement/{yyyymmdd}')
    if overwrite:
        pass
    else:
        if p.exists():
            print(f'src/fin_statement_loader.py: {yyyymmdd} already exists')
            return
    p.mkdir(parents=True, exist_ok=True)

    for script in ['src/fin_statement_loader.py']:
        listed_security_info = pd.read_csv(f'{FILE_PATH}/listed_info/{yyyymmdd}.csv')
        for security_code in tqdm(listed_security_info.query('Sector33Code!=9999')['Code']):
            try:
                res = subprocess.run(['python', script, str(yyyymmdd), str(security_code)])
            except Exception as e:
                print(security_code, e)
            time.sleep(1)
        print(script)


if __name__ == "__main__":
    """
    https://jpx.gitbook.io/j-quants-api/api-reference/data-spec API仕様書
    https://github.com/J-Quants/jquants-api-client-python APIクライアント仕様書
    当日の24時ごろ更新されるデータもあるので、毎日深夜に実行して前日分のデータを取得するのがよさそう
    """
    target_date = dt.datetime.now() - dt.timedelta(days=1)
    yyyymmdd = target_date.strftime('%Y%m%d')

    # 営業日でかつ12/31でないなら処理 （⇔ 土日、祝日、12/31,1/1～1/3はスキップ）
    if jpbizday.is_bizday(target_date) and (target_date.month, target_date.day) != (12,31):
        pass
    else:
        exit()

    # ディレクトリ作成
    for dir in ['listed_info', 'trade_info', 'index_price', 'fin_announcement', 'prices_daily_quotes', 'fin_statement']:
        p = pathlib.Path(f'{FILE_PATH}/{dir}')
        p.mkdir(parents=True, exist_ok=True)

    # script実行
    for script in ['src/trade_info_loader.py', 'src/index_price_loader.py', 'src/fin_announcement_loader.py']:
        with timer(script):
            res = subprocess.run(['python', script])
    
    for script in ['src/listed_info_loader.py']:
        with timer(script):
            res = subprocess.run(['python', script, yyyymmdd])
    
    # 2017-01-04以降の価格データを一括取得. adjpriceの都合上、毎日全データを更新
    script = 'src/prices_daily_quotes_loader.py'
    with timer(script):
        res = subprocess.run(['python', script, dt.datetime(2017,1,4).strftime('%Y%m%d'), yyyymmdd])

    #load_financial_statement(yyyymmdd, overwrite=False)
