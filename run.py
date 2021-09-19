
from src import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app(os.getenv("FLASK_ENV"))
