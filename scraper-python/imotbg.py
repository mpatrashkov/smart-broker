from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
url = 'https://www.imot.bg/pcgi/imot.cgi?act=5&adv=1a164785296310473&slink=8712mk&f1=11'
driver.get(url)
driver.find_element(By.CLASS_NAME, "fc-cta-consent").click()
features_arr = []
features_el = driver.find_elements(
    By.XPATH, "/html/body/div[2]/table/tbody/tr[1]/td[1]/form/table[3]/tbody/tr/td")
for feature in features_el:
    features_arr.append(feature.text.split('\n'))
features = []
for el in features_arr:
    features += el
for i in range(len(features)):
    features[i] = features[i][2:]
features = [i for i in features if i]
driver.find_element(By.ID, "dots_link_more").click()
picture_links = []
pictures_moving = driver.find_element(By.ID, "pictures_moving")
for picture in pictures_moving.find_elements(By.CSS_SELECTOR, "a"):
    picture_links.append(f'https:{picture.get_attribute("data-link")}')
property = {
    "title": driver.find_element(By.CSS_SELECTOR, "div.advHeader > div.title").text,
    "price": driver.find_element(By.ID, "cena").text,
    "price_per_sq_meter":  driver.find_element(By.ID, "cenakv").text,
    "address": driver.find_element(By.CSS_SELECTOR, "div.advHeader > div.info > div.location").text,
    "area": driver.find_element(By.CSS_SELECTOR, ".adParams > div:nth-child(1)").text,
    "floor": driver.find_element(By.CSS_SELECTOR, ".adParams > div:nth-child(2)").text,
    "type": driver.find_element(By.CSS_SELECTOR, ".adParams > div:nth-child(3)").text,
    "description": driver.find_element(By.ID, "description_div").text,
    "features": features,
    "pictures": picture_links
}
agency = {
    "title": driver.find_element(By.CSS_SELECTOR, "a.name").text,
    "phone": driver.find_element(By.CSS_SELECTOR, "div.phone").text,
    "address": driver.find_element(By.CSS_SELECTOR, "div.adress:nth-child(5)").text
}
print(property)
print(agency)
driver.quit()
