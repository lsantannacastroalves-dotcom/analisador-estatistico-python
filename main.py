"""Ponto de entrada do Analisador Estatístico."""
import csv
from estatistica import ler_dados_terminal, ler_dados_csv, analisar_dados


def main():
    print("=" * 55)
    print("          ANALISADOR ESTATÍSTICO EM PYTHON")
    print("=" * 55)
    print("[1] Inserir dados via terminal (separados por vírgula)")
    print("[2] Carregar arquivo CSV")
    opcao = input("\nEscolha uma opção: ").strip()

    try:
        if opcao == "1":
            dados = ler_dados_terminal()
        elif opcao == "2":
            caminho = input("Caminho do arquivo CSV (ex.: dados.csv): ").strip()
            dados = ler_dados_csv(caminho)
        else:
            print("Opção inválida. Escolha 1 ou 2.")
            return

        analisar_dados(dados)
    except (ValueError, OSError, csv.Error) as erro:
        print(f"\nNão foi possível processar os dados: {erro}")
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")


if __name__ == "__main__":
    main()
