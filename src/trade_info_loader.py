import requests
import pandas as pd
from utils import headers, FILE_PATH


r = requests.get("https://api.jpx-jquants.com/v1/markets/trades_spec", headers=headers)

columns_list = [
    'PublishedDate', 'StartDate', 'EndDate', 
    'Section', 'ProprietarySales', 'ProprietaryPurchases', 
    'ProprietaryTotal', 'ProprietaryBalance', 'BrokerageSales', 
    'BrokeragePurchases', 'BrokerageTotal', 'BrokerageBalance', 
    'TotalSales', 'TotalPurchases', 'TotalTotal', 
    'TotalBalance', 'IndividualsSales', 'IndividualsPurchases', 
    'IndividualsTotal', 'IndividualsBalance', 'ForeignersSales', 
    'ForeignersPurchases', 'ForeignersTotal', 'ForeignersBalance', 
    'SecuritiesCosSales', 'SecuritiesCosPurchases', 'SecuritiesCosTotal', 
    'SecuritiesCosBalance', 'InvestmentTrustsSales', 'InvestmentTrustsPurchases', 
    'InvestmentTrustsTotal', 'InvestmentTrustsBalance', 'BusinessCosSales', 
    'BusinessCosPurchases', 'BusinessCosTotal', 'BusinessCosBalance', 
    'OtherCosSales', 'OtherCosPurchases', 'OtherCosTotal', 
    'OtherCosBalance', 'InsuranceCosSales', 'InsuranceCosPurchases', 
    'InsuranceCosTotal', 'InsuranceCosBalance', 'CityBKsRegionalBKsEtcSales', 
    'CityBKsRegionalBKsEtcPurchases', 'CityBKsRegionalBKsEtcTotal', 'CityBKsRegionalBKsEtcBalance', 
    'TrustBanksSales', 'TrustBanksPurchases', 'TrustBanksTotal', 
    'TrustBanksBalance', 'OtherFinancialInstitutionsSales', 'OtherFinancialInstitutionsPurchases', 
    'OtherFinancialInstitutionsTotal', 'OtherFinancialInstitutionsBalance']
df = pd.DataFrame(columns=columns_list)

for i, item in enumerate(r.json()['trades_spec']):
    df.loc[i, :] = item

df.to_csv(f'{FILE_PATH}/trade_info/trades_spec.csv', index=False, encoding='utf-8-sig')