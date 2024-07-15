import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

GOOGLE_FORM = "https://forms.gle/ZDNZ2bQj5iiwC2369"

class DataFill:
    def __init__(self):
        self.FORM_URL = GOOGLE_FORM

        # Keep Chrome browser open after program finishes
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)

    def auto_fill(self, address, price, link):
        self.driver.get(self.FORM_URL)

        try:
            address_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="i1"]'))
            )
            price_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="i5"]'))
            )
            link_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="i9"]'))
            )
            submit_form = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="button"].uArJ5e.UQuaGc.Y5sE8d.VkkpIf.QvWxOd'))
            )

            address_box.send_keys(address)
            price_box.send_keys(price)
            link_box.send_keys(link)
            submit_form.click()

            # Wait for the form to submit and the confirmation page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.freebirdFormviewerViewResponseConfirmationMessage'))
            )

            # Look for the "Submit another response" link
            # Click "Submit another response" link
            time.sleep(0.1)
            submit_another = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            submit_another.click()

        except Exception as e:
            print(f"Error occurred: {e}")

class ScrapeZillowData:
    def __init__(self, url):
        self.url = url
        self.property_address = []
        self.property_price = []
        self.property_link = []

    def scrape_data(self):
        response = requests.get(self.url)
        website_html = response.text
        soup = BeautifulSoup(website_html, "html.parser")

        self.property_address = soup.find_all(name="address", attrs={"data-test": "property-card-addr"})
        self.property_price = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
        self.property_link = soup.find_all(name="a", attrs={"data-test": "property-card-link"})

    def clean_address(self, address_text):
        # Remove extra spaces, newlines, and vertical bars from address text
        cleaned_address = address_text.strip().replace("\n", "").replace("|", "")
        return cleaned_address

    def get_data(self):
        list_dictionary = {
            "Address": [],
            "Price": [],
            "Link": [],
        }

        for address in self.property_address:
            # Clean up the address text
            cleaned_address = self.clean_address(address.get_text())
            list_dictionary["Address"].append(cleaned_address)

        for price in self.property_price:
            # Extracting only the dollar amount
            price_text = price.get_text().strip()
            price_cleaned = ''.join(filter(lambda x: x.isdigit() or x == '$', price_text))
            # Adding comma in number eg 1,234
            formatted_price = "${:,}".format(int(price_cleaned.replace('$', '')))
            list_dictionary["Price"].append(formatted_price)

        for link in self.property_link:
            href = link["href"]
            if not href.startswith("http"):
                href = "https://www.zillow.com" + href
            list_dictionary["Link"].append(href)

        return list_dictionary

# Export a CSV copy of the data
def export_to_csv(data):
    with open('zillow_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Address', 'Price', 'Link'])
        writer.writeheader()
        for i in range(len(data["Address"])):
            writer.writerow({
                'Address': data["Address"][i],
                'Price': data["Price"][i],
                'Link': data["Link"][i],
            })

if __name__ == "__main__":
    ZILLOW_URL = "https://shorturl.at/FLl6X"
    scraper = ScrapeZillowData(ZILLOW_URL)
    scraper.scrape_data()
    data = scraper.get_data()
    print(data)

    export_to_csv(data)

    filler = DataFill()
    for i in range(len(data["Address"])):
        filler.auto_fill(data["Address"][i], data["Price"][i], data["Link"][i])
