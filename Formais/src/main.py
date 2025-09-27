from leitor_json import LeitorJson

def main():
    leitor = LeitorJson()

    try:
        dados = leitor.carrega_automato("data/dataap.json")
        print("Autômato carregado com sucesso!")
        print(dados)

    except Exception as erro:
        print(f"[ERRO] Falha ao carregar o autômato: {erro}")

if __name__ == "__main__":
    main()