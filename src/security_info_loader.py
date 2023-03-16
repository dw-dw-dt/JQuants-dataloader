import requests
import pandas as pd
from utils import headers, FILE_PATH


yyyymmdd = 20230316
r = requests.get(f"https://api.jpx-jquants.com/v1/listed/info?date={yyyymmdd}", headers=headers)

columns_list = [
    'Date', 'Code', 'CompanyName', 'Sector17Code', 
    'Sector17CodeName', 'Sector33Code', 'Sector33CodeName', 
    'ScaleCategory', 'MarketCode', 'MarketCodeName'
]
df = pd.DataFrame(columns=columns_list)

for i, item in enumerate(r.json()['info']):
    df.loc[i, :] = item

df.to_csv(f'{FILE_PATH}/security_info/{yyyymmdd}.csv', index=False, encoding='utf-8-sig')