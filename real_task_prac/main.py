import asyncio
from datetime import datetime
from time import time

from pandas import DataFrame

from real_task_prac.config import DATE_FORMAT
from real_task_prac.file_processor import FileProcessor
from real_task_prac.models import Result
from real_task_prac.models.database import BaseModel, async_engine, AsyncSession
from real_task_prac.parsers.url_parser import UrlParser


async def insert_bulletin(table: DataFrame, date: datetime, session: AsyncSession, file_processor: FileProcessor):
    async for dto in file_processor.get_rows(table):
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
            'date': date
        }
        session.add(Result(**result_data))


async def main():
    async with async_engine.connect() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    url_parser = UrlParser()
    urls = await url_parser.parse()
    file_processor = FileProcessor(urls, url_parser)
    await file_processor.write_files()
    async with AsyncSession() as session:
        await file_processor.iterate_files(insert_bulletin, session)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    start_time = time()

    asyncio.run(main())

    print(f"Общее время выполнения: {time() - start_time}")
