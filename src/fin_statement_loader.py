from utils import FILE_PATH, MyMail, MyPassword
import jquantsapi


code = 72030
cli = jquantsapi.Client(mail_address=MyMail, password=MyPassword)
df = cli.get_fins_statements(code=code)

df.to_csv(f'{FILE_PATH}/fin_statement/{code}.csv', index=False, encoding='utf-8-sig')