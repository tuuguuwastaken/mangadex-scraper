import selenium
import re
import os
import urllib
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
  def __init__(self) -> None:
    driver = None
    url = None
    outputPath = "./images"

  def SetURL(self,url):
    url_pattern = r'^https?://(?:www\.)?[^\s/$.?#].[^\s]*$'
    if re.match(url_pattern, url):
      self.url = url      
    else:
      print('The prodived input is not a URL setURL with the correct information please')  
      
  def setDriver(self,):
    self.driver = webdriver.Chrome()
  
  def Start(self,output="./images",url=None):
    if url == None:
      url = self.url
    
    links = []
      
    driver = self.driver
    driver.implicitly_wait(300)
    print('scraping')
    driver.get(url)
    driver.maximize_window()
    elems = driver.find_elements(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div[3]/div/div[9]/div[2]/div[2]/div[2]/div/div[2]/div")
    for elem in elems:
      stuff = elem.find_element(By.XPATH,'div/div/div/a')
      language = stuff.find_element(By.XPATH,'img').get_attribute("title")
      link = stuff.get_attribute("href")
      if(language.lower() == "english"):
        links.append(link)
      
    driver.get(links[0])
    title = driver.find_element(By.CLASS_NAME,'reader--header-title')
    time.sleep(6)
    mangaImages = driver.find_elements(By.CLASS_NAME,'img')
    print(len(mangaImages))
    for image in mangaImages:
      
      # status = image.find_element(By.CLASS_NAME,'img').get_attribute("src")
      print(image.get_attribute('src'))
    # print(links)
    WebDriverWait(driver, 900).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
    
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[9]/div[2]/div[2]/div[2]/div/div[2]/div[1]
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[9]/div[2]/div[2]/div[2]/div/div[2]/div[2]
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[9]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/a[1]
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[9]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/a[1]
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[9]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/a[1]/
    
    
    # link xpath
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div[1]/img
    # /html/body/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div[1]
    
if __name__ == "__main__":
  scrapper = Scraper()
  scrapper.setDriver()
  scrapper.SetURL('https://mangadex.org/title/960a03a6-0c21-470c-be84-973304b2f7bd/oh-my-devil')
  scrapper.Start()
  