import requests
from bs4 import BeautifulSoup
import csv


url = "https://bbc.com"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
data = []
headings = soup.find_all("h2")
for head in headings:
    data.append(head.text)
# print(data[:10])

links = soup.find_all("a")
link_ = []
for link in links:
    href = link.get("href")
    if href and href.startswith('http'):
        link_.append(href)
print(link_[:10])