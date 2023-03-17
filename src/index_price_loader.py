from utils import FILE_PATH, MY_MAIL, MY_PASSWORD
import jquantsapi


cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
df = cli.get_indices_topix()

df.to_csv(f'{FILE_PATH}/index_price/topix.csv', index=False, encoding='utf-8-sig')