from flask_testing import TestCase
from flask import Flask
from db import get_db_test
from api.user import verify_password
from models import User

def delete_user_if_present(id):
    db = get_db_test()
    if db.query(User).filter(User.username == id).first() is not None:
        db.query(User).filter(User.username == id).delete()
        db.commit()


class MyTest(TestCase):

    TESTING = True

    def create_app(self):
        from api import tag,note,user

        app = Flask(__name__)
        app.register_blueprint(tag.tag)
        app.register_blueprint(note.note)
        app.register_blueprint(user.user)
        app.config['TESTING'] = True
        return app
    
    def test_login(self):
        a = verify_password('user1','qwerty')
        self.assertEqual(a,'user1')

    def test_login_bad_password(self):
        a = verify_password('user1','notqwerty')
        self.assertNotEqual(a,'user1')
    
    def test_login_bad_username(self):
        a = verify_password('user4','qwerty')
        self.assertNotEqual(a,'user4')

    def test_create_user(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "test@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,200)

    def test_create_user_bad_body(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": 1,
        "email": "test@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,400)

    def test_create_user_user_exists(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user1",
        "email": "test@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,400)

    def test_create_user_email_exists(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "admin@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,400)

    def test_get_user(self):
        response = self.client.get('user/user3')
        self.assertEqual(response.status_code,404)

    def test_update_user(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        auth = ('user1', 'qwerty')
        response = self.client.put('user/user3',json=tag_obj,auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,200)

    def test_update_user_bad_id(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        auth = ('user1', 'qwerty')
        response = self.client.put('user/user4',json=tag_obj,auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,404)
    
    def test_update_user_bad_user(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        auth = ('user2', 'qwerty')
        response = self.client.put('user/user3',json=tag_obj,auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,401)

    def test_update_user_bad_body(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        tag_obj = {
        "username": 1,
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        auth = ('user1', 'qwerty')
        response = self.client.put('user/user3',json=tag_obj,auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,400)

    def test_update_user_username_exists(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        tag_obj = {
        "username": "user2",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        auth = ('user1', 'qwerty')
        response = self.client.put('user/user3',json=tag_obj,auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,400)

    def test_update_user_email_exists(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        tag_obj = {
        "username": "user3",
        "email": "admin@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        auth = ('user1', 'qwerty')
        response = self.client.put('user/user3',json=tag_obj,auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,400)

    def test_delete_tag(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        auth = ('user1', 'qwerty')        
        response = self.client.delete("user/user3", auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,200)

    def test_delete_tag_bad_username(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        auth = ('user1', 'qwerty')        
        response = self.client.delete("user/user4", auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,404)
    
    def test_delete_tag_bad_user(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        auth = ('user2', 'qwerty')        
        response = self.client.delete("user/user3", auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,401)

    def test_get_stats(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        auth = ('user3', 'qwerty')        
        response = self.client.get("user/stat/user3", auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,200)

    def test_get_stats_bad_user(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        auth = ('user2', 'qwerty')        
        response = self.client.get("user/stat/user3", auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,401)

    def test_get_stats_bad_username(self):
        delete_user_if_present("user3") 
        tag_obj = {
        "username": "user3",
        "email": "haha@gmail.com",
        "password": "qwerty",
        "firstName": "Carl",
        "lastName": "Jackson"
        }
        response = self.client.post('user/',json=tag_obj)
        auth = ('user3', 'qwerty')        
        response = self.client.get("user/stat/user4", auth = auth)
        delete_user_if_present("user3") 
        self.assertEqual(response.status_code,404)