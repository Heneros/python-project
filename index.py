import requests
from bs4 import BeautifulSoup
import csv 
import time 
from urllib.parse import urljoin, urlparse 
from watchfiles import watch
import asyncio
from database.session import engine
from database.queries import create_user, get_user_by_tid, update_user_settings
from database.models import Base 

print("Watch")


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы созданы/проверены!")

    # user = await create_user(
    #     telegram_id=123456789, 
    #     username="homer_dev",
    #     settings={"language": "ru", "notifications": True}
    # )


if __name__ == "__main__":
    asyncio.run(main())


# class WebScraper:
#     def __init__(self, base_url, headers=None):
#         self.base_url = base_url
#         self.session = requests.Session()

#     default_headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }

#     if headers:
#         default_headers.update(headers)

#     self.session.headers.update(default_headers)


#     def get_page(self, url):
#          """Récupère le contenu d'une page web"""
#          try: 
#              response = self.session.get(url, timeout=10)
#              response.raise_for_status()
#              return response 
#          except requests.exceptions.RequestException as e:
#              print(f"Err get_page  {e}")
#              return None 