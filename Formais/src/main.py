from leitor_json import LeitorJson
from automato_de_pilha import AutomatoDePilha
from typing import Optional

def main():
    menu = """==== Simulador de autômato de pilha ====
    [1] Importar e validar autômato de pilha (.json)
    [2] Processar cadeia
    [0] Sair\n"""

    automato = None # Armazena a instância do autômato

    # Fluxo de execução
    while True:
        print(menu)
        escolha = input(">: ")

        # 0 -> Fecha
        # 1 -> Importa JSON
        # 2 -> Processa cadeia
        match escolha:
            case "0":
                print("Fim de execução.")
                break
            
            case "1":
                novo_automato = importa_automato()
                if novo_automato:
                    automato = novo_automato
                    processa_cadeia(automato)
            
            case "2":
                if automato is None:
                    print("Erro: Nenhum autômato carregado. Importe antes de processar cadeias!\n")

                else:
                    processa_cadeia(automato)

            case _:
                print("Opção inválida! Tente novamente.\n")

# Método de chamada da importação do autômato
def importa_automato() -> Optional[AutomatoDePilha]:

    while True:
        print("==== Importação do autômato ==== ")
        caminho_arquivo = input("Caminho do arquivo .json (ou 0 para voltar): ")
        print()

        if (caminho_arquivo == "0"):
            return None

        try:
            leitor = LeitorJson()
            data = leitor.carrega_automato(caminho_arquivo)
            print("Autômato carregado com sucesso!")

            automato = AutomatoDePilha(data)
            automato.validar_estrutura()
            print("Autômato validado com sucesso!\n")
            return automato
        
        except Exception as e:
            print(f"Erro ao importar / validar autômato: {e}\n")

# Método de chamada do processaamento da cadeia 
def processa_cadeia(automato: AutomatoDePilha) -> None:

    while True:
        print("==== Processamento de cadeias ====")
        cadeia = input("Insira a cadeia que deseja processar (ou 0 para voltar): ")
        print()

        if cadeia == "0":
            return None

        try:
            resultado = automato.simular_nao_deterministico(cadeia)
        
        except Exception as e:
            print(f"Erro ao processar cadeia: {e}\n")

if __name__ == "__main__":
    main()