# Simulador de Autômato de Pilha

Projeto da disciplina **Linguagens Formais e Computabilidade** do curso de **Ciência da Computação (UFPB)**.

Este projeto tem como objetivo simular o processamento de **Autômatos de Pilha (APs)** a partir da leitura de suas descrições formais (em JSON) e a validação de cadeias de entrada.

## Sumário:
1. [Requisitos e execução](#requisitos-e-execução)

    1.1 [Requisitos](#requisitos)

    1.2 [Como Executar o projeto](#como-executar-o-projeto)

2. [Estrutura do projeto](#estrutura-do-projeto)

    2.1 [Estrutura JSON](#estrutura-json)

      2.1.1 [Estrutura de cada transição](#estrutura-de-cada-transição)

3. [Formato de Entrada](#requisito-e-formato-de-entrada)
4. [Explorando o código fonte](#explorando-o-código-fonte)
    
    4.1. [Processamento de entrada (`leitor_json`)](#processamento-de-entrada-leitor_json)
    
    4.2. [Simulação do automato (`automato_de_pilha`)](#simulação-do-autômato-automato_de_pilha)
  
    4.3 [Execução (`main`)](#execução-main)

## Requisitos e execução
### Requisitos
O único pré-requisito para rodar este projeto é ter o Python 3 instalado.
> Todos os módulos utilizados fazem parte da biblioteca padrão da linguagem, portanto não é necessário instalar dependências extras.


### Como executar o projeto
1. Clone o repositório:
```git
git clone git@github.com:guilopeszw/Trabalhos.git
```

2. Acesse a pasta do projeto: 
```bash
cd Trabalhos/Formais
```

3. Execute o programa principal:
```bash
python3 src/main.py
```
> ! Certifique-se de executar o main.py a partir do diretório raiz do projeto (Formais).

## Estrutura do projeto
O projeto segue o paradigma de **Programação Orientada a Objetos** utilizando **Python**, com a seguinte estrutura:

```txt
Formais
├── data/                  
├── src/                   
│   ├── automato_de_pilha.py
│   ├── leitor_json.py
│   └── main.py
├── alunos.txt            
└── README.md      
```
- `data`: Arquivos .json com a descrição dos autômatos.
- `src`: Código-fonte principal.
- `alunos.txt`: Alunos do projeto.
- `README.md`: Documentação.

## Requisitos e Formato de Entrada
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
### Estrutura JSON
- `estados`: Lista de todos os estados.
- `alfabeto_entrada`: Símbolos válidos na fita de entrada.
- `alfabeto_pilha`: Símbolos válidos para a pilha.
- `estado_inicial`: Estado de partida.
- `estados_finais`: Lista de estados de aceitação.
- `transicoes`: Lista de transições válidas.

#### Estrutura de cada transição:
- `estado_origem`: Estado atual.
- `leitura`: Símbolo da fita de entrada (ou `""` para transição épsilon).
- `topo_pilha`: Símbolo esperado no topo da pilha (ou `""`).
- `substituir_topo`: Símbolo(s) a empilhar (ou `""`).
- `estado_destino`: Próximo estado.

## Explorando o código fonte

### Processamento de entrada (`leitor_json`)
A classe LeitorJson é responsável por carregar e validar a definição do autômato a partir de um arquivo .json. Seu funcionamento ocorre em três etapas principais:
1. Recebimento do caminho do arquivo: recebe como entrada o caminho para o .json que descreve o autômato.
2. Validação da estrutura: após abrir o arquivo, verifica se todos os campos obrigatórios que definem as propriedades do autômato estão presentes.
3. Extração dos dados: retorna os dados do autômato prontos para serem utilizados na simulação.

> ! Importante: toda a lógica de leitura está envolta em blocos de tratamento de exceções. Caso o arquivo seja inválido ou malformado, a exceção é lançada e tratada diretamente no main, garantindo que a execução não seja interrompida abruptamente e facilitando a identificação de erros de entrada.

### Simulação do autômato (`automato_de_pilha`)

### Execução (`main`)
O arquivo main.py funciona como ponto de entrada do programa e gerenciador do fluxo de execução. Ele apresenta um menu interativo que organiza as principais funcionalidades:

1. `main()`: 
    - Exibe o menu inicial.
    - Controla o fluxo da aplicação via laços de repetição (while True).
    - Encaminha a execução para os métodos correspondentes à opção escolhida pelo usuário:
      - [1] Importar autômato de pilha.
      - [2] Validar/processar cadeia.
      - [0] Encerrar programa.

2. `importa_automato()`
    - Instancia a classe LeitorJson e realiza a leitura de um arquivo .json.
    - Caso o arquivo seja válido, inicializa o objeto AutomatoDePilha.
    - Em caso de erro, apresenta mensagens claras ao usuário sem interromper o programa.

3. `processa_cadeia()`
    - Recebe a cadeia digitada pelo usuário e a submete ao AutomatoDePilha.
    - Exibe de forma clara se a cadeia foi aceita ou rejeitada.
    - Caso nenhum autômato tenha sido importado antes, emite um aviso para que o usuário realize a importação primeiro.

> O `main` funciona como uma camada de interface textual entre o usuário e a lógica interna do projeto, centralizando o tratamento de exceções e mantendo a execução contínua mesmo diante de entradas inválidas.
