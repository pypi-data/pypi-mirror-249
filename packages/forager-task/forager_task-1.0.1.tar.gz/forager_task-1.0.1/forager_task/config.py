import os

from dotenv import load_dotenv

load_dotenv()

HUNTER_API_KEY = os.environ.get('HUNTER_API_KEY')
