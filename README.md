# Analisador Estatístico em Python

Projeto para a disciplina de **Probabilidade e Estatística**. O programa recebe números pelo terminal ou por um arquivo CSV e apresenta medidas estatísticas em três níveis de organização dos dados.

## Funcionalidades

1. **Dados não agrupados:** média, mediana e moda com a biblioteca padrão `statistics`.
2. **Dados agrupados sem intervalos:** tabela de frequência absoluta e acumulada; média, mediana e moda calculadas a partir da tabela.
3. **Dados agrupados em intervalos:** classes calculadas pelo critério de Sturges, amplitude, frequências, média, mediana, moda pelo método de Czuber, Q1, Q3, D2, D7, P15, P22, P63 e P70. As fórmulas desta etapa são implementadas no próprio código, sem bibliotecas estatísticas.

## Arquivos

- `main.py`: menu e execução do programa.
- `estatistica.py`: entrada dos dados, tabelas e cálculos.
- `dados.csv`: conjunto de dados de exemplo.
- `relatorio.pdf`: relatório técnico do projeto.

## Como executar

É necessário ter Python 3 instalado.

1. Baixe os arquivos deste repositório.
2. Abra um terminal na pasta do projeto.
3. Execute:

```bash
python main.py
```

Em alguns sistemas, o comando pode ser `python3 main.py`.

Escolha a opção 1 para digitar números separados por vírgula, por exemplo `10, 12, 12, 15, 20`. Use ponto para casas decimais, por exemplo `15.5`. Escolha a opção 2 para informar o caminho do CSV, como `dados.csv`.

## Integrantes

Cauã puello, Caio rocha, gustavo rocha, joão vitor santos, Lucas santanna 

## Observação

As medidas da Parte 3 são estimativas para dados agrupados e são calculadas por interpolação dentro das classes. Confirme com o professor se a turma utiliza uma convenção específica para o posicionamento de quartis, decis e percentis.
