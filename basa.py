import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request
from dotenv import load_dotenv
import os


load_dotenv()

connection = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    cursor_factory=RealDictCursor
)
connection.autocommit = True
