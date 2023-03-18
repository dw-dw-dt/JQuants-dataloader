import requests
import json
import time
import pathlib
from contextlib import contextmanager


REFRESH_TOKEN = json.load(open('token.json', 'r'))['jquants']
MY_MAIL = json.load(open('token.json', 'r'))['mail']
MY_PASSWORD = json.load(open('token.json', 'r'))['password']
ID_TOKEN = requests.post(f"https://api.jpx-jquants.com/v1/token/auth_refresh?refreshtoken={REFRESH_TOKEN}").json()['idToken']
headers = {f'Authorization': 'Bearer {}'.format(ID_TOKEN)}
FILE_PATH = '/mnt/d/JQuants-loader-files'


@contextmanager
def timer(name):
    t0 = time.time()
    print('[{}] start'.format(name))
    yield
    print('[{}] done in {} s'.format(name,time.time()-t0))


def create_dir():
    for dir in ['listed_info', 'trade_info', 'index_price', 'fin_announcement', 'prices_daily_quotes', 'fin_statement/cache']:
        p = pathlib.Path(f'{FILE_PATH}/{dir}')
        p.mkdir(parents=True, exist_ok=True)