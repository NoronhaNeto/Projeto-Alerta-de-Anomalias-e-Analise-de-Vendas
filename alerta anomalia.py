import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))   # trabalha sempre na pasta do script

SQL = '''
WITH diario AS (
  SELECT data, categoria, SUM(valor) AS total
  FROM vendas
  GROUP BY data, categoria
),
calc AS (
  SELECT data, categoria, total,
         AVG(total) OVER (
           PARTITION BY categoria
           ORDER BY data
           ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
         ) AS media_7d
  FROM diario
)
SELECT data,
       categoria,
       ROUND(total, 2) AS total,
       ROUND(media_7d, 2) AS media_7d,
       ROUND(total * 1.0 / media_7d - 1, 3) AS desvio
FROM calc
WHERE media_7d IS NOT NULL
  AND total < 0.7 * media_7d
ORDER BY data DESC;
'''


def enviar_alerta(texto):
    janela = tk.Tk()
    janela.withdraw()
    janela.attributes('-topmost', True)
    messagebox.showwarning('ALERTA: queda anormal de vendas',
                           texto.replace(' | ', '\n'))
    janela.destroy()


def montar_mensagem(l):
    return (f'ALERTA: {l.categoria} em {l.data} | vendas R$ {l.total:.2f}, '
            f'{l.desvio:.0%} vs média de 7 dias (R$ {l.media_7d:.2f}) | '
            'Responsável: [definir] | Prazo: hoje, 18h')


con = sqlite3.connect('dados/vendas.db')
anomalias = pd.read_sql(SQL, con)
vendas = pd.read_sql('SELECT * FROM vendas', con)
ultima_data = vendas['data'].max()
con.close()

anomalias.to_csv('dados/alertas.csv', index=False)   # alimenta o Power BI

hoje = anomalias[anomalias['data'] == ultima_data]
if hoje.empty:
    print('Sem anomalias hoje.')

for l in hoje.itertuples():
    enviar_alerta(montar_mensagem(l))