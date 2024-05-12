# Importing the Datas
from dash import Dash, html,dcc,Output,Input
import pandas as pd
import plotly.express as px
import numpy as np


# Adding all the DataFrames
app=Dash(__name__)
df=pd.read_csv('covariance_df_with_NO')
# Making all the figures

# Fig1
x_temp=['NaN','very strong negative','strong negative','moderate negative','weak negative','weak positive','moderate positive','strong positive','very strong positive']
y_temp=[(df['strength_with_DK2']=='Nan').sum(),
        (df['strength_with_DK2']=='very strong negative').sum(),
        (df['strength_with_DK2']=='strong negative').sum(),
        (df['strength_with_DK2']=='moderate negative').sum(),
        (df['strength_with_DK2']=='weak negative').sum(),
        (df['strength_with_DK2']=='weak positive').sum(),
        (df['strength_with_DK2']=='moderate positive').sum(),
        (df['strength_with_DK2']=='strong positive').sum(),
        (df['strength_with_DK2']=='very strong positive').sum()]
df1=pd.DataFrame(columns=['Bin','Covariance Values with DK2'])
for i in range (0,len(x_temp)):
    df1.loc[i,'Bin']=x_temp[i]
    df1.loc[i,'Covariance Values with DK2']=y_temp[i]
fig1=px.bar(df1,x='Bin',y='Covariance Values with DK2',title='Covariance values with DK2')

# Fig2
fig2=px.box(df,x='hour',y='covariance_value_with_DK2',title='Whole Year')

#Fig3
fig3=px.box(df[df['month']==1],x='hour',y='covariance_value_with_DK2',title='Month1')


# Fig4
x_temp=['NaN','very strong negative','strong negative','moderate negative','weak negative','weak positive','moderate positive','strong positive','very strong positive']
y_temp=[(df['strength_with_DK1']=='Nan').sum(),
        (df['strength_with_DK1']=='very strong negative').sum(),
        (df['strength_with_DK1']=='strong negative').sum(),
        (df['strength_with_DK1']=='moderate negative').sum(),
        (df['strength_with_DK1']=='weak negative').sum(),
        (df['strength_with_DK1']=='weak positive').sum(),
        (df['strength_with_DK1']=='moderate positive').sum(),
        (df['strength_with_DK1']=='strong positive').sum(),
        (df['strength_with_DK1']=='very strong positive').sum()]
df1=pd.DataFrame(columns=['Bin','Covariance Values with DK1'])
for i in range (0,len(x_temp)):
    df1.loc[i,'Bin']=x_temp[i]
    df1.loc[i,'Covariance Values with DK1']=y_temp[i]
fig4=px.bar(df1,x='Bin',y='Covariance Values with DK1',title='Covariance values with DK1')


# Fig5
fig5=px.box(df,x='hour',y='covariance_value_with_DK1',title='Whole Year')
# Fig6
fig6=px.box(df[df['month']==1],x='hour',y='covariance_value_with_DK1',title='Month1')


# Making the layout
app.layout=html.Div(children=[
    html.H1(children='NO Dataset'),
    html.Div(children=''' All the graphs are based on NO Dataset'''),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    # dcc.Graph(figure=fig3),
    dcc.RadioItems(
        id='1',
        options=[{'label':'Month1','value':1},
                 {'label':'Month2','value':2},
                 {'label':'Month3','value':3},
                 {'label':'Month4','value':4},
                 {'label':'Month5','value':5},
                 {'label':'Month6','value':6},
                 {'label':'Month7','value':7},
                 {'label':'Month8','value':8},
                 {'label':'Month9','value':9},
                 {'label':'Month10','value':10},
                 {'label':'Month11','value':11},
                 {'label':'Month12','value':12},
                 ],
        value=1,
        inline=True
    ),
    dcc.Graph(id="graph1"),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.RadioItems(
        id='2',
        options=[{'label':'Month1','value':1},
                 {'label':'Month2','value':2},
                 {'label':'Month3','value':3},
                 {'label':'Month4','value':4},
                 {'label':'Month5','value':5},
                 {'label':'Month6','value':6},
                 {'label':'Month7','value':7},
                 {'label':'Month8','value':8},
                 {'label':'Month9','value':9},
                 {'label':'Month10','value':10},
                 {'label':'Month11','value':11},
                 {'label':'Month12','value':12},
                 ],
        value=1,
        inline=True
    ),
    dcc.Graph(id="graph2")

])

# Running the app
if __name__ == '__main__':
    @app.callback(
        Output("graph1", "figure"),
        Output("graph2", "figure"),
        Input("1", "value"),
        Input("2", "value"))
    def generate_chart(temp1,temp2):
        df3=pd.read_csv('covariance_df_with_NO')
        print("here is the temp",temp1)
        df3=df3[df3['month']==temp1]
        fig1=px.box(df3, x='hour', y='covariance_value_with_DK2',title=f'Month{temp1}')

        df3 = pd.read_csv('covariance_df_with_NO')
        print("here is the temp", temp2)
        df3 = df3[df3['month'] == temp2]
        fig2 = px.box(df3, x='hour', y='covariance_value_with_DK1', title=f'Month{temp2}')

        return fig1,fig2


    app.run_server(debug=True)

