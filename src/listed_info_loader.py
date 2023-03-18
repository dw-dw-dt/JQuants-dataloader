from utils import FILE_PATH, MY_MAIL, MY_PASSWORD
import jquantsapi
import click


@click.command()
@click.argument('yyyymmdd')
def main(yyyymmdd):
    cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
    df = cli.get_list(date_yyyymmdd=yyyymmdd)

    df.to_csv(f'{FILE_PATH}/listed_info/cache/{yyyymmdd}.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()