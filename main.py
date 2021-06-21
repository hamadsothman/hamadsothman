from bs4 import BeautifulSoup
import requests
from googlesearch import search
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div

my_results_list = []
query = "my life goal is "

for i in search(query, # The query you want to run
    tld = 'com',  # The top level domain
    lang = 'en',  # The language
    num = 10,  # Number of results per page
    start = 0,  # First result to retrieve
    stop = 10,  # Last result to retrieve
    pause = 2.0,  # Lapse between HTTP requests
    ):
    my_results_list.append(i)
    print(i)

html = []

for links in my_results_list:
    goals_website_html = requests.get(f"{links}").text
    soup = BeautifulSoup(goals_website_html, "lxml")

# goals_text_html = requests.get("https://www.google.com/search?client=firefox-b-d&q=my+life+goal+is+to").text
# soup = BeautifulSoup(goals_text_html, "lxml")
# results = soup.find_all("div", class_ = "g")
#
# print(soup)
# print(results)