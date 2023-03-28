import requests
import json
from bs4 import BeautifulSoup
import time

scraping_hn = True
page = 1
output = []

headers = { 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

print('Starting Hacker News Scraper...')

# Continue scraping until the scraper reaches the last page
while scraping_hn:
    time.sleep(0.5) # Wait before each request to avoid overloading the server
    response = requests.get(f"https://news.ycombinator.com/?p={page}", headers=headers)
    html = response.text

    print(f"Scraping {response.url}")

    # Use Beautiful Soup to parse the HTML
    soup = BeautifulSoup(html, features="html.parser")
    articles = soup.find_all(class_="athing")

    # Extract data from each article on the page
    for article in articles:
        data = {
            "URL": article.find(class_="titleline").find("a").get('href'),
            "title": article.find(class_="titleline").getText(),
            "rank": article.find(class_="rank").getText().replace(".", "")
        }
        output.append(data)

    # Check if the scraper reached the last page
    next_page = soup.find(class_="morelink")

    if next_page != None:
        page += 1
    else:
        scraping_hn = False
        print(f'Finished scraping! Scraped a total of {len(output)} items.')

# Save scraped data
print('Saving output data to JSON file.')
save_output = open("hn_data.json", "w")  
json.dump(output, save_output, indent = 6, ensure_ascii=False)
save_output.close()