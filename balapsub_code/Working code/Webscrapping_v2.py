# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 03:46:41 2022

@author: bala
"""

# importing required models and items
#   Module      Item
#     |           |
from bs4 import BeautifulSoup      # Beautifulsoup for html parser and webscrapping
import requests                    # html python library
import os                          # os module in python
import pandas as pd                # pandas module
import re                          # regular expression 

os.system("cls")
######################################################################################################
#####               Webpage requests, parsing and scrapping data                           ###########
######################################################################################################
#url of website to scrap data
url = f'https://www.stadt-koeln.de/leben-in-koeln/verkehr/parken/parkhaeuser/'
page = requests.get(url)                                                    # get the response of page from the url
soup= BeautifulSoup(page.content, 'html.parser')                            # store page content by html parsing using beautifulsoup
table = soup.find_all('table')        # find all the tables in webpage

######################################################################################################
#####               Data processing using pandas module                                    ###########
######################################################################################################
df = pd.read_html(str(table))         # assign tables as dataframe using pandas
df=pd.concat(df, axis=0, ignore_index=True)  # concatenate multiple dataframe into single data frame
df.columns = ['Parkhaus','Art','Adress','Betriebszeit','Weitere Datei']    # Headers of Dataframe

# seperate numbers (free available parking places) from strings (Parking place name also with numbers)
df['Freie Plätz'] = df['Parkhaus'].apply(lambda x: re.split('(\d+)', x)[1] if "Stadion" not in x
                                               else (x.split("(P+R)")[1] if "(P+R)" in x
                                                     else (x.split("Bus")[1] if "Bus" in x
                                                           else (x.split("Pkw")[1] if "Pkw" in x
                                                                 else re.split("(P\d)", x)[2]))))
df["Parkhaus"] = df["Parkhaus"].apply(lambda x: re.split('(\d+)', x)[0] if "Stadion" not in x
                                                else (x.split("(P+R)")[0] + "(P+R)" if "(P+R)" in x
                                                      else (x.split("Bus")[0] + "Bus" if "Bus" in x
                                                            else (x.split("Pkw")[0] + "Pkw" if "Pkw" in x
                                                                  else re.split('(P\d)', x)[0] + re.split('(P\d)', x)[1]))))
# Seperate house number from pincode / PLZ
zip_code_len = 10
df["Adress"] = df["Adress"].apply(lambda x: x[:-zip_code_len] + " " + x[-zip_code_len:])

######################################################################################################
#####               write data as csv file                                                 ###########
######################################################################################################
df.to_csv('Free_available_parking.csv', index=False, sep=";",encoding='utf-8', mode='w+') 
    
######################################################################################################
