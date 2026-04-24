# letterfitting-validacao

## Descrição

Este repositório contém um app desenvolvido com `marimo` para validação de regras de igualdade entre pares de colunas em um conjunto de dados tipográficos (`dados.csv`).

O objetivo é apoiar a revisão de fontes/letterfitting comparando valores de medidas (por exemplo, espaçamento de letras ou métricas de contorno) entre formas que devem ser iguais (p. ex. `Be` vs `He`, `bd` vs `nd`).

## Como funciona

1. Lê `dados.csv` com `pandas`.
2. Converte para numérico as colunas relevantes, usando coercion para valores não numéricos.
3. Filtra as linhas em que `manter_na_analise? == 'Sim'`.
4. Define regras de igualdade (`regras_raw`) como tuplas `(alvo, referencia, descrição)`:
   - letras maiúsculas: comparações baseadas em referência visual (ex. `B` com `H`, `C` com `O`).
   - letras minúsculas: comparações pareadas (ex. `bd` com `nd`, `ce` com `oe`).
5. Ordena as regras para exibição no dropdown.
6. Cria interface interativa `marimo`:
   - dropdown com cada regra de igualdade
   - ao escolher, calcula diferença entre `alvo` e `referencia` somente onde ambos existem
   - mostra histograma das diferenças com linha ideal (0) e linha da média real
   - informa média e número de observações

## Como executar

Pré-requisitos:
- Python 3.x
- bibliotecas: `pandas`, `plotly`, `marimo`

Exemplo:

```bash
pip install pandas plotly marimo
marimo run app.py
```

Em seguida, acesse a interface gerada pelo app (normalmente em `localhost:port`) e selecione uma regra.

## Estrutura do `app.py`

- `app = marimo.App(width="medium")`: define a app e tamanho da interface.
- `@app.cell def _():` bloco inicial (carregamento + UI) retorna `df_analise`, `mo`, `px`, `selecao`.
- Segundo bloco usa `selecao.value` para analisar a regra escolhida.
- Cria `fig = px.histogram(...)` e configura layout com escala simétrica em torno de 0.
- `mo.vstack` e `mo.hstack` montam a visualização com texto, estatísticas e gráfico.

## Observações

- O script presume que `dados.csv` tem colunas nomeadas como no `colunas_iguais` e a coluna de filtro `manter_na_analise?`.
- Caso as colunas não existam no CSV, elas são ignoradas na conversão numérica.
- Regras podem ser ajustadas pelo usuário em `regras_raw` para outros pares de comparação.

## Novas implementações

- Inseri no README uma explicação completa linha-a-linha do fluxo do `app.py`.
- Descrevi as regras tratadas atualmente (maiúsculas e minúsculas) e o mecanismo de ordenação/seleção.
- Atualizei o passo de interface para explicar o histograma e as linhas de referência 0 (Tracy) e média real (vermelha tracejada).
- Adicionei instruções de instalação e execução do app (`pip install ...`, `python app.py`).
- Incluí detalhes de layout `marimo` (`mo.vstack`, `mo.hstack`), cálculo de diferenças e estatísticas exibidas.

