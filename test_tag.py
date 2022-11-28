import unittest
from unittest import TestCase

from api.errors import *
from models import Tag
from db import get_db
from api.tag import tag_get,tag_create,verify_password
from lab6 import app
import requests
from flask_httpauth import HTTPBasicAuth
def delete_tag_if_present(id):
    db = get_db()
    if db.query(Tag).filter(Tag.idTag == id).first() is not None:
        db.query(Tag).filter(Tag.idTag == id).delete()
        db.commit()
    
class TestUser(TestCase):

    def setUp(self) -> None:
        self.tag = Tag(
            idTag=100,
            text='text',
        )

    def test_login(self):
        with app.app_context():
            a = verify_password('user5','qwerty')
            self.assertEqual(a,'user5')

    def test_login_bad(self):
        with app.app_context():
            a = verify_password('user6','notqwerty')
            self.assertNotEqual(a,'user5')

    def test_get_tag_by_id(self):
        with app.app_context():
            db = get_db()
            delete_tag_if_present(100)
            db.add(Tag(
                idTag=100,
                text='text',
            ))
            db.commit()
            a = tag_get(100)
            db.query(Tag).filter(Tag.idTag == 100).delete()
            db.commit()
            #print(a)
            self.assertEqual(a.status_code,200)

    def test_create_tag(self):
        with app.app_context():
            db = get_db()
            delete_tag_if_present(102)
            
            url = "http://127.0.0.1:5000/tag"
            tag_obj = {"idTag":102,"text":"testTag"}
            x = requests.post(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            db.query(Tag).filter(Tag.idTag == 102).delete()
            db.commit()
            self.assertEqual(x.status_code,200)

    def test_create_tag_bad_data(self):
        with app.app_context():
            db = get_db()
            delete_tag_if_present(101)
            
            url = "http://127.0.0.1:5000/tag"
            tag_obj = {"idTag":101,"text":1}
            x = requests.post(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            db.query(Tag).filter(Tag.idTag == 101).delete()
            db.commit()
            self.assertEqual(x.status_code,400)

    def test_create_tag_bad_id(self):
        with app.app_context():
            db = get_db()
            
            url = "http://127.0.0.1:5000/tag"
            tag_obj = {"idTag":1,"text":1}
            x = requests.post(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            self.assertEqual(x.status_code,400) 
    
    def test_update_tag(self):
        with app.app_context():
            db = get_db()
            delete_tag_if_present(103)
            
            url = "http://127.0.0.1:5000/tag"
            tag_obj = {"idTag":103,"text":"testTag"}
            x = requests.post(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            url = "http://127.0.0.1:5000/tag/103"
            tag_obj = {"text":"testTag2"}
            x = requests.put(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            db.query(Tag).filter(Tag.idTag == 103).delete()
            db.commit()
            self.assertTrue(x.status_code==200)

    def test_update_tag_bad_id(self):
        with app.app_context():
            db = get_db()
            delete_tag_if_present(105)
            
            url = "http://127.0.0.1:5000/tag"
            tag_obj = {"idTag":105,"text":"testTag"}
            x = requests.post(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            url = "http://127.0.0.1:5000/tag/123213"
            tag_obj = {"text":"testTag2"}
            x = requests.put(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            self.assertTrue(x.status_code == 404)
        
    def test_delete_tag(self):
        with app.app_context():
            db = get_db()
            delete_tag_if_present(104)
            
            url = "http://127.0.0.1:5000/tag"
            tag_obj = {"idTag":104,"text":"testTag"}
            x = requests.post(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            url = "http://127.0.0.1:5000/tag/104"
            tag_obj = {"text":"testTag2"}
            x = requests.delete(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            
            self.assertTrue(db.query(Tag).filter(Tag.idTag == 104).first() == None)

    def test_delete_tag_bad_id(self):
        with app.app_context():
            db = get_db()
            delete_tag_if_present(106)
            
            url = "http://127.0.0.1:5000/tag"
            tag_obj = {"idTag":106,"text":"testTag"}
            x = requests.post(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            url = "http://127.0.0.1:5000/tag/10444"
            tag_obj = {"text":"testTag2"}
            x = requests.delete(url=url,json=tag_obj,auth = ('user5', 'qwerty'))
            #print('----\n',x.text,'\n----\n')

            db.query(Tag).filter(Tag.idTag == 104).delete()
            db.commit()
            self.assertTrue(x.status_code == 404)