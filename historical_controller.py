import subprocess
import time
import pathlib
from tqdm import tqdm
import pandas as pd
import datetime as dt
import jpbizday
from src.utils import FILE_PATH, create_dir


if __name__ == "__main__":
    """
    listed_infoのみrange指定のapiが無いため手動で取得します.
    """
    from_date = dt.datetime(2017,1,4)
    to_date = dt.datetime.now() - dt.timedelta(days=1)

    # ディレクトリ作成
    create_dir()

    # script実行
    script = 'src/listed_info_loader.py'
    dates = pd.date_range(start=from_date, end=to_date, freq='D')

    for date in tqdm(dates):
        if jpbizday.is_bizday(date) and (date.month, date.day) != (12,31):
            pass
        else:
            continue

        yyyymmdd = date.strftime('%Y%m%d')
        file = pathlib.Path(f'{FILE_PATH}/listed_info/{yyyymmdd}.csv')

        if file.exists():
            continue
        else:
            pass

        _r = subprocess.run(['python', script, yyyymmdd])
        time.sleep(1)
