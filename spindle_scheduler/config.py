import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent)


DB_URL = os.environ["DB_URL"]

DB_SCHEMA = os.environ["DB_SCHEMA"]
