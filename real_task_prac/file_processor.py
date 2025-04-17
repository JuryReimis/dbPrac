from datetime import datetime
from pathlib import Path
from time import time
from typing import Generator

from pandas import DataFrame

from real_task_prac.config import BULLETINS_DIR, DATE_FORMAT
from real_task_prac.dto.row_to_result_model_dto import RowToResultModelDTO
from real_task_prac.parsers.XLS_parser import XLSParser
from real_task_prac.parsers.url_parser import UrlParser


class FileProcessor:

    def __init__(self, links: list[str], parser: UrlParser):
        self.links = links
        self.parser = parser
        self.check_dirs()

    @staticmethod
    def check_dirs():
        if BULLETINS_DIR.exists():
            print('Директория найдена')
            return
        print(f"Создаю {BULLETINS_DIR}")
        BULLETINS_DIR.mkdir()

    @staticmethod
    def get_date_format(date: str) -> datetime:
        date_format = datetime.strptime(date, DATE_FORMAT)
        return date_format

    def write_files(self):
        start_time = time()
        for url in self.links:
            file_name = Path(url).name.split(
                '.xls'
            )[0] + '.xls'
            if (BULLETINS_DIR / file_name).exists():
                continue
            response = self.parser.download_by_link(url)
            if response.status_code == 200:
                with (BULLETINS_DIR / file_name).open(mode='wb') as f:
                    f.write(response.content)
        print(f"Загрузка и запись файлов на диск завершена за {time() - start_time}")

    def iterate_files(self) -> dict[datetime, DataFrame]:
        start_time = time()
        tables = dict()
        for file in BULLETINS_DIR.iterdir():
            if file.is_file() and file.suffix == '.xls':
                dictionary, result, date = XLSParser(file).read_excel()
                tables[self.get_date_format(date)] = result
        print(f"Обработка файлов завершена за {time() - start_time}")
        return tables

    @staticmethod
    def get_rows(table: DataFrame) -> Generator[RowToResultModelDTO, None, None]:
        for index, row in table.iterrows():
            exchange_product_id: str = row.iloc[1]
            exchange_product_name: str = row.iloc[2]
            delivery_basis_name: str = row.iloc[3]
            volume: int = row.iloc[4]
            total: int = row.iloc[5]
            count: int = row.iloc[-1]

            yield RowToResultModelDTO(
                exchange_product_id=exchange_product_id,
                exchange_product_name=exchange_product_name,
                oil_id=exchange_product_id[:4],
                delivery_basis_id=exchange_product_id[4:7],
                delivery_basis_name=delivery_basis_name,
                delivery_type_id=exchange_product_id[-1],
                volume=volume,
                total=total,
                count=count
            )
