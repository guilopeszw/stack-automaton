import json
from typing import Dict, Any

class LeitorJson:
    
    def __init__(self):
        self.propriedades = [
            "estados",
            "alfabeto_entrada",
            "alfabeto_pilha",
            "estado_inicial",
            "estados_finais",
            "transicoes"
        ]

    # Função para a validação das propriedades (verificar se todos os atributos estão no JSON)
    def valida_propriedades(self, arquivo: Dict[str, Any]) -> None:
        for propriedade in self.propriedades:
            if propriedade not in arquivo:
                raise ValueError(f"Campo obrigatório '{propriedade}' não encontrado no JSON.")

    def carrega_automato(self, caminho: str) -> Dict[str, Any]:
        try: 
            with open(caminho, "r", encoding="utf-8") as file:
                dados = json.load(file)
            
            self.valida_propriedades(dados)

            # Remover espaços extras nos dados (caso o JSON não esteja limpo)
            dados["estados"] = [estado.strip() for estado in dados["estados"]]
            dados["alfabeto_entrada"] = [simbolo.strip() for simbolo in dados["alfabeto_entrada"]]
            dados["alfabeto_pilha"] = [simbolo.strip() for simbolo in dados["alfabeto_pilha"]]
            dados["estado_inicial"] = dados["estado_inicial"].strip()
            dados["estados_finais"] = [estado.strip() for estado in dados["estados_finais"]]

            # Limpar espaços nas transições
            transicoes_processadas = []

            for transicao in dados["transicoes"]:
                transicao_limpa = {
                    "estado_origem": transicao["estado_origem"].strip(),
                    "leitura": transicao["leitura"].strip(),
                    "topo_pilha": transicao["topo_pilha"].strip(),
                    "substituir_topo": transicao["substituir_topo"].strip(),
                    "estado_destino": transicao["estado_destino"].strip(),
                }
                transicoes_processadas.append(transicao_limpa)

            dados["transicoes"] = transicoes_processadas
            return dados
        
        # Exceções
        except FileNotFoundError:
            raise Exception(f"Arquivo '{caminho}' não foi encontrado.")
        
        except json.JSONDecodeError:
            raise Exception("Erro ao decodificar o arquivo JSON. Verifique se ele está bem formatado.")
        
        except Exception as e:
            raise Exception(f"Erro ao carregar o arquivo: {str(e)}")