# Simulador de Autômato de Pilha

Projeto da disciplina **Linguagens Formais e Computabilidade** do curso de **Ciência da Computação (UFPB)**.

Este projeto tem como objetivo simular o processamento de **Autômatos de Pilha (APs)** a partir da leitura de suas descrições formais (em JSON) e a validação de cadeias de entrada.

## Sumário:
1. [Requisitos e execução](#requisitos-e-execução)
2. [Estrutura do projeto](#estrutura-do-projeto)
3. [Formato de Entrada](#requisito-e-formato-de-entrada)
4. Funcionamento e execução do simulador
5. Explorando o código fonte
    
    5.1. Processamento de entrada (`leitor_json`)
    
    5.2. Simulação do automato (`automato_de_pilha`)
    
    5.3 Execução (`main`)

## Requisitos e execução
Antes de tudo, o único pré-requisito necessário para roda o projeto é a presença do python 3 instalado. Todos os módulo usados durante o projeto são módulos base da linguagem.

### Execução
1. Clone o repositório:
```git
git clone git@github.com:guilopeszw/Trabalhos.git
```

2. Vá até o repositório clonado, identifique a pasta geral do projeto e execute o main.py no caminho mãe de todo o projeto.
```bash
cd Formais
python3 src/main.py
```

## Estrutura do projeto
O projeto segue o paradigma de **Programação Orientada a Objetos** utilizando **Python**, com a seguinte estrutura:

```txt
\data
\src
    automato_de_pilha.py
    leitor_json.py
    main.py
alunos.txt
README.md
```
- `/data`: Contém os arquivos .json com a descrição dos autômatos.
- `/src`: Código-fonte principal do projeto.
- `alunos.txt`: Alunos do projeto.
- `README.md`: Documentação.


# Requisitos e Formato de Entrada
O simulador lê a descrição do AP a partir de um arquivo JSON estruturado. Exemplo do arquivo JSON estruturado:

```json
{
  "estados": ["q0", "q1", "q2"],
  "alfabeto_entrada": ["a", "b"],
  "alfabeto_pilha": ["Z", "A"],
  "estado_inicial": "q0",
  "estados_finais": ["q2"],
  "transicoes": [
    {
      "estado_origem": "q0",
      "leitura": "a",
      "topo_pilha": "Z",
      "substituir_topo": "AZ",
      "estado_destino": "q1"
    }
    // Outras transições...
  ]
}
```

Campos obrigatórios:
- `estados`: Lista de todos os estados.
- `alfabeto_entrada`: Símbolos válidos na fita de entrada.
- `alfabeto_pilha`: Símbolos válidos para a pilha.
- `estado_inicial`: Estado de partida.
- `estados_finais`: Lista de estados de aceitação.
- `transicoes`: Lista de transições válidas.

Estrutura de cada transição:
- `estado_origem`: Estado atual.
- `leitura`: Símbolo da fita de entrada (ou `""` para transição épsilon).
- `topo_pilha`: Símbolo esperado no topo da pilha (ou `""`).
- `substituir_topo`: Símbolo(s) a empilhar (ou `""`).
- `estado_destino`: Próximo estado.





# Funcionamento Detalhado da Classe 
A classe AutomatoPilha é o núcleo do simulador.
Função: Construtor da classe. Operação:
1. Inicializa todos os atributos internos (self.estados, self.pilha, self.estado_atual, etc.).
2. Chama self.carregar_automato(json_file) para popular os dados.
3. Chama self.validar_automato() para verificar a consistência dos dados carregados.
Função: Carrega os dados do AP a partir do arquivo JSON especificado. Operação:
1. Abre e decodifica o arquivo JSON.
2. Extrai os valores para todos os atributos do autômato (estados, alfabetos, etc.).
3. Inclui tratamento de exceções para lidar com erros de arquivo não encontrado (FileNotFoundError) ou erros de sintaxe no JSON (json.JSONDecodeError).
Função: Garante que a descrição do AP é formalmente correta e consistente. Este é um requisito obrigatório do projeto ("verificação de erros nos dados de entrada"). Verificações Principais (lançam Exception em caso de falha):
1. Verifica se as listas essenciais (estados, alfabeto_entrada, alfabeto_pilha) estão preenchidas.
2. Garante que o estado_inicial e pelo menos um estados_finais foram especificados.
3. Verifica se o estado_inicial e todos os estados listados em estados_finais existem na lista principal de estados.
4. Validação de Transições: Itera sobre cada transição para garantir:
    ◦ Todos os campos obrigatórios (estado_origem, leitura, topo_pilha, substituir_topo, estado_destino) estão presentes.
    ◦ Estados de origem e destino existem.
    ◦ Símbolos de leitura (se não vazios "") pertencem ao alfabeto_entrada.
    ◦ Símbolos de topo_pilha e substituir_topo (se não vazios "") pertencem ao alfabeto_pilha.
Função: Encontra todas as transições que podem ser executadas a partir da configuração atual do AP. Operação: Filtra a lista self.transicoes buscando aquelas onde:
1. O estado_origem corresponde ao estado atual.
2. O campo leitura corresponde ao simbolo_entrada ou é uma string vazia "" (transição épsilon na fita).
3. O campo topo_pilha corresponde ao topo_pilha atual ou é uma string vazia "" (transição épsilon na pilha).
Função: Aplica as alterações de estado e pilha definidas pela transição escolhida. Operação:
1. Desempilhamento (Pop): Se a transição exige um topo_pilha não vazio e ele está presente, o símbolo é removido (pop) da pilha.
2. Empilhamento (Push): Se o campo substituir_topo não for vazio, o símbolo é adicionado (append) à pilha.
3. O self.estado_atual é atualizado para o estado_destino.
Função: Executa a simulação completa da cadeia de entrada. Lógica:
1. Inicializa o estado atual para estado_inicial e limpa a pilha.
2. Entra em um loop de processamento, imprimindo o estado, símbolo e pilha a cada passo.
3. Busca transições válidas usando buscar_transicoes.
4. Regra de Rejeição/Aceitação (Falha de Transição): Se transicoes_validas estiver vazia, verifica se a entrada foi consumida e se o estado atual é final para determinar ACEITAÇÃO, caso contrário REJEITA.
5. Execução: O código seleciona apenas a primeira transição válida encontrada (transicao = transicoes_validas).
6. Chama executar_transicao e avança a posicao na cadeia apenas se um símbolo da fita foi consumido.
7. Condição de Aceitação (Fim da Cadeia): Se a entrada foi totalmente consumida e o estado_atual é um estados_finais, a cadeia é ACEITA.
8. Prevenção de Loop Infinito: O código implementa uma checagem de segurança; se a posição na fita exceder o comprimento da entrada em 100 caracteres (posicao > len(entrada) + 100), é detectado um possível loop infinito (especialmente útil para transições épsilon) e a cadeia é REJEITADA.
5. Função de Execução ()
A função main gerencia a interação com o usuário através de argumentos de linha de comando (sys.argv).
1. Argumentos:
    ◦ Se nenhum argumento for fornecido, solicita interativamente o caminho do arquivo JSON e a cadeia de entrada.
    ◦ Se apenas o arquivo JSON for fornecido (len(sys.argv) == 2), solicita a cadeia de entrada.
    ◦ Se ambos forem fornecidos (len(sys.argv) == 3), utiliza os argumentos diretamente.
2. Inicialização: Cria a instância de AutomatoPilha e inicia a simulação chamando automato.simular(entrada).
3. Saída: Imprime o Resultado final: ACEITA ou REJEITA, e trata quaisquer exceções que tenham ocorrido durante o carregamento ou simulação.
6. Limitação Crucial e Requisito de Projeto
Simulação de Não-Determinismo:
O projeto exige que o simulador realize a simulação de todas as possíveis formas com que a cadeia pode ser processada.
ATENÇÃO: A implementação atual do método simular seleciona apenas a primeira transição válida encontrada (transicao = transicoes_validas).
Para atender integralmente ao requisito de não-determinismo, que é comum em APs, o código precisa ser modificado para explorar todos os caminhos de transicoes_validas, utilizando técnicas como recursão ou backtracking para testar todas as sequências de processamento e reportar a aceitação se qualquer caminho for bem-sucedido.