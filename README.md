# 🚗 FIPE Automation Bot (Dual Mode)

> Um robô robusto em Python para consulta automatizada de preços de veículos na Tabela FIPE, apresentando múltiplas estratégias de busca e persistência de dados.

## 📋 Sobre o Projeto

Este projeto é uma solução de **RPA (Robotic Process Automation)** desenvolvida com foco em Engenharia de Software e performance. Ele automatiza a extração de dados do site oficial da FIPE.

O grande diferencial desta versão é a implementação de **duas estratégias de busca distintas**, demonstrando versatilidade técnica:

1. **Busca Inteligente (O(1)):** Utiliza a injeção de texto e simulação de teclado (`ENTER`) para filtrar resultados instantaneamente.
2. **Busca Sequencial (O(N)):** Navega através da iteração de índices da lista, útil para varreduras completas ou quando o nome exato é desconhecido.

---

## 🚀 Destaques Técnicos

* **Arquitetura Híbrida de Busca:** Implementação de polimorfismo na estratégia de seleção (`consultar_carro_pesquisa` vs `consultar_carro_index`).
* **CLI Interativa:** Menu no terminal que permite ao usuário escolher o modo de operação em tempo de execução.
* **Persistência Incremental:** Sistema inteligente que lê o arquivo JSON existente e adiciona novos registros (append) sem sobrescrever o histórico.
* **Resiliência e Logging:** Monitoramento completo via Logs (Arquivo + Console) e sistema de **Auto-Screenshot** em caso de falhas, facilitando o debugging.
* **POO & Clean Code:** Código modularizado na classe `FipeBot`, seguindo princípios de responsabilidade única.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Automação:** Selenium WebDriver (EdgeDriver)
* **Manipulação de Dados:** JSON
* **Sistema:** OS, Datetime, Time, Logging

---

## ⚙️ Instalação e Configuração

### Pré-requisitos

* Python 3 instalado.
* Navegador Microsoft Edge instalado.

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/SEU-USUARIO/tabela-FIPE.git
cd tabela-FIPE

```


2. **Crie o ambiente virtual:**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

```


3. **Instale as dependências:**
```bash
pip install -r requirements.txt

```



---

## 💻 Como Usar

Execute o arquivo principal:

```bash
python fipe_pro.py

```

O programa abrirá um **Menu Interativo** no terminal:

```text
------------------------------
🤖 FIPE BOT - SELECIONE O MODO
1 - Pesquisa Inteligente (Por Texto - Rápido)
2 - Pesquisa Sequencial (Por Posição/Index)
------------------------------
Digite o número da opção (1 ou 2): 

```

### Opção 1: Pesquisa Inteligente (Recomendada)

Ideal quando você sabe exatamente o nome do carro. É extremamente rápida.

* *Configuração:* Edite a lista `parametros` dentro do bloco `if modo == "1"` no código.
* *Exemplo:* `["dezembro/2025", "Alfa Romeo", "145 Quadrifoglio 2.0", "1998 Gasolina"]`

### Opção 2: Pesquisa Sequencial

Ideal para testes de varredura ou quando se quer pegar "o primeiro da lista".

* *Configuração:* Edite a lista `indices_busca` dentro do bloco `elif modo == "2"`.
* *Exemplo:* `[0, 12, 1, 0]` (Seleciona o 1º Mês, a 13ª Marca, o 2º Modelo, etc).

---

## 📂 Estrutura do Projeto

```text
tabela-FIPE/
│
├── erros/                 # Screenshots de falhas (Gerado automaticamente)
├── venv/                  # Ambiente Virtual
├── fipe_pro.py            # Código fonte principal (Classe FipeBot)
├── fipe_resultado.json    # Banco de dados (Histórico de consultas)
├── robo_fipe.log          # Arquivo de logs técnicos
└── README.md              # Documentação

```

---

## 👤 Autor

**Isabela Firmino**