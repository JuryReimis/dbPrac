from datetime import datetime

import requests
from bs4 import Tag, BeautifulSoup

from real_task_prac.config import URL, REPORTING_START_DATE


class UrlParser:

    def __init__(self):
        self.default_url = URL + 'markets/oil_products/trades/results/'

    @staticmethod
    def get_bulletins_date(link: Tag):
        date = link.parent.parent.find('span').text
        datetime_format = datetime.strptime(date, "%d.%m.%Y")
        return datetime_format

    @staticmethod
    def get_data_from_site(url: str) -> BeautifulSoup | None:
        response = requests.get(url)
        if response.status_code == 404:
            return None
        return BeautifulSoup(response.text, 'html.parser')

    def get_links(self, soup: BeautifulSoup, break_flag: bool = False) -> tuple[list[str], bool]:
        result = []
        # Поиск по ссылкам на xls файлы с определенным текстом заголовка ссылки
        links = [link for link in soup.select('a.accordeon-inner__item-title.link.xls') if
                 link.text == "Бюллетень по итогам торгов в Секции «Нефтепродукты»"]
        for link in links:
            if self.get_bulletins_date(link) < REPORTING_START_DATE:  # Проверка даты документа
                print("Остановка парсинга, найдена дата", self.get_bulletins_date(link))
                break_flag = True
                break
            result.append(link.get('href'))
        return result, break_flag

    def parse(self) -> list[str]:
        result = []
        page = 1
        while True:
            # Пока цикл не получит break_flag, будет обрабатывать новые страницы
            print(f"Парсинг страницы #{page}")
            soup = self.get_data_from_site(f'{self.default_url}?page=page-{page}')
            if soup is None:
                # Если в status_code пришел 404 - остановка работы. На сайте кончились страницы.
                print(f"Страница № {page} не найдена. Остановка работы")
                break
            links, break_flag = self.get_links(soup)
            result.extend(links)
            if break_flag is True:
                break
            page += 1
        return result

    @staticmethod
    def download_by_link(link):
        response = requests.get(URL + link)
        return response

