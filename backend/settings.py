from dotenv import load_dotenv
import os

load_dotenv()
database_name = os.environ.get("DB_NAME")