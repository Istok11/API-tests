import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000/").rstrip("/")
TIMEOUT = int(os.getenv("TIMEOUT", 10))