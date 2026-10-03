from bs4 import BeautifulSoup

from scraper.fetchers import PlaywrightFetcher


def main() -> None:
    url = "https://quotes.toscrape.com/js/"

    with PlaywrightFetcher(headless=True) as fetcher:
        print(f"📥 Загружаю {url}")
        html = fetcher.fetch(url)

    if not html:
        print("❌ Не удалось загрузить страницу")
        return

    print(f"✅ Получено {len(html):,} байт HTML")

    soup = BeautifulSoup(html, "lxml")
    quotes = soup.select(".quote")

    for q in quotes[:3]:
        text = q.select_one(".text").get_text(strip=True)
        author = q.select_one(".author").get_text(strip=True)
        print(f"   • {text[:70]}... — {author}")


if __name__ == "__main__":
    main()
