from real_task_prac.config import DATE_FORMAT
from real_task_prac.file_processor import FileProcessor
from real_task_prac.models import Result
from real_task_prac.models.database import BaseModel, engine, Session
from real_task_prac.parsers.url_parser import UrlParser


if __name__ == '__main__':
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)

    url_parser = UrlParser()
    urls = url_parser.parse()
    file_processor = FileProcessor(urls, url_parser)
    file_processor.write_files()
    tables = file_processor.iterate_files()

    for key in sorted(tables.keys()):
        # Для каждого отчета создается своя транзакция
        with Session() as sess:
            print(f"Запись отчета за {key.strftime(DATE_FORMAT)}")
            new_rows = []
            for dto in file_processor.get_rows(tables[key]):
                result_data = {
                    'exchange_product_id': dto.exchange_product_id,
                    'exchange_product_name': dto.exchange_product_name,
                    'oil_id': dto.oil_id,
                    'delivery_basis_id': dto.delivery_basis_id,
                    'delivery_basis_name': dto.delivery_basis_name,
                    'delivery_type_id': dto.delivery_type_id,
                    'volume': dto.volume,
                    'total': dto.total,
                    'count': dto.count,
                    'date': key
                }
                new_rows.append(result_data)
            sess.bulk_insert_mappings(Result, new_rows)
            sess.commit()
