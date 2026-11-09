import sqlite3
import pandas as pd

df = pd.read_csv('dados/vendas.csv')
con = sqlite3.connect('dados/vendas.db')
df.to_sql('vendas', con, if_exists='replace', index=False)
con.close()
print('Banco criado: tabela vendas com', len(df), 'linhas')