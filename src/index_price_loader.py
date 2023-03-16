from utils import FILE_PATH, MyMail, MyPassword
import jquantsapi


cli = jquantsapi.Client(mail_address=MyMail, password=MyPassword)
df = cli.get_indices_topix()

df.to_csv(f'{FILE_PATH}/index_price/topix.csv', index=False, encoding='utf-8-sig')