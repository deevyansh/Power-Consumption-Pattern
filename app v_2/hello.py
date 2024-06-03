# Create a NOdata and VAdata
MODE='NO'

import pandas as pd
df1=pd.read_csv(f'data/Peak hour {MODE}_DK1.csv')
df2=pd.read_csv(f'data/Peak hour {MODE}_DK2.csv')
import pymysql
db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
cursor = db.cursor()
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {MODE}data(
    Month INT,
    Date INT,
    Hour INT,
    Covariance FLOAT,
    Value FLOAT
    )
""")

for i in range (0,len(df1)):
    input_query=f'INSERT INTO {MODE}data (Month,Date,Hour,Covariance,Value) VALUES(%s,%s,%s,%s,%s)'
    data=(int(df1.loc[i,'month']),int(df1.loc[i,'date']),int(df1.loc[i,'hour']),float(df1.loc[i,'covariance']),float(df1.loc[i,'value']))
    cursor.execute(input_query,data)
for i in range (0,len(df2)):
    month = int(df2.loc[i, 'month'])
    date = int(df2.loc[i, 'date'])
    hour = int(df2.loc[i, 'hour'])
    data = (month, date, hour)
    input_query1 = f'SELECT * FROM {MODE}data WHERE Month=%s AND Date=%s AND Hour=%s'
    cursor.execute(input_query1,data)
    l=cursor.fetchall()
    if(len(l)<=0):
        data = (int(df2.loc[i, 'month']), int(df2.loc[i, 'date']), int(df2.loc[i, 'hour']), float(df2.loc[i, 'covariance']),float(df2.loc[i, 'value']))
        input_query = f'INSERT INTO {MODE}data (Month,Date,Hour,Covariance,Value) VALUES(%s,%s,%s,%s,%s)'
        cursor.execute(input_query, data)

db.commit()
cursor.close()