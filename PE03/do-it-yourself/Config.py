class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://DIYUser:user@localhost/DIYinstructions'
    SQLALCHEMY_TRACK_MODIFICATIONS = False