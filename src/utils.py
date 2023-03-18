import json
import time
import pathlib
import jquantsapi
from contextlib import contextmanager


MY_MAIL = json.load(open('token.json', 'r'))['mail']
MY_PASSWORD = json.load(open('token.json', 'r'))['password']
DETA_KEY = json.load(open('token.json', 'r'))['deta']
FILE_PATH = '/mnt/d/JQuants-loader-files'


@contextmanager
def timer(name):
    t0 = time.time()
    print('[{}] start'.format(name))
    yield
    print('[{}] done in {} s'.format(name,time.time()-t0))


def create_dir():
    for dir in ['listed_info', 'trade_info', 'index_price', 'fin_announcement', 'prices_daily_quotes', 'fin_statement/cache']:
        p = pathlib.Path(f'{FILE_PATH}/{dir}')
        p.mkdir(parents=True, exist_ok=True)


def index_price_loader(cli: jquantsapi.Client):
    """
    2021年1月から足元までの指数データを取得することができます。
    取得可能な指数データはTOPIX（東証株価指数）のみとなります。
    """
    df = cli.get_indices_topix()
    df.to_csv(f'{FILE_PATH}/index_price/topix.csv', index=False, encoding='utf-8-sig')


def trade_info_loader(cli: jquantsapi.Client):
    """
    2017年1月から足元までの投資部門別売買状況（金額）のデータを取得することができます。
    配信データは下記のページで公表している内容と同一です。データの単位は千円です。
    https://www.jpx.co.jp/markets/statistics-equities/investor-type/index.html
    """
    df = cli.get_markets_trades_spec()
    df.to_csv(f'{FILE_PATH}/trade_info/trades_spec.csv', index=False, encoding='utf-8-sig')


def prices_daily_quotes_loader(cli: jquantsapi.Client):
    """
    2017年1月から足元までの株価データを取得することができます。
    株価は分割・併合を考慮した調整済み株価（小数点第２位四捨五入）と調整前の株価を取得することができます。
    """
    df = cli.get_price_range().reset_index(drop=True)
    df.tail(10000).to_csv(f'{FILE_PATH}/prices_daily_quotes/prices_daily_quotes_tail.csv', index=False, encoding='utf-8-sig')
    df.to_pickle(f'{FILE_PATH}/prices_daily_quotes/prices_daily_quotes.pkl')


def fin_announcement_loader(cli: jquantsapi.Client):
    """
    下記のサイトで、3月期・9月期決算会社分に更新があった場合のみ19時ごろに更新されます。
    https://www.jpx.co.jp/listing/event-schedules/financial-announcement/index.html
    """
    df = cli.get_fins_announcement()
    df.to_csv(f'{FILE_PATH}/fin_announcement/fin_announcement.csv', index=False, encoding='utf-8-sig')


def fin_statement_loader(cli: jquantsapi.Client):
    """
    2017年1月以降のデータをもとに作成されております。
    """
    df = cli.get_statements_range(cache_dir=f'{FILE_PATH}/fin_statement/cache').reset_index(drop=True)
    df.to_csv(f'{FILE_PATH}/fin_statement/fin_statement.csv', index=False, encoding='utf-8-sig')
