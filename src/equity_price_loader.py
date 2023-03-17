from utils import FILE_PATH, MY_MAIL, MY_PASSWORD
import jquantsapi


yyyymmdd = 20230316
cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
df = cli.get_prices_daily_quotes(date_yyyymmdd=yyyymmdd)

df.to_csv(f'{FILE_PATH}/equity_price/{yyyymmdd}.csv', index=False, encoding='utf-8-sig')