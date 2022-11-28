import unittest
from unittest import TestCase

from api.errors import *
from models import User
from db import get_db
from api.user import verify_password,get_user
from lab6 import app
import requests
from flask_httpauth import HTTPBasicAuth

def delete_user_if_present(id):
    db = get_db()
    if db.query(User).filter(User.username == id).first() is not None:
        db.query(User).filter(User.username == id).delete()
        db.commit()

class TestUser(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            firstName='first_name',
            lastName='last_name',
            email='email',
            password='password'
        )

    def test_login(self):
        with app.app_context():
            a = verify_password('user5','qwerty')
            self.assertEqual(a,'user5')

    def test_login_bad(self):
        with app.app_context():
            a = verify_password('user6','notqwerty')
            self.assertNotEqual(a,'user5')
    def test_add_user(self):
        user = self.user
    def test_get_user(self):
        with app.app_context():
            db = get_db()
            a = get_user('user5')
            #print(a)
            self.assertEqual(a.status_code,200)
    def test_get_user_bad_id(self):
        with app.app_context():
            db = get_db()
            a = get_user('5')
            #print(a)
            self.assertEqual(a.status_code,404)
    def test_create(self):
        with app.app_context():
            db = get_db()
            delete_user_if_present("user777")
            url = "http://127.0.0.1:5000/user"
            tag_obj = {
                "username": "user777",
                "email": "ailuweq@gmail.com",
                "password": "qwerty",
                "firstName": "Carl",
                "lastName": "Jackson"
                }

            x = requests.post(url=url,json=tag_obj)
            #print('----\n',x.text,'\n----\n')
            db.query(User).filter(User.username=='user777').delete()
            db.commit()
            self.assertEqual(x.status_code,200)

    def test_create_used_email(self):
        with app.app_context():
            db = get_db()
            delete_user_if_present("user777")
            url = "http://127.0.0.1:5000/user"
            tag_obj = {
                "username": "user777",
                "email": "ailu@gmail.com",
                "password": "qwerty",
                "firstName": "Carl",
                "lastName": "Jackson"
                }

            x = requests.post(url=url,json=tag_obj)
            #print('----\n',x.text,'\n----\n')
            db.query(User).filter(User.username=='user777').delete()
            db.commit()
            self.assertEqual(x.status_code,400)
    def test_create_used_email(self):
        with app.app_context():
            db = get_db()
            delete_user_if_present("user777")
            url = "http://127.0.0.1:5000/user"
            tag_obj = {
                "username": "user6",
                "email": "ailuqwewq@gmail.com",
                "password": "qwerty",
                "firstName": "Carl",
                "lastName": "Jackson"
                }

            x = requests.post(url=url,json=tag_obj)
            #print('----\n',x.text,'\n----\n')
            db.query(User).filter(User.username=='user777').delete()
            db.commit()
            self.assertEqual(x.status_code,400)
    
    def test_update_user(self):
        with app.app_context():
            db = get_db()
            delete_user_if_present("user778")
            url = "http://127.0.0.1:5000/user"
            tag_obj = {
                "username": "user778",
                "email": "ailuqwewq@gmail.com",
                "password": "qwerty",
                "firstName": "Carl",
                "lastName": "Jackson"
                }

            x = requests.post(url=url,json=tag_obj)
            url = "http://127.0.0.1:5000/user/user778"
            tag_obj = {
                "username": "user778",
                "email": "ailuqwewq@gmail.com",
                "password": "qwerty",
                "firstName": "Mike",
                "lastName": "Jackson"
                }
            x = requests.put(url=url,json=tag_obj, auth =  ('user778', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            db.query(User).filter(User.username=='user778').delete()
            db.commit()
            self.assertEqual(x.status_code,200)

    def test_update_user_bad_email(self):
        with app.app_context():
            db = get_db()
            delete_user_if_present("user779")
            url = "http://127.0.0.1:5000/user"
            tag_obj = {
                "username": "user779",
                "email": "ailuqwewq@gmail.com",
                "password": "qwerty",
                "firstName": "Carl",
                "lastName": "Jackson"
                }

            x = requests.post(url=url,json=tag_obj)
            url = "http://127.0.0.1:5000/user/user779"
            tag_obj = {
                "username": "user779",
                "email": "ailu@gmail.com",
                "password": "qwerty",
                "firstName": "Mike",
                "lastName": "Jackson"
                }
            x = requests.put(url=url,json=tag_obj, auth =  ('user779', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            db.query(User).filter(User.username=='user779').delete()
            db.commit()
            self.assertEqual(x.status_code,400)

    def test_update_user_bad_id(self):
        with app.app_context():
            db = get_db()
            delete_user_if_present("user780")
            url = "http://127.0.0.1:5000/user"
            tag_obj = {
                "username": "user780",
                "email": "ailuqwewq@gmail.com",
                "password": "qwerty",
                "firstName": "Carl",
                "lastName": "Jackson"
                }

            x = requests.post(url=url,json=tag_obj)
            url = "http://127.0.0.1:5000/user/user780"
            tag_obj = {
                "username": "user5",
                "email": "ailu@gmail.com",
                "password": "qwerty",
                "firstName": "Mike",
                "lastName": "Jackson"
                }
            x = requests.put(url=url,json=tag_obj, auth =  ('user780', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            db.query(User).filter(User.username=='user780').delete()
            db.commit()
            self.assertEqual(x.status_code,401)

    def test_delete(self):
        with app.app_context():
            db = get_db()
            delete_user_if_present("user781")
            url = "http://127.0.0.1:5000/user"
            tag_obj = {
                "username": "user781",
                "email": "ailuqqwewq@gmail.com",
                "password": "qwerty",
                "firstName": "Carl",
                "lastName": "Jackson"
                }

            x = requests.post(url=url,json=tag_obj)
            url = "http://127.0.0.1:5000/user/user781"
            x = requests.delete(url=url, auth =  ('user781', 'qwerty'))
            #print('----\n',x.text,'\n----\n')
            db.query(User).filter(User.username=='user781').delete()
            db.commit()
            self.assertEqual(x.status_code,200)


if __name__ == '__main__':
    unittest.main()