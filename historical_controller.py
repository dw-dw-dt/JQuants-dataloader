import subprocess
import time
import pathlib
from tqdm import tqdm
import pandas as pd
import datetime as dt
import jpbizday
from src.utils import FILE_PATH


if __name__ == "__main__":
    """
    listed_infoのみrange指定のapiが無いため手動で取得します.
    """
    from_date = dt.datetime(2017,1,4)
    to_date = dt.datetime.now() - dt.timedelta(days=1)

    # ディレクトリ作成
    for dir in ['listed_info', 'trade_info', 'index_price', 'fin_announcement', 'prices_daily_quotes', 'fin_statement/cache']:
        p = pathlib.Path(f'{FILE_PATH}/{dir}')
        p.mkdir(parents=True, exist_ok=True)

    dates = pd.date_range(start=from_date, end=to_date, freq='D')

    # script実行
    for date in tqdm(dates):
        if jpbizday.is_bizday(date) and (date.month, date.day) != (12,31):
            pass
        else:
            continue

        yyyymmdd = date.strftime('%Y%m%d')

        script = 'src/listed_info_loader.py'
        p = pathlib.Path(f'{FILE_PATH}/listed_info/{yyyymmdd}.csv')
        if p.exists():
            pass
        else:
            res = subprocess.run(['python', script, yyyymmdd])
            time.sleep(1)
