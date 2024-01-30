from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go 
from app import template_theme, url_theme


# url_theme = dbc.themes.DARKLY
#template_theme = 'Flatly'

from globals import *
from app import app
# from app import template_theme

import pdb

load_figure_template([template_theme])

app.layout = dbc.Col([
    # Row 1
    dbc.Row([ 


################# Card Receita
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Receita'),
                    html.H5('R$ 100', id='p-receita-dashboard', style={})
                ],style={'padding-left': '20px', 'padding-top':'10px'})
            ])
        ], width=4),

################# Card Despesas
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Despesas'),
                    html.H5('R$ -', id='p-despesas-dashboard', style={})
                ],style={'padding-left': '20px', 'padding-top':'10px'})
            ])
        ], width=4),

################# Card Saldo
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo'),
                    html.H5('R$ -', id='p-saldo-dashboard', style={})
                ],style={'padding-left': '20px', 'padding-top':'10px'})
            ])
        ], width=4),

    ]),

#=================== Row 2
    dbc.Row([
        dbc.Col(dcc.DatePickerRange(month_format='Do MMM YY',
                                end_date_placeholder_text='Data...',
                                start_date=datetime.today() - timedelta(days=360),
                                end_date=datetime.today(),
                                updatemode='singledate',
                                id='date-filter',
                                style={'z-index':'100'}),style={'padding':'10px'},md=4),
        #dbc.Col(dcc.Dropdown(id='dp-receita'),style={'padding':'10px'}, md=4),
        #dbc.Col(dcc.Dropdown(id='dp-despesa'),style={'padding':'10px'}, md=4),

    ]),

# Graficos Linhas 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Categoria das Receitas'),
                dcc.Graph(id='categ-receita',
                                style={'margin':'0px 0px 5px 0px',
                                       'padding':'0px'}),
                      
                      ],style={'margin':'5px 5px 5px 5px',
                                       'padding':'5px'})
            ], md=4, lg=4,sm=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Categoria das Despesas'),
                dcc.Graph(id='categ-despesas',
                          style={'margin':'0px 0px 5px 0px',
                                       'padding':'0px'})
                ],style={'margin':'5px 5px 5px 5px',
                                       'padding':'5px'})
        ], md=4, lg=4,sm=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Método Pagamento Despesas'),
                dcc.Graph(id='metodo-pgto-despesas-dash',
                          style={'margin':'0px 0px 5px 0px',
                                       'padding':'0px'})
                ],style={'margin':'5px 5px 5px 5px',
                                       'padding':'5px'})
        ], md=4, lg=4,sm=4)
        # dbc.Col([
        #     dcc.Graph(id='categ-rec-des')
        # ], md=6)
    ]),

#=================== Row 3
# Gráficos Linha 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Categoria das Despesas'),
                dcc.Graph(id='desp-categ-barras')
                ],style={'margin':'5px 5px 5px 5px',
                                       'padding':'5px'})
        ], md=6, lg=6,sm=6),
        dbc.Col([
            dbc.Card([
                html.Legend('Receitas x Despesas'),
                dcc.Graph(id='desp-rec-barras')
                ],style={'margin':'5px 5px 5px 5px',
                                       'padding':'5px'})
        ], md=6, lg=6,sm=6),
    ]),
#=================== Row 4
# Gráficos Linha 4
    dbc.Row([
        dbc.Col([
            dbc.Card([

                dbc.Row([
                    dbc.Col([
                        html.H5('R$ -', id='card1-desp-tipo-barras', style={})
                    ])
                
                ]),

                dbc.Row([
                    # dbc.Col(dcc.Dropdown(id='dp-check-catego-barras',
                    #                      multi=True),md=12),
                    dbc.Col(dcc.Checklist(id='dp-check-catego-barras'),md=6),
                    
                ]),

                dcc.Graph(id='desp-tipo-barras')
            ])
        ])
    ]),
#=================== Row 5
# Gráficos Linha 5
    dbc.Row([
        dbc.Col([
            dbc.Card([

                dbc.Row([
                    # dbc.Col(dcc.Dropdown(id='dp-check-catego-barras',
                    #                      multi=True),md=12),
                    html.H5('Evolução Receitas e Despesas', style={}),
                    
                ]),

                dbc.Row([dcc.Graph(id='evolution-month-line-5-lines')
                    ])

            ],style={'margin':'5px 5px 5px 5px','padding':'5px'})
        ])
    ]),
])


# RECEITA
@app.callback(
    Output("p-receita-dashboard", "children"),
    Input('store-receitas','data'),
    Input('date-filter','start_date'),
    Input('date-filter','end_date')
)

def alt_card_receita(data,start_date,end_date):
    
    df = pd.DataFrame(data)




    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')

    # import pdb
    # pdb.set_trace()

    df['Data'] = df['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    
    df = df[df['Data'].between(start_date,end_date)]
    v = float(df['Valor'].sum())




    
    return f'R${v}'

# DESPESAS
@app.callback(
    Output("p-despesas-dashboard", "children"),
    Input('store-despesas','data'),
    Input('date-filter','start_date'),
    Input('date-filter','end_date')
)

def alt_card_despesa(data,start_date,end_date):
    
    df = pd.DataFrame(data)
    

    #start_date = '2023-08-01T09:25:39.851113'
    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')

    df['Data'] = df['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    df = df[df['Data'].between(start_date,end_date)]
    v = float(df['Valor'].sum())

    # import pdb
    # pdb.set_trace()

    
    return f'R${v}'


 

@app.callback(Output('p-saldo-dashboard','children'),
              Input('store-receitas','data'),
              Input('store-despesas','data'),
              Input('date-filter','start_date'),
              Input('date-filter','end_date')
              )

def alt_saldo(receita,despesa,dt_start,dt_end):

    

    dt_start = datetime.strptime(dt_start[0:10], '%Y-%m-%d')
    dt_end = datetime.strptime(dt_end[0:10], '%Y-%m-%d')

    

    df_r = pd.DataFrame(receita)
    df_r['Data'] = df_r['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    df_r = df_r[df_r['Data'].between(dt_start,dt_end)]

    
    

    df_d = pd.DataFrame(despesa)
    df_d['Data'] = df_d['Data'].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    df_d = df_d[df_d['Data'].between(dt_start,dt_end)]

    # import pdb
    # pdb.set_trace()

    val_r = df_r['Valor'].sum()
    val_d = df_d['Valor'].sum()

    

    s = val_r - val_d

    # import pdb
    # pdb.set_trace()

    return f'R$ {s}'


# Altera primeiro grafico linha 2
@app.callback(
    Output('categ-receita','figure'),
    Input('store-receitas','data'),
    Input('date-filter','start_date'),
    Input('date-filter','end_date')
)

def grafico1(receita,start_date,end_date):


    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')



    df = pd.DataFrame(receita)
    df['Data'] = df['Data'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    df = df[df['Data'].between(start_date,end_date)]
    fig = px.pie(df, 
                 values='Valor', 
                 names=df['Categoria'], 
                 hole=.5,
                 #title="Categoria das Receitas"
                 )
    
    fig.update_layout(template=template_theme,
                      height=200,
                      margin=dict(l=5, r=5, t=5, b=5)
                      )
    

    return fig


# Altera Segundo e Terceiro grafico linha 2
@app.callback(
    Output('categ-despesas','figure'),
    Output('metodo-pgto-despesas-dash','figure'),
    Input('store-despesas','data'),
    Input('date-filter','start_date'),
    Input('date-filter','end_date')
)

def grafico2(despesa,start_date,end_date):

    df = pd.DataFrame(despesa)

    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
    
    df['Data'] = df['Data'].apply(lambda x:  datetime.strptime(x, '%Y-%m-%d'))

    
    df = df[df['Data'].between(start_date,end_date)]

    # import pdb
    # pdb.set_trace()

    fig1 = px.pie(df, 
                 values='Valor', 
                 names=df['Categoria'], 
                 hole=.5,
                 #title="Categoria das Despesas"
                 )
    
    fig2 = px.pie(df, 
                 values='Valor', 
                 names=df['MetodoPagamento'], 
                 hole=.5,
                 #title="Categoria das Despesas"
                 )
    # fig = go.Figure(go.Bar(
    #             x=df['Valor'],
    #             y=df['Categoria'],
    #             orientation='h'

    #                          ))

   
    
    fig1.update_layout(template=template_theme,
                      height=200,
                      margin=dict(l=5, r=5, t=5, b=5)
                      )
    
    fig2.update_layout(template=template_theme,
                      height=200,
                      margin=dict(l=5, r=5, t=5, b=5)
                      )

    return fig1,fig2

# @app.callback(
#     Output('metodo-pgto-despesas-dash','figure')
# )

# Altera 1º grafico linha 3
@app.callback(
    Output('desp-categ-barras','figure'),
    Input('store-despesas','data'),
    Input('date-filter','start_date'),
    Input('date-filter','end_date')
)

def grafico1(despesa,start_date,end_date):

    
    df_despesas = pd.DataFrame(despesa)

    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
    
    df_despesas['Data'] = df_despesas['Data'].apply(lambda x:  datetime.strptime(x, '%Y-%m-%d'))

   

    df = df_despesas[df_despesas['Data'].between(start_date,end_date)]
    df = df.groupby('Categoria')['Valor'].sum()
    
    # import pdb
    # pdb.set_trace()

    fig = px.bar(df,
                 df.index,
                 df.values,
                 text_auto=True,
                 color=df.index
                 #title='Tipo das Despesas'
                 )
    fig.update_layout(template=template_theme,
                      height=300,
                      margin=dict(l=5, r=5, t=5, b=5)
                      )

    return fig


# Altera 2º grafico linha 3
# @app.callback(
#     Output('desp-rec-barras','figure'),
#     Input('store-receitas','data'),
#     Input('store-despesas','data'),
#     Input('date-filter','start_date'),
#     Input('date-filter','end_date')
# )

# def grafico1(receita,despesa,start_date,end_date):

    
#     df_despesas = pd.DataFrame(despesa)

#     df = df_despesas[df_despesas['Data'].between(start_date,end_date)]
#     df = df.groupby('Categoria')['Valor'].sum()
#     #pdb.set_trace()

#     fig = px.bar(df,df.index,df.values)

#     return fig

# Altera segundo grafico linha 3
@app.callback(
    #Output('categ-rec-des','figure'),
    Output('desp-rec-barras','figure'),
    Input('store-receitas','data'),
    Input('store-despesas','data'),
    Input('date-filter','start_date'),
    Input('date-filter','end_date')
)

def grafico1(receitas,despesa,start_date,end_date):

    
    df_receitas = pd.DataFrame(receitas)
    df_receitas['Tipo'] = 'Receita'
    df_despesa = pd.DataFrame(despesa)
    df_despesa['Tipo'] = 'Despesa'
    
    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')



    
    
    df_receitas['Data'] = df_receitas['Data'].apply(lambda x:  datetime.strptime(x, '%Y-%m-%d'))
    df_despesa['Data'] = df_despesa['Data'].apply(lambda x:  datetime.strptime(x, '%Y-%m-%d'))

    df_final = pd.concat([df_receitas,df_despesa])

   

    #datetime.strptime('2023-07-30', '%Y-%m-%d').date()

    #df_final['Data'] = df_final['Data'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())

    # pdb.set_trace()
    
    df = df_final[df_final['Data'].between(start_date,end_date)]
    # fig1 = px.pie(df, 
    #              values='Valor', 
    #              names=df['Tipo'], 
    #              hole=.3,
    #              title="Percentual Despesas")

    

    # dt = date(2023,8,1)

    # dt.strftime('%b')+'-'+str(dt.year)
    
    df['Mes'] = df['Data'].apply(lambda x: str(x.year)+'-'+str(x.month))



    
    df_bar = df.groupby(['Tipo','Mes'])[['Valor']].sum()
    df_bar.reset_index(inplace=True)
    df_bar.sort_values('Mes',inplace=True)

    # import pdb
    # pdb.set_trace()

    # fig2 = go.Figure()

    # fig2.add_trace(go.Bar(
    #     x=df_bar['Mes'],
    #     y=df_bar['Valor'],
    #     text=df_bar['Valor'],
    # ))

    # fig2 = go.Figure([
    #             go.Bar(
    #                 x=df_bar['Mes'],
    #                 y=df_bar['Valor'],
    #                 text=df_bar['Valor']
    #     )
    # ])
    
    fig2 = px.bar(df_bar,
                  x=df_bar['Mes'],
                  y=df_bar['Valor'],
                  color='Tipo',
                  barmode='group',
                  #orientation='h',
                  #title='Receitas x Despesas',
                  #text_auto=True
                  text=df_bar['Valor']
                  )

    # import pdb
    # pdb.set_trace()

    # datetime.now().date().strftime("%B")

    # data = datetime.now().date()

    


    #fig1.update_layout(template=template_theme)
    fig2.update_layout(template=template_theme,
                       margin=dict(l=5, r=5, t=5, b=5),
                       height=300,
                       xaxis_title=None,
                       yaxis_title=None,
                       #uniformtext_minsize=8,
                       )

    return fig2
# ALTERA GRAFICO DROPDOWN LINHA 4 
@app.callback(
[Output('dp-check-catego-barras','options'),    
Output('dp-check-catego-barras','value')],    
Input('store-despesas','data'),
Input('date-filter','start_date'),
Input('date-filter','end_date')
)
def altera_dp_desp_barras(data_desp,start_date,end_date):
    df_desp = pd.DataFrame(data_desp)



    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
    df_desp['Data'] = df_desp['Data'].apply(lambda x:  datetime.strptime(x, '%Y-%m-%d'))

    df_desp = df_desp[df_desp['Data'].between(start_date,end_date)]

    df_desp = df_desp['Categoria'].value_counts()

    options = df_desp.index

    # import pdb
    # pdb.set_trace()



    return [options,options]



# ALTERA GRAFICO LINHA 4 
@app.callback(
    [Output('desp-tipo-barras','figure'),
    Output('card1-desp-tipo-barras','children')],
    Input('store-despesas','data'),
    Input('date-filter','start_date'),
    Input('date-filter','end_date'),
    Input('dp-check-catego-barras','value')
)
def alter_grafico_tipo_desp(data_desp,start_date,end_date,values_dp):
    df_desp = pd.DataFrame(data_desp)

    start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
    df_desp['Data'] = df_desp['Data'].apply(lambda x:  datetime.strptime(x, '%Y-%m-%d'))

    df_desp = df_desp[df_desp['Data'].between(start_date,end_date)]
    df = pd.DataFrame()

    if values_dp ==None:
        df = pd.concat([df_desp,df])
    elif type(values_dp) == str:
        values_dp = [values_dp]
        df = pd.concat([df_desp[df_desp['Categoria'].isin(values_dp)],df])
    elif type(values_dp) == list:
        df = pd.concat([df_desp[df_desp['Categoria'].isin(values_dp)],df])
    elif type(values_dp) == list and len(values_dp) == 1:
        df = pd.concat([df_desp,df])
    else:
        df = pd.concat([df_desp,df])

    
    df_sumarizado = df.groupby('Tipo')[['Valor']].sum()
    df_sumarizado.reset_index(inplace=True)

    df_sumarizado['Valor'] = round(df_sumarizado['Valor'],2)

    # import pdb
    # pdb.set_trace()
    df_sumarizado.sort_values('Valor', ascending=False, inplace=True)


    val_total = df_sumarizado['Valor'].sum()
    val_total = round(val_total,2)
    val_total = f'Tipo das Despesas - R$ {val_total:.2f}'

    # import pdb
    # pdb.set_trace()


    fig = px.bar(df_sumarizado,
                  x=df_sumarizado['Tipo'],
                  y=df_sumarizado['Valor'],
                  color='Tipo',
                  #orientation='h',
                  #barmode='group',
                  #title='Receitas x Despesas',
                  text_auto=True
                  )

    # fig = px.line(df_sumarizado,
    #               x=df_sumarizado['Tipo'],
    #               y=df_sumarizado['Valor'],
    #               #color='Tipo',
    #               template=template_theme,
    #               #barmode='group',
    #               #title='Receitas x Despesas',
    #               text=df_sumarizado['Valor']
    #               )    
    
    fig.update_layout(template=template_theme,
                      height=400,
                      margin=dict(l=5, r=5, t=5, b=5),
                      xaxis_title=None,
                      yaxis_title=None,
                      hovermode="x unified"
                      
                      )

    # import pdb
    # pdb.set_trace()

    return [fig,val_total]

@app.callback(
    Output('evolution-month-line-5-lines','figure'),
    Input('store-receitas','data'),
    Input('store-despesas','data'),

)
def alter_grafico_linha_5(data_rec, data_desp):

    df_receitas = pd.DataFrame(data_rec)
    df_despesas = pd.DataFrame(data_desp)


    lista_df = ['receitas','despesas',]
    df_final= pd.DataFrame()

    for i in lista_df:
        if i =='receitas':
            df_rec = df_receitas[['Data','Valor']]
            df_rec['Tipo'] = 'Receitas'
            df_gph =df_rec 
        elif i =='despesas':
            df_desp = df_despesas[['Data','Valor']]
            df_desp['Tipo'] = 'Despesas'
            df_gph =df_desp 


        df_gph['Data'] = pd.to_datetime(df_gph['Data'])
        df_gph['ano'] = df_gph['Data'].apply(lambda x: x.year)
        df_gph['mes'] = df_gph['Data'].apply(lambda x: str(x.year)+'-'+str(x.month))  

        df_gph = df_gph.groupby(['ano','mes','Tipo']).sum().reset_index()
        df_gph.sort_values(['ano','mes'],inplace=True)

        df_gph['Evolucao Ult. Mês'] = (df_gph['Valor'] - df_gph['Valor'].shift())/df_gph['Valor'].shift()
        minindx = df_gph.loc[df_gph.index.min()]['Valor']
        df_gph['Evolucao Periodo'] = (df_gph['Valor']-minindx)/minindx
        
        df_final = pd.concat([df_final,df_gph])

        df_final.fillna(0,inplace=True)

    fig = px.line(df_final,
        x='mes',
        y='Valor',
        color='Tipo',
        hover_name='Tipo',
        hover_data={'ano':False,
                    'mes':False,
                    'Tipo':False,
                    'Evolucao Ult. Mês':':.2%',
                    'Evolucao Periodo':':.2%',
                    'Valor':f':.2f'}
        )

    fig.update_layout(template=template_theme,
                      height=400,
                      margin=dict(l=5, r=5, t=5, b=5),
                      xaxis_title=None,
                      yaxis_title=None,
                      hovermode="x unified",
                                            )

    return fig



