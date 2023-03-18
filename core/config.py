import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = 'nbcX80iPChLIAJQRqBG4IDsiyM62uLEqsXYOuI4gyMgSWW2XQCTXHaLEjj4js4Qx' #  os.getenv('API_KEY')
SECRET_KEY = '55vLHUNUQ0ICj2eFCQNul0aqBEGje3Dy8NpAGevur6OQP2K6iu6yj1loybLWN2yw' #  os.getenv('SECRET_KEY')

DB_ROOT = 'sqlite+aiosqlite:///./'
DB_NAME = 'binance.db'
