import sqlite3
import math
from pprint import pprint

import random
 
from security_data import SecurityData
from account_manager import AccountManager
 
# Utility Functions
 
def mean(vals):
    nvals = len(vals)
    if nvals==0:
        return 0
    else:
        return sum(vals,0.0)/nvals
 
def variance(vals):
    vals_mean = mean(vals)
    return sum([pow(v-vals_mean,2) for v in vals])/(len(vals)-1)
 
def stdev(vals):
    return variance(vals)**(0.5)
 
# Your implementation goes here
 
# Computes the maximum drawdown
 
def mdd(vals):
    rslt=0
    peak=-99999
    dd=[ 0 for x in range(len(vals))]
 
    for i in range(len(vals)):
        if (vals[i] > peak):
            peak=vals[i]
        dd[i]=100.0*(peak-vals[i])/peak
        if (dd[i]>rslt):
            rslt=dd[i]
    return rslt
 
class AccountMetrics:
 
    def __init__(self,con):
        self.account_manager=AccountManager(con)
        self.security_data=SecurityData(con)

    def compare_vs_sharpe(self, acct1, acct2, acct2_vals): #acct1=S&P500 (unless comparing against S&P 500, where acct1=4% fixed rate); acct2=strategy
        acct1_returns = self.all_returns(acct1)
        acct2_returns = self.all_returns(acct2)
        acct1_total = sum(acct1_returns)
        acct2_total = sum(acct2_returns)
        stdev_val = stdev(acct2_vals)
        sharpe = (acct2_total - acct1_total) / stdev_val
        return sharpe
 
    def month_returns(self,account_id,as_of_date):
        my_stocks=self.account_manager.get_holdings(account_id,as_of_date)
        stock_ids=[ h[0] for h in my_stocks ]
        stock_returns=self.security_data.get_returns(stock_ids,as_of_date)
        my_value=0
        my_base=0
        for i in range(len(my_stocks)):
            if stock_returns[i] is not None:
                my_value=my_value+my_stocks[i][1]*(1+stock_returns[i])
            else:
                my_value=my_value+my_stocks[i][1]
            my_base=my_base+my_stocks[i][1]
        return (my_value - my_base)        
 
    def all_returns(self,account_id):
        dates=self.security_data.get_dates()
        annual=[]
        for d in dates:
            month=self.month_returns(account_id,d)
            annual.append(month)
        return annual

    def show_stats(self,vals):
        mean_val=mean(vals);
        variance_val=variance(vals)
        stdev_val=stdev(vals)
        mdd_val=mdd(vals)
        print("Average Return: %s" %mean_val)
        #print("The variance: %s" %variance_val)
        #print("The stdev: %s" %stdev_val)
        print("Maximum drawdown: %s" %mdd_val)
 
if __name__=='__main__':
    con = sqlite3.connect('qse_test.db')
    my_metrics=AccountMetrics(con)
    my_manager=AccountManager(con)
    acct = my_manager.get_accounts()
    security_data = SecurityData(con)

    for x in range(len(acct)):
        account=x+1
        rslt=my_metrics.all_returns(account)
        total=sum(rslt)
        up_months = 0
        down_months = 0
        # If you want sharpe ratio to compare S&P 500, create account to assume 4% growth rate and use acct_id as first argument
        sharpe_rat = my_metrics.compare_vs_sharpe(2, account, rslt)
        for result in rslt:
            if result > 0:
                up_months += 1
            else:
                down_months += 1
        print
        print("Account %s Monthly Returns:" %account)
        print rslt
        print("Cumulative Return: %s" %total)
        my_metrics.show_stats(rslt)
        print("No. Up Months: %s" %up_months)
        print("No. Down Months: %s" %down_months)
        print("Ex-Post Sharpe Ratio: %s" %sharpe_rat)

