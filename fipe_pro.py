# --- IMPORTAÇÃO DE BIBLIOTECAS ---
import json 
import logging  
import os 
from datetime import datetime  
from time import sleep 

# Importações do Selenium (a ferramenta de automação)
from selenium import webdriver
from selenium.webdriver.common.by import By  # Para localizar elementos (por ID, XPATH, etc)
from selenium.webdriver.support.ui import WebDriverWait  # Para esperar elementos carregarem
from selenium.webdriver.support import expected_conditions as EC  # Condições de espera (ex: estar clicável)
from selenium.webdriver.edge.options import Options  # Para configurar o navegador Edge

# --- CONFIGURAÇÃO DE LOGS ---
# Aqui definimos que o robô vai escrever o que faz tanto num arquivo .log quanto na tela preta.
logging.basicConfig(
    level=logging.INFO,  # Nível de detalhe (INFO mostra o básico, DEBUG mostraria tudo)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato: Data - Nível - Mensagem
    handlers=[
        logging.FileHandler("robo_fipe.log"),  # Salva num arquivo de texto
        logging.StreamHandler()  # Mostra no terminal
    ]
)

# --- CLASSE DO ROBÔ ---
class FipeBot:
    def __init__(self, headless=False):
        """
        Método Construtor: Executado automaticamente quando criamos o robô.
        :param headless: Se True, o navegador roda escondido (sem janela).
        """
        self.url = "https://veiculos.fipe.org.br/"
        # Chama a função interna que abre o navegador
        self.driver = self._iniciar_driver(headless)
        # Cria um 'vigia' que espera até 20 segundos pelos elementos aparecerem
        self.wait = WebDriverWait(self.driver, 20)

    def _iniciar_driver(self, headless):
        """ Configura e abre o navegador Edge. """
        logging.info("Iniciando configurações do navegador...")
        options = Options()
        
        # Se headless for True, ativa o modo fantasma (bom para servidores)
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        
        # Truque para sites não detectarem facilmente que é um robô
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Retorna o navegador aberto
        return webdriver.Edge(options=options)

    def _tirar_screenshot(self, nome_erro):
        """ 
        Função de Debug: Tira uma foto da tela quando algo dá errado. 
        Isso ajuda a descobrir se foi bug do site ou do código.
        """
        # Se a pasta 'erros' não existir, cria ela
        if not os.path.exists("erros"):
            os.makedirs("erros")
        
        # Define o nome do arquivo com a data e hora exata
        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"erros/{data_hora}_{nome_erro}.png"
        
        # Salva a imagem
        self.driver.save_screenshot(nome_arquivo)
        logging.info(f"Screenshot do erro salvo em: {nome_arquivo}")

    def _clicar(self, xpath):
        """ Função genérica para clicar em qualquer elemento de forma segura. """
        try:
            # Espera até o elemento estar "clicável" na tela
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.click()
            sleep(1) # Pequena pausa para a animação do site acontecer
        except Exception as e:
            # Se falhar, avisa no log, tira foto e para o programa
            logging.error(f"Erro ao clicar em {xpath}: {e}")
            self._tirar_screenshot("erro_clique") 
            raise

    def _selecionar_opcao_index(self, xpath_lista, index):
        """ 
        Abre uma lista (dropdown) e clica num item baseada na posição (index).
        Ex: index 0 = primeiro item, index 1 = segundo item...
        """
        try:
            # Espera a lista (ul) ficar visível na tela
            ul_opcoes = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_lista)))
            # Pega todos os itens da lista (tags <li>)
            opcoes = ul_opcoes.find_elements(By.TAG_NAME, 'li')
            
            # Verifica se o índice que pedimos existe na lista
            if len(opcoes) > index:
                texto_opcao = opcoes[index].text
                logging.info(f"Selecionando opção: {texto_opcao}")
                opcoes[index].click() # Clica na opção
                sleep(2) # Pausa importante: o site da FIPE carrega dados via AJAX aqui
            else:
                logging.warning(f"Índice {index} não existe na lista.")
        except Exception as e:
            logging.error(f"Erro ao selecionar opção: {e}")
            self._tirar_screenshot("erro_selecao")
            raise

    def consultar_carro(self, indices):
        """
        Executa o passo a passo completo da consulta.
        :param indices: Lista de números [Ref, Marca, Modelo, Ano]
        """
        try:
            logging.info("Acessando site da FIPE...")
            self.driver.get(self.url)
            
            # 1. Clica na aba 'Carros'
            self._clicar('//*[@id="front"]/div[1]/div[2]/ul/li[1]/a')

            # 2. Seleciona o Mês de Referência (primeiro dropdown)
            self._clicar('//*[@id="selectTabelaReferenciacarro_chosen"]')
            self._selecionar_opcao_index('//*[@id="selectTabelaReferenciacarro_chosen"]/div/ul', indices[0])

            # 3. Seleciona a Marca
            self._clicar('//*[@id="selectMarcacarro_chosen"]')
            self._selecionar_opcao_index('//*[@id="selectMarcacarro_chosen"]/div/ul', indices[1])

            # 4. Seleciona o Modelo
            self._clicar('//*[@id="selectAnoModelocarro_chosen"]')
            self._selecionar_opcao_index('//*[@id="selectAnoModelocarro_chosen"]/div/ul', indices[2])

            # 5. Seleciona o Ano do Carro
            self._clicar('//*[@id="selectAnocarro_chosen"]')
            self._selecionar_opcao_index('//*[@id="selectAnocarro_chosen"]/div/ul', indices[3])

            # 6. Clica no botão roxo 'Pesquisar'
            logging.info("Pesquisando valores...")
            self._clicar('//*[@id="buttonPesquisarcarro"]')
            
            sleep(3) # Pausa de segurança para garantir o carregamento

            # Chama a função que lê a tabela de resultados
            return self._extrair_dados()

        except Exception as e:
            # Se qualquer coisa der errado no fluxo principal:
            logging.critical(f"Falha fatal no fluxo: {e}")
            self._tirar_screenshot("erro_fatal")
        finally:
            # O bloco 'finally' roda sempre, garantindo que o navegador feche
            self.encerrar()

    def _extrair_dados(self):
        """ Lê a tabela HTML final e transforma num Dicionário Python. """
        logging.info("Extraindo dados da tabela...")
        dados = {}
        try:
            # ESTRATÉGIA INTELIGENTE:
            # Espera até que o texto "Preço Médio" apareça no corpo da página.
            # Isso confirma que a tabela foi carregada visualmente.
            self.wait.until(EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"), "Preço Médio")
            )

            # Encontra a tabela na página
            tabela = self.driver.find_element(By.TAG_NAME, 'table')
            
            # Pega todas as linhas (tr) da tabela
            linhas = tabela.find_elements(By.TAG_NAME, 'tr')
            
            # Loop: Para cada linha da tabela...
            for linha in linhas:
                # Pega as colunas (td)
                colunas = linha.find_elements(By.TAG_NAME, 'td')
                # Se tiver 2 colunas (ex: "Marca" | "Fiat"), salva no dicionário
                if len(colunas) == 2:
                    chave = colunas[0].text.strip(':') # Remove os dois pontos
                    valor = colunas[1].text
                    if chave and valor: 
                        dados[chave] = valor
            
            logging.info("Dados extraídos com sucesso!")
            return dados

        except Exception as e:
            logging.error(f"Erro na extração: {e}")
            self._tirar_screenshot("erro_extracao_conteudo")
            return None

    def salvar_json(self, dados, nome_arquivo="fipe_resultado.json"):
        """ Salva o dicionário num arquivo .json bonito e legível. """
        if dados:
            # Abre o arquivo em modo de escrita ('w') com suporte a acentos (utf-8)
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                # dump: escreve os dados no arquivo
                # indent=4: deixa o arquivo organizado com identação
                # ensure_ascii=False: permite salvar acentos (ç, é, ã) corretamente
                json.dump(dados, f, indent=4, ensure_ascii=False)
            logging.info(f"Dados salvos com sucesso em {nome_arquivo}")
        else:
            logging.warning("Nenhum dado para salvar.")

    def encerrar(self):
        """ Fecha o navegador para liberar memória do computador. """
        logging.info("Fechando navegador.")
        self.driver.quit()

# --- BLOCO PRINCIPAL DE EXECUÇÃO ---
if __name__ == "__main__":
    # 1. Cria o robô (mude headless=True para não ver a janela abrindo)
    bot = FipeBot(headless=False)
    
    # 2. Define quais opções queremos selecionar em cada passo
    # Lista: [Mês Referência, Marca, Modelo, Ano]
    # Obs: Os números são os índices (0 é o primeiro da lista)
    indices_busca = [0, 12, 1, 0] 
    
    # 3. Manda o robô trabalhar
    resultado = bot.consultar_carro(indices_busca)
    
    # 4. Salva o resultado final
    bot.salvar_json(resultado)