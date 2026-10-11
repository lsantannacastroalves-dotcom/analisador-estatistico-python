"""Funções estatísticas do projeto.

Parte 1: usa statistics, conforme solicitado no enunciado.
Partes 2 e 3: cálculos implementados com lógica e fórmulas próprias.
"""
import csv
import math
import statistics


def ler_dados_terminal():
    """Recebe números separados por vírgula e devolve uma lista de floats."""
    entrada = input("Digite os números separados por vírgula: ").strip()
    if not entrada:
        raise ValueError("Nenhum dado foi informado.")
    try:
        # A entrada usa vírgula como separador; use ponto decimal para números decimais.
        dados = [float(item.strip()) for item in entrada.split(",")]
    except ValueError:
        raise ValueError("Digite números separados por vírgula e use ponto nos decimais. Ex.: 10, 12, 12, 15.5")
    validar_dados(dados)
    return dados


def ler_dados_csv(caminho):
    """Lê valores numéricos de um CSV; aceita uma coluna ou várias células numéricas."""
    dados = []
    with open(caminho, "r", newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.reader(arquivo)
        for numero_linha, linha in enumerate(leitor, start=1):
            for celula in linha:
                valor = celula.strip()
                if not valor:
                    continue
                try:
                    dados.append(float(valor.replace(",", ".")))
                except ValueError:
                    # Permite um cabeçalho textual apenas na primeira linha.
                    if numero_linha == 1 and not dados:
                        continue
                    raise ValueError(
                        f"Valor não numérico na linha {numero_linha}: {valor!r}"
                    )
    validar_dados(dados)
    return dados


def validar_dados(dados):
    if not dados:
        raise ValueError("A lista de dados está vazia.")
    if any(not math.isfinite(x) for x in dados):
        raise ValueError("Todos os valores devem ser números finitos.")


def formatar(numero):
    return f"{numero:.2f}"


def tabela_frequencias(dados):
    """Cria frequência absoluta e acumulada sem usar bibliotecas estatísticas."""
    frequencias = {}
    for valor in dados:
        frequencias[valor] = frequencias.get(valor, 0) + 1
    tabela = []
    acumulada = 0
    for valor in sorted(frequencias):
        fi = frequencias[valor]
        acumulada += fi
        tabela.append((valor, fi, acumulada))
    return tabela


def media_tabela(tabela, n):
    return sum(valor * fi for valor, fi, _ in tabela) / n


def mediana_tabela(tabela, n):
    """Calcula a mediana usando as frequências acumuladas."""
    posicoes = [(n + 1) // 2] if n % 2 else [n // 2, n // 2 + 1]
    valores_centrais = []
    for posicao in posicoes:
        for valor, fi, acumulada in tabela:
            anterior = acumulada - fi
            if anterior < posicao <= acumulada:
                valores_centrais.append(valor)
                break
    return sum(valores_centrais) / len(valores_centrais)


def moda_tabela(tabela):
    maior_frequencia = max(fi for _, fi, _ in tabela)
    return [valor for valor, fi, _ in tabela if fi == maior_frequencia]


def criar_classes(dados):
    """Cria classes pelo critério de Sturges e retorna limites, fi e Fi."""
    n = len(dados)
    minimo, maximo = min(dados), max(dados)
    quantidade = max(1, math.ceil(1 + 3.322 * math.log10(n)))
    amplitude_total = maximo - minimo
    if amplitude_total == 0:
        largura = 1.0
    else:
        largura = amplitude_total / quantidade
    classes = []
    acumulada = 0
    for i in range(quantidade):
        inferior = minimo + i * largura
        superior = minimo + (i + 1) * largura
        if i == quantidade - 1:
            fi = sum(1 for x in dados if inferior <= x <= superior)
        else:
            fi = sum(1 for x in dados if inferior <= x < superior)
        acumulada += fi
        classes.append({
            "inferior": inferior,
            "superior": superior,
            "fi": fi,
            "Fi": acumulada,
            "marca": (inferior + superior) / 2,
        })
    return classes, largura, quantidade


def media_classes(classes, n):
    return sum(classe["marca"] * classe["fi"] for classe in classes) / n


def localizar_classe(classes, posicao):
    """Localiza a classe que contém a posição estatística (1 até n)."""
    for i, classe in enumerate(classes):
        if classe["Fi"] >= posicao and classe["fi"] > 0:
            anterior = classes[i - 1]["Fi"] if i > 0 else 0
            return i, classe, anterior
    # Proteção contra pequenas diferenças de ponto flutuante.
    for i in range(len(classes) - 1, -1, -1):
        if classes[i]["fi"] > 0:
            anterior = classes[i - 1]["Fi"] if i > 0 else 0
            return i, classes[i], anterior
    raise ValueError("Não foi possível localizar uma classe com frequência positiva.")


def quantil_classes(classes, n, proporcao, largura):
    """Interpolação linear: L + ((posição - F anterior) / fi) * h."""
    posicao = n * proporcao
    indice, classe, anterior = localizar_classe(classes, posicao)
    if largura == 0:
        return classe["inferior"]
    return classe["inferior"] + ((posicao - anterior) / classe["fi"]) * largura


def mediana_classes(classes, n, largura):
    return quantil_classes(classes, n, 0.5, largura)


def moda_czuber(classes, largura):
    """Moda agrupada pelo método de Czuber."""
    indice = max(range(len(classes)), key=lambda i: classes[i]["fi"])
    classe = classes[indice]
    if largura == 0:
        return classe["inferior"]
    fm = classe["fi"]
    f_anterior = classes[indice - 1]["fi"] if indice > 0 else 0
    f_seguinte = classes[indice + 1]["fi"] if indice < len(classes) - 1 else 0
    d1 = fm - f_anterior
    d2 = fm - f_seguinte
    if d1 + d2 == 0:
        return (classe["inferior"] + classe["superior"]) / 2
    return classe["inferior"] + (d1 / (d1 + d2)) * largura


def imprimir_tabela_frequencias(tabela):
    print("\nValor (xi) | Freq. Absoluta (fi) | Freq. Acumulada (Fi)")
    print("-" * 57)
    for valor, fi, acumulada in tabela:
        print(f"{valor:10.2f} | {fi:19d} | {acumulada:19d}")


def imprimir_tabela_classes(classes):
    print("\nIntervalo de Classe              | fi | Fi")
    print("-" * 48)
    for i, classe in enumerate(classes):
        fechamento = "]" if i == len(classes) - 1 else ")"
        intervalo = f"[{classe['inferior']:.2f}, {classe['superior']:.2f}{fechamento}"
        print(f"{intervalo:32} | {classe['fi']:2d} | {classe['Fi']:3d}")


def analisar_dados(dados):
    validar_dados(dados)
    n = len(dados)
    print(f"\nArquivo/dados processados com sucesso! (n = {n} elementos)")

    # PARTE 1: statistics é usado somente nesta etapa.
    print("\n" + "-" * 55)
    print("PARTE 1: DADOS NÃO AGRUPADOS (statistics)")
    print("-" * 55)
    print(f"Média:   {formatar(statistics.mean(dados))}")
    print(f"Mediana: {formatar(statistics.median(dados))}")
    try:
        print(f"Moda:    {formatar(statistics.mode(dados))}")
    except statistics.StatisticsError:
        print("Moda:    não foi possível determinar.")

    # PARTE 2: estatísticas calculadas a partir da tabela de frequências.
    print("\n" + "-" * 55)
    print("PARTE 2: FREQUÊNCIA SEM INTERVALO DE CLASSE")
    print("-" * 55)
    tabela = tabela_frequencias(dados)
    imprimir_tabela_frequencias(tabela)
    modas = moda_tabela(tabela)
    moda_texto = ", ".join(formatar(x) for x in modas)
    print(f"\nCalculados pela tabela: Média = {formatar(media_tabela(tabela, n))}")
    print(f"Mediana = {formatar(mediana_tabela(tabela, n))} | Moda = {moda_texto}")

    # PARTE 3: fórmulas implementadas sem statistics, pandas, numpy ou scipy.
    print("\n" + "-" * 55)
    print("PARTE 3: FREQUÊNCIA COM INTERVALO DE CLASSE")
    print("-" * 55)
    classes, largura, quantidade = criar_classes(dados)
    print(f"Quantidade de classes (Sturges): {quantidade}")
    print(f"Amplitude de cada classe: {formatar(largura)}")
    imprimir_tabela_classes(classes)
    print("\nResultados pelas fórmulas para dados agrupados:")
    print(f"Média:   {formatar(media_classes(classes, n))}")
    print(f"Mediana: {formatar(mediana_classes(classes, n, largura))}")
    print(f"Moda (Czuber): {formatar(moda_czuber(classes, largura))}")
    print(f"Quartis: Q1 = {formatar(quantil_classes(classes, n, 0.25, largura))}"
          f" | Q3 = {formatar(quantil_classes(classes, n, 0.75, largura))}")
    print(f"Decis:   D2 = {formatar(quantil_classes(classes, n, 0.20, largura))}"
          f" | D7 = {formatar(quantil_classes(classes, n, 0.70, largura))}")
    print("Percentis: " + " | ".join(
        f"P{p} = {formatar(quantil_classes(classes, n, p / 100, largura))}"
        for p in (15, 22, 63, 70)
    ))
