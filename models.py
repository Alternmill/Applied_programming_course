from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DateTime, Table,String

engine = create_engine('mysql+pymysql://root:1111@localhost:3306/notes')
engine.connect()

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = "user"

    idUser = Column(Integer, primary_key=True)
    username = Column(VARCHAR(25), nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(35), nullable=False)
    firstName = Column(VARCHAR(25), nullable=False)
    lastName = Column(VARCHAR(25), nullable=False)
    userStatus = Column(Integer(), nullable=False)

    notes = relationship("Note")


class Tag(BaseModel):
    __tablename__ = "tag"

    idTag = Column(Integer, primary_key=True)
    text = Column(VARCHAR(45), nullable=False)


class Note(BaseModel):
    __tablename__ = "note"

    idNote = Column(Integer, primary_key=True)
    ownerId = Column(Integer, ForeignKey(User.idUser))
    title = Column(VARCHAR(45), nullable=False)
    isPublic = Column(VARCHAR(5), nullable=False)
    text = Column(VARCHAR(404), nullable=False)
    dateOfEditing = Column(DateTime, nullable=False)


class Tags(BaseModel):
    __tablename__ = "tags"

    id = Column(Integer, primary_key = True)
    idNote = Column(Integer, ForeignKey(Note.idNote))
    idTag = Column(Integer, ForeignKey(Tag.idTag))


class EditNote(BaseModel):
    __tablename__ = "editnote"

    id = Column(Integer, primary_key = True)
    idUser = Column(Integer, ForeignKey(User.idUser))
    idNote = Column(Integer, ForeignKey(Note.idNote))


class Stats(BaseModel):
    __tablename__ = "stats"

    idStats = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey(User.idUser))
    numOfNotes = Column(Integer, nullable=False)
    numOfEditingNotes = Column(Integer, nullable=False)
    dateOfCreating = Column(DateTime, nullable=False)


class Admin(BaseModel):
    __tablename__ = "admins"
    
    username = Column(String(30), nullable=False,primary_key = True)
