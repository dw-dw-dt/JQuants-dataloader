import requests
import json
import time
import pathlib
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager


REFRESH_TOKEN = json.load(open('token.json', 'r'))['jquants']
MY_MAIL = json.load(open('token.json', 'r'))['mail']
MY_PASSWORD = json.load(open('token.json', 'r'))['password']
ID_TOKEN = requests.post(f"https://api.jpx-jquants.com/v1/token/auth_refresh?refreshtoken={REFRESH_TOKEN}").json()['idToken']
headers = {f'Authorization': 'Bearer {}'.format(ID_TOKEN)}
FILE_PATH = '/mnt/d/JQuants-loader-files'
DETA_KEY = json.load(open('token.json', 'r'))['deta']


@contextmanager
def timer(name):
    t0 = time.time()
    print('[{}] start'.format(name))
    yield
    print('[{}] done in {} s'.format(name,time.time()-t0))


def create_dir():
    for dir in ['listed_info/cache', 'trade_info', 'index_price', 'fin_announcement', 'prices_daily_quotes', 'fin_statement/cache']:
        p = pathlib.Path(f'{FILE_PATH}/{dir}')
        p.mkdir(parents=True, exist_ok=True)


def load_concated_listed_info():
    p = pathlib.Path(f'{FILE_PATH}/listed_info/cache')
    buff = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(pd.read_csv, file) for file in p.iterdir() if file.suffix == '.csv']
        for future in as_completed(futures):
            df = future.result()
            buff.append(df)
    return pd.concat(buff).sort_values(['Date', 'Code'])


def save_concated_listed_info():
    df = load_concated_listed_info().reset_index(drop=True)
    df.tail(10000).to_csv(f'{FILE_PATH}/listed_info/listed_info.csv', index=False, encoding='utf-8-sig')
    df.to_pickle(f'{FILE_PATH}/listed_info/listed_info.pkl')
        