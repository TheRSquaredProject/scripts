# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 22:52:41 2018

@author: aminm
"""
import os
import re


class Article:
    """
    Represents a Daily Star article
    """
    def __init__(self,section_title,article_title,article_content, date):
        """ 
        Constructor
        
         @param {string} section_title - Title of the section
         @param {string} article_title - Title of the article
         @param {BeautifulSoup obj} article_content - A BeautifulSoup obj that encapsulates the contents of the article
         @param {string} date - Date of the articles
        """
        self.section_title = section_title
        self.article_title = article_title
        self.article_content = article_content
        self.date = date
    
    def getSectionTitle(self):
        """ 
        Returns the section_title
        """
        return self.section_title
    
    def getArticleTitle(self):
        """ 
        Returns the aritlce_title
        """
        return self.article_title
    
    def getArticleContent(self):
        """ 
        Returns the article_content
        """
        return self.article_content
    
    def extractText(self):
        """
        Extracts the articles from article_content and transforms it from BeautifulSoup obj to string
        
        @returns Article text in string format
        """
        paras = self.article_content.find('div',attrs={'class':["field-body view-mode-full","field-body"]}).find_all('p')
        text = self._extractParasAndFormText(paras)
        return text
    
    def _extractParasAndFormText(self,paras):
        """
        Extracts the string text from BeautifulSoup paragraphs
        
        @param {BeautifulSoup obj} paras - Contains article text
        @returns Article text in string format
        """
        
        text = "\n ".join([str(para.text) for para in paras])
        return text
    
    def _createDirectories(self,dirPath):
        """ 
        Creates directories if they do not exist
        
        @param {string} dirPath - Directory path
        """
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
            
    def _sanitizeText(self,text):
        """
        Removes undesireable characters from the text so that they are valid file name.
        
        @param {string} text - tex tto be sanitized
        """
        text = text.strip().lower()
        textWithoutSpecialChar = re.sub("[.?!\"\n',:]","",text)
        return re.sub("[ ]","_",textWithoutSpecialChar)
            
    def writeToFile(self):
        """ 
        Write the article to a txt file.
        """
        dirPath  = self._sanitizeText(f"{self.date}/{self.section_title}")
        self._createDirectories(dirPath)
    
        fileName = self._sanitizeText(f'{self.date}/{self.section_title}/{self.article_title}') + ".txt"
    
        with open(fileName,"w+", encoding="utf-8") as fobj:
            fobj.write(self.extractText())