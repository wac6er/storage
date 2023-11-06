# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 14:47:00 2023

@author: w7car
"""

import pandas as pd 
import requests 
import time 
from bs4 import BeautifulSoup 
import random 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import bs4
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import datetime

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.sec.gov/edgar/browse/?CIK=1682852&owner=exclude')
df = []
states = pd.read_csv(r"C:\Users\w7car\Downloads\storage - Sheet1.csv")['states_lifeStorage']
for state in states.dropna():
    state = state.replace(' ','-')
    url = 'https://www.lifestorage.com/storage-units/'+state+'/'
    
    driver.get(url)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    soup = driver.page_source
    soup = str(BeautifulSoup(soup, "lxml"))
    spl = soup.split('/storage-units/'+state)
    len(spl)
    links = []
    for i in range(len(spl)-2):
        links.append('https://www.lifestorage.com/storage-units/'+state+spl[i+1].split('"')[0])
    
    links = pd.DataFrame(links).drop_duplicates()
    links = links[links[0]!='https://www.lifestorage.com/storage-units/'+state]
    links = links[links[0]!='https://www.lifestorage.com/storage-units/'+state+'/'].reset_index(drop=True)[0]
     
    for l in range(len(links)-1):
      try:
        url = links[l]
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        soup = driver.page_source

        soup = str(BeautifulSoup(soup, "lxml")).split('startingAt":{"correlationId')[1]
        spl = soup.split('"storeId":"')
        
        for o in range(len(spl)-1):
          store_id = spl[o+1].split('"')[0]
          unit_id = spl[o+1].split('"uid":"')[1].split('"')[0]
          current_price = spl[o+1].split('"web":')[1].split('}')[0]
          initial_price = spl[o+1].split('"street":')[1].split(',')[0]
          features = spl[o+1].split('"display":"')
          for z in range(len(features)-1):
            if z ==0:
              size = features[z+1].split('"')[0]
            elif z ==1:
              feature = features[z+1].split('"')[0]
            else:
              feature = feature + ', '+features[z+1].split('"')[0]
        
          available = spl[o+1].split('"available":')[1].split(',')[0]
          total = spl[o+1].split('"total":')[1].split('}')[0]
          if total == 0:
              total = 1
          df.append({
              'Unit_ID':unit_id,
              'Store_ID':store_id,
              'Current_Price':current_price,
              'Initial_Price':initial_price,
              'Size ':size,
              'Features':feature,
              'Available':available,
              'Total':total,
              'URL':url
          })
        try:
            pd.DataFrame(df).to_csv('life_storage_19.csv')
            print(len(pd.DataFrame(df).drop_duplicates().reset_index(drop=True)))
            print(state)
            print(links[l])
        except:
            dfd=0
      except:
        print('ERROR')
        time.sleep(10)
        
driver.quit()
time.sleep(13)
        

driver = webdriver.Chrome(ChromeDriverManager().install())

df = []
states = pd.read_csv(r"C:\Users\w7car\Downloads\storage - Sheet1 (1).csv")['states_extraStorage']
for state in states.dropna():

    state = state.lower().lower().replace(' ','-')
    url = 'https://www.extraspace.com/sitemap/states/'+state+'/'
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(random.uniform(2,3))
    soup = driver.page_source
    soup = str(BeautifulSoup(soup, "lxml"))
    driver.save_screenshot('jpeg.png')
    spl = soup.split('/facilities/us/'+state)
    links = []
    for i in range(len(spl)-1):
      try:
        int(spl[i+1].split('"')[0].split('/')[2])
        try:
          if len(spl[i+1].split('"')[0].split('/')[3])==0:
            links.append('https://www.extraspace.com/storage/facilities/us/'+state+spl[i+1].split('"')[0])
        except:
          dfd=0
          print('error')
      except:
        dfd = 0
        print('error')

    for l in range(len(links)):
      try:
        url = links[l]
        driver.get(url)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        soup = driver.page_source
        soup = str(BeautifulSoup(soup, "lxml")).split('startingAt":{"correlationId')[1]
        spl = soup.split('"storeId":"')

        for o in range(len(spl)-1):
          store_id = spl[o+1].split('"')[0]
          unit_id = spl[o+1].split('"uid":"')[1].split('"')[0]
          current_price = spl[o+1].split('"web":')[1].split('}')[0]
          initial_price = spl[o+1].split('"street":')[1].split(',')[0]
          features = spl[o+1].split('"display":"')
          for z in range(len(features)-1):
            if z ==0:
              size = features[z+1].split('"')[0]
            elif z ==1:
              feature = features[z+1].split('"')[0]
            else:
              feature = feature + ', '+features[z+1].split('"')[0]

          available = spl[o+1].split('"available":')[1].split(',')[0]
          total = spl[o+1].split('"total":')[1].split('}')[0]

          df.append({
              'Unit_ID':unit_id,
              'Store_ID':store_id,
              'Current_Price':current_price,
              'Initial_Price':initial_price,
              'Size ':size,
              'Features':feature,
              'Available':available,
              'Total':total,
              'URL':url
          })
        pd.DataFrame(df).drop_duplicates().reset_index(drop=True).to_csv('Extra_Space_19.csv')
        print(len(pd.DataFrame(df).drop_duplicates(subset=['Unit_ID','Store_ID']).reset_index(drop=True)))
      except:
        driver.quit()
        print('ERROR')
        time.sleep(2)
        driver = webdriver.Chrome(ChromeDriverManager().install())
    