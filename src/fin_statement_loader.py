from utils import FILE_PATH, MY_MAIL, MY_PASSWORD
import jquantsapi
import click


@click.command()
@click.argument('yyyymmdd')
@click.argument('code')
def main(yyyymmdd, code):
    cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)
    df = cli.get_fins_statements(code=code)

    df.to_csv(f'{FILE_PATH}/fin_statement/{yyyymmdd}/{code}.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
