# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 22:51:13 2018

@author: aminm
"""
from bs4 import BeautifulSoup
import requests
import time as pytime
from Article import Article
from get_fake_user_proxies import getProxy

class Section:
    """ 
    Represents a section for Daily Star i.e. Front Page, Sports etc
    """
    def __init__(self, section_title,articles_raw,date):
        """ 
        Constructor
        
        @param {string} section_title - Title of the section
        @param {[BeautifulSoup obj]} articles_raw - A list of BeautifulSoup obj. Each obj contains all the articles for a section
        @param {string} date - Date of the articles
        """
        self.section_title = section_title
        self.articles_raw = articles_raw
        self.date = date
        
    def writeArticlesToFile(self):
        """ 
        Extracts and transforms each article from BeautifulSoup to an Article obj, then writes the article text to file
        """
        counter = 0
        waitTime = 250
        
        base = "https://www.thedailystar.net/"
        #spoofedIp = getProxy()['ip']
        spoofedProxy = getProxy()
        spoofedProxyWithPort = spoofedProxy['ip']+ ":" +spoofedProxy['port'] #need to refactor
        proxy = {"http": f"http://{str(spoofedProxyWithPort)}"}
        for article in self.articles_raw:
            try:
                article_title = article.h5.text
                article_url = base + article.a['href']
                response = requests.get(article_url, proxies=proxy)
                
                article_soup = BeautifulSoup(response.text, 'html.parser')
                articleObj = Article(self.section_title, article_title,article_soup, self.date)
                articleObj.writeToFile()
                counter += 1
            except Exception as e:             
                print(f"Error writing {article_title}")
                print(f"Error message: {e}")
                spoofedProxy = getProxy()
                spoofedProxyWithPort = spoofedProxy['ip']+ ":" +spoofedProxy['port'] #need to refactor
                proxy = {"http:": f"http://{str(spoofedProxyWithPort)}"}
                #print(f"Waiting {waitTime} seconds before making new requests...")
                #pytime.sleep(waitTime)
                continue
        
       
        
        print(f"Wrote {counter} articles to file")
       
        
        
            