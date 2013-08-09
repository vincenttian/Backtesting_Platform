import sqlite3
import math
from pprint import pprint

import random

'''
The class AccountManager contains functions to update information in the account and holding table in the database. 
It supports creation of accounts for new trading strategies.
Each entry in the account table represents a stock trading account implementing a trading strategy.
Each entry in the holding table represents a stock holding at a given time in an account.
'''

class AccountManager:
    def __init__(self,con):
        self.con=con
    def get_accounts(self):
        '''Return a list of accounts'''
        sql='select * from account'
        return [r for r in self.con.execute(sql)]

    def get_holdings(self, account_id, as_of_date):
        '''Return a list of (security, amount) in an account at a given date 

        acount_id: an integer representing an account id
        as_of_date: 'YYYY-MM-DD' text formatted date
        '''
        sql='select security_id,amount from holding where account_id=? AND as_of_date=?'
        return [r for r in self.con.execute(sql,(account_id,as_of_date))]

    def new_account(self):
        account_id=None
        accounts=self.get_accounts()
        ids=[r[0] for r in accounts]
        account_id=max(ids)+1
        return account_id        

    def add_stock(self, acct, date, security_id, amount):
        row=[acct, security_id, amount, date]
        sql='insert into holding(account_id,security_id,amount,as_of_date) values (?,?,?,?)'
        self.con.execute(sql,row)
        self.con.commit()  

    def delete_stock(self, acct, date, security_id):
        '''Remove a stock in the holding table for an account at a given date '''
        sql="DELETE FROM holding WHERE account_id=? AND security_id=? AND as_of_date=?"
        self.con.execute(sql,(acct,security_id,date))
        self.con.commit()    

    def add_stocks(self, acct, date, stock_rows):
        '''The stock_rows is a list of (security_id, amount) tuples '''
        sql='insert into holding(account_id,security_id,amount,as_of_date) values (?,?,?,?)'
        for stock in stock_rows:
            row=[acct, stock[0], stock[1], date]
            self.con.execute(sql,row)
        self.con.commit()    

    def add_holdings(self, holding_rows):
        '''The holding_rows is a list of (account_id, security_id, amount, date) tuples '''
        sql='insert into holding(account_id,security_id,amount,as_of_date) values (?,?,?,?)'
        self.con.executemany(sql,holding_rows)
        self.con.commit()    

    def add_account(self, account_id, rating, desc):
        sql='insert into account(account_id,rating,desc) values(?,?,?)'
        account_row=[account_id, rating, desc]
        self.con.execute(sql,account_row)
        self.con.commit()    

    ## This function needs further testing
    def update_rating(self, account_id, rating):
        sql='update account set rating=? where account_id=?'
        self.con.execute(sql,(rating,account_id))
        self.con.commit()

if __name__=='__main__':
    con = sqlite3.connect('qse_test.db')
    account_manager = AccountManager(con)
    accounts=account_manager.get_accounts()
    id=account_manager.new_account()
    holding_1=account_manager.get_holdings(1, "2008-01-31")
    #account_manager.add_stock(1,"2009-01-31",782,1)

    print "...The account Id of a newly created account will be..."
    print id

    print "...All accounts ..."
    pprint(accounts)
    print

    print "...Holding at one date..."
    pprint(holding_1)
    print 



