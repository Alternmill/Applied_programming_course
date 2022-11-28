from lab6 import  User, Note, Tag, Stats, EditNote, Tags
from datetime import datetime
from db import *
user1 = User(username='user2', firstName='name2user', lastName='surname2user', email='user2@email.com',
             password='passwordUser2', userStatus=1)
user2 = User(username='user3', firstName='name3user', lastName='surname3user', email='user3@email.com',
             password='passwordUser3', userStatus=1)
tag1 = Tag(text='life')
tag2 = Tag(text='Lviv')
list_of_tags = Tags(idNote=1, idTag=1)
note1 = Note(ownerId=1, title='My perfect life', isPublic='true', text='Hello!It`s me and my perfect life', dateOfEditing=datetime.now())
stats1 = Stats(userId=1, numOfNotes=1, numOfEditingNotes=0, dateOfCreating=datetime.now())
editnote1 = EditNote(idUser=2, idNote=1)

session = get_db()

session.add(user1)
session.add(user2)
session.commit()

session.add(tag1)
session.add(tag2)
session.commit()

session.add(note1)
session.add(stats1)
session.commit()

session.add(editnote1)
session.add(list_of_tags)
session.commit()
