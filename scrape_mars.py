import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests as req
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path)

def scrape():
    browser = init_browser()

# --------------------------------------------------------------------------
# NASA Mars News - Scrape the NASA Mars News Site and collect the latest
# News Title and Paragragh Text. Assign the text to variables that you can
# reference later.
# --------------------------------------------------------------------------
    
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)
    time.sleep(1)

    html = browser.html
    news_soup = bs(html, 'html.parser')

    latest_art = news_soup.find("div", class_="list_text")
    news_date = latest_art.find("div", class_="list_date").text
    news_title = latest_art.find("div", class_="content_title").text
    news_p = latest_art.find("div", class_="article_teaser_body").text

# --------------------------------------------------------------------------
# JPL Mars Space Images - Visit the url for JPL's Featured Space Image.
# Use splinter to navigate the site and find the image url for the current
# Featured Mars Image and assign the url string to a variable called
# featured_image_url.
# --------------------------------------------------------------------------
   
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(1)

    browser.find_link_by_partial_text('FULL IMAGE').click()
    browser.is_element_present_by_text('more info', wait_time=1)
    browser.find_link_by_partial_text('more info').click()

    html1 = browser.html
    jpl_soup = bs(html1, "html.parser")

    url_ini = "https://www.jpl.nasa.gov"
    featured_image_url = url_ini + jpl_soup.find('figure', class_="lede").find('a')['href']

# --------------------------------------------------------------------------
# Mars Weather - Visit the Mars Weather twitter account and scrape the
# latest Mars weather tweet from the page. Save the tweet text for the
# weather report as a variable called mars_weather
# --------------------------------------------------------------------------

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(1)

    html = browser.html
    weather_soup = bs(html, 'html.parser')

    mars_weather = weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather.a.extract()
    mars_weather.text
    mars_weather = mars_weather.text.replace('\n', ". ")
  
# --------------------------------------------------------------------------
# Mars Facts - Visit the Mars Facts webpage here and use Pandas to scrape
# the table containing facts about the planet including Diameter, Mass, etc.
# --------------------------------------------------------------------------

    mars_facts = pd.read_html('https://space-facts.com/mars/')[1]
    mars_facts.columns=['Description', 'Value']
    mars_facts.set_index('Description', inplace=True)

    mars_facts.to_html('mars_facts.html')

# --------------------------------------------------------------------------
# Mars Hemispheres - Visit the USGS Astrogeology site to obtain
# high resolution images for each of Mars' hemispheres.
# --------------------------------------------------------------------------


    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(1)

    html = browser.html
    hemisp_soup = bs(html, 'html.parser')

    group = hemisp_soup.find('div', class_="collapsible results")
    group1 = group.find_all('div', class_="item")
    main_url = "https://astrogeology.usgs.gov"

    hemisphere_image_urls = []
    dict_hem = {}

    for item in group1:
        hem_img_url = main_url + item.find('a', class_="itemLink product-item")['href']
        browser.visit(hem_img_url)
        browser.find_link_by_partial_text('Open').click()
        
        html_hem = browser.html
        soup_hem = bs(html_hem, "html.parser")
        
        img_url = main_url + soup_hem.find('img', class_="wide-image")['src']
        title = soup_hem.find('h2', class_="title").text.split(" ")
        title = title[0] + " " + title[1]
        dict_hem = {
            "title": title,
            "img_url": img_url
        }
        hemisphere_image_urls.append(dict_hem)

    scrape = {
        "news_date": news_date,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()
    
    return scrape





