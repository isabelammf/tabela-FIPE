from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def clicar_elemento_por_xpath(navegador, xpath):
    elemento = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    elemento.click()
    time.sleep(2)


def clicar_elemento_por_xpath_com_visibilidade(navegador, xpath):
    elemento = WebDriverWait(navegador, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, xpath))
    )
    elemento[0].click()  # Clica no primeiro elemento visível se houver mais de um
    time.sleep(2)

def lista_elementos_visiveis_por_xpath(navegador, xpath):
    opcoes = WebDriverWait(navegador, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, xpath))
    )
    return opcoes

def preencher_barra_de_pesquisa(navegador, texto, xpath_barra_de_pesquisa):
    campo_de_pesquisa = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_barra_de_pesquisa))
    )
    campo_de_pesquisa.clear()  # Limpa o campo de pesquisa, se houver texto preexistente
    campo_de_pesquisa.send_keys(texto)  # Preenche o campo com o texto desejado

def selecionar_ano_mes_por_pesquisa(navegador, mes_ano):
    preencher_barra_de_pesquisa(navegador, mes_ano, '//*[@id="selectTabelaReferenciacarro_chosen"]/div/div/input')
    clicar_elemento_por_xpath_com_visibilidade(navegador, '//*[@id="selectTabelaReferenciacarro_chosen"]/div/ul')

def selecionar_ano_mes_por_posicao(navegador, posicao):
    opcoes_mes_ano = lista_elementos_visiveis_por_xpath(navegador, '//*[@id="selectTabelaReferenciacarro_chosen"]/div/ul')
    lista_elementos = opcoes_mes_ano[0].find_elements(By.CSS_SELECTOR, 'li')
    lista_elementos[posicao].click()

def selecionar_marca_por_pesquisa(navegador, marca):
    preencher_barra_de_pesquisa(navegador, marca, '//*[@id="selectMarcacarro_chosen"]/div/div/input')
    clicar_elemento_por_xpath_com_visibilidade(navegador, '//*[@id="selectMarcacarro_chosen"]/div/ul')

def selecionar_marca_por_posicao(navegador, posicao):
    opcoes_marca = lista_elementos_visiveis_por_xpath(navegador, '//*[@id="selectMarcacarro_chosen"]/div/ul')
    lista_elementos = opcoes_marca[0].find_elements(By.CSS_SELECTOR, 'li')
    lista_elementos[posicao].click()

# Inicializa o navegador
navegador = webdriver.Edge()

# Abra uma página
navegador.get("https://veiculos.fipe.org.br/")

##############################################################

# 1) Clicar em 'Consulta de carros e utilitários pequenos'
clicar_elemento_por_xpath(navegador, '//*[@id="front"]/div[1]/div[2]/ul/li[1]/a')

# 2) Cliacar na caixa mês/ano
clicar_elemento_por_xpath(navegador, '//*[@id="selectTabelaReferenciacarro_chosen"]')

# Pesquisar mês/ano e clicar
#selecionar_ano_mes_por_pesquisa(navegador, 'agosto/2004')

# Selecionar por posição e clicar
selecionar_ano_mes_por_posicao(navegador, 1)

# 3) marca
clicar_elemento_por_xpath(navegador, '//*[@id="selectMarcacarro_chosen"]')

#selecionar_marca_por_pesquisa(navegador, 'BYD')
selecionar_marca_por_posicao(navegador,2)

# 4) modelo
# 5) ano/modelo
# 6) pesquisar 
# 7) salvar dados da tabela em um dicionário
time.sleep(10)
