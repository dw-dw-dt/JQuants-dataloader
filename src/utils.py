import requests
import json


REFRESH_TOKEN = json.load(open('token.json', 'r'))['jquants']
MyMail = json.load(open('token.json', 'r'))['mail']
MyPassword = json.load(open('token.json', 'r'))['password']
ID_TOKEN = requests.post(f"https://api.jpx-jquants.com/v1/token/auth_refresh?refreshtoken={REFRESH_TOKEN}").json()['idToken']
headers = {f'Authorization': 'Bearer {}'.format(ID_TOKEN)}
FILE_PATH = '/mnt/d/JQuants-loader-files'