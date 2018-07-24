import requests
from bs4 import BeautifulSoup
from datetime import timedelta

from Section import Section
from get_fake_user_proxies import getProxy       
from get_fake_user_agent import getRandomUserAgent

def findSectionsAndArticlesFromContent(content):
    """ 
    Finds and extracts all the news sections from the html content
    
    @param {string} date - String representation of the date for the sections
    @param {BeautifulSoup obj} - BeautifulSoup obj that contains all the html content
    @returns A dictionary mapping sections to their articles
    """
    articlesInSection = {}
    
    for section in content:
        section_title = section.find('div',attrs={'class':"container page-title centered"}).find('h2').text
        articles = section.find_all('div',attrs={'class':"list-content"})
        articlesInSection[section_title] = articles
        
    return articlesInSection

def populateSections(newsDate, articlesInSection):
    """Returns a list of Section objects """
    sections = []
    for section_title, articles in list(articlesInSection.items()):
        sectionObj = Section(section_title,articles, newsDate)
        sections.append(sectionObj)
    
    return sections


def getContentAndTimeList(start_date, end_date):
    """Retrieves a list of content from Daily Star and a list of dates for which to scrape""" 
    content_list = []
    
    time_list = getDatesToScrape(start_date, end_date)
       
    for i in range(len(time_list)): #O(n)
        content_list.append(getContent(time_list[i]))
        
    return content_list, time_list

def getDatesToScrape(start_date, end_date):
    """ 
    Returns a list of date in string format, iterating  from start to end date.
    Start and end dates need to changed manually inside the method.
    """
  
    dates = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

    return [str(d) for d in dates]

def getContent(newsDate):
    """ 
    Makes a GET request and gets html content back. 
    
    @param {string} date - Date for which we want the html content
    @returns 
    """
    address = "https://www.thedailystar.net/newspaper?date={}".format(newsDate)
    
    response = makeSpoofedRequest(address)
    print(f"Successfully made call to {address}")
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find_all('div',attrs={'class':"panel-pane pane-news-col no-title block"}) 

    return content

def makeSpoofedRequest(address):
    """ 
    Makes a GET request using a proxy
    """
    header = getRandomUserAgent()
    proxy = getProxy()
    response = requests.get(address, headers=header ,proxies=proxy)
    
    return response        

def keepTrackOfScrapedArticles(newsDate):
    """
    Writes the date to file a file. The date represents successfull scraping for that date
    """
    
    with open("successful_scraped_dates.txt", "a+") as file:
        file.write(f"{newsDate}\n")
            

    
    

