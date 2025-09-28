from leitor_json import LeitorJson
from automato_de_pilha import AutomatoDePilha
from typing import Optional

def main():
    menu = """==== Simulador de autômato de pilha ====
    [1] Importar e validar autômato de pilha (.json)
    [2] Processar cadeia
    [0] Sair\n"""

    automato = None # Armazena a instância do autômato

    while True:
        print(menu)
        escolha = input(">: ")

        match escolha:
            case "0":
                print("Fim de execução.")
                break
            
            case "1":
                novo_automato = importa_automato()
                if novo_automato:
                    automato = novo_automato
            
            case "2":
                if automato is None:
                    print("Erro: Nenhum autômato carregado. Importe antes de processar cadeias!\n")

                else:
                    processa_cadeia(automato)

            case _:
                print("Opção inválida! Tente novamente.\n")
    
def importa_automato() -> Optional[AutomatoDePilha]:

    while True:
        print("==== Importação do autômato ==== ")
        caminho_arquivo = input("Caminho do arquivo .json (ou 0 para voltar): \n")

        if (caminho_arquivo == "0"):
            return None

        try:
            leitor = LeitorJson()
            data = leitor.carrega_automato(caminho_arquivo)
            print("Autômato carregado com sucesso!\n")

            automato = AutomatoDePilha(data)
            automato.validar_estrutura()
            print("Autômato validado com sucesso!")
            return automato
        
        except Exception as e:
            print(f"Erro ao importar / validar autômato: {e}\n")

def processa_cadeia(automato: AutomatoDePilha) -> None:
    print("==== Processamento de cadeias ====")
    cadeia = input("Insira a cadeia que deseja processar: ")

    try:
        resultado = automato.simular(cadeia)
        if resultado:
            print("Resultado: Cadeia ACEITA pelo autômato.\n")
        
        else:
            print("Resultado: Cadeia REJEITADA pelo autômato.\n")
    
    except Exception as e:
        print(f"Erro ao processar cadeia: {e}\n")

if __name__ == "__main__":
    main()