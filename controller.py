import subprocess
import time
import pathlib
from tqdm import tqdm
import pandas as pd
import datetime as dt
from src.utils import FILE_PATH


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

    for script in ['src/trade_info_loader.py', 'src/index_price_loader.py', 'src/fin_announcement_loader.py', 
                   'src/equity_price_loader.py', 'src/listed_info_loader.py']:
        res = subprocess.run(['python', script, yyyymmdd])
        print(script)
        time.sleep(1)

    load_financial_statement(yyyymmdd, overwrite=False)
