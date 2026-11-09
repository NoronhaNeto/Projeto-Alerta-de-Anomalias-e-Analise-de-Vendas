
# Projeto-Alerta-de-Anomalias-e-Analise-de-Vendas
Detecção automática de quedas anormais de vendas por categoria, com alerta acionável e dashboard em Power BI.

# Alerta de Queda de Vendas

Detecção automática de quedas anormais de vendas por categoria, com alerta acionável e dashboard em Power BI.

**Tecnologias:** Python (pandas, sqlite3, tkinter) · SQL (CTEs e funções de janela) · Power BI (DAX)

![Dashboard de acompanhamento de vendas](imagens/dashboard.png)

## Contexto e problema de negócio

Em operações de varejo, uma queda brusca de vendas em uma categoria pode ter causas como ruptura de estoque, falha de preço ou problema no ponto de venda. Quando o acompanhamento é manual, essas quedas costumam ser percebidas tarde, porque o total geral esconde o problema: uma queda forte em uma categoria some quando somada às demais.

Este projeto automatiza essa vigilância. Todo dia, ele compara cada categoria com o seu próprio comportamento recente, identifica desvios relevantes e avisa quem precisa agir, com responsável e prazo.

## Como funciona

```
Dados de vendas (CSV) → Banco SQLite → Consulta SQL (detecção) → Alerta na tela → CSV de anomalias → Dashboard Power BI
```

1. **`gerar_dados.py`** cria 90 dias de vendas simuladas em 4 categorias (Bebidas, Mercearia, Limpeza e Hortifruti), com sazonalidade de fim de semana e uma queda de 60% injetada em Bebidas no último dia, para validar que o alerta dispara.
2. **`carregar_banco.py`** carrega o CSV em um banco SQLite (`dados/vendas.db`).
3. **`alerta.py`** roda uma consulta SQL que calcula, para cada categoria, a média dos 7 dias anteriores e sinaliza os dias em que a venda ficou mais de 30% abaixo dessa média. Para o dia mais recente, exibe uma janela de alerta no Windows com a categoria, o tamanho da queda, o responsável e o prazo.
4. As anomalias detectadas são salvas em **`dados/alertas.csv`**, que alimenta o dashboard no Power BI.

## Regra de detecção

Há alerta quando:

```
venda do dia < 70% da média dos 7 dias anteriores (mesma categoria)
```

Isso equivale a uma queda maior que 30%. A consulta usa uma **função de janela**:

```sql
AVG(total) OVER (PARTITION BY categoria
  ORDER BY data
  ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS media_7d
```

- `PARTITION BY categoria` faz o cálculo separado para cada categoria.
- `ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING` usa os 7 dias anteriores **sem incluir o dia atual**, para que a própria queda não distorça a referência.
- O limite (30%) e a janela (7 dias) são parâmetros ajustáveis na consulta.

## O alerta

O alerta foi pensado para ser **acionável**: além do aviso, ele informa a categoria afetada, o valor vendido, o desvio em relação à média e um responsável com prazo de resposta.

```
ALERTA: Bebidas em 2026-11-08
vendas R$ 640.12, -60% vs média de 7 dias (R$ 1604.30)
Responsável: [definir]
Prazo: hoje, 18h
```

*(exemplo ilustrativo com valores fictícios)*

![Janela de alerta](imagens/alerta.png)

## Dashboard (Power BI)

O painel reúne faturamento por categoria, participação de cada categoria na quantidade vendida, evolução diária das vendas com linha de desvio padrão e indicadores como faturamento total, média, variação e desvio padrão. O dasboard é total interativo, podendo ser filtrado por categoria e periodo desejavel.  O arquivo do painel está em `dashboard/`.

## Como executar

**Requisitos:** Python 3.10 ou superior e Windows (o alerta usa uma janela do `tkinter`, que já vem com o Python).

```bash
pip install pandas
python gerar_dados.py
python carregar_banco.py
python alerta.py
```

Depois do último comando, deve aparecer a janela de alerta com a queda de Bebidas. Para abrir o dashboard, use o Power BI Desktop e aponte as fontes de dados para os CSVs da pasta `dados/`.

## Estrutura do projeto

```
alerta-vendas/
├── dados/            # vendas.csv e alertas.csv (o vendas.db é gerado localmente)
├── imagens/          # prints do dashboard e do alerta
├── dashboard/        # arquivo .pbix do Power BI
├── gerar_dados.py
├── carregar_banco.py
├── alerta.py
└── README.md
```

## Limitações e próximos passos

- Os dados são **simulados**; o projeto não usa informações reais de nenhuma empresa.
- A regra não considera sazonalidade (feriados e dias da semana). Uma melhoria é comparar com o mesmo dia da semana nas semanas anteriores.
- O mesmo limite vale para todas as categorias; o ideal é calibrar por categoria com o histórico.
- Próximos passos: conexão com um banco real (PostgreSQL ou MySQL via SQLAlchemy), alerta também por e-mail ou mensagem, histórico de status dos alertas (aberto, em análise, resolvido) e detecção de aumentos anormais e de ruptura de estoque.

## Aprendizados

Projeto desenvolvido durante minha transição da contabilidade para a análise de dados. Ele me fez praticar SQL com funções de janela, automação de rotinas com Python, construção de dashboards e a tradução de um problema operacional em uma solução analítica.

## Autor

**José Ferreira Noronha Neto**  
Contador em transição para Análise de Dados  
[LinkedIn](www.linkedin.com/in/josé-ferreira-noronha-neto-04a49a299) · noronha_ferreira@yahoo.com
