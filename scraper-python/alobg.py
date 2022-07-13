import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import re
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://www.alo.bg/"
# listing_url = "https://www.alo.bg/8157555"

regex_photos = r'user_files\/[a-z]\/.*\/\d+_\d*_big\.jpg'
regex_listing = r'\/\d+'
regex_currency = r'[^a-zA-Zа-яА-Я]+'


def wait_element(driver, by: By, selector, time=20):
    try:
        return WebDriverWait(driver, time).until(EC.presence_of_element_located((by, selector)))
    except:
        return False


def get_photos(page_source):
    matches = re.findall(regex_photos, page_source)
    urls = [base_url + x for x in matches]
    return urls

def get_extras(driver):
    extras = []
    extrasEl = driver.find_elements(By.CLASS_NAME, 'ads-params-multi')
    for extraEl in extrasEl:
        extras.append(extraEl.text.strip())
    return extras

def scrape_listing(driver, listing_id=8157555):
    data = {
        'id': 0,
        'url': "",
        'from': "",
        'listingType': "",
        'title': "",
        'description': "",
        'price': 0,
        'currency': "",
        # 'price_string': "",
        'pricesqm': 0,
        'year': 0,
        'type': "",
        'address': "",
        'area': "",
        'area_string': "",
        'buildingType': "",
        'furniture': "",
        'floor': "",
        'floorNumber': "",
        'status': "",
        'agents': [],
        'extras': [],
        'photos': [],
    }

    if type(listing_id) is int:
        listing_url = f"https://www.alo.bg/{listing_id}"
    elif "http" in listing_id:
        listing_url = listing_id
    else:
        listing_url = None

    if listing_url is None:
        return

    id = listing_url.split('/')[-1]
    data['id'] = int(id)
    data['url'] = listing_url

    driver.get(listing_url)
    title = wait_element(driver, By.CSS_SELECTOR,
                         '.large-headline.highlightable')
    if title:
        data['title'] = title.text.strip()
        description = wait_element(driver, By.CSS_SELECTOR, '.word-break-all.highlightable')
        data['description'] = description.text.strip()

    info_rows_elements = driver.find_elements(By.CLASS_NAME,
                                              'ads-params-row')
    for row in info_rows_elements:
        text = row.text.strip()
        rowData = text.split(":")[1].strip()
        if 'Вид на имота' in text:
            data['type'] = rowData
        elif 'Местоположение' in text:
            data['address'] = re.sub(' +', ' ', rowData).split(", (")[0]
        elif 'Степен на завършеност' in text:
            data['status'] = rowData.split(" ")[0]
        elif 'Година на строителство' in text:
            regexYear = re.search('\d{4}', rowData)
            if regexYear:
                data['year'] = int(regexYear.group(0))
        elif 'Обзавеждане' in text:
            data['furniture'] = rowData
        elif 'Номер на етажа' in text:
            regexFloor = re.search('\d+', rowData)
            if regexFloor:
                data['floorNumber'] = regexFloor.group(0)
        elif 'Етаж' in text:
            data['floor'] = rowData
        elif 'Квадратура' in text:
            data['area_string'] = rowData
            data['area'] = re.search('\d+', rowData).group(0)
        elif 'Обява от' in text:
            data['from'] = ':'.join(text.split(":")[1:]).strip()
        elif 'Вид строителство' in text:
            data['buildingType'] = rowData
        elif 'Цена' in text or 'Месечен наем' in text:
            if 'Не е обявена' in rowData:
                continue
            if 'Цена' in text:
                data['listingType'] = 'sell'
            elif 'Месечен наем' in text:
                data['listingType'] = 'rent'
            try:
                sqmPriceEl = row.find_element(
                By.CLASS_NAME, 'ads-params-price-sub')
                sqmPriceText = sqmPriceEl.text.strip()
                sqmPrice = float(''.join(sqmPriceText.split()[:-1]))
                priceText = rowData.replace(sqmPriceText, '')
                splitPrice = priceText.split()
                currency = splitPrice[-1]
                price = ''.join(splitPrice[:-1])
            except NoSuchElementException:
                splitPrice = rowData.split()
                currency = splitPrice[-1]
                price = ''.join(splitPrice[:-1])
                sqmPrice =  0
                priceText = rowData
            data['currency'] = re.sub(regex_currency, '', currency).upper()
            data['price'] = float(price)
            # data['price_string'] = ' '.join(splitPrice) + re.sub(regex_currency, '', splitPrice[-1]).upper()
            data['pricesqm'] = sqmPrice
    extras = get_extras(driver)
    photos = get_photos(driver.page_source)
    data['photos'] = photos
    data['extras'] = extras
    return data

def scrape_urls(driver, start_url):
    links = []
    done = False
    i = 1
    while not done:
        driver.get(start_url + f"&page={i}")
        if '404 Not Found' in driver.page_source:
            done = True
            break
        containerEl = wait_element(driver, By.ID, "content_container", 5)
        linkEls = containerEl.find_elements(By.TAG_NAME, "a")
        for linkEl in linkEls:
            linkHref = linkEl.get_attribute('href')
            if not linkHref is None and linkHref.split("/")[-1].isnumeric() and "alo.bg" in linkHref:
                if linkHref not in links:
                    links.append(linkHref)
        time.sleep(0.01)
        i += 1
    return links

def main():
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument("--incognito")
    driver = webdriver.Firefox(options=options)
    driver.install_addon(os.path.dirname(os.path.abspath(__file__))+"\\ga-optout.xpi")
    driver.set_window_size(1920, 1080)
    driver.get("https://alo.bg")

    cookies = wait_element(driver, By.ID, 'button_i_accept', 5)
    if cookies:
        cookies.click()

    # TEMP TEMP TEMP
    scrape_listings = scrape_urls(driver, 'https://www.alo.bg/obiavi/imoti-naemi/apartamenti/?region_id=2')
    data_arr = []
    for listing in scrape_listings:
        data_arr.append(scrape_listing(driver, listing))
        time.sleep(0.01)

    jsonString = json.dumps(data_arr, ensure_ascii=False)
    jsonFile = open("data.json", "w", encoding="utf-8")
    jsonFile.write(jsonString)
    jsonFile.close()

    driver.quit()
    print(jsonString)


if __name__ == "__main__":
    main()
