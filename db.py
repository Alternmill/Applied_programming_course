from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


connection_string = 'mysql://root:1111@127.0.0.1:3306/notes'
engine = create_engine(connection_string, echo=False)
Session = sessionmaker(bind=engine, autoflush=False)
db = Session()

def get_db():
    return db
