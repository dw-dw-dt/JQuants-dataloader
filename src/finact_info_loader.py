import requests
import pandas as pd
from utils import headers, FILE_PATH


code = 72030
r = requests.get(f"https://api.jpx-jquants.com/v1/fins/statements?code={code}", headers=headers)

columns_list = [
    'Profit', 'ForecastDividendPerShare1stQuarter', 'ForecastDividendPerShareFiscalYearEnd', 
    'NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock', 'ForecastDividendPerShareAnnual', 'ForecastNetSales', 
    'ChangesBasedOnRevisionsOfAccountingStandard', 'ResultDividendPerShareFiscalYearEnd', 'CurrentFiscalYearStartDate',
    'MaterialChangesInSubsidiaries', 'AverageNumberOfShares', 'OrdinaryProfit', 
    'ChangesInAccountingEstimates', 'DisclosedDate', 'ForecastDividendPerShare3rdQuarter', 
    'CurrentFiscalYearEndDate', 'CurrentPeriodEndDate', 'ForecastDividendPerShare2ndQuarter',
    'EquityToAssetRatio', 'TotalAssets', 'OperatingProfit', 
    'DisclosureNumber', 'ApplyingOfSpecificAccountingOfTheQuarterlyFinancialStatements', 'ForecastEarningsPerShare', 
    'NumberOfTreasuryStockAtTheEndOfFiscalYear', 'ResultDividendPerShare2ndQuarter', 'LocalCode', 
    'TypeOfDocument', 'ForecastOperatingProfit', 'ResultDividendPerShareAnnual', 
    'ForecastOrdinaryProfit', 'ForecastProfit', 'EarningsPerShare', 
    'DisclosedUnixTime', 'Equity', 'NetSales', 
    'ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard', 'ResultDividendPerShare3rdQuarter', 'BookValuePerShare', 
    'ResultDividendPerShare1stQuarter', 'TypeOfCurrentPeriod', 'DisclosedTime', 
    'RetrospectiveRestatement']
df = pd.DataFrame(columns=columns_list)

for i, item in enumerate(r.json()['statements']):
    df.loc[i, :] = item

df.to_csv(f'{FILE_PATH}/finact_info/{code}.csv', index=False, encoding='utf-8-sig')