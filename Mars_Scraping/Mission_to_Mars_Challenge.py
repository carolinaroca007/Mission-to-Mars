
#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


#Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)



#Parse the HTML
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ## Featured Images


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


df.to_html()


# # Mars Weather

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars' Hemisphere Images and Titles

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere
html = browser.html
mars_hemi = soup(html, 'html.parser')


collapsible_results = mars_hemi.find_all(class_="results")
count = 1
#1, 3, 5, 7

for item in range(4):
    
    hemispheres = {}
    html = browser.html
    mars_hemi = soup(html, 'html.parser')
    browser.find_by_css('.product-item')[count].click()
    ## grab the a link and store the href in hempisphere
    html = browser.html
    mars_hemi = soup(html, 'html.parser')
    hemi_url = mars_hemi.find('div', class_='downloads').select_one('ul li a').get("href")
    hemi_title = mars_hemi.find('h2', class_="title").get_text()

    hemispheres["img_url"] = hemi_url
    hemispheres["title"] = hemi_title
    hemisphere_image_urls.append(hemispheres)

    browser.back()
    count = count + 2     
        

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()




