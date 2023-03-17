import subprocess
import time
import pathlib
from tqdm import tqdm
import pandas as pd
import datetime as dt
import jpbizday
from src.utils import FILE_PATH


def load_financial_statement(yyyymmdd, overwrite=False):
    p = pathlib.Path(f'{FILE_PATH}/fin_statement/{yyyymmdd}')
    if overwrite:
        pass
    else:
        if p.exists():
            print(f'{yyyymmdd} already exists')
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


if __name__ == "__main__":
    """
    jpbizdayは
    土日では無いこと
    祝日では無いこと
    1/1 ～ 1/3 では無いこと
    を基準にしているようです
    """
    from_date = dt.datetime(2017,1,4)
    to_date = dt.datetime.now() - dt.timedelta(days=1)
    target_date = from_date

    # ディレクトリ作成
    for dir in ['listed_info', 'trade_info', 'index_price', 'fin_announcement', 'prices_daily_quotes', 'fin_statement']:
        p = pathlib.Path(f'{FILE_PATH}/{dir}')
        p.mkdir(parents=True, exist_ok=True)

    # script実行
    while target_date <= to_date:
        if jpbizday.is_bizday(target_date) and (target_date.month, target_date.day) != (12,31):
            pass
        else:
            target_date += dt.timedelta(days=1)
            continue

        yyyymmdd = target_date.strftime('%Y%m%d')

        script = 'src/listed_info_loader.py'
        res = subprocess.run(['python', script, yyyymmdd])

        # load_financial_statement(yyyymmdd) # latestだけ取得すると上場廃止銘柄のデータが取れない

        target_date += dt.timedelta(days=1)
        print(target_date)
        time.sleep(1)
