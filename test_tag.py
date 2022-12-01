from flask_testing import TestCase
from flask import Flask
from db import get_db_test
from api.tag import verify_password
from models import Tag
def delete_tag_if_present(id):
    db = get_db_test()
    if db.query(Tag).filter(Tag.idTag == id).first() is not None:
        db.query(Tag).filter(Tag.idTag == id).delete()
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
        a = verify_password('user3','qwerty')
        self.assertNotEqual(a,'user3')

    def test_get_tag_by_id(self):
        response = self.client.get("/tag/1")
        self.assertEqual(response.status_code,200)
   
    def test_get_tag_by_id_no_id(self):
        response = self.client.get("/tag/3")
        self.assertEqual(response.status_code,404)

    def test_create_tag(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        auth = ('user1', 'qwerty')
        response = self.client.post("/tag/",json = tag_obj, auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,200)

    def test_create_tag_bad_body(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":12}
        auth = ('user1', 'qwerty')
        response = self.client.post("/tag/",json = tag_obj, auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,400)

    def test_create_tag_bad_id(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":1,"text":"test"}
        auth = ('user1', 'qwerty')
        response = self.client.post("/tag/",json = tag_obj, auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,400)
    
    def test_update_tag(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        tag_obj1 = {"text":"testTag"}
        auth = ('user1', 'qwerty')
        self.client.post("/tag/",json = tag_obj, auth = auth)
        response = self.client.put("/tag/3",json = tag_obj1, auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,200)

    def test_update_tag_bad_id(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        tag_obj1 = {"text":"testTag"}
        auth = ('user1', 'qwerty')
        self.client.post("/tag/",json = tag_obj, auth = auth)
        response = self.client.put("/tag/4",json = tag_obj1, auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,404)

    def test_update_tag_not_admin(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        tag_obj1 = {"text":"testTag"}
        auth = ('user1', 'qwerty')
        auth2 = ('user2', 'qwerty')
        self.client.post("/tag/",json = tag_obj, auth = auth)
        response = self.client.put("/tag/3",json = tag_obj1, auth = auth2)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,401)

    def test_update_tag_bad_body(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        tag_obj1 = {"text":1}
        auth = ('user1', 'qwerty')
        self.client.post("/tag/",json = tag_obj, auth = auth)
        response = self.client.put("/tag/3",json = tag_obj1, auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,400)
    
    def test_delete_tag(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        auth = ('user1', 'qwerty')
        self.client.post("/tag/",json = tag_obj, auth = auth)
        response = self.client.delete("/tag/3", auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,200)

    def test_delete_tag_bad_id(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        auth = ('user1', 'qwerty')
        self.client.post("/tag/",json = tag_obj, auth = auth)
        response = self.client.delete("/tag/4", auth = auth)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,404)

    def test_delete_tag_not_admin(self):
        delete_tag_if_present(3)
        tag_obj = {"idTag":3,"text":"testTag"}
        auth = ('user1', 'qwerty')
        auth2 = ('user2', 'qwerty')
        self.client.post("/tag/",json = tag_obj, auth = auth)
        response = self.client.delete("/tag/3", auth = auth2)
        delete_tag_if_present(3)
        self.assertEqual(response.status_code,401)