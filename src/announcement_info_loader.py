import requests
import pandas as pd
from utils import headers, FILE_PATH


r = requests.get("https://api.jpx-jquants.com/v1/fins/announcement", headers=headers)

columns_list = ['Code', 'Date', 'CompanyName', 'FiscalYear', 'SectorName', 'FiscalQuarter', 'Section']
df = pd.DataFrame(columns=columns_list)

for i, item in enumerate(r.json()['announcement']):
    df.loc[i, :] = item

df.to_csv(f'{FILE_PATH}/announcement_info/announcement.csv', index=False, encoding='utf-8-sig')