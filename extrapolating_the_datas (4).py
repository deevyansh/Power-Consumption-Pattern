# Importing the important libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Importing the documents
df1=pd.read_excel('/content/VAl1Sep22-1Sep23.xlsx')
df1=df1.drop_duplicates()
df2=pd.read_csv('/content/VAl20_21.csv')
df2=df2.drop_duplicates()

#Changing the columns and rows of the df2
df2[['Date','values','measurement']]=df2['Date;value;measurement'].str.split(';',expand=True)
df2=df2.drop(columns='Date;value;measurement')
df2[['date','time']]=df2['Date'].str.split(' ',expand=True)
df2=df2.drop(columns='Date')
df2[['dates','month','year']]=df2['date'].str.split('-',expand=True)
df2=df2.drop(columns='date')
df2[['hour','minutes']]=df2['time'].str.split(':',expand=True)
df2=df2.drop(columns='time')
df2['minutes'].value_counts()
df2=df2.drop(columns='minutes')
df2=df2.rename(columns={'dates':'date'})
df2=df2.drop(columns='measurement')
df2['year'] = df2['year'].astype(int)
df2['month'] = df2['month'].astype(int)
df2['date'] = df2['date'].astype(int)
df2['hour'] = df2['hour'].astype(int)

#changing the columns and rows of df1
df1['date']=df1['dt'].dt.day
df1['month']=df1['dt'].dt.month
df1['year']=df1['dt'].dt.year
df1['hour']=df1['dt'].dt.hour
df1=df1.drop(columns='dt')

# Checking the years , making it campatible
df1['year'].value_counts()
df2['year'].value_counts()
df2.drop(df2.head(23).index,inplace=True)
df2.drop(df2.tail(1).index,inplace=True)
df2=df2.reset_index()
df_2021=df2
df1=df1.sort_values(by=['month','date','hour'])
df_2023=df1[:(8735-2904)]
df_2022=df1[(8735-2904):]
df_2023=df_2023.reset_index(drop=True)

# ExtraPoalting the Graphs of 2022 using 2021 and 2023
import pandas as pd
new_rows = []
# Iterate through rows of df1_2023 and df2 simultaneously
for i, (index,row1) in enumerate(df_2023.iterrows()):
    row2 = df_2021.iloc[i]
    new_row_data = {'date': row1['date'],'year': 2022,'month': row1['month'],'hour': row1['hour'],'values': (float(row1['values']) + float(row2['values'])) / 2}
    new_rows.append(new_row_data)
df_2022 = df_2022.append(new_rows, ignore_index=True)
df_2022['year'] = df_2022['year'].astype(int)
df_2022['month'] = df_2022['month'].astype(int)
df_2022['date'] = df_2022['date'].astype(int)
df_2022['hour'] = df_2022['hour'].astype(int)

# Including the 3 remaining Days
df_2022['month'].value_counts()
df_2022['month'].value_counts()
value_counts_by_month_date = df_2022.groupby(['month', 'date']).size()
value_counts_by_month_date_df = value_counts_by_month_date.reset_index(name='counts')
value_counts_by_month_date_df['counts'].value_counts()
# Missing datas
october_31_data = df_2022[(df_2022['month'] == 10) & (df_2022['date'] == 31)]
october_31_data['date'] = 30
october_31_data['month'] = 10
march_26_data=df_2022[(df_2022['month']==3) & (df_2022['date']==25) & (df_2022['hour']==23)]
march_26_data['date'] = 26
#Appending the datas
df_2022 = df_2022.append(october_31_data, ignore_index=True)
df_2022 = df_2022.append(march_26_data, ignore_index=True)
df_2022.sort_values(by=['month','date','hour'], inplace=True)
df_2022=df_2022.reset_index(drop=True)

# Extrapolating the graph of 2023 using the 2022 and 2021
rows_data=[]
for i in range (5832,8760):
  new_row_data={'date': df_2022.iloc[i]['date'],'year': 2023,'month': df_2022.iloc[i]['month'], 'hour':df_2022.iloc[i]['hour'], 'values': (float(2*(df_2022.iloc[i]['values']))-float(df_2021.iloc[i]['values']))}
  rows_data.append(new_row_data)
df_2023=df_2023.append(rows_data,ignore_index=True);
df_2023.sort_values(by=['month','date','hour'], inplace=True)
df_2023=df_2023.reset_index(drop=True)
"""# Missing the days of the year 2023"""
march_26_data=df_2022[(df_2022['month']==3) & (df_2022['date']==25) & (df_2022['hour']==23)]
march_26_data['date'] = 26
march_26_data['year']=23
df_2023 = df_2023.append(march_26_data, ignore_index=True)
df_2023.sort_values(by=['month','date','hour'], inplace=True)
df_2023=df_2023.reset_index(drop=True)

#Extrapolating the 2020,2019,2018 using 2021,2022,2023
# Create empty DataFrames for years 2020, 2019, and 2018
df_2020 = pd.DataFrame()
df_2019 = pd.DataFrame()
df_2018 = pd.DataFrame()
for i in range(0, 8760):
    # Calculate values for the respective years
    values_2020 = ((2 * float(df_2021.iloc[i]['values'])) - (float(df_2022.iloc[i]['values'])))
    values_2019 = ((2 * values_2020) - (float(df_2021.iloc[i]['values'])))
    values_2018 = ((3 * values_2020) - (2 * float(df_2021.iloc[i]['values'])))

    # Create new rows for each year and append them to the respective DataFrames
    new_row_2020 = {
        'values': values_2020,
        'date': df_2021.iloc[i]['date'],
        'month': df_2021.iloc[i]['month'],
        'year': 2020,
        'hour': df_2021.iloc[i]['hour']
    }
    new_row_2019 = {
        'values': values_2019,
        'date': df_2021.iloc[i]['date'],
        'month': df_2021.iloc[i]['month'],
        'year': 2019,
        'hour': df_2021.iloc[i]['hour']
    }
    new_row_2018 = {
        'values': values_2018,
        'date': df_2021.iloc[i]['date'],
        'month': df_2021.iloc[i]['month'],
        'year': 2018,
        'hour': df_2021.iloc[i]['hour']
    }
    df_2020 = pd.concat([df_2020, pd.DataFrame([new_row_2020])], ignore_index=True)
    df_2019 = pd.concat([df_2019, pd.DataFrame([new_row_2019])], ignore_index=True)
    df_2018 = pd.concat([df_2018, pd.DataFrame([new_row_2018])], ignore_index=True)
print("DataFrame for 2023:")
print(df_2023)
print("DataFrame for 2022:")
print(df_2022)
print("DataFrame for 2021:")
df_2021=df_2021.drop(columns='index')
print(df_2021)
print("DataFrame for 2020:")
print(df_2020)
print("\nDataFrame for 2019:")
print(df_2019)
print("\nDataFrame for 2018:")
print(df_2018)

import pandas as pd
mixed_df=pd.DataFrame()
mixed_df['date']=df_2023['date']
mixed_df['year']=df_2023['year']
mixed_df['month']=df_2023['month']
mixed_df['hour']=df_2023['hour']
mixed_df['values_2023']=df_2023['values'].astype(float).round(2)
mixed_df['values_2022']=df_2022['values'].astype(float).round(2)
mixed_df['values_2021']=df_2021['values'].astype(float).round(2)
mixed_df['values_2020']=df_2020['values'].astype(float).round(2)
mixed_df['values_2019']=df_2019['values'].astype(float).round(2)
mixed_df['values_2018']=df_2018['values'].astype(float).round(2)
mixed_df

"""#Random Graph Generator"""

import matplotlib.pyplot as plt
import random
i=random.randint(0, 8759)
y_values=[mixed_df['values_2018'].iloc[i],mixed_df['values_2019'].iloc[i],mixed_df['values_2020'].iloc[i],mixed_df['values_2021'].iloc[i],mixed_df['values_2022'].iloc[i],mixed_df['values_2023'].iloc[i]]
x_values=[2018,2019,2020,2021,2022,2023]
plt.plot(x_values,y_values)
plt.xlabel('year')
plt.ylabel('values')
plt.show()

"""# Importing the Producers Data(DK1)"""

# Changes so that i can run easliy on the second set
import pandas as pd
DK1_2018=pd.read_excel("/content/ElectricityBalanceNonvDK1_1_2018_30_12_2018.xlsx")
DK1_2019=pd.read_excel("/content/ElectricityBalanceNonv DK1_1_1_2019_30_12_2019.xlsx")
DK1_2020=pd.read_excel("/content/ElectricityBalanceNonv DK1_1_1_20_30_12_20.xlsx")
DK1_2021=pd.read_excel('/content/ElectricityBalanceNonv 1_1_21_30_12_21.xlsx')
DK1_2022=pd.read_excel("/content/ElectricityBalanceNonv DK1_1_1_22_30_12_22.xlsx")
DK1_2023=pd.read_excel("/content/ElectricityBalanceNonv DK1_1_1_23_30_12_23.xlsx")

"""# Changing the Datas(DK1)"""

def processed_dfs(start_year,end_year,df):
  start_date=pd.to_datetime(f'{start_year}-01-01')
  end_date=pd.to_datetime(f'{end_year}-01-01')
  complete_data_range=pd.date_range(start=start_date,end=end_date, freq='H')
  complete_df=pd.DataFrame({'HourUTC':complete_data_range})
  complete_df=complete_df.drop(complete_df.tail(1).index)
  df=pd.merge(complete_df,df,on='HourUTC',how='left')
  df.fillna(0,inplace=True)
  df['HourUTC'] = df['HourUTC'].astype(str)
  df[['dates', 'time']] = df['HourUTC'].str.split(' ', expand=True)
  df[['year','month','date']]=df['dates'].str.split('-',expand=True)
  df[['hour','minutes','seconds']]=df['time'].str.split(':',expand=True)
  df=df.drop(columns=['seconds','minutes','time','dates','HourUTC','PriceArea','HourDK'])
  return df

DK1_2018=processed_dfs(2018,2019,DK1_2018)
DK1_2019=processed_dfs(2019,2020,DK1_2019)
DK1_2020=processed_dfs(2020,2021,DK1_2020)
DK1_2021=processed_dfs(2021,2022,DK1_2021)
DK1_2022=processed_dfs(2022,2023,DK1_2022)
DK1_2023=processed_dfs(2023,2024,DK1_2023)
DK1_2020 = DK1_2020[(DK1_2020['month'] != '02') | (DK1_2020['date'] != '29')]
DK1_2020=DK1_2020.reset_index(drop=True)
print("DK1_2018")
print(DK1_2018)
print("DK1_2019")
print(DK1_2019)
print("DK1_2020")
print(DK1_2020)
print("DK1_2021")
print(DK1_2021)
print("DK1_2022")
print(DK1_2022)
print("DK1_2023")
print(DK1_2023)

"""# Generating the mixed df of the producers(DK1)"""

producer_mixed_df=pd.DataFrame()
producer_mixed_df['date']=DK1_2018['date']
producer_mixed_df['month']=DK1_2018['month']
producer_mixed_df['hour']=DK1_2018['hour']
producer_mixed_df['2018_values']=DK1_2018['TotalLoad'].astype(float).round(2)
producer_mixed_df['2019_values']=DK1_2019['TotalLoad'].astype(float).round(2)
producer_mixed_df['2020_values']=DK1_2020['TotalLoad'].astype(float).round(2)
producer_mixed_df['2021_values']=DK1_2021['TotalLoad'].astype(float).round(2)
producer_mixed_df['2022_values']=DK1_2022['TotalLoad'].astype(float).round(2)
producer_mixed_df['2023_values']=DK1_2023['TotalLoad'].astype(float).round(2)
producer_mixed_df

"""# Importing the Producers Datas(DK2)"""

DK2_2018=pd.read_excel("/content/ElectricityBalanceNonv DK2_1_1_201830_12_2018.xlsx")
DK2_2019=pd.read_excel("/content/ElectricityBalanceNonv DK2_1_1_2019_30_12_2019.xlsx")
DK2_2020=pd.read_excel("/content/ElectricityBalanceNonv Dk2_1_1_20_30_12_20.xlsx")
DK2_2021=pd.read_excel('/content/ElectricityBalanceNonv _DK2_1_1_21_30_12_21.xlsx')
DK2_2022=pd.read_excel("/content/ElectricityBalanceNonv DK1_1_1_22_30_12_22.xlsx")
DK2_2023=pd.read_excel("/content/ElectricityBalanceNonvDk2_1_1_23_30_12_23.xlsx")

"""# Changing the datas of Producers(DK2)"""

def processed_dfs(start_year,end_year,df):
  start_date=pd.to_datetime(f'{start_year}-01-01')
  end_date=pd.to_datetime(f'{end_year}-01-01')
  complete_data_range=pd.date_range(start=start_date,end=end_date, freq='H')
  complete_df=pd.DataFrame({'HourUTC':complete_data_range})
  complete_df=complete_df.drop(complete_df.tail(1).index)
  df=pd.merge(complete_df,df,on='HourUTC',how='left')
  df.fillna(0,inplace=True)
  df['HourUTC'] = df['HourUTC'].astype(str)
  df[['dates', 'time']] = df['HourUTC'].str.split(' ', expand=True)
  df[['year','month','date']]=df['dates'].str.split('-',expand=True)
  df[['hour','minutes','seconds']]=df['time'].str.split(':',expand=True)
  df=df.drop(columns=['seconds','minutes','time','dates','HourUTC','PriceArea','HourDK'])
  return df

DK2_2018=processed_dfs(2018,2019,DK2_2018)
DK2_2019=processed_dfs(2019,2020,DK2_2019)
DK2_2020=processed_dfs(2020,2021,DK2_2020)
DK2_2021=processed_dfs(2021,2022,DK2_2021)
DK2_2022=processed_dfs(2022,2023,DK2_2022)
DK2_2023=processed_dfs(2023,2024,DK2_2023)
DK2_2020 = DK2_2020[(DK2_2020['month'] != '02') | (DK2_2020['date'] != '29')]
DK2_2020=DK2_2020.reset_index(drop=True)
print("DK2_2018")
print(DK2_2018)
print("DK2_2019")
print(DK2_2019)
print("DK2_2020")
print(DK2_2020)
print("DK2_2021")
print(DK2_2021)
print("DK2_2022")
print(DK2_2022)
print("DK2_2023")
print(DK2_2023)

"""# Mixed df of the Producers(DK2)"""

producer_mixed_df2=pd.DataFrame()
producer_mixed_df2['date']=DK2_2018['date']
producer_mixed_df2['month']=DK2_2018['month']
producer_mixed_df2['hour']=DK2_2018['hour']
producer_mixed_df2['2018_values']=DK2_2018['TotalLoad'].astype(float).round(2)
producer_mixed_df2['2019_values']=DK2_2019['TotalLoad'].astype(float).round(2)
producer_mixed_df2['2020_values']=DK2_2020['TotalLoad'].astype(float).round(2)
producer_mixed_df2['2021_values']=DK2_2021['TotalLoad'].astype(float).round(2)
producer_mixed_df2['2022_values']=DK2_2022['TotalLoad'].astype(float).round(2)
producer_mixed_df2['2023_values']=DK2_2023['TotalLoad'].astype(float).round(2)
producer_mixed_df2

"""# Calculating the Covariance of the DK1"""

covariance_df = pd.DataFrame()

# Assuming df_2018, df_2019, df_2020, df_2021, df_2022, df_2023, dfDK_2018, dfDK_2019, dfDK_2020, dfDK_2021, dfDK_2022, dfDK_2023 are your DataFrames

# Convert every column to float
df_2018['values'] = df_2018['values'].astype(float)
df_2019['values'] = df_2019['values'].astype(float)
df_2020['values'] = df_2020['values'].astype(float)
df_2021['values'] = df_2021['values'].astype(float)
df_2022['values'] = df_2022['values'].astype(float)
df_2023['values'] = df_2023['values'].astype(float)

DK1_2018['TotalLoad'] = DK1_2018['TotalLoad'].astype(float)
DK1_2019['TotalLoad'] = DK1_2019['TotalLoad'].astype(float)
DK1_2020['TotalLoad'] = DK1_2020['TotalLoad'].astype(float)
DK1_2021['TotalLoad'] = DK1_2021['TotalLoad'].astype(float)
DK1_2022['TotalLoad'] = DK1_2022['TotalLoad'].astype(float)
DK1_2023['TotalLoad'] = DK1_2023['TotalLoad'].astype(float)

# Perform calculations
covariance_df['sum of the consumer'] = (df_2018['values'] + df_2019['values'] + df_2020['values'] + df_2021['values'] + df_2022['values'] + df_2023['values']).astype(float)
covariance_df['sum of the square of the consumers'] = ((df_2018['values']**2) + (df_2019['values']**2) + (df_2020['values']**2) + (df_2021['values']**2) + (df_2022['values']**2) + (df_2023['values']**2)).astype(float)
covariance_df['sum of the producers'] = (dfDK_2018['TotalLoad'] + dfDK_2019['TotalLoad'] + dfDK_2020['TotalLoad'] + dfDK_2021['TotalLoad'] + dfDK_2022['TotalLoad'] + dfDK_2023['TotalLoad']).astype(float)
covariance_df['sum of the square of the producers'] = ((dfDK_2018['TotalLoad']**2) + (dfDK_2019['TotalLoad']**2) + (dfDK_2020['TotalLoad']**2) + (dfDK_2021['TotalLoad']**2) + (dfDK_2022['TotalLoad']**2) + (dfDK_2023['TotalLoad']**2)).astype(float)
covariance_df['produce of the consumer and producer'] = ((dfDK_2018['TotalLoad'] * df_2018['values']) + (dfDK_2019['TotalLoad'] * df_2019['values']) + (dfDK_2020['TotalLoad'] * df_2020['values']) + (dfDK_2021['TotalLoad'] * df_2021['values']) + (dfDK_2022['TotalLoad'] * df_2022['values']) + (dfDK_2023['TotalLoad'] * df_2023['values'])).astype(float)
covariance_df['hour']=df_2018['hour']
covariance_df['day']=df_2018['date']
covariance_df['month']=df_2018['month']

covariance_df = covariance_df.iloc[:8734]
covariance_df

covariance_df['Numerator'] = (8734 * covariance_df['produce of the consumer and producer']) - (covariance_df['sum of the consumer'] * covariance_df['sum of the producers'])
covariance_df['Denominator'] = (((8734 * covariance_df['sum of the square of the consumers']) - (covariance_df['sum of the consumer']**2)) * ((8734 * covariance_df['sum of the square of the producers']) - (covariance_df['sum of the producers']**2)))
covariance_df['Final'] = covariance_df['Numerator'] / (covariance_df['Denominator']**(0.5))
covariance_df=covariance_df.drop(columns='Numerator')
covariance_df=covariance_df.drop(columns='Denominator')
covariance_df

"""# Plotting the Graph"""

covariance_mean_hour_df = covariance_df.groupby(['hour'])['Final'].mean()

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(covariance_mean_hour_df.index, covariance_mean_hour_df.values, marker='o', linestyle='-')
plt.xlabel('Hour')
plt.ylabel('Mean Final Value')
plt.title('Mean Final Value by Hour')
plt.grid(True)

# Show plot
plt.show()



