import subprocess
import time
import pathlib
from tqdm import tqdm
import pandas as pd
import datetime as dt
import jpbizday
from utils import FILE_PATH, save_concated_listed_info


if __name__ == "__main__":
    """
    listed_infoのみrange指定のapiが無いため手動で取得します.
    listed_info_loader.pyを何度も実行しています
    """
    from_date = dt.datetime(2017,1,4)
    to_date = dt.datetime.now() - dt.timedelta(days=1)

    # script実行
    script = 'src/listed_info_loader.py'
    dates = pd.date_range(start=from_date, end=to_date, freq='D')
    existing_file_list = set([file.stem for file in pathlib.Path(f'{FILE_PATH}/listed_info/cache').iterdir()])

    for date in tqdm(dates):
        yyyymmdd = date.strftime('%Y%m%d')
        
        if yyyymmdd in existing_file_list:
            continue

        if jpbizday.is_bizday(date) and (date.month, date.day) != (12,31):
            pass
        else:
            continue

        _r = subprocess.run(['python', script, yyyymmdd])
        time.sleep(1)
    
    # 統合ファイルの作成
    save_concated_listed_info()