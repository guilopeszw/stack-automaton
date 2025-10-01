from typing import List, Dict
from collections import deque
from copy import deepcopy

class AutomatoDePilha:

    # Construtor (Recebe as própriedades da instância da classe leitor_json)
    def __init__(self, data) -> None:

        self.estados = data["estados"]
        self.alfabeto_entrada = data["alfabeto_entrada"]
        self.alfabeto_pilha = data["alfabeto_pilha"]
        self.estado_inicial = data["estado_inicial"]
        self.estados_finais = data["estados_finais"]
        self.transicoes = data["transicoes"]

        self.pilha = []
        self.estado_atual = self.estado_inicial
    
    # Valida os atributos do autômato
    def validar_estrutura(self) -> None:
        
        if not self.estados:
            raise Exception("Lista de estados não pode estar vazia.")
        
        if not self.alfabeto_pilha:
            raise Exception("Alfabeto da pilha não pode estar vazio.")
        
        if not self.estado_inicial:
            raise Exception("Estado inicial deve ser especificado.")
        
        if not self.estados_finais:
            raise Exception("Pelo menos um estado final deve ser especificado.")

        if self.estado_inicial not in self.estados:
            raise Exception("Estado inicial não está na lista de estados.") 
        
        for estado in self.estados_finais:
            if estado not in self.estados:
                raise Exception(f"Estado final '{estado}' não está na lista de estados.")
        
        # Validando transições
        for i, transicao in enumerate(self.transicoes):
            if not isinstance(transicao, dict):
                raise Exception(f"Transição {i+1} deve ser um objeto. ") 
            
            if transicao['estado_origem'] not in self.estados:
                raise Exception(f"Estado origem '{transicao['estado_origem']}' não existe. ")
            
            if transicao['estado_destino'] not in self.estados:
                raise Exception(f"Estado destino '{transicao['estado_destino']}' não existe. ")

            # Verificar símbolos do alfabeto
            if transicao['leitura'] != "" and transicao['leitura'] not in self.alfabeto_entrada:
                raise Exception(f"Símbolo de leitura '{transicao['leitura']}' não está no alfabeto de entrada.") # verifica se o símbolo de leitura está no alfabeto de entrada
            
            if transicao['topo_pilha'] != "" and transicao['topo_pilha'] not in self.alfabeto_pilha:
                raise Exception(f"Símbolo do topo da pilha '{transicao['topo_pilha']}' não está no alfabeto da pilha.") # verifica se o símbolo do topo da pilha está no alfabeto da pilha
            
            if transicao['substituir_topo'] != "" and transicao['substituir_topo'] not in self.alfabeto_pilha:
                raise Exception(f"Símbolo de substituição '{transicao['substituir_topo']}' não está no alfabeto da pilha.") # verifica se o símbolo de substituição está no alfabeto da pilha
    

    # busca as transições possíveis a partir do estado atual
    def buscar_transicoes(self, estado: str, simbolo_entrada: str, topo_pilha: str) -> List[Dict]:
        # aqui, buscamos as transições válidas a partir do estado atual, símbolo de entrada e topo da pilha
        transicoes_validas = []
        
        for transicao in self.transicoes:
            # Verifica se está no mesmo estado da transição
            # É transição vazia ou o simbolo da entrada é o mesmo da leitura
            # Topo da pilha é vazia ou o simbolo esperado conincide com o simbolo esperado na transição
            if (transicao['estado_origem'] == estado and 
                (transicao['leitura'] == simbolo_entrada or transicao['leitura'] == "") and 
                (transicao['topo_pilha'] == topo_pilha or transicao['topo_pilha'] == "")):
                transicoes_validas.append(transicao)
        
        return transicoes_validas
            
    def simular_nao_deterministico(self, entrada: str, limite_passos: int = 500):
        # Fila para BFS
        fila = deque()

        # Elemento da fila composto por ->(estado_atual, posicao, pilha, caminho, passos)
        fila.append((self.estado_inicial, 0, [], [], 0))

        # Lista de processamentos
        resultados = []

        while fila:
            # Desenfileira um nó
            estado, posicao, pilha, caminho, passos = fila.popleft()

            # Verificação do limite
            if passos >= limite_passos:
                resultados.append((caminho, "LIMITE ATINGIDO"))
                continue

            simbolo_atual = entrada[posicao] if posicao < len(entrada) else ""
            topo_pilha = pilha[-1] if pilha else ""

            # Busca as transicoes validas 
            transicoes_validas = self.buscar_transicoes(estado, simbolo_atual, topo_pilha)

            # Verifica a aceitação
            if not transicoes_validas:
                # Aceita somente se estiver em estado_final e toda a entrada foi consumida
                if estado in self.estados_finais and posicao >= len(entrada):
                    resultados.append((caminho, "ACEITA"))

                else:
                    resultados.append((caminho, "REJEITA"))

                continue

            # Expandir cada transição válida
            for transicao in transicoes_validas:
                novo_estado = transicao["estado_destino"]
                nova_pilha = deepcopy(pilha) # pilhas independentes para os caminhos

                # Atualiza pilha
                if transicao["topo_pilha"]:

                    # Se a transição exige um símbolo específico no topo, verifica se remove ele
                    if nova_pilha and nova_pilha[-1] == transicao["topo_pilha"]:
                        nova_pilha.pop()

                    else:
                        continue

                if transicao["substituir_topo"]:
                    for s in reversed(transicao["substituir_topo"]):
                        nova_pilha.append(s)

                # Se a transição consome símbolo (leitura != ""), avança posicao em 1; caso contrário (episilon), não avança.
                nova_posicao = posicao + (1 if transicao["leitura"] else 0)
                novo_caminho = caminho + [(posicao, simbolo_atual, estado, list(pilha), transicao)]

                fila.append((novo_estado, nova_posicao, nova_pilha, novo_caminho, passos + 1))

        # Mostrar resultados
        for caminho, resultado in resultados:
            print("\n=== Novo processamento ===")

            for passo in caminho:
                pos, simbolo, estado, pilha_antiga, trans = passo
                print(f"Posição={pos}, Símbolo='{simbolo}', Estado={estado}, Pilha={pilha_antiga}, Transição={trans}")

            print("Resultado:", resultado)
            print()
