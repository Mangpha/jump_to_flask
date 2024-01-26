import os
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv(verbose=True)

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = URL.create(
    "postgresql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT"),
)
# "postgresql://{user}:{pw}@{url}:{port}/{db}".format(
#     user=os.getenv("DB_USER"),
#     pw=os.getenv("DB_PASSWORD"),
#     url=os.getenv("DB_HOST"),
#     port=os.getenv("DB_PORT"),
#     db=os.getenv("DB_NAME"),
# )
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY")
