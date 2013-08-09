import sqlite3
import math
from pprint import pprint
import random
from security_data import SecurityData
from account_manager import AccountManager
from account_metrics import AccountMetrics

'''
This file sets up a new account for the following trading strategy:
Invest a fixed amount (e.g. 100) of fund into each security where eq>75, arm>90, and rv>50. Only hold those stocks.
At the end of each month, replace the stocks in the account by investing a fixed amount (e.g., 100) of fund into new stocks that have the above signals.
'''

if __name__=='__main__':
    con = sqlite3.connect('qse_test.db')
    security_data = SecurityData(con)
    account_manager = AccountManager(con)
    account_metrics = AccountMetrics(con)
    dates = security_data.get_dates()
    new_id=account_manager.new_account()
    #print new_id
    rows=[]

    def signal_selection(eq,arm,rv):
        if eq>75 and arm>90 and rv>50:
            return True
        else:
            return False

    for d in dates:
        signals = security_data.get_security_signals(d,
                                                 signal_selection)
        security_ids = [s[0] for s in signals]
        for id in security_ids:
            row=[new_id, id, 100, d]
            rows.append(row)
    account_manager.add_holdings(rows)
    account_manager.add_account(new_id,0,"Invest 100 each month into securities where eq>75, arm>90, and rv>50")
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

