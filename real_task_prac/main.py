import asyncio
from time import time

from real_task_prac.config import DATE_FORMAT
from real_task_prac.file_processor import FileProcessor
from real_task_prac.models import Result
from real_task_prac.models.database import BaseModel, async_engine, AsyncSession
from real_task_prac.parsers.url_parser import UrlParser


async def main():
    async with async_engine.connect() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    url_parser = UrlParser()
    urls = await url_parser.parse()
    file_processor = FileProcessor(urls, url_parser)
    await file_processor.write_files()
    tables = await file_processor.iterate_files()

    start_insert_time = time()
    for key in sorted(tables.keys()):
        # Для каждого отчета создается своя транзакция
        async with AsyncSession() as sess:
            print(f"Запись отчета за {key.strftime(DATE_FORMAT)}")
            new_rows = []
            async for dto in file_processor.get_rows(tables[key]):
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
                new_rows.append(Result(**result_data))
            sess.add_all(new_rows)
            await sess.commit()
    print(f"Загрузка в базу данных завершена за {time() - start_insert_time}")


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    start_time = time()

    asyncio.run(main())

    print(f"Общее время выполнения: {time() - start_time}")
