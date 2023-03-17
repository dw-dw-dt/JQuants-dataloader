from utils import FILE_PATH, MY_MAIL, MY_PASSWORD
import jquantsapi
import click


@click.command()
@click.argument('from_yyyymmdd')
@click.argument('to_yyyymmdd')
def main(from_yyyymmdd, to_yyyymmdd):
    cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
    df = cli.get_price_range(
        start_dt=from_yyyymmdd, 
        end_dt=to_yyyymmdd
    ).reset_index(drop=True)
    

    df.tail(10000).to_csv(f'{FILE_PATH}/prices_daily_quotes/prices_daily_quotes_tail.csv', index=False, encoding='utf-8-sig')
    df.to_pickle(f'{FILE_PATH}/prices_daily_quotes/prices_daily_quotes.pkl')


if __name__ == '__main__':
    main()