import sqlite3
import math
from pprint import pprint
import random
from security_data import SecurityData
from account_manager import AccountManager
from account_metrics import AccountMetrics
 
'''
This file sets up a new account for the following trading strategy:
Invest a fixed amount (e.g. 100) of fund into 500 randomly chosen securities.
 
At the end of each month, replace the entire holdings in the account by investing the fixed 
amount of fund to a new set of 500 randomly selected stocks.
 
'''
 
if __name__=='__main__':
    con = sqlite3.connect('qse_test.db')
    security_data = SecurityData(con)
    account_manager = AccountManager(con)
    account_metrics = AccountMetrics(con)
    dates = security_data.get_dates()
    stock_ids=security_data.get_security()
    
    if len(stock_ids)<=500:
        print "There are insufficient number of securities in the database for this trading strategy."
        exit(1)
 
    new_id=account_manager.new_account()
    #print new_id
 
    rows=[]
 
    for d in dates:
        my_ids=random.sample(stock_ids, 500)
        for id in my_ids:
            row=[new_id, id, 100, d]
            rows.append(row)
    account_manager.add_holdings(rows)
    account_manager.add_account(new_id,0,"Invest 100 each month in 500 randomly chosen stocks")
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