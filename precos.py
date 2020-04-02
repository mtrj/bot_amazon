# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup

class amazon():
    def __init__(self, pesquisa=[]):
        self.headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.pesquisa, self.precos, self.titulos = list(pesquisa), [], []

    def busca(self):
        precos, pesquisa, titulos = self.precos, self.pesquisa, self.titulos
        for i in range(len(pesquisa)):
            pesquisa[i] = pesquisa[i].replace(' ', '+')
            link = 'https://www.amazon.com.br/s?k={}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss'.format(pesquisa[i])
            page = requests.get(link, headers=self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            price = soup.find_all('span',attrs={'class':'a-offscreen'})
            desc = soup.find_all('span',attrs={'class':'a-size-medium a-color-base a-text-normal'})
            try:
                precos.append(float(price[0].text.replace('R$','').replace('.','').replace(',','.')))
                titulos.append(desc[0].text)
            except:
                precos.append(0)
                titulos.append(pesquisa[i].replace('+', ' '))
        return pd.DataFrame(data=precos,columns={'Preço'}, index=titulos)
