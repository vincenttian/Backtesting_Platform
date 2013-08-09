# A library for accessing security data

from pprint import pprint

import sqlite3

class SecurityData:
    '''Query the underlying db for data about securities'''
    
    def __init__(self,con):
        self.con = con

    def get_dates(self):
        '''Return a list of dates on which we have signal data'''
        sql = 'select distinct as_of_date from signal'
        return [r[0] for r in self.con.execute(sql)]

    def get_security(self):
        #Returns a lit of all security_ids in the securities table 
        sql = 'select distinct security_id from security'
        return [r[0] for r in self.con.execute(sql)]

    def get_returns(self,
                   security_ids,
                   as_of_date):
        '''Get a list of forward one month returns.

        security_ids: list of security_ids
        as_of_date: 'YYYY-MM-DD' text formatted date
        '''        
        result = []
        sql = 'select r.ret_1m from returns r where security_id=? and as_of_date=?'
        for s in security_ids:                
            r = self.con.execute(sql,(s,as_of_date)).fetchone()
            if r is None:
                result.append(r)
            else:
                result.append(r[0])
        return result

    def get_security_signals(self,as_of_date,criteria):
        '''Get a list of security_ids and their signals
        according to some criteria.
        
        as_of_date: 'YYYY-MM-DD' text formatted date
        criteria: arbitrary function that takes an argument for
         each signal and returns a boolean
        '''
        
        result = []
        sql = 'select security_id, eq, arm, rv from signal where as_of_date=?'
        for r in self.con.execute(sql,(as_of_date,)):
            if criteria(r[1],r[2],r[3]):
                result.append(r)
        return result

    def get_sp500(self,as_of_date):
        '''Return the security_ids of the sp500 on a given date.
        Note, sp500 may not have exactly 500 securities for a variety of reasons.'''
        sql = 'select security_id from sp500 where as_of_date=?'
        return [r[0] for r in self.con.execute(sql,(as_of_date,))]

    def get_company_info(self,security_ids,fields):
        '''Return a list of tuples, (ticker, name, gics_code, and gics_name),
        for each of security_ids.
        security_ids: list of security_ids
        fields: list of strings ['ticker', 'company_name', 'gics_code', 'gics_name']
        '''
        
        fieldmap = dict(ticker='s.ticker',
                        company_name='s.company_name',
                        gics_code='i.gics_code',
                        gics_name='g.gics_name')

        select = []
        for f in fields:
            assert f in set(['ticker', 'company_name', 'gics_code', 'gics_name'])
            select.append(fieldmap[f])   
        if len(fields)==1:
            select = select[0]
        else:
            select = ','.join(select)
        sql = '''
        select %s
        from security s
        left outer join security_industry i on
        s.security_id=i.security_id
        left outer join gics g
        on i.gics_code=g.gics_code
        where s.security_id=?
        ''' % select
        return [self.con.execute(sql,(s,)).fetchone() for s in security_ids]

if __name__=='__main__':
    con = sqlite3.connect('qse_test.db')
    security_data = SecurityData(con)
    def signal_selection(eq,arm,rv):
        if eq>90 and arm>85 and arm>rv and rv>70:
            return True
        else:
            return False
    dates = security_data.get_dates()
    adate = '2008-05-31'
    signals = security_data.get_security_signals(adate,
                                                 signal_selection)
    security_ids = [s[0] for s in signals]
    returns = security_data.get_returns(security_ids,
                                        adate)
    sp500_ids = security_data.get_sp500(adate)
    company_info = security_data.get_company_info(security_ids,
                                                  ['ticker', 'company_name', 'gics_name']) 

    get_industry = security_data.get_industry()   

    print '...dates...'
    pprint(dates)
    print
    
    
    print '...signals...'
    pprint(signals)
    print
    
    print '...returns...'
    pprint(returns)
    print

    print '...company_info...'
    pprint(company_info)
    print

    print '...get_industry...'
    pprint(get_industry)
    print
    
#     print '...sp500_ids...'
#     pprint(sp500_ids)
#     print

