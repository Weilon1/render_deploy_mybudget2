import os
import dash
from dash import html, dcc, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date, timedelta
import plotly.express as px
import numpy as np
import pandas as pd

from globals import *
import pdb 



# ========= Layout ========= #
app.layout = dbc.Col([
                html.H1('MyBudget', className='text-primary'),
                html.H1('By Weilon', className='text-info'),
                html.Hr(),

#Seção de perfil ===============================
        
        dbc.Button(id='botao_avatar',
            children=[html.Img(src='assets/img_hom.png', id='avatar', alt='Avatar', className='perfil_avatar')
                      ], style={'background-color':'transparent', 'border-color':'transparente'}),

#Botões Receita, Despesa ===============================

        dbc.Row([
            dbc.Col([
                dbc.Button(color='success', id='open-novo-receita',
                           children=['+ Receita'])
                            
            ], width=6),
            dbc.Col([
                dbc.Button(color='danger', id='open-novo-despesa',
                           children=['- Despesa'])
                            
            ], width=6),
        ]),
        # Modal Receita
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Adicionar Receita')),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição: '),
                        dbc.Input(placeholder='Ex.: Salário, Dividendos da Bolsa e etc...', id='txt-receita')
                        ], width=4),
                    dbc.Col([
                        dbc.Label('Valor'),
                        dbc.Input(placeholder='$100.00', id='valor-receita', value='')
                    ], width=4),
                    dbc.Col([
                        dbc.Label('Categoria'),
                        dbc.Input(placeholder='Salário, Comissão, Extras e etc..', id='categoria-receita', value='')
                    ], width=4),

                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Data: '),
                            dcc.DatePickerSingle(id='date-receitas',
                                                min_date_allowed=date(2020, 1, 1),
                                                max_date_allowed=date(2030, 12, 31),
                                                date=datetime.date(datetime.today()),
                                                style={'width':'100%'}
                                                ),
                        ], width=4),

                    dbc.Row(html.Div(id='div-test'))

                    ], style={'margin-top':'25px'}),
                ]),
                
            dbc.ModalFooter([
                dbc.Button('Excluir Receita', id='btn-deletar-receita', color='danger'),
                dbc.Button('Adicionar Receita', id='btn-salvar-receita', color='success'),
                dbc.Popover(dbc.PopoverBody('Receita Excluída'), target='btn-deletar-receita', placement='left', trigger='click'),
                dbc.Popover(dbc.PopoverBody('Receita Salva'), target='btn-salvar-receita', placement='left', trigger='click')
            ])

            ])
        ], style={'background-color': 'rgba(17, 140, 79, 0.05)'},
            id='modal-novo-receita',
            size='lg',
            is_open=False,
            centered=True,
            backdrop=True),

    # Modal despesa
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Tipo Despesa: '),
                        dbc.Input(placeholder='Ex.: Aluguel, Gasolina, Conta de luz...', id='txt-despesa')
                        ], width=3),
                    dbc.Col([
                        dbc.Label('Valor: '),
                        dbc.Input(placeholder='$100.00', id='valor-despesa', value='')
                    ], width=3),
                    dbc.Col([
                        dbc.Label('Categoria: '),
                        #dbc.Input(placeholder='Contas Fixas, Lazer, Liberdade Financeira e etc..', id='categoria-despesa', value='')
                        dcc.Dropdown(
                                    # ['Despesas Essenciais',
                                    #   'Lazer',
                                    #   'Educação',
                                    #   'Liberdade Financeira',
                                    #   'Reserva de Emergência'],
                                     id='categoria-despesa')
                    ], width=3),
                    dbc.Col([
                        dbc.Label('Método Pagamento: '),
                        #dbc.Input(placeholder='Contas Fixas, Lazer, Liberdade Financeira e etc..', id='categoria-despesa', value='')
                        dcc.Dropdown(
                                     ['Crédito','Débito','Pix','Dinheiro'],
                                     id='metodo-pagamento-despesa')
                    ], width=3),

                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Data: '),
                            dcc.DatePickerSingle(id='date-despesas',
                                                min_date_allowed=date(2020, 1, 1),
                                                max_date_allowed=date(2030, 12, 31),
                                                date=datetime.date(datetime.today()),
                                                style={'width':'100%'}
                                                ),
                        ], width=4),

                    ], style={'margin-top':'25px'}),
                ]),

                dbc.ModalFooter([
                dbc.Button('Deletar Despesa', id='btn-deletar-despesa', color='danger'),
                dbc.Button('Adicionar Despesa', id='btn-salvar-despesa', color='success'),
                dbc.Popover(dbc.PopoverBody('Despesa Salva'), target='btn-salvar-despesa', placement='left', trigger='click'),
                dbc.Popover(dbc.PopoverBody('Despesa Excluida'), target='btn-deletar-despesa', placement='left', trigger='click')
            ])
                
            ])
        ], style={'background-color': 'rgba(17, 140, 79, 0.05)'},
            id='modal-novo-despesa',
            size='lg',
            is_open=False,
            centered=True,
            backdrop=True),



#Seção Nav ========================================
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink('Dashboard',href='/Dashboard',active='extract'),
                dbc.NavLink('Extratos',href='/Extratos',active='extract'),
                dbc.NavLink('Planejamento',href='/Planejamento',active='extract'),
            ],vertical=True, pills=True, id='nav_buttons', style={'margin-bottom': '50px'}
        )


], id='sidebar_completa')

# =========  Callbacks  =========== #
# DROPDOWN CATEGORIA DESPESA
@app.callback(
Output('categoria-despesa','options'),
Input('store-categoria','data')
)
def change_dp_catego(data):
    #data = df_categoria.to_dict()
    data = data['Categoria']

    options = [{'label': i, 'value':i} for i in data.values()]

    # import pdb
    # pdb.set_trace()

    return options


# Pop-up Receita
@app.callback(
Output('modal-novo-receita', 'is_open'),
Input('open-novo-receita', 'n_clicks'),
State('modal-novo-receita', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    

# Pop-up despesa
@app.callback(
Output('modal-novo-despesa', 'is_open'),
Input('open-novo-despesa', 'n_clicks'),
State('modal-novo-despesa', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    
@app.callback(
Output('store-receitas', 'data'),
#Output('div-test','children'),
Input('btn-salvar-receita', 'n_clicks'),
Input('btn-deletar-receita', 'n_clicks'),
    [
        State('txt-receita', 'value'),
        State('valor-receita', 'value'),
        State('categoria-receita', 'value'),
        State('date-receitas', 'date'),
        State('store-receitas', 'data'),
    ]
)
def salva_receita(n,n2,descricao,valor,categ,dt, dic_receita):

    # SALVAR RECEITA
    df_receitas = pd.DataFrame(dic_receita)

    df_receitas_total = pd.DataFrame()

    retirar = pd.DataFrame()
    if 'btn-salvar-receita' == ctx.triggered_id and not (valor == '' or valor ==None):
        valor = round(float(valor),2)
        dt = pd.to_datetime(dt).date()
        categ = categ

        add = {'Data':[dt],
               'Valor':[valor],
               'Categoria':[categ],
               'Tipo':[descricao]}
        
        add = pd.DataFrame(add)

        df_receitas = pd.concat([df_receitas,add])

        df_receitas.reset_index(inplace=True)
        df_receitas.drop(columns='index',inplace=True)
        
        
        # import pdb
        # pdb.set_trace()

        #df_receitas = pd.read_csv('df_receitas.csv', index_col=0, parse_dates=True)

        #df_receitas.loc[df_receitas.shape[0]] = [dt,valor, categ, descricao]

        #df_receitas_total = pd.concat([df_receitas,df_add],ignore_index=True)

        # import pdb
        # pdb.set_trace()

        df_receitas.to_csv('df_receitas.csv')

        

    # DELETAR RECEITA
    elif 'btn-deletar-receita' == ctx.triggered_id and not (valor == '' or valor ==None):
        valor = round(float(valor),2)
        #dt = pd.to_datetime(dt).date()
        categ = categ

        retirar = df_receitas[(df_receitas['Data']==dt) & 
                     (df_receitas['Valor']==valor) &
                     (df_receitas['Categoria']==categ)&
                     (df_receitas['Tipo']==descricao)
                     ] 
        
        df_receitas.drop(retirar.index, inplace=True)

        df_receitas.to_csv('df_receitas.csv')

        # import pdb
        # pdb.set_trace()

    return df_receitas.to_dict()

# SALVAR DESPESA

@app.callback(
Output('store-despesas', 'data'),
#Output('div-test','children'),
Input('btn-salvar-despesa', 'n_clicks'),
Input('btn-deletar-despesa', 'n_clicks'),
    [
        State('txt-despesa', 'value'),
        State('valor-despesa', 'value'),
        State('categoria-despesa', 'value'),
        State('date-despesas', 'date'),
        State('store-despesas', 'data'),
        State('metodo-pagamento-despesa','value')
    ]
)
def salva_despesa(n,n2,descricao,valor,categ,dt, dic_despesa,metodo_pgt_desp):

    # Salva despesas
    df_despesas = pd.DataFrame(dic_despesa)
    retirar = pd.DataFrame()

    

    if 'btn-salvar-despesa' == ctx.triggered_id and not (valor == '' or valor ==None):
        valor = round(float(valor),2)
        dt = pd.to_datetime(dt).date()
        categ = categ

        add = {'Data':[dt],
               'Valor':[valor],
               'Categoria':[categ],
               'Tipo':[descricao],
               'MetodoPagamento':[metodo_pgt_desp]}
        
        add = pd.DataFrame(add)

        #df_despesas.loc[df_despesas.shape[0]] = [dt,valor, categ, descricao]

        df_despesas = pd.concat([df_despesas,add])
        df_despesas.reset_index(inplace=True)
        df_despesas.drop(columns='index', inplace=True)
        # import pdb
        # pdb.set_trace()

        
        df_despesas.to_csv('df_despesas.csv')

    #Deletar despesas
        
    elif 'btn-deletar-despesa' == ctx.triggered_id and not (valor == '' or valor ==None):
        valor = round(float(valor),2)
        #dt = pd.to_datetime(dt).date()
        categ = categ

        df_despesas = pd.read_csv('df_despesas.csv', index_col=0, parse_dates=True)


        # retirar = df_despesas[(df_despesas['Data']=='2023-07-30') & 
        #             (df_despesas['Valor']==100.0) &
        #             (df_despesas['Categoria']=='Contas Fixas')&
        #             (df_despesas['Tipo']=='Gasolina')
        #             ] 
        
        # df_despesas.drop(retirar.index)

        retirar = df_despesas[(df_despesas['Data']==dt) & 
                     (df_despesas['Valor']==valor) &
                     (df_despesas['Categoria']==categ)&
                     (df_despesas['Tipo']==descricao)
                     ] 
        
        df_despesas.drop(retirar.index, inplace=True)

        # import pdb
        # pdb.set_trace()

        df_despesas.to_csv('df_despesas.csv',index=True)


    return df_despesas.to_dict()

# DELETAR DESPESA

# @app.callback(
# Output('store-despesas', 'data'),
# Input('btn-deletar-despesa', 'n_clicks'),
#     [
#         State('txt-despesa', 'value'),
#         State('valor-despesa', 'value'),
#         State('categoria-despesa', 'value'),
#         State('date-despesas', 'date'),
#         State('store-despesas', 'data'),
#     ]
# )
# def deletar_despesa(n,descricao,valor,categ,dt, dic_despesa):

    

#     if n and not (valor == '' or valor ==None):
#         valor = round(float(valor),2)
#         dt = pd.to_datetime(dt).date()
#         categ = categ

#         df_despesas = pd.read_csv('df_despesas.csv', index_col=0, parse_dates=True)

#         # dt = '2023-07-30'
#         # valor = 100.0
#         # categ = 'Contas Fixas'
#         # descricao = 'Gasolina'

#         retirar = df_despesas[(df_despesas['Data']==dt) & 
#                     (df_despesas['Valor']==valor) &
#                     (df_despesas['Categoria']==categ)&
#                     (df_despesas['Tipo']==descricao)
#                     ] 
        
        
#         import pdb
#         pdb.set_trace()

#         df_despesas.drop(retirar.index)

#         df_despesas.to_csv('df_despesas.csv',index=True)
        

#         #df_despesas.to_csv('df_despesas.csv')

        

#     return df_despesas.to_dict()

    
if __name__ == '__main__':
    app.run_server(port=8051, debug=True)
