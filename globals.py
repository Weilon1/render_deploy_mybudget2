import pandas as pd
import os

# os.listdir()

if ('df_receitas.csv') in os.listdir() and ('df_despesas.csv') in os.listdir():
    df_receitas = pd.read_csv('df_receitas.csv', index_col=0, parse_dates=True)
    
    df_despesas = pd.read_csv('df_despesas.csv', index_col=0, parse_dates=True)

    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])

    df_receitas['Data'] = df_receitas['Data'].apply(lambda x: x.date())
    df_despesas['Data'] = df_despesas['Data'].apply(lambda x: x.date())

    

else:
    data_structure = {'Data':[],
                        'Valor':[],
                        'Categoria':[],
                        'Tipo':[]
                        }
    
    data_structure_desp = {'Data':[],
                        'Valor':[],
                        'Categoria':[],
                        'Tipo':[],
                        'MetodoPagamento':[]
                        }
    
    
    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure_desp)
    df_receitas.to_csv('df_receitas.csv',index=True)
    df_despesas.to_csv('df_despesas.csv',index=True)



if ('df_categoria.csv') in os.listdir():
    df_categoria = pd.read_csv('df_categoria.csv', index_col=0, parse_dates=True)

else:
    structure_catego = {
        #'Mes': [],
        'Categoria':['Custos Fixos','Conforto','Metas','Prazeres','Liberdade Financeira', 'Conhecimento'],
        'MetaPercentualGasto':[0.30,0.15,0.15,0.10,0.25,0.05],
        #'Valor Gasto':[],
        #'Valor Devo Gastar':[],
        #'Utilizado':[],
        #'Total':[]
    }

    df_categoria = pd.DataFrame(structure_catego)
    df_categoria.to_csv('df_categoria.csv')

# import calendar, datetime  






# lista_df = ['receitas','despesas',]
# df_final= pd.DataFrame()
# for i in lista_df:
#     if i =='receitas':
#         df_rec = df_receitas[['Data','Valor']]
#         df_rec['Tipo'] = 'Receitas'
#         df_gph =df_rec 
#     elif i =='despesas':
#         df_desp = df_despesas[['Data','Valor']]
#         df_desp['Tipo'] = 'Despesas'
#         df_gph =df_desp 
    

#     df_gph['Data'] = pd.to_datetime(df_gph['Data'])
#     df_gph['ano'] = df_gph['Data'].apply(lambda x: x.year)
#     df_gph['mes'] = df_gph['Data'].apply(lambda x: str(x.month)+'-'+calendar.month_abbr[x.month])  
    
#     df_gph = df_gph.groupby(['ano','mes','Tipo']).sum().reset_index()
#     df_gph.sort_values(['ano','mes'],inplace=True)

#     df_gph['Evolucao'] = round((df_gph['Valor'] - df_gph['Valor'].shift())/df_gph['Valor'].shift(),2)
#     minindx = df_gph.loc[df_gph.index.min()]['Valor']
#     df_gph['Evolucao Periodo'] = (df_gph['Valor']-minindx)/minindx
#     df_final = pd.concat([df_final,df_gph])
    

# import plotly.express as px

# fig = px.line(df_final,
#         x='mes',
#         y='Evolucao',
#         color='Tipo',
#         hover_name='Tipo',
#         hover_data={'ano':False,
#                     'mes':False,
#                     'Tipo':False,
#                     'Evolucao':':.2%',
#                     'Evolucao Periodo':':.2%',
#                     'Valor':f':.2f'}
#         )

# fig.update_layout(hovermode="x unified")

# df_final.fillna(0,inplace=True)

# import datetime
# df_receitas[df_receitas['Data']==datetime.datetime(2023,6,2).date()].index

# df_receitas['Data'].iloc[0]

# df_receitas.drop(df_receitas[df_receitas['Data']==datetime.datetime(2023,6,2).date()].index,axis=0)


