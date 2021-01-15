# Bibliotecas

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

# Pegando a url

### na qual irei adicionar o final da url das paginas seguintes
url_base = 'https://www.tripadvisor.com.br/' 

### primeira pagina
url_first_page = "https://www.tripadvisor.com.br/Restaurant_Review-g303322-d2347832-Reviews-Outback_Steakhouse_ParkShopping-Brasilia_Federal_District.html"


# Acessando a pagina para realizar a automacao da mudanca de pagina
option = Options()
option.headless = True
driver = webdriver.Firefox(options = option) #assim eu nao fico vizualizando a pagina

driver.get(url_first_page) # entrando na primeira pagina
time.sleep(3) 
driver.find_element_by_xpath(f'//*[@id="_evidon-accept-button"]').click() # realizando um clique no botao


# Criando as listas nas quais irei adicionar as informacoes coletadas pelo BeautifulSoup
reviews_list = []
reviews_titles_list = []
date_list = []
ratings_bubbles_list = []

# Fazendo o request da pagina (primeira pagina)
r = requests.get(url_first_page)
soup = bs(r.content, 'html.parser')


# Realizando um loop para fazer web scrape de cada pagina
for i in range(218):
    # Coletando os dados da pagina

    ### critica

    reviews = soup.select('div.reviewSelector div.entry')
    for r in reviews:
        reviews_list.append(r.get_text())

    ### titulo da critica

    reviews_titles = soup.select('div.quote a span')
    for t in reviews_titles:
        reviews_titles_list.append(t.get_text())

    ### momento da critica

    date = soup.select('span.ratingDate')
    for d in date:
        date_list.append(d['title'])

    ### pontuacao

    ratings_bubbles = soup.select('div.ui_column.is-9 span.ui_bubble_rating')
    for b in ratings_bubbles:
        ratings_bubbles_list.append(b['class'][1])

    ### muda de pagina
    ### Apos a coleta das informacoes, selenium ira mudar para a pagina seguinte

    try:
        driver.find_element_by_xpath(
            f"/html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[3]/div/div[5]/div/div[12]/div/div/a[2]").click()
        print('page', i)

    except:
        driver.find_element_by_xpath(
            f"/html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[3]/div/div[5]/div/div[13]/div/div/a[2]").click()


    # Com a mudanca da pagina, o beautifulsoup precisa acessar a url da nova pagina    
     
    next_page = str(soup.find_all('a', attrs={'class': 'nav'})[1]['href'])
    r = requests.get(url_base + next_page)
    soup = bs(r.content, 'html.parser')

    time.sleep(5)

    # volta

driver.quit()


# Criando um dicionario para armazenar as listas

df_reviews = {'title': reviews_titles_list,
              'text': reviews_list,
              'date': date_list,
              'rating': ratings_bubbles_list}

# Transformando o dicionario em DataFrame e salvando em um arquivo CSV

df_reviews = pd.DataFrame(df_reviews)
df_reviews.to_csv('web_scrape_tripadvisor_final.csv', encoding='utf-8')
