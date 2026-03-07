class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost/project"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret123"