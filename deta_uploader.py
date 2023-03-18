from deta import Deta
from src.utils import FILE_PATH, DETA_KEY


if __name__ == '__main__':
    """
    https://deta.space/docs/en/reference/cli CLIドキュメント
    """
    deta = Deta(DETA_KEY)
    
    # Upload files. If exists, it will be overwritten.
    drive = deta.Drive('JQuants_files')
    drive.put(name='trade_spec.csv', path = f'{FILE_PATH}/trade_info/trades_spec.csv')
    drive.put(name='prices_daily_quotes.pkl', path = f'{FILE_PATH}/prices_daily_quotes/prices_daily_quotes.pkl')
    drive.put(name='fin_announcement.csv', path = f'{FILE_PATH}/fin_announcement/fin_announcement.csv')
    drive.put(name='fin_statement.csv', path = f'{FILE_PATH}/fin_statement/fin_statement.csv')
    drive.put(name='topix.csv', path = f'{FILE_PATH}/index_price/topix.csv')
    drive.put(name='listed_info.pkl', path = f'{FILE_PATH}/listed_info/listed_info.pkl')
