##=======================================================================================
##  Home work: Module12-Web scrapping for Mars Data
##=======================================================================================

# Import dependancies
from splinter import Browser
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    # Variable to accommodata all the scrapped data 
    mars_data = {}

    ## 1. Scrape Mars News website ===========================================================
    #
    # Establish website connection using splinter browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    visit_url = 'https://redplanetscience.com/'
    browser.visit(visit_url)

    # Scrape Mars News website to get latest_news_title and text
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Search for the latest news title and text (soup syntax), use find() will only get one object in return 
    text_soup = soup.find('div', class_='list_text')
    latest_news_title = (text_soup.find('div', class_='content_title')).text
    latest_news_text = (text_soup.find('div', class_='article_teaser_body')).text

    ## 2. Scrape JPL Mars Space Image website ===================================================
    #
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    visit_url = 'https://spaceimages-mars.com/'
    browser.visit(visit_url)    

    # Scrape the website to get the full size featured image url
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find('div', class_='floating_text_area')
    feature_img_url = soup.find('a')['href']
    feature_img_url = visit_url + feature_img_url
    
    ## 3. Mars Facts website =====================================================================
    #
    # Scrape with Pandas to get the fact tables.
    url = 'https://galaxyfacts-mars.com/'
    fact_table = pd.read_html(url)       

    # The first reading is Mars and Earch comparision fact, take second reading which states Mars measurement fact
    fact_df = pd.DataFrame(fact_table[1])
    fact_table = fact_df.to_html()
    
    ## 4. Mars Hemispheres website ===============================================================
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    hemisphere_main_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_main_url)    

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    
    # Find image titles and html urls from the hemisphere main page
    title_list = []
    img_html_list = []
    for item in items:
        img_html = item.find('a')['href']
        img_html_list.append(hemisphere_main_url+ img_html)
        title = item.find('h3').text
        title_list.append(title)

    # Find high resolution image url from its image html page
    img_url_list = []
    for item in img_html_list:
        browser.visit(item)   
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        image = img_soup.find('img', class_="wide-image").get('src') # or use img_soup.find('img', class_="wide-image")['src']
        img_url_list.append(hemisphere_main_url+image)

    # Save titles and img_urls into a dictionary
    img_url_dict = []
    for i in range(len(img_url_list)):
        img_url_dict.append({
                    'title': title_list[i],
                    'img_url': img_url_list[i]
            })

    mars_data = {
        'news_title' : latest_news_title,
        'news_p' : latest_news_text,
        'feature_img_url' : feature_img_url,
        'fact_table' : fact_table, 
        'hemisphere_img_url' : img_url_dict 
        }

    browser.quit() 
    # print(mars_data)

    return mars_data

if __name__ == "__main__":
    scrape()


