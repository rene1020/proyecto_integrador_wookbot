from dotenv import dotenv_values

class Config:
    config = dotenv_values_values(".env")
    
    SECRET_KEY = config['fbb5a3e6c91fe08109c50d818166dfe9db9e5f0ef9fa315c8f729964a9c1edbf']
    SERVER_NAME = "127.0.0.1:5000"
    DEBUG = True

    DATABASE_USERNAME = config['DATABASE_USERNAME']
    DATABASE_PASSWORD = config['DATABASE_PASSWORD']
    DATABASE_HOST = config['DATABASE_HOST']
    DATABASE_PORT = config['DATABASE_PORT']

    TEMPLATE_FOLDER = "templates/"
    STATIC_FOLDER = "static_folder/"