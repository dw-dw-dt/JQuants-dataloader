from deta import Deta
from src.utils import FILE_PATH, DETA_KEY, timer


if __name__ == '__main__':
    """
    https://deta.space/docs/en/reference/cli CLIドキュメント
    """
    deta = Deta(DETA_KEY)
    
    # Upload a file. If exists, it will be overwritten.
    with timer('uploading trade_info'):
        drive = deta.Drive('trade_info')
        drive.put(name='trade_spec.csv', path = f'{FILE_PATH}/trade_info/trades_spec.csv')
    
    with timer('uploading prices_daily_quotes'):
        drive = deta.Drive('prices_daily_quotes')
        drive.put(name='prices_daily_quotes.pkl', path = f'{FILE_PATH}/prices_daily_quotes/prices_daily_quotes.pkl')
    
    with timer('uploading fin_announcement'):
        drive = deta.Drive('fin_announcement')
        drive.put(name='fin_announcement.csv', path = f'{FILE_PATH}/fin_announcement/fin_announcement.csv')
    
    with timer('uploading fin_statement'):
        drive = deta.Drive('fin_statement')
        drive.put(name='fin_statement.csv', path = f'{FILE_PATH}/fin_statement/fin_statement.csv')
    
    with timer('uploading index_price'):
        drive = deta.Drive('index_price')
        drive.put(name='topix.csv', path = f'{FILE_PATH}/index_price/topix.csv')
    
    with timer('uploading listed_info'):
        drive = deta.Drive('listed_info')
        drive.put(name='listed_info.csv', path = f'{FILE_PATH}/listed_info/listed_info.pkl')

