from pathlib import Path
from typing import Optional

import pandas as pd
from pandas import DataFrame


class XLSParser:

    def __init__(self, file_path: Path):
        pd.set_option("display.max_rows", None)  # Показать все строки
        pd.set_option("display.max_columns", None)  # Показать все столбцы

        self.path = file_path

    def read_excel(self, start_marker="Единица измерения: Метрическая тонна") -> tuple[
        Optional[dict],
        Optional[DataFrame],
        Optional[str]
    ]:
        try:
            print(f"Обработка файла {self.path}")
            # Чтение файла
            df = pd.read_excel(self.path, engine="xlrd", header=None)

            bulletin_date = df[1][3].split('Дата торгов: ')[1].strip()

            # Поиск строки с маркером
            start_index = df[df[1] == start_marker].index
            if len(start_index) == 0:
                raise ValueError(f"Маркер '{start_marker}' не найден в файле.")
            start_index = start_index[0]

            # Извлечение заголовков
            header1 = df.iloc[start_index + 1]
            header2 = df.iloc[start_index + 2]

            # Создание словаря индексов
            header_dict = {}
            last_h1 = None
            for idx in range(len(header1)):
                if pd.notna(header1[idx]):
                    h1 = header1[idx]
                    last_h1 = h1
                else:
                    h1 = last_h1
                h2 = header2[idx] if pd.notna(header2[idx]) else ""

                if h2 == "":
                    header_dict[h1] = idx
                else:
                    header_dict[f"{h1} {h2}"] = idx

            # Извлечение таблицы (начиная с третьей строки после заголовка)
            table_data = []  # Список для хранения строк таблицы
            last_column_index = len(header1) - 1  # Индекс последнего столбца

            for row_index in range(start_index + 3, len(df)):
                row = df.iloc[row_index]

                # Проверка, является ли строка пустой (конец таблицы)
                if row.isnull().all() or row.count() <= 5:
                    break

                # Проверка, что значение в последнем столбце > 0
                last_value = row[last_column_index]
                try:
                    last_value = int(last_value)
                except ValueError:
                    last_value = 0
                if pd.notna(row[last_column_index]) and last_value > 0:
                    table_data.append(row.tolist())

            # Создание DataFrame из отфильтрованных строк
            table = pd.DataFrame(table_data, columns=[
                f"{header1[idx]} {header2[idx]}" if pd.notna(header2[idx]) else header1[idx]
                for idx in range(len(header1))])

            return header_dict, table, bulletin_date
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            return None, None, None
