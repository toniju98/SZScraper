from splinter import Browser
from bs4 import BeautifulSoup
import json
from time import sleep


def scrape():
    time = "null"
    title = "null"
    keywords = "null"
    summary = "null"
    text = "null"

    if soup.find_all("time"):
        time = soup.find("time")['datetime']

    if soup.find_all("span", "css-1kuo4az"):
        title = soup.find("span", "css-1kuo4az").get_text()

    if soup.find_all("span", "css-1keap3i"):
        keywords = soup.find("span", "css-1keap3i").get_text()

    if soup.find_all("p", "css-1psf6fc"):
        summary = soup.find("p", "css-1psf6fc").get_text()

    if soup.find_all("div", "css-isuemq e1lg1pmy0"):
        text = soup.find("div", "css-isuemq e1lg1pmy0").get_text()

    return time, title, keywords, summary, text


def save_articles(weblink):
    time, title, keywords, summary, text = scrape()
    json_form = {"headline": title, "date": time,
                 "text": text, "category": keywords, "author": time,
                 "summary": summary, "url": weblink}
    return json_form


def save_all(all_articles):
    articles = {'articles': all_articles}
    # TODO: insert location where to store the json
    with open("YOUR_FILE_NAME", "w", encoding="utf8") as outfile:
        json.dump(articles, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # State the location of your driver
    # TODO: download chromedriver.exe and insert path to your .exe
    executable_path = {"executable_path": "YOUR_PATH_TO_CHROMEDRIVER.EXE"}
    # Instantiate a browser object as follows...
    # Pass 'headless=False' to make Chrome launch a visible window
    browser = Browser("chrome", **executable_path, headless=False)
    newspaper_url = 'https://www.sueddeutsche.de/politik'
    browser.visit(newspaper_url)
    sleep(30)
    soup = BeautifulSoup(browser.html, 'html.parser')
    article_head = soup.find_all("div", "mainpage department")
    articles = soup.find("div", "mainpage department sz-page__main-column")
    articles_new = soup.find_all("div", "sz-teaserlist-element sz-teaserlist-element--separator-line")
    links = []
    for a in articles_new:
        b = "null"
        if a.find_all("a", href=True):
            b = a.find("a", href=True)
            links.append(b['href'])
    all_articles_list = []
    for link in links:
        browser.visit(link)
        soup = BeautifulSoup(browser.html, 'html.parser')
        scrape()
        all_articles_list.append(save_articles(link))
    save_all(all_articles_list)
