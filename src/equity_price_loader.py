import requests
import pandas as pd
from utils import headers, FILE_PATH


yyyymmdd = 20230316
r = requests.get(f"https://api.jpx-jquants.com/v1/prices/daily_quotes?date={yyyymmdd}", headers=headers)

columns_list = [
    'Close', 'Code', 'Date', 
    'AdjustmentHigh', 'Volume', 'TurnoverValue', 
    'AdjustmentClose', 'AdjustmentLow', 'Low', 
    'High', 'Open', 'AdjustmentOpen', 
    'AdjustmentFactor', 'AdjustmentVolume'
]
df = pd.DataFrame(columns=columns_list)

for i, item in enumerate(r.json()['daily_quotes']):
    df.loc[i, :] = item

df.to_csv(f'{FILE_PATH}/equity_price/{yyyymmdd}.csv', index=False, encoding='utf-8-sig')