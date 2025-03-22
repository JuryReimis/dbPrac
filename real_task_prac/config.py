import datetime
from pathlib import Path

from dotenv import load_dotenv
import os


load_dotenv('.env')

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')


BULLETINS_DIR = Path(__file__).resolve().parent / 'bulletins'

URL = "https://spimex.com/"

DATE_FORMAT = "%d.%m.%Y"

REPORTING_START_DATE = datetime.datetime.strptime('01.01.2023', DATE_FORMAT)
