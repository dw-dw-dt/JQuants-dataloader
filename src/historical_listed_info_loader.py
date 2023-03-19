import pandas as pd
import datetime as dt
import jpbizday
import jquantsapi
import click
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import FILE_PATH, MY_MAIL, MY_PASSWORD


@click.command()
@click.argument('max_workers', type=int, default=5)
def main(max_workers):
    """
    listed_infoのみrange指定のapiが無いため手動で取得します.
    """
    cli = jquantsapi.Client(mail_address=MY_MAIL, password=MY_PASSWORD)

    from_date = dt.datetime(2017,1,4)
    to_date = dt.datetime.now() - dt.timedelta(days=1)
    dates = pd.date_range(start=from_date, end=to_date, freq='D')
    target_dates = [date.strftime('%Y%m%d') for date in dates 
                    if jpbizday.is_bizday(date) and (date.month, date.day) != (12,31)]

    buff = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(cli.get_listed_info, '', date) for date in target_dates]
        for future in as_completed(futures):
            buff.append(future.result())
    
    df = pd.concat(buff).sort_values(["Date", "Code"]).reset_index(drop=True)
    df.tail(10000).to_csv(f'{FILE_PATH}/listed_info_tail.csv', index=False, encoding='utf-8-sig')
    df.to_pickle(f'{FILE_PATH}/listed_info.pkl')


if __name__ == "__main__":
    main()
