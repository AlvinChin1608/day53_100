from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FORM_URL = "https://forms.gle/ZDNZ2bQj5iiwC2369"

"I created this mainly to test the CSS selector and XPATH of the HTML ELement"

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)


address_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="i1"]')))
address_box.send_keys("Test", Keys.TAB)

price_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="i5"]')))
price_box.send_keys("Test", Keys.TAB)

link_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="i9"]')))
link_box.send_keys("Test", Keys.TAB)

submit_form = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="button"].uArJ5e.UQuaGc.Y5sE8d.VkkpIf.QvWxOd')))

submit_form.send_keys(Keys.ENTER)

submit_another = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))

submit_another.click()