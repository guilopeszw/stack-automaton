import json
import sys

from typing import List, Dict, Any, Tuple, Optional

class AutomatoPilha:

    def __init__(self, json_file: str):
        # Elementos
        self.estados = []
        self.alfabeto_entrada = []
        self.alfabeto_pilha = []
        self.estado_inicial = ""
        self.estados_finais = []

        # Transições
        self.transicoes = []
        self.pilha = []
        self.estado_atual = ""
        
        self.carregar_automato(json_file)
        self.validar_automato()
    
    def carregar_automato(self, json_file: str):
        # aqui o autômato é carregado a partir do arquivo JSON
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            self.estados = data.get('estados', [])
            self.alfabeto_entrada = data.get('alfabeto_entrada', [])
            self.alfabeto_pilha = data.get('alfabeto_pilha', [])
            self.estado_inicial = data.get('estado_inicial', '')
            self.estados_finais = data.get('estados_finais', [])
            self.transicoes = data.get('transicoes', [])
            
        except FileNotFoundError:
            raise Exception(f"Arquivo {json_file} não foi encontrado. ")
        
        except json.JSONDecodeError:
            raise Exception("Erro ao decodificar o arquivo JSON. ")
        
        except Exception as e:
            raise Exception(f"Erro ao carregar arquivo: {str(e)}. ")
        
        # colocamos as exceções para garantir que o autômato foi carregado corretamente
    
    def validar_automato(self):
        # aqui, novamente, validamos o autômato para garantir que está correto e consistente com as definições formais.
        if not self.estados:
            raise Exception("Lista de estados não pode estar vazia.") # verifica se a lista de estados está vazia
        
        if not self.alfabeto_entrada:
            raise Exception("Alfabeto de entrada não pode estar vazio.") # verifica se o alfabeto de entrada está vazio
        
        if not self.alfabeto_pilha:
            raise Exception("Alfabeto da pilha não pode estar vazio.") # verifica se o alfabeto da pilha está vazio
        
        if not self.estado_inicial:
            raise Exception("Estado inicial deve ser especificado.") # verifica se o estado inicial está vazio
        
        if not self.estados_finais:
            raise Exception("Pelo menos um estado final deve ser especificado.") # verifica se a lista de estados finais está vazia
        # lembrando que: dentro de qualquer autômato, é obrigatório ter pelo menos um estado inicial, mas não é
        # obrigatório ter estados finais. Porém, para que o autômato aceite alguma cadeia, é necessário que haja pelo menos um estado final.
        

        if self.estado_inicial not in self.estados:
            raise Exception("Estado inicial não está na lista de estados.") # verifica se o estado inicial está na lista de estados
        
        for estado in self.estados_finais:
            if estado not in self.estados:
                raise Exception(f"Estado final '{estado}' não está na lista de estados.") # verifica se os estados finais estão na lista de estados
        
        # aqui vamos validar as transições, para garantir que não temos erros nas transições (inviabilizando o funcionamento do AP)
        for i, transicao in enumerate(self.transicoes):
            if not isinstance(transicao, dict):
                raise Exception(f"Transição {i+1} deve ser um objeto. ") # verifica se a transição é um dicionário
            
            campos_obrigatorios = ['estado_origem', 'leitura', 'topo_pilha', 'substituir_topo', 'estado_destino']
            for campo in campos_obrigatorios:
                if campo not in transicao:
                    raise Exception(f"Campo '{campo}' ausente na transição {i+1}. ") # verifica se todos os campos obrigatórios estão presentes
            
            # Verificar se estados de origem e destino existem
            if transicao['estado_origem'] not in self.estados:
                raise Exception(f"Estado origem '{transicao['estado_origem']}' não existe. ") # verifica se o estado de origem está na lista de estados
            if transicao['estado_destino'] not in self.estados:
                raise Exception(f"Estado destino '{transicao['estado_destino']}' não existe. ") # verifica se o estado de destino está na lista de estados

            # Verificar símbolos do alfabeto (exceto strings vazias)
            if transicao['leitura'] != "" and transicao['leitura'] not in self.alfabeto_entrada:
                raise Exception(f"Símbolo de leitura '{transicao['leitura']}' não está no alfabeto de entrada.") # verifica se o símbolo de leitura está no alfabeto de entrada
            if transicao['topo_pilha'] != "" and transicao['topo_pilha'] not in self.alfabeto_pilha:
                raise Exception(f"Símbolo do topo da pilha '{transicao['topo_pilha']}' não está no alfabeto da pilha.") # verifica se o símbolo do topo da pilha está no alfabeto da pilha
            if transicao['substituir_topo'] != "" and transicao['substituir_topo'] not in self.alfabeto_pilha:
                raise Exception(f"Símbolo de substituição '{transicao['substituir_topo']}' não está no alfabeto da pilha.") # verifica se o símbolo de substituição está no alfabeto da pilha

    def buscar_transicoes(self, estado: str, simbolo_entrada: str, topo_pilha: str) -> List[Dict]:
        # aqui, buscamos as transições válidas a partir do estado atual, símbolo de entrada e topo da pilha
        transicoes_validas = []
        
        for transicao in self.transicoes:
            if (transicao['estado_origem'] == estado and
                (transicao['leitura'] == simbolo_entrada or transicao['leitura'] == "") and
                (transicao['topo_pilha'] == topo_pilha or transicao['topo_pilha'] == "")):
                transicoes_validas.append(transicao)
        
        return transicoes_validas
    
    def executar_transicao(self, transicao: Dict, simbolo_lido: bool):
        """Executa uma transição específica."""
        # aqui, atualizamos o estado atual e a pilha conforme a transição escolhida
        if transicao['topo_pilha'] != "":
            if self.pilha and self.pilha[-1] == transicao['topo_pilha']:
                self.pilha.pop()
        
        if transicao['substituir_topo'] != "":
            self.pilha.append(transicao['substituir_topo'])
        
        # aqui, atualizamos o estado atual do autômato
        self.estado_atual = transicao['estado_destino']
        
        return simbolo_lido or transicao['leitura'] != ""
    
    def simular(self, entrada: str) -> bool:
        # simulamos o autômato de pilha com a entrada fornecida
        self.estado_atual = self.estado_inicial
        self.pilha = []
        posicao = 0
        
        print(f"Simulando entrada: '{entrada}' ")
        print(f"Estado inicial: {self.estado_atual} ")
        print(f"Pilha inicial: {self.pilha} ")
        print(" ")
        
        while True:
            simbolo_atual = entrada[posicao] if posicao < len(entrada) else ""
            topo_pilha = self.pilha[-1] if self.pilha else ""
            
            print(f"Posição: {posicao}, Símbolo: '{simbolo_atual}', Estado: {self.estado_atual}, Pilha: {self.pilha} ")
            
            transicoes_validas = self.buscar_transicoes(self.estado_atual, simbolo_atual, topo_pilha)
            
            if not transicoes_validas:
                # Verificar se é estado final e entrada foi consumida
                if self.estado_atual in self.estados_finais and posicao >= len(entrada):
                    print("ACEITA: Estado final atingido e entrada consumida. ")
                    return True
                else:
                    print("REJEITA: Nenhuma transição válida encontrada. ")
                    return False
            
            # Para simplicidade, usar primeira transição válida (pode ser expandido para não-determinismo)
            transicao = transicoes_validas[0]
            print(f"Transição: {transicao}")
            
            simbolo_consumido = self.executar_transicao(transicao, transicao['leitura'] != "")
            
            if simbolo_consumido:
                posicao += 1
            
            # Verificar se entrada foi totalmente consumida e estamos em estado final
            if posicao >= len(entrada) and self.estado_atual in self.estados_finais:
                print("ACEITA: Estado final atingido e entrada consumida.")
                return True
            
            # Evitar loop infinito
            if posicao > len(entrada) + 100:
                print("REJEITA: Possível loop infinito detectado.")
                return False

def main():
    if len(sys.argv) == 1:
        # se nenhum argumento foi fornecido:
        arquivo_json = input("Digite o caminho do arquivo JSON: ")
        entrada = input("Digite a entrada para simular: ")
    elif len(sys.argv) == 2:
        # se apenas o arquivo JSON foi fornecido
        arquivo_json = sys.argv[1]
        entrada = input("Digite a entrada para simular: ")
    elif len(sys.argv) == 3:
        # se ambos foram fornecidos
        arquivo_json = sys.argv[1]
        entrada = sys.argv[2]
    else:
        print("Uso: python automato_de_pilha.py [arquivo_json] [entrada]")
        print("Ou execute sem parâmetros para entrada interativa")
        return
    
    try:
        automato = AutomatoPilha(arquivo_json)
        resultado = automato.simular(entrada)
        print(f"\nResultado final: {'ACEITA' if resultado else 'REJEITA'}")
        
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()