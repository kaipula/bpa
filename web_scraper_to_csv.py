import csv
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGES = 3
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def scrape_page(page_no):
    response = requests.get(BASE_URL.format(page_no), timeout=15)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price_text = article.select_one("p.price_color").text
        price = float(re.sub(r"[^\d.]", "", price_text))
        rating = RATINGS.get(article.select_one("p.star-rating")["class"][1], 0)
        stock = article.select_one("p.availability").text.strip()
        books.append({"Title": title, "Price": price, "Rating": rating, "Stock": stock})
    return books


if __name__ == "__main__":
    all_books = []
    for page in range(1, TOTAL_PAGES + 1):
        books = scrape_page(page)
        all_books.extend(books)
        print(f"Page {page} scraped - {len(books)} books found")

    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Rating", "Stock"])
        writer.writeheader()
        writer.writerows(all_books)

    print(f"\nTotal {len(all_books)} records exported to books.csv")
    print("\nFirst 5 records:")
    for b in all_books[:5]:
        print(f"  {b['Title'][:38]:<38}  GBP {b['Price']:>6}  {b['Rating']} star")
