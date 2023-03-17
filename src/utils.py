import requests
import json
import time
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