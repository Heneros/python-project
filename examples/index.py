import datetime
import random
from urllib.request import urlopen

from bs4 import BeautifulSoup

random.seed(datetime.datetime.now().timestamp())


# pages = set()


# def getLinks(articleUrl):
#     req = Request(
#         f"http://en.wikipedia.org{articleUrl}",
#         headers={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         },
#     )
#     html = urlopen(req)
#     bs = BeautifulSoup(html, "html.parser")

#     try:
#         print(bs.h1.getText())
#         bodyContent = bs.find("div", {"id": "bodyContent"}).find_all("p")
#         if len(bodyContent):
#             print(bodyContent[0])
#         print(bs.find(id="ca-edit").find("a").attrs["href"])
#         print(bs.h1.get_text())
#         print(bs.find(id="mw-content-text").find_all("p")[0])
#         print(bs.find(id="ca-edit").find("span").find("a").attrs["href"])
#     except AttributeError:
#         print("This page is missing something! Continuing.")

#     for link in bs.find_all("a", href=re.compile("^(/wiki/)")):
#         if "href" in link.attrs:
#             if link.attrs["href"] not in pages:
#                 newPage = link.attrs["href"]
#                 print("-" * 20)
#                 print(newPage)
#                 pages.add(newPage)
#                 getLinks(newPage)


from urllib.request import Request


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f"URL: {self.url}")
        print(f"TITLE: {self.title}")

        print(f"BODY: \n{self.body[:500]}...")


class Website:
    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:
    def getPage(url):
        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            },
        )
        try:
            html = urlopen(req, timeout=10)
        except Exception as e:
            print(f" Error loalong {url}: {e}")
            return None
        return BeautifulSoup(html.read(), "html.parser")

    def safeGet(bs, selector):
        try:
            elems = bs.select(selector)
        except Exception:
            return ""
        if elems:
            return "\n".join(e.get_text(strip=True) for e in elems)
        return ""



    def getContent(website, path):
        if not path.startswith("/"):
            path = "/" + path
        url = website.url.rstrip("/") + path
        bs = Crawler.getPage(url)
        if bs is None:
            return Content(url, "", "")
        title = Crawler.safeGet(bs, website.titleTag)
        body = Crawler.safeGet(bs, website.bodyTag)
        return Content(url, title, body)


siteData = [
    ["O'Reilly Media", "https://www.oreilly.com", "h1", "div.title-description"],
    ["Reuters", "https://www.reuters.com", "h1", "div.ArticleBodyWrapper"],
    ["Brookings", "https://www.brookings.edu", "h1", "div.post-body"],
    ["CNN", "https://edition.cnn.com", "h1", "body"],
    ["WIKI", "https://wikipedia.org/wiki", "h1", "div#mp-upper"],
]

websites = [Website(name, url, t, b) for name, url, t, b in siteData]


Crawler.getContent(
    websites[4],
    "/Main_Page",
).print()
