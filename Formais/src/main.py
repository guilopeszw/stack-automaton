from leitor_json import LeitorJson
from automato_de_pilha import AutomatoDePilha

def main():
    leitor = LeitorJson()

    try:
        dados = leitor.carrega_automato("data/dataap.json")
        print("Autômato carregado com sucesso!")
        
        automato = AutomatoDePilha(dados)
        automato.validar_estrutura()
        print("Autômato validado com sucesso!")


    except Exception as erro:
        print(f"[ERRO] Falha ao carregar o autômato: {erro}")

if __name__ == "__main__":
    main()