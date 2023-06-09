import json
import time
import pandas as pd
import numpy as np
import datetime as dt
import pathlib
import jquantsapi
from deta import Deta
from contextlib import contextmanager


MY_MAIL = json.load(open('token.json', 'r'))['mail']
MY_PASSWORD = json.load(open('token.json', 'r'))['password']
DETA_KEY = json.load(open('token.json', 'r'))['deta']
FILE_PATH = json.load(open('token.json', 'r'))['filepath']


@contextmanager
def timer(name):
    t0 = time.time()
    print('[{}] start'.format(name))
    yield
    print('[{}] done in {} s'.format(name,time.time()-t0))


def create_dir():
    if not pathlib.Path(f'{FILE_PATH}').exists():
        raise ValueError('Please set correct FILE_PATH in token.json')
    pathlib.Path(f'{FILE_PATH}/cache').mkdir(parents=True, exist_ok=True)


def save_df(df: pd.DataFrame, file_name: str):
    """
    受け取ったデータフレームをcsvとfeatherで保存する。
    """
    limit_row = 10000
    df = df.reset_index(drop=True)

    # csvで保存
    if len(df) > limit_row:
        df.tail(limit_row).to_csv(f'{FILE_PATH}/{file_name}_tail.csv', index=False, encoding='utf-8-sig')
    else:
        df.to_csv(f'{FILE_PATH}/{file_name}.csv', index=False, encoding='utf-8-sig')

    # featherで保存
    df.to_feather(f'{FILE_PATH}/{file_name}.feather')


def indices_topix_loader(cli: jquantsapi.Client):
    """
    2021年1月から足元までの指数データを取得することができます。
    取得可能な指数データはTOPIX(東証株価指数)のみとなります。
    """
    save_df(cli.get_indices_topix(), 'topix')


def trades_spec_loader(cli: jquantsapi.Client):
    """
    2017年1月から足元までの投資部門別売買状況(金額)のデータを取得することができます。
    配信データは下記のページで公表している内容と同一です。データの単位は千円です。
    https://www.jpx.co.jp/markets/statistics-equities/investor-type/index.html
    """
    save_df(cli.get_markets_trades_spec(), 'trades_spec')


def prices_daily_quotes_loader(cli: jquantsapi.Client):
    """
    2017年1月から足元までの株価データを取得することができます。
    株価は分割・併合を考慮した調整済み株価（小数点第２位四捨五入）と調整前の株価を取得することができます。
    """
    save_df(cli.get_price_range(), 'prices_daily_quotes')


def fin_announcement_loader(cli: jquantsapi.Client):
    """
    下記のサイトで、3月期・9月期決算会社分に更新があった場合のみ19時ごろに更新されます。
    https://www.jpx.co.jp/listing/event-schedules/financial-announcement/index.html
    """
    save_df(cli.get_fins_announcement(), 'fin_announcement')


def fin_statement_loader(cli: jquantsapi.Client):
    """
    2017年1月以降のデータをもとに作成されております。
    """
    df = cli.get_statements_range(cache_dir=f'{FILE_PATH}/cache')

    # cacheをcsv.gzで保存し,再読み込みした時に date -> str, str -> int になっている. cliの次のリリース(いつ?)で修正される予定.
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    # データ変換
    modify_cols = []
    for col in df.columns:
        if '－' in set(df[col]) or 'nan' in set(df[col]) or '' in set(df[col]):
            modify_cols.append(col)
    for col in modify_cols:
        df[col] = df[col].replace({'－': np.nan, 'nan': np.nan, '': np.nan})

    # 型変換
    columns_type = {
        "DisclosureNumber": int,
        "DisclosedDate": dt.datetime,
        "ApplyingOfSpecificAccountingOfTheQuarterlyFinancialStatements": bool,
        "AverageNumberOfShares": float,
        "BookValuePerShare": float,
        "ChangesBasedOnRevisionsOfAccountingStandard": bool,
        "ChangesInAccountingEstimates": bool,
        "ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard": bool,
        "CurrentFiscalYearEndDate": dt.datetime,
        "CurrentFiscalYearStartDate": dt.datetime,
        "CurrentPeriodEndDate": dt.datetime,
        "DisclosedTime": str,
        "DisclosedUnixTime": str,
        "EarningsPerShare": float,
        "Equity": float,
        "EquityToAssetRatio": float,
        "ForecastDividendPerShare1stQuarter": float,
        "ForecastDividendPerShare2ndQuarter": float,
        "ForecastDividendPerShare3rdQuarter": float,
        "ForecastDividendPerShareAnnual": float,
        "ForecastDividendPerShareFiscalYearEnd": float,
        "ForecastEarningsPerShare": float,
        "ForecastNetSales": float,
        "ForecastOperatingProfit": float,
        "ForecastOrdinaryProfit": float,
        "ForecastProfit": float,
        "LocalCode": str,
        "MaterialChangesInSubsidiaries": bool,
        "NetSales": float,
        "NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock": float,
        "NumberOfTreasuryStockAtTheEndOfFiscalYear": float,
        "OperatingProfit": float,
        "OrdinaryProfit": float,
        "Profit": float,
        "ResultDividendPerShare1stQuarter": float,
        "ResultDividendPerShare2ndQuarter": float,
        "ResultDividendPerShare3rdQuarter": float,
        "ResultDividendPerShareAnnual": float,
        "ResultDividendPerShareFiscalYearEnd": float,
        "RetrospectiveRestatement": bool,
        "TotalAssets": float,
        "TypeOfCurrentPeriod": str,
        "TypeOfDocument": str,
    }
    for col in df.columns:
        if columns_type[col] == dt.datetime:
            df[col] = pd.to_datetime(df[col].map(str), format='%Y-%m-%d')
        elif columns_type[col] == bool:  # boolはnp.nanがTrueになる
            df[col] = df[col].astype(str)
        elif columns_type[col] == int or columns_type[col] == float:
            df[col] = df[col].astype(columns_type[col])
    
    save_df(df, 'fin_statement')


def deta_upload():
    """
    https://deta.space/docs/en/reference/cli CLIドキュメント
    並列アップロードはうまくいかなかったので、一つずつアップロードする。
    """
    deta = Deta(DETA_KEY)
    
    # Upload files. If exists, it will be overwritten.
    drive = deta.Drive('JQuants_files')
    drive.put(name='trade_spec.feather', path = f'{FILE_PATH}/trades_spec.feather')
    drive.put(name='prices_daily_quotes.feather', path = f'{FILE_PATH}/prices_daily_quotes.feather')
    drive.put(name='fin_announcement.feather', path = f'{FILE_PATH}/fin_announcement.feather')
    drive.put(name='fin_statement.feather', path = f'{FILE_PATH}/fin_statement.feather')
    drive.put(name='topix.feather', path = f'{FILE_PATH}/topix.feather')
    drive.put(name='listed_info.feather', path = f'{FILE_PATH}/listed_info.feather')
