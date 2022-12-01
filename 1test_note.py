import unittest
from unittest import TestCase

from api.errors import *
from models import Note
from db import get_db
from api.note import note_get,verify_password
from lab6 import app
import requests
from sqlalchemy.sql import func
from flask_httpauth import HTTPBasicAuth
def delete_note_if_present(id):
    db = get_db()
    if db.query(Note).filter(Note.idNote == id).first() is not None:
        db.query(Note).filter(Note.idNote == id).delete()
        db.commit()

class TestUser(TestCase):

    def test_login(self):
        with app.app_context():
            a = verify_password('user5','qwerty')
            self.assertEqual(a,'user5')

    def test_login_bad(self):
        with app.app_context():
            a = verify_password('user6','notqwerty')
            self.assertNotEqual(a,'user5')


    def test_get_note_by_id(self):
        with app.app_context():
            db = get_db()
            delete_note_if_present(12)
            db.add(Note(idNote = 12,
                text='text',
                ownerId=6,
                isPublic = True,
                title = 'qwerty',
                dateOfEditing = func.now() 
                ))
            
            db.commit()
            url = "http://127.0.0.1:5000/note/12"
           
            x = requests.get(url=url,auth = ('user6','qwerty'))
            db.query(Note).filter(Note.idNote == 12).delete()
            db.commit()
            #print(x.text)
            self.assertEqual(x.status_code,200)
    def test_get_note_by_bad_id(self):
        with app.app_context():
            db = get_db()
            delete_note_if_present(101)
            db.add(Note(idNote = 101,
                text='text',
                ownerId=5,
                isPublic = True,
                title = 'qwerty',
                dateOfEditing = func.now() 
                ))
            
            db.commit()
            url = "http://127.0.0.1:5000/note/102132"
           

            x = requests.get(url=url,auth = ('user5','qwerty'))
            db.query(Note).filter(Note.idNote == 101).delete()
            db.commit()
            #print(x.text)
            self.assertNotEqual(x.status_code,404)

    def test_get_note_by_admin(self):
        with app.app_context():
            db = get_db()
     
            url = "http://127.0.0.1:5000/note/1"

            x = requests.get(url=url,auth = ('user5','qwerty'))
            
            #print(x.text)
            self.assertEqual(x.status_code,200)

    def test_update_note(self):
        with app.app_context():
            db = get_db()
            delete_note_if_present(111)
            db.add(Note(idNote = 111,
                text='text',
                ownerId=6,
                isPublic = True,
                title = 'qwerty',
                dateOfEditing = func.now() 
                ))
            
            db.commit()
            url = "http://127.0.0.1:5000/note/111"
            obj = {
                   "title": "Trip to lviv",
                    "isPublic": True,
                    "text": "Today i was in Lviv. It was great!",
                    "tags": []
                  }

            x = requests.put(url=url,json = obj, auth = ('user6','qwerty'))
            db.query(Note).filter(Note.idNote == 111).delete()
            db.commit()
            #print(x.text)
            self.assertEqual(x.status_code,200)
    def test_update_note_admin(self):
        with app.app_context():
            db = get_db()
        
            url = "http://127.0.0.1:5000/note/2"
            obj = {
                   "title": "Trip to lviv",
                    "isPublic": True,
                    "text": "Today i was in Lviv. It was great!",
                    "tags": []
                  }

            x = requests.put(url=url,json = obj, auth = ('user5','qwerty'))
           
            #print(x.text)
            self.assertEqual(x.status_code,200)
    def test_update_note_bad_tags(self):
        with app.app_context():
            db = get_db()
            delete_note_if_present(104)
            db.add(Note(idNote = 104,
                text='text',
                ownerId=6,
                isPublic = True,
                title = 'qwerty',
                dateOfEditing = func.now() 
                ))
            
            db.commit()
            url = "http://127.0.0.1:5000/note/102"
            obj = {
                   "title": "Trip to lviv",
                    "isPublic": True,
                    "text": "Today i was in Lviv. It was great!",
                    "tags": [3]
                  }

            x = requests.put(url=url,json = obj, auth = ('user5','qwerty'))
            db.query(Note).filter(Note.idNote == 102).delete()
            db.commit()
            #print(x.text)
            self.assertEqual(x.status_code,200)

    def test_delete_note(self):
        with app.app_context():
            db = get_db()
            delete_note_if_present(107)
            db.add(Note(idNote = 107,
                text='text',
                ownerId=6,
                isPublic = True,
                title = 'qwerty',
                dateOfEditing = func.now() 
                ))
            
            db.commit()
            url = "http://127.0.0.1:5000/note/107"

            x = requests.delete(url=url, auth = ('user6','qwerty'))
            db.query(Note).filter(Note.idNote == 107).delete()
            db.commit()
            #print(x.text)
            self.assertEqual(x.status_code,200)
    def test_delete_note_admin(self):
        with app.app_context():
            db = get_db()
            delete_note_if_present(108)
            db.add(Note(idNote = 108,
                text='text',
                ownerId=6,
                isPublic = True,
                title = 'qwerty',
                dateOfEditing = func.now() 
                ))
            
            db.commit()
            url = "http://127.0.0.1:5000/note/108"

            x = requests.delete(url=url, auth = ('user5','qwerty'))
            db.query(Note).filter(Note.idNote == 108).delete()
            db.commit()
            #print(x.text)
            self.assertEqual(x.status_code,200)
    def test_delete_note_bad_id(self):
        with app.app_context():
            db = get_db()
            delete_note_if_present(109)
            db.add(Note(idNote = 109,
                text='text',
                ownerId=6,
                isPublic = True,
                title = 'qwerty',
                dateOfEditing = func.now() 
                ))
            
            db.commit()
            url = "http://127.0.0.1:5000/note/101237"

            x = requests.delete(url=url, auth = ('user5','qwerty'))
            db.query(Note).filter(Note.idNote == 109).delete()
            db.commit()
            #print(x.text)
            self.assertEqual(x.status_code,200)