import sqlite3
import math
from pprint import pprint
import random
from security_data import SecurityData
from account_manager import AccountManager
from account_metrics import AccountMetrics
 
'''
This file sets up a new account for the following trading strategy:
 
Invest a fixed amount (e.g. 100) of fund into each stock in an industry sector, such as 
Electronic Equipment & Instruments
 
If there are gains for a stock in a month, sell the gain portion to bring the investment in the stock 
back to the fixed amount for the next month.
 
If there are losses for a stock in a month, add fund for the loss portion to buy the stock to bring 
the investment to the stock back to the fixed amount for the next month.
'''
 
if __name__=='__main__':
 
    industry_name="Electronic Equipment & Instruments"
    industry_code="452030"
 
    con = sqlite3.connect('qse_test.db')
    security_data = SecurityData(con)
    account_manager = AccountManager(con)
    account_metrics = AccountMetrics(con)
    dates = security_data.get_dates()
    stock_ids=security_data.get_security()
 
    stock_info=security_data.get_company_info(stock_ids, ['ticker', 'company_name', 'gics_code', 'gics_name'])
 
    new_id=account_manager.new_account()
    #print new_id
    industry_ids=[]
    for i in range(len(stock_ids)):
        if stock_info[i][2]==industry_code:
            industry_ids.append(stock_ids[i])
    if len(industry_ids)<1:
        print("The database contains no stocks in the sector: %s" %industry_name)
 
    print "...The target stock ids..."
    pprint(industry_ids)
    print
    rows=[]
    for d in dates:
        for count in range(len(industry_ids)):
            row=[new_id, industry_ids[count], 100, d]
            rows.append(row)
    account_manager.add_holdings(rows)
    account_manager.add_account(new_id,0,"Invest 100 each month in the sector %s" %industry_name)
    all_acct=account_manager.get_accounts()
 
    print "... All Accounts ..."
    pprint(all_acct)
    print
 
    '''
    stocks_071231=account_manager.get_holdings(new_id,"2007-12-31")
    num=len(stocks_071231)
    print("The number of stocks in the account %s is %s on 2007-12-31" %(new_id,num))
    '''
 
    #### Show performance metrics for the new account ####
 
    rslt=account_metrics.all_returns(new_id)
    total=sum(rslt)
    up_months = 0
    down_months = 0
    for result in rslt:
            if result > 0:
                up_months += 1
            else:
                down_months += 1
    print("Account %s Monthly Returns: " %new_id)
    print rslt
    print("Cumulative Returns: %s" %total)
    account_metrics.show_stats(rslt)
    print("No. Up Months: %s" %up_months)
    print("No. Down Months: %s" %down_months)