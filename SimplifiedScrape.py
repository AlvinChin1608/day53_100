import requests
from bs4 import BeautifulSoup
from pprint import pprint

ZILLOW_URL = "https://shorturl.at/FLl6X"

response = requests.get(ZILLOW_URL)
website_html = response.text
pprint(website_html)

soup = BeautifulSoup(website_html, "html.parser")

property_address = soup.find_all(name="address", attrs={"data-test": "property-card-addr"})
property_price = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
property_link = soup.find_all(name="a", attrs={"data-test": "property-card-link"})


list_dictionary = {
    "Address": [],
    "Price": [],
    "Link": [],
}

for address in property_address:
    list_dictionary["Address"].append(address.get_text())

for price in property_price:
    list_dictionary["Price"].append(price.get_text())

for link in property_link:
    href = link["href"]
    if not href.startswith("http"):
        href = "https://www.zillow.com"+href
    list_dictionary["Link"].append(href)

print(list_dictionary)