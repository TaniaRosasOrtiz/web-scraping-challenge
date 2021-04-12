# Import Dependencies
import pandas as pd
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_data_dict={}
    # ----------------------------------------
    # NASA Mars News 
    # https://redplanetscience.com/

    # URL Scrape
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text

    # ----------------------------------------
    # JPL Mars Space Images - Featured Image  
    # https://spaceimages-mars.com/

    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    image_url=soup.find_all('a', class_='showimg fancybox-thumbs')
    image_url=soup.find('a', class_='showimg fancybox-thumbs')['href']
    featured_image_url=url+image_ur

    # ----------------------------------------
    # Mars Facts
    # https://galaxyfacts-mars.com/

    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    tables = pd.read_html(url)
    mars_facts = tables[1]
    mars_html = mars_facts.to_html()
    mars_html = mars_html.replace('\n','')
    mars_html

    # ----------------------------------------
    # Mars Facts:Mars Hemispheres
    # https://marshemispheres.com/ 

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    results = soup.find('div',class_='collapsible results')
    results_item = results.find_all('div',class_='item')

    hemisphere_image_urls=[]

    for item in results_item:
        # Error handling
        try:
            # hemisphere title
            hemisphere = item.find('div',class_='description')
            title = hemisphere.h3.text
            
            # image url:  click each of the links to the hemispheres to find the image url to the full resolution image
            hemisphere_url = hemisphere.a['href']
            browser.visit(url+hemisphere_url)
            html=browser.html
            soup=bs(html,'html.parser')
            dd_all=soup.find_all('dd')
            dd = dd_all[1]
            image_src = url+dd.a['href']
            
            # check results
            print('-'*30)
            print(title)
            print(image_src)
            
            # dictionary with the image url string and the hemisphere title
            hemisphere_dict={
                'title' : title,
                'image_url' : image_src
            }
            
            hemisphere_image_urls.append(hemisphere_dict)
        except Exception as e:
            print(e)

    # ----------------------------------------
    # return one Python dictionary containing all of the scraped data
    mars_dictionary={
        # NASA Mars News 
        "news_title": news_title,
        "news_p": news_p,
        # JPL Mars Space Images
        "featured_image_url": featured_image_url,
        # Mars Facts
        "mars_facts": mars_facts,
        # Mars Hemispheres
        "mars_hemispheres": hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    return mars_dictionary