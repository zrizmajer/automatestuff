
# ! python3
# flickr_images_download.py - goes to a photo-sharing site
# like Flickr or Imgur, searches for a category of photos,
# and then downloads a specified number of resulting images.

import requests, os, bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Url of desired photo-sharing site
url = 'https://www.flickr.com/'
# Desired search phrase
phrase = 'handsome guy'
# Desired number of pictures to download
posts = 15
# Create destination folder for downloads
os.makedirs('flickr', exist_ok=True)
# Create webdriver object
browser = webdriver.Chrome('C:\\Users\\rizma\\AppData\\Local\\Programs\\chromedriver.exe')
# Open url in browser
browser.get(url)
# Find search bar
searchElem = browser.find_element_by_xpath('//*[@id="search-field"]')
# Type in and submit search phrase, wait for 5 seconds
searchElem.send_keys(phrase)
searchElem.submit()
browser.implicitly_wait(5)
# Find and open first result picture
imageElem = browser.find_element_by_class_name('overlay')
imageElem.click()
# HTML element of page for special keys
htmlElem = browser.find_element_by_tag_name('html')
while posts != 0:
    # Create requests object of result url
    result_url = browser.current_url
    res = requests.get(result_url)
    # Create soup object
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    # Check if result page is not an Ad
    try:
        adElem = browser.find_element_by_link_text('Ad')
        htmlElem.send_keys(Keys.RIGHT)
    # If result page not an ad
    except:
        # Find img elements on page
        imageElem = soup.select('img')
        # Check if img elements were foud:
        if not imageElem:
            print('Image was not found')
        else:
            try:
                # Get correct image url from soup
                imageUrl = 'http:' + imageElem[2].get('src')
                # Check if image url is valid
                res = requests.get(imageUrl)
                res.raise_for_status()
            # Filter missing images
            except requests.exceptions.MissingSchema:
                htmlElem.send_keys(Keys.RIGHT)
                continue
        # Create image file in flickr directory
        imageFile = open(os.path.join('flickr', os.path.basename(imageUrl)), 'wb')
        # Save image in file
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
        # Move to next image in results
        htmlElem = browser.find_element_by_tag_name('html')
        htmlElem.send_keys(Keys.RIGHT)
        posts -= 1
browser.close()
os.system('explorer.exe flickr')
print('Done')
