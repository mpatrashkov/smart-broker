import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json

base_url = "https://www.alo.bg/"
# listing_url = "https://www.alo.bg/8157555"

regex_photos = r'user_files\/[a-z]\/.*\/\d+_\d*_big\.jpg'


def wait_element(driver, by: By, selector, time=20):
    try:
        return WebDriverWait(driver, time).until(EC.visibility_of_element_located((by, selector)))
    except:
        return False


def get_photos(page_source):
    matches = re.findall(regex_photos, page_source)
    urls = [base_url + x for x in matches]
    return urls


def scrape_listing(driver, listing_id=8157555):
    data = {
        'id': 0,
        'url': "",
        'from': "",
        'title': "",
        'description': "",
        'price': 0,
        'currency': "",
        'price_string': "",
        'pricesqm': 0,
        'year': 0,
        'type': "",
        'address': "",
        'area': "",
        'area_string': "",
        'buildingType': "",
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
            data['from'] = ''.join(text.split(":")[1:]).strip()
        elif 'Вид строителство' in text:
            data['buildingType'] = rowData
        elif 'Цена' in text:
            sqmPriceEl = row.find_element(
                By.CLASS_NAME, 'ads-params-price-sub')
            sqmPriceText = sqmPriceEl.text.strip()
            sqmPrice = float(''.join(sqmPriceText.split()[:-1]))
            priceText = rowData.replace(sqmPriceText, '')
            splitPrice = priceText.split()
            currency = splitPrice[-1]
            price = ''.join(splitPrice[:-1])
            data['currency'] = currency
            data['price'] = float(price)
            data['price_string'] = priceText
            data['pricesqm'] = sqmPrice
    photos = get_photos(driver.page_source)
    data['photos'] = photos
    return data


def main():
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get("https://alo.bg")

    cookies = wait_element(driver, By.ID, 'button_i_accept', 5)
    if cookies:
        cookies.click()

    # TEMP TEMP TEMP
    scrape_listings = [8157555, 8079387, 8027337, 8090750]

    data_arr = []
    for listing in scrape_listings:
        data_arr.append(scrape_listing(driver, listing))

    jsonString = json.dumps(data_arr, ensure_ascii=False)
    jsonFile = open("data.json", "w", encoding="utf-8")
    jsonFile.write(jsonString)
    jsonFile.close()


if __name__ == "__main__":
    main()
