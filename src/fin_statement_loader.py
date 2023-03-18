from utils import FILE_PATH, MY_MAIL, MY_PASSWORD
import jquantsapi


def main():
    cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
    df = cli.get_statements_range(cache_dir=f'{FILE_PATH}/fin_statement/cache').reset_index(drop=True)

    df.to_csv(f'{FILE_PATH}/fin_statement/fin_statement.csv', index=False, encoding='utf-8-sig')
    

if __name__ == '__main__':
    main()
