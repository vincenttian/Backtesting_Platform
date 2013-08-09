import sqlite3
import os

from table_sql import sql_scripts, data_dir

def load_data(con,filename, sql_drop, sql_create, sql_index, sql_insert):

    def parse_file(f):    
        fin = file(f)
        rows = []
        def map_null(s):
            if s == '\N' or s=='NULL' or s=='':
                return None
            else:
                return s
        for l in fin:
            row = [map_null(s) for s in l.strip().split('\t')]
            rows.append(row)
        return rows
    rows = parse_file(os.path.join(data_dir,filename))
    print 'Loading %s rows from %s ...' % (len(rows), filename)
    
    con.execute(sql_drop)
    con.execute(sql_create)
    con.execute(sql_index)
    con.execute('pragma synchronous=0')
    con.executemany(sql_insert,rows)
    con.commit()

if __name__=='__main__':
    con = sqlite3.connect("qse_test.db")
    for s in sql_scripts:
        load_data(con,*s)
    con.close()
