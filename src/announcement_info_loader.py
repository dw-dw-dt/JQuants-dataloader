from utils import FILE_PATH, MyMail, MyPassword
import jquantsapi


cli = jquantsapi.Client(mail_address=MyMail, password=MyPassword)
df = cli.get_fins_announcement()

df.to_csv(f'{FILE_PATH}/fin_announcement/fin_announcement.csv', index=False, encoding='utf-8-sig')