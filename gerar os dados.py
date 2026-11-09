import os
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)
os.makedirs('dados', exist_ok=True)

categorias = {'Bebidas': 1500, 'Mercearia': 2500, 'Limpeza': 1000, 'Hortifruti': 1200}
fim = date.today()
inicio = fim - timedelta(days=89)

linhas = []
dia = inicio
while dia <= fim:
    fator = 1.25 if dia.weekday() >= 5 else 1.0   # fim de semana vende mais
    for cat, base in categorias.items():
        valor = base * fator * random.uniform(0.9, 1.1)
        if cat == 'Bebidas' and dia == fim:
            valor *= 0.4   # queda artificial de 60% no último dia
        linhas.append({'data': dia.isoformat(), 'categoria': cat,
                       'valor': round(valor, 2), 'quantidade': int(valor / 20)})
    dia += timedelta(days=1)

pd.DataFrame(linhas).to_csv('dados/vendas.csv', index=False)
print('vendas.csv criado com', len(linhas), 'linhas')

import sqlite3
import pandas as pd

df = pd.read_csv('dados/vendas.csv')
con = sqlite3.connect('dados/vendas.db')
df.to_sql('vendas', con, if_exists='replace', index=False)
con.close()
print('Banco criado: tabela vendas com', len(df), 'linhas')