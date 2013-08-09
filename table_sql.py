# Keep the table loading scripts here.
# (table_name, drop, create, index, table load)

# Directory where raw data files are located 
data_dir = 'raw_data'

sql_scripts = [

    ('account.txt',
     'drop table if exists account',
     'create table account(account_id int, rating int, desc text)',
     'create index account_i1 on account (account_id)',
     'insert into account(account_id,rating,desc) values (?,?,?)'
    ),

    ('holding.txt',
     'drop table if exists holding',
     'create table holding(account_id int, security_id int, amount real, as_of_date text)',
     'create index holding_i1 on holding (account_id)',
     'insert into holding(account_id,security_id,amount,as_of_date) values (?,?,?,?)'
    ),

    ('signal.txt',
     'drop table if exists signal',
     'create table signal(security_id int,as_of_date text,eq int,arm int,rv int )',
     'create index signal_i1 on signal (security_id,as_of_date)',
     'insert into signal(security_id,as_of_date,eq,arm,rv) values (?,?,?,?,?)'
    ),
    
    ('returns.txt',
     'drop table if exists returns',
     'create table returns(security_id int,as_of_date text,ret_1m real)',
     'create index returns_i1 on returns (security_id,as_of_date)',
     'insert into returns(security_id,as_of_date,ret_1m) values (?,?,?)'
     ),

    ('security.txt',
     'drop table if exists security',
     'create table security (security_id int,ticker text, company_name text)',
     'create index security_i1 on security (security_id)',
     'insert into security (security_id,ticker,company_name) values (?,?,?)'
     ),
    
    (
    'sp500.txt',
    'drop table if exists sp500',
    'create table sp500(as_of_date text, security_id int)',
    'create index sp500_i1 on sp500 (security_id,as_of_date)',
    'insert into sp500 (as_of_date,security_id) values (?,?)'    
    ),
    
    ('security_industry.txt',
     'drop table if exists security_industry',
     'create table security_industry (security_id int, gics_code text)',
     'create index security_industry_i1 on security_industry (security_id)',
     'insert into security_industry (security_id,gics_code) values (?,?)'
     ),

    ('gics.txt',
     'drop table if exists gics',
     'create table gics (gics_code text, gics_name text)',
     'create index gics_i1 on gics (gics_code)',
     'insert into gics (gics_code,gics_name) values (?,?)'
     )
    
    ]

