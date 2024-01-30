from dash import html, dcc, Dash, dash_table
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar

from globals import *
from app import app


# from dash import Dash, dash_table
# import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# app = Dash(__name__)

# app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

# if __name__ == '__main__':
#     app.run(debug=True)

# df_teste = pd.read_csv(r'C:\Users\Weilon\Desktop\Python\Projetos\Gestão de Gastos (Criar)\df_despesas.csv')

# df_teste



layout = dbc.Col([
            dbc.Row([ # LINHA 1
                dbc.Col([
                    dbc.Card([
                        html.Legend('Total Gasto'),
                        html.H5('R$ -', id='total-gasto-card', style={}),
                    ])
                ],md=4),
                dbc.Col([
                    dbc.Card([
                        html.Legend('Devo Gastar'),
                        html.H5('R$ -', id='devo-gastar-card', style={})
                        ])
                ],md=4),
                dbc.Col([
                    dbc.Card([
                        html.Legend('Utilizado'),
                        html.H5('%', id='utilizado-card', style={})
                        ])
                ],md=4)
            ]),
            dbc.Row([ # LINHA 2
                dcc.DatePickerRange(
                            month_format='Do MMM YY',
                                end_date_placeholder_text='Data...',
                                start_date=(datetime.now().date() - timedelta(days=datetime.now().date().day-1)),
                                end_date=datetime.now().date(),
                                updatemode='singledate',
                                id='date-picker-config',
                                style={'z-index':'100',
                                       'padding':'5px'}
                        ) 
            ]),
            dbc.Row([ # LINHA 3
                dbc.Col([
                    dbc.Card([
                        
                        html.Legend('Resumo'),
                        dash_table.DataTable(
                            id='tbl-desp',
                            # columns=[
                            #     {"name": i, "id": i} for i in df_despesas.columns
                            # ],
                            style_header={'backgroundColor': 'rgb(255, 255, 255)',
                                          'color': 'black',
                                          'fontWeight': 'bold',
                                          'font': '20px Arial'
                                                   },
                            style_data={'backgroundColor': 'rgb(255, 255, 255)',
                                                    'color': 'black',
                                                    'font': '14px sans-serif'
                                                },
                            style_cell={'textAlign': 'left',
                                        'padding':'10px'},
                            style_as_list_view=True,
                            style_table={'overflowX': 'auto',
                                         'padding':'5px'}
                            # css=[{
                            #     'selector': '.dash-spreadsheet td div',
                            #     'rule': '''
                            #         line-height: 15px;
                            #         max-height: 20px; min-height: 20px; height: 20px;
                            #         display: block;
                            #         overflow-y: hidden;
                            #     '''
                            # }]
                                         
                                         
                                        
                        ),
                    ])
                ],md=6),
                dbc.Col([
                    dbc.Card([
                        html.Legend('Metas'),
                        dash_table.DataTable(
                            id='tbl-meta',
                            style_header={'backgroundColor': 'rgb(255, 255, 255)',
                                          'color': 'black',
                                          'fontWeight': 'bold',
                                          'font': '20px Arial'
                                                   },
                            style_data={'backgroundColor': 'rgb(255, 255, 255)',
                                                    'color': 'black',
                                                    'font': '14px sans-serif'
                                                },
                            style_cell={'textAlign': 'left',
                                        'padding':'10px'},
                            style_as_list_view=True,
                            style_table={'overflowX': 'auto',
                                         'padding':'5px'}
                        ),
                        # dcc.Slider(0.0,1.0,0.1,
                        #            value=0.0,
                        #            id='slide')
                    ])
                ],md=6)
            
            ]),
            
                
                
        ])

@app.callback(
    [Output('tbl-desp','columns'),
    Output('tbl-desp','data')],
    Input('store-despesas','data'),
    Input('date-picker-config','start_date'),
    Input('date-picker-config','end_date'),
    Input('store-categoria','data'),
    Input('store-receitas','data')
)
def update_table(data_desp,dt_start,dt_end,data_cat,data_rec):
    df_despesa = pd.DataFrame(data_desp)
    df_receita = pd.DataFrame(data_rec)
    df_categoria = pd.DataFrame(data_cat)

    dt_start = datetime.strptime(dt_start, '%Y-%m-%d')
    dt_end = datetime.strptime(dt_end, '%Y-%m-%d')

    df_despesa['Data'] = df_despesa['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    df_receita['Data'] = df_receita['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    # df['Data'].astype(datetime)

    df_despesa = df_despesa[df_despesa['Data'].between(dt_start,dt_end)]
    df_receita = df_receita[df_receita['Data'].between(dt_start,dt_end)]

    val_receita = df_receita['Valor'].sum()

    df_despesa = (df_despesa.groupby(['Categoria'])['Valor'].sum()).reset_index()



    
    # df_categoria
    # df_despesas = (df_despesas.groupby(['Categoria'])['Valor'].sum()).reset_index()
    # df_despesas['(%) Devo Gastar'] = ''

    df_despesa = pd.merge(df_categoria, df_despesa, how='left',on =['Categoria'])

    df_despesa['Devo Gastar'] = df_despesa['MetaPercentualGasto'].apply(lambda x : round(x*val_receita),2)
    df_despesa['Utilizado'] = round(df_despesa['Valor']/df_despesa['Devo Gastar'],2)*100
    df_despesa['Utilizado'] = df_despesa['Utilizado'].apply(lambda x: round(x,2))
    df_despesa['Total'] = df_despesa['Valor'].apply(lambda x : round((x/val_receita)*100,2))


    df_despesa.drop(columns='MetaPercentualGasto', inplace=True)
    df_despesa.fillna(0, inplace=True)
    

    

    #f'R${1000000:,.2f}'.replace(',','.')

    df_despesa['Valor'] = df_despesa['Valor'].apply(lambda x: f'R${x:,.2f}'.replace(',','.'))
    df_despesa['Devo Gastar'] = df_despesa['Devo Gastar'].apply(lambda x: f'R${x:,.2f}'.replace(',','.'))
    df_despesa['Utilizado'] = df_despesa['Utilizado'].apply(lambda x: f'{x}%')
    df_despesa['Total'] = df_despesa['Total'].apply(lambda x: f'{x}%')
      
    df_despesa.rename(columns={'Valor':'Valor Gasto'}, inplace=True)
    

    # import pdb
    # pdb.set_trace()

    columns=[{"name": i, "id": i} for i in df_despesa.columns]
    data_table = df_despesa.to_dict('records')

    

    return [columns,data_table]

@app.callback(
Output('tbl-meta','columns'),
Output('tbl-meta','data'),
Input('store-categoria','data')
)
def change_tbl_meta(data):

    df = pd.DataFrame(data)

    df['MetaPercentualGasto'] = df['MetaPercentualGasto'].apply(lambda x: f'{round(x*100,0)}%')

    columns=[{"name": i, "id": i} for i in df.columns]
    data_table = df.to_dict('records')

    # import pdb
    # pdb.set_trace()

    return [columns,data_table]

@app.callback(
[Output('total-gasto-card','children'),
Output('devo-gastar-card','children'),
Output('utilizado-card','children')],
#Input('tbl-desp','data'),
Input('store-receitas','data'),
Input('store-despesas','data'),
Input('date-picker-config','start_date'),
Input('date-picker-config','end_date')

)
def valores_totais(data_rec,data_desp,dt_start,dt_end):

    df_receita = pd.DataFrame(data_rec)
    df_despesa = pd.DataFrame(data_desp)

    dt_start = datetime.strptime(dt_start, '%Y-%m-%d')
    dt_end = datetime.strptime(dt_end, '%Y-%m-%d')

    df_receita['Data'] = df_receita['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    df_receita = df_receita[df_receita['Data'].between(dt_start,dt_end)]

    df_despesa['Data'] = df_despesa['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    df_despesa = df_despesa[df_despesa['Data'].between(dt_start,dt_end)]

    # import pdb
    # pdb.set_trace()

    df_despesa['Valor'].sum()

    total_gasto = df_despesa['Valor'].sum()
    devo_gastar = df_receita['Valor'].sum()
    utilizado = round((total_gasto/devo_gastar)*100,2)
    utilizado = f'{utilizado}%'


    
    return [f'R$ {total_gasto}',f'R$ {devo_gastar}',utilizado]

  
    
