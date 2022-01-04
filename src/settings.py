from os import environ

SECRET_KEY = environ.get('SECRET_KEY')

DB_USER = environ.get('MARIADB_USER')
DB_PASSWORD = environ.get('MARIADB_PASSWORD')
DB_PORT = environ.get('MARIADB_PORT')
DB_NAME = environ.get('MARIADB_DATABASE')
