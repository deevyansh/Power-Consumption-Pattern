import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
df1=pd.read_csv('data/Peak hour NO_DK2.csv')
df2=pd.read_csv('data/Peak hour NO_DK1.csv')
fig,ax1=plt.subplots()

df1['month'] = df1['month'].astype(int)
df1['date'] = df1['date'].astype(int)
df1['hour'] = df1['hour'].astype(int)
df1['x-axis']=datetime(2000,10,10,0)
for i in range (len(df1)):
    df1.loc[i,'x_axis'] = datetime(2020,df1.loc[i,'month'] , df1.loc[i,'date'] , df1.loc[i,'hour'])
ax1.scatter(df1['x_axis'],df1['value'],label='DK1')
ax1.set_xlabel('month-date-hour')
ax1.set_ylabel('Quantity(KW)')
ax1.grid()


df2['month'] = df2['month'].astype(int)
df2['date'] = df2['date'].astype(int)
df2['hour'] = df2['hour'].astype(int)
df2['x-axis']=datetime(2020,1,1,1)
for i in range (len(df2)):
    df2.loc[i,'x-axis']=datetime(2020,df1.loc[i,'month'],df1.loc[i,'date'],df1.loc[i,'hour'])
ax1.scatter(df2['x-axis'],df2['value'],label='DK2')
ax1.grid()
ax1.legend()
ax1.set_title('NO with DK1 and DK2 -> Peak Hours with their quantity')

plt.xticks(rotation=90)
plt.show()
