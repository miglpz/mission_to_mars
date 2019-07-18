from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

def scrape_all():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title":news_title, 
        "news_paragraph":news_paragraph, 
        "featured_image":featured_image(browser),
        "mars_weather":mars_weather(browser),
        "mars_facts":mars_facts(browser),
        "mars_hemispheres":mars_hemispheres(browser)
    }

    return data

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try: 
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find('div', class_="content_title").text
        news_paragraph = slide_elem.find('div', class_="article_teaser_body").text
    except: AttributeError
        
    browser.quit()
    
    return news_title, news_paragraph

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_element = browser.find_by_id('full_image')
    browser.is_element_present_by_text('more info', wait_time=2)
    more_info_elem = browser.find_link_by_partial_text('more info')
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    except: AttributeError
        
    browser.quit()
    
    return img_url

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport'
    browser.visit(url)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    try: 
        weather_soup.find('div', class_="css-1dbjc4n")
        timeline = weather_soup.find('div', class_="js-tweet-text-container")
        weather_tweet = timeline.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    except: AttributeError

    browser.quit()
    
    return weather_tweet

def mars_facts(browser):
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    mars_facts = pd.read_html(url)
    mars_table = mars_facts[1]
    mars_table_final = mars_table.rename(columns = {0 : "Description", 1 : "Value"})
    mars_table_final = mars_table_final.set_index("Description")

    browser.quit()
    
    return mars_table_final

def mars_hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    for item in items:     
        title = item.find('h3').text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)    
        partial_img_html = browser.html
        soup = BeautifulSoup(partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    browser.quit()
    
    return hemisphere_image_urls
    


