from utils import FILE_PATH, MY_MAIL, MY_PASSWORD
import jquantsapi


def main():
    cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
    df = cli.get_markets_trades_spec()

    df.to_csv(f'{FILE_PATH}/trade_info/trades_spec.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
