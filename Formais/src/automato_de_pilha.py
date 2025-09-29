
import sys
import json
from typing import List, Dict, Tuple, Set

class AutomatoDePilha:
    def __init__(self, data) -> None:
        # inicializa o automato com os dados do arquivo json
        self.estados = data["estados"]
        self.alfabeto_entrada = data["alfabeto_entrada"]
        self.alfabeto_pilha = data["alfabeto_pilha"]
        self.estado_inicial = data["estado_inicial"]
        self.estados_finais = data["estados_finais"]
        self.transicoes = data["transicoes"]

    def validar_estrutura(self) -> None:
        # verifica se todos os campos obrigatórios estão preenchidos
        if not self.estados:
            raise Exception("Lista de estados não pode estar vazia.")
        if not self.alfabeto_pilha:
            raise Exception("Alfabeto da pilha não pode estar vazio.")
        if not self.estado_inicial:
            raise Exception("Estado inicial deve ser especificado.")
        if not self.estados_finais:
            raise Exception("Pelo menos um estado final deve ser especificado.")

        # verifica se os estados inicial e finais existem na lista de estados
        if self.estado_inicial not in self.estados:
            raise Exception("Estado inicial não está na lista de estados.")
        for estado in self.estados_finais:
            if estado not in self.estados:
                raise Exception(f"Estado final '{estado}' não está na lista de estados.")

        # verifica se todas as transições são válidas
        for i, transicao in enumerate(self.transicoes):
            if not isinstance(transicao, dict):
                raise Exception(f"Transição {i+1} deve ser um objeto.")

            # verifica se os estados de origem e destino existem
            if transicao['estado_origem'] not in self.estados:
                raise Exception(f"Estado origem '{transicao['estado_origem']}' não existe.")
            if transicao['estado_destino'] not in self.estados:
                raise Exception(f"Estado destino '{transicao['estado_destino']}' não existe.")

            # verifica se os símbolos usados estão nos alfabetos corretos
            if transicao['leitura'] != "" and transicao['leitura'] not in self.alfabeto_entrada:
                raise Exception(f"Símbolo de leitura '{transicao['leitura']}' não está no alfabeto de entrada.")
            if transicao['topo_pilha'] != "" and transicao['topo_pilha'] not in self.alfabeto_pilha:
                raise Exception(f"Símbolo do topo da pilha '{transicao['topo_pilha']}' não está no alfabeto da pilha.")
            if transicao['substituir_topo'] != "" and transicao['substituir_topo'] not in self.alfabeto_pilha:
                raise Exception(f"Símbolo de substituição '{transicao['substituir_topo']}' não está no alfabeto da pilha.")

    def buscar_transicoes(self, estado: str, simbolo_entrada: str, topo_pilha: str) -> List[Dict]:
        # encontra todas as transições possíveis a partir do estado atual
        transicoes_validas = []
        for transicao in self.transicoes:
            # verifica se a transição pode ser executada com os parâmetros atuais
            if (transicao['estado_origem'] == estado and
                (transicao['leitura'] == simbolo_entrada or transicao['leitura'] == "") and
                (transicao['topo_pilha'] == topo_pilha or transicao['topo_pilha'] == "")):
                transicoes_validas.append(transicao)
        return transicoes_validas

    def executar_transicao(self, transicao: Dict, pilha: List[str]) -> List[str]:
        # aplica uma transição na pilha e retorna a nova pilha
        nova_pilha = pilha.copy()
        # remove o símbolo do topo se especificado na transição
        if transicao['topo_pilha'] != "":
            if nova_pilha and nova_pilha[-1] == transicao['topo_pilha']:
                nova_pilha.pop()
        # adiciona o novo símbolo no topo se especificado
        if transicao['substituir_topo'] != "":
            nova_pilha.append(transicao['substituir_topo'])
        return nova_pilha

    def simular(self, entrada: str) -> None:
        print(f"\nSimulando entrada: '{entrada}'\n")

        # configuração inicial: (estado, posição na entrada, pilha, histórico)
        configuracao_inicial = (self.estado_inicial, 0, [], [])
        caminhos_aceitos = []
        caminhos_rejeitados = []

        # controla quais configurações já foram visitadas para evitar loops infinitos
        visitados: Set[Tuple[str, int, Tuple[str]]] = set()
        # pilha para explorar todas as possibilidades (busca em profundidade)
        pilha_execucao = [configuracao_inicial]

        while pilha_execucao:
            estado_atual, posicao, pilha_atual, historico = pilha_execucao.pop()

            # verifica se já visitamos esta configuração
            config_key = (estado_atual, posicao, tuple(pilha_atual))
            if config_key in visitados:
                continue
            visitados.add(config_key)

            # obtém o símbolo atual da entrada e o topo da pilha
            simbolo_atual = entrada[posicao] if posicao < len(entrada) else ""
            topo_pilha = pilha_atual[-1] if pilha_atual else ""

            # busca transições possíveis
            transicoes = self.buscar_transicoes(estado_atual, simbolo_atual, topo_pilha)

            # se não há transições possíveis, verifica se aceita ou rejeita
            if not transicoes:
                if posicao >= len(entrada) and estado_atual in self.estados_finais:
                    caminhos_aceitos.append(historico + [(estado_atual, posicao, pilha_atual.copy())])
                else:
                    caminhos_rejeitados.append(historico + [(estado_atual, posicao, pilha_atual.copy())])
                continue

            # para cada transição possível, cria uma nova configuração
            for transicao in transicoes:
                nova_pilha = self.executar_transicao(transicao, pilha_atual)
                novo_estado = transicao['estado_destino']
                # avança na entrada apenas se a transição consome um símbolo
                novo_pos = posicao + (1 if transicao['leitura'] != "" else 0)
                novo_historico = historico + [(estado_atual, posicao, pilha_atual.copy(), transicao)]
                pilha_execucao.append((novo_estado, novo_pos, nova_pilha, novo_historico))

        # mostra todos os caminhos que levaram à aceitação
        for i, caminho in enumerate(caminhos_aceitos, 1):
            print(f"\nCaminho ACEITO {i}:")
            for passo in caminho:
                if len(passo) == 4:
                    estado, pos, pilha, transicao = passo
                    print(f" Estado: {estado}, Pos: {pos}, Pilha: {pilha}, Transição: {transicao}")
                else:
                    estado, pos, pilha = passo
                    print(f" Estado: {estado}, Pos: {pos}, Pilha: {pilha}")
        
        # mostra todos os caminhos que levaram à rejeição
        for i, caminho in enumerate(caminhos_rejeitados, 1):
            print(f"\nCaminho REJEITADO {i}:")
            for passo in caminho:
                if len(passo) == 4:
                    estado, pos, pilha, transicao = passo
                    print(f" Estado: {estado}, Pos: {pos}, Pilha: {pilha}, Transição: {transicao}")
                else:
                    estado, pos, pilha = passo
                    print(f" Estado: {estado}, Pos: {pos}, Pilha: {pilha}")

        print(f"\nResumo: {len(caminhos_aceitos)} aceito(s), {len(caminhos_rejeitados)} rejeitado(s).")


if __name__ == "__main__":0
    # verifica se o arquivo foi passado como argumento
    if len(sys.argv) < 2:
            print("Uso: python automato_de_pilha.py <arquivo.json>")
        sys.exit(1)

    # carrega os dados do automato do arquivo json
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    # cria e valida o automato
    ap = AutomatoDePilha(data)
    ap.validar_estrutura()

    # pede a entrada do usuário e simula o automato
    cadeia = input("Digite a cadeia de entrada: ")
    ap.simular(cadeia)

