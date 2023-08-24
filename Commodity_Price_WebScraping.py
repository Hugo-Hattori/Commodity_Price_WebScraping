#Passo 1: Abrir o navegador
from selenium import webdriver
navegador = webdriver.Chrome()

#Passo 2: Importar a base de dados
import pandas as pd
tabela = pd.read_excel("commodities.xlsx")

#Passo 3: Pesquisar os preços atuais (cotação atual)
for linha in tabela.index:
    produto = tabela.loc[linha, "Produto"]
    produto = produto.replace("ó","o").replace("ã","a").replace("ç","c").replace("ú","u").replace("é","e").replace("á","a")
    link = f"https://www.melhorcambio.com/{produto.lower()}-hoje"
    navegador.get(link)
    preco = navegador.find_element("xpath", '//*[@id="comercial"]').get_attribute("value")
    
    #Ajuste moeda brasileira
    preco = preco.replace(".","").replace(",",".") 
    
    #Passo 4: Atualizar os preços na base de dados
    tabela.loc[linha,"Preço Atual"] = float(preco)
navegador.quit()

#Passo 5: Criar planilha com dados atualizados e com a decisão de compra (VERDADEIRO = Compra, FALSO = Não Compra)
tabela["Comprar"] = tabela["Preço Atual"] < tabela["Preço Ideal"]
   
#Criando planilha nova atualizada
tabela.to_excel("commodities_atualizado.xlsx", index=False)
