import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = 'nbcX80iPChLIAJQRqBG4IDsiyM62uLEqsXYOuI4gyMgSWW2XQCTXHaLEjj4js4Qx' #  os.getenv('API_KEY')
SECRET_KEY = '55vLHUNUQ0ICj2eFCQNul0aqBEGje3Dy8NpAGevur6OQP2K6iu6yj1loybLWN2yw' #  os.getenv('SECRET_KEY')

DB_ROOT = 'sqlite+aiosqlite:///./'
DB_NAME = 'binance.db'

CLOSE = 4
HIGH = 2
LOW = 3

INDEX_FOR_1MIN = 0
INDEX_FOR_5MIN = 1
INDEX_FOR_15MIN = 2

H1_TIMESTAMP = 3600

EVERY_5MINUTES = (0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55)
EVERY_15MINUTES = (0, 15, 30, 45)
