from utils import FILE_PATH, MyMail, MyPassword
import jquantsapi


cli = jquantsapi.Client(mail_address=MyMail, password=MyPassword)
df = cli.get_markets_trades_spec()

df.to_csv(f'{FILE_PATH}/trade_info/trades_spec.csv', index=False, encoding='utf-8-sig')