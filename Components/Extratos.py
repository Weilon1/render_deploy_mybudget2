from dash import html, dcc, Dash, dash_table, ctx
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
            dbc.Row([
                dbc.Col([
                        dbc.Row([
                            dbc.Card([
                                dbc.Row([
                                 dbc.Col([
                                 html.H3('Extratos'),
                                        ],md=4),
                                dbc.Col([
                                dcc.DatePickerRange(
                                month_format='Do MMM YY',
                                end_date_placeholder_text='Data...',
                                start_date=(datetime.now().date() - timedelta(days=datetime.now().date().day-1)),
                                end_date=datetime.now().date(), 
                                updatemode='singledate',
                                id='date-picker-config',
                                style={'z-index':'100'}),
                                        ],md=4),
                                dbc.Col([
                                    dcc.Dropdown(['Receitas','Despesas'],
                                                 id='dp-mod',
                                                 value=['Receitas','Despesas'],
                                                 multi=True
                                                 )
                                        ],md=4)
                        
                            ])
                        ]),
                    ]),
                    dbc.Card([
                        dash_table.DataTable(
                            id='tbl-extrato',
                            # columns=[
                            #     {"name": i, "id": i} for i in df_despesas.columns
                            # ],
                              style_header={'backgroundColor': 'rgb(30, 30, 30)',
                                                       'color': 'white',
                                                       'font':'20px Calibri'
                                                   },
                              style_data={'backgroundColor': 'rgb(30, 30, 30)',
                                                    'color': 'white',
                                                    'font':'15px Calibri'
                                                },
                               editable=True,
                               row_deletable=True,
                               sort_action='native',
                               filter_action="native",
                               column_selectable="single",
                               #row_selectable="multi",
                               selected_rows=[],
                               row_selectable="multi",
                               sort_mode="multi",
                               page_size=20,
                               style_table={'height': '500px', 'overflowY': 'auto'}
                                         
                                         
                                        
                        )
                    ]),
                    html.Button('Download', id='btn-download-table'),
                    dcc.Download(id='download-table')
                ],md=9),
                dbc.Col([
                dbc.Row(dbc.Card([
                    html.Legend('Total Receitas:'),
                    html.H5('R$-',id='rec-total-ext')

                ])),
                dbc.Row(dbc.Card([
                    html.Legend('Total Despesas:'),
                    html.H5('R$-',id='desp-total-ext')
                ]))],md=3),
                
            ])
                
                
        ])

@app.callback(
    [Output('tbl-extrato','columns'),
    Output('tbl-extrato','data'),],
    Input('store-despesas','data'),
    Input('store-receitas','data'),
    Input('date-picker-config','start_date'),
    Input('date-picker-config','end_date'),
    Input('dp-mod','value')
)
def update_table(data,data_rec,dt_start,dt_end,mod):
    # Separa os df
    df_desp = pd.DataFrame(data)
    df_desp['Modalidade'] = 'Despesas'
    df_rec = pd.DataFrame(data_rec)
    df_rec['Modalidade'] = 'Receitas'

    # Concatena os dados
    df = pd.concat([df_desp,df_rec])

    # Transforma as variaveis em datetime
    dt_start = datetime.strptime(dt_start, '%Y-%m-%d')
    dt_end = datetime.strptime(dt_end, '%Y-%m-%d')
    
    # Insere coluna de mês e ajusta a de data
    df['Mes'] = df['Data'].apply(lambda x: x[0:7])
    df['Data'] = pd.to_datetime(df['Data'])

    # filta os dados
    df = df[df['Data'].between(dt_start,dt_end)]
    mod = [mod] if type(mod) ==str else mod
    df = df[df['Modalidade'].isin(mod)]

    

    # Ajusta a coluna de data
    df['Data'] = df['Data'].apply(lambda x: x.date())

    # Aplica o formato de tabela para o df
    columns=[{"name": i, "id": i} for i in df.columns]
    data_table = df.to_dict('records')
    table = [columns,data_table]

    # import pdb
    # pdb.set_trace()

    return table

# @app.callback(
#     Output('rec-total-ext','children'),
#     Output('desp-total-ext','children'),
#     Input('store-receitas','data'),
#     Input('store-despesas','data'),
#     Input('date-picker-config','start_date'),
#     Input('date-picker-config','end_date')
# )
# def update_cads_totais(data_rec,data_desp,dt_start,dt_end):
#     df_rec = pd.DataFrame(data_rec)
#     df_rec = df_rec[df_rec['Data'].between(dt_start,dt_end)]
    
#     df_desp = pd.DataFrame(data_desp)
#     df_desp = df_desp[df_desp['Data'].between(dt_start,dt_end)]

#     vlr_receita = df_rec['Valor'].sum()
#     vlr_desp = df_desp['Valor'].sum()

#     import pdb
#     pdb.set_trace()

#     return [vlr_receita,vlr_desp]

@app.callback(
    Output('rec-total-ext','children'),
    Output('desp-total-ext','children'),
    Input('tbl-extrato','data')
)
def update_cards(data_table):
    df = pd.DataFrame(data_table)
    valores = df.groupby('Modalidade')['Valor'].sum()
    vlr_rec = valores['Receitas'] if valores['Receitas'] is not None else 0
    vlr_desp = valores['Despesas'] if valores['Despesas'] is not None else 0

    # import pdb
    # pdb.set_trace()

    # df.to_csv('df_teste.csv')

    return [vlr_rec,vlr_desp]

@app.callback(
    Output('download-table','data'),
    Input('btn-download-table','n_clicks'),
    Input('store-despesas','data'),
    Input('store-receitas','data'),
    Input('date-picker-config','start_date'),
    Input('date-picker-config','end_date'),
    Input('dp-mod','value'),
    prevent_initial_call=True,
)
def download_table_extato(n_clicks,desp,rec,start_dt,end_dt,dp_value):
    if 'btn-download-table' == ctx.triggered_id:
        df_rec = pd.DataFrame(rec)
        df_rec['Modalidade'] = 'Receitas'
        df_desp = pd.DataFrame(desp)
        df_desp['Modalidade'] = 'Despesas'

        start_dt = datetime.strptime(start_dt, '%Y-%m-%d')
        end_dt = datetime.strptime(end_dt, '%Y-%m-%d')

        df_extrato = pd.concat([df_desp,df_rec])
        df_extrato['Data'] = df_extrato['Data'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

        df_extrato = df_extrato[df_extrato['Data'].between(start_dt,end_dt)]
        dp_value = [dp_value] if type(dp_value) ==str else dp_value
        df_extrato = df_extrato[df_extrato['Modalidade'].isin(dp_value)]

        now = datetime.now()
        datetime.strftime(now,'%Y-%m-%d %H:%M:%S')

        nome_arquivo = f'extrato_{now}.csv'

        # if 'btn-salvar-receita' == ctx.triggered_id and not (valor == '' or valor ==None):
        #ctx.triggered_id

    # import pdb
    # pdb.set_trace()
        
    

    

    return dcc.send_data_frame(df_extrato.to_csv, nome_arquivo)
    
