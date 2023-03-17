import subprocess
import time
from tqdm import tqdm
import pandas as pd
import datetime as dt
from src.utils import FILE_PATH


if __name__ == "__main__":
    # 1-shot code 
    # for script in ['src/trade_info_loader.py', 'src/index_price_loader.py', 'src/fin_announcement_loader.py']:
    #     res = subprocess.Popen(['python', script])
    #     res.wait()

    # loop code 1
    from_date = dt.datetime(2017,1,4).strftime('%Y%m%d')
    to_date = dt.datetime.now().strftime('%Y%m%d')
    # TODO

    # loop code 2
    for script in ['src/fin_statement_loader.py']:
        listed_security_info = pd.read_csv(f'{FILE_PATH}/listed_info/20230316.csv')
        for security_code in tqdm(listed_security_info.query('Sector33Code!=9999')['Code']):
            try:
                res = subprocess.Popen(['python', script, str(security_code)])
                res.wait()
            except Exception as e:
                print(security_code, e)
            time.sleep(1)
