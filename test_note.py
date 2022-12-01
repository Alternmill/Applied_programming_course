from flask_testing import TestCase
from flask import Flask
from db import get_db_test
from api.note import verify_password
from models import Note,Tags,EditNote
def delete_note_if_present(id):
    db = get_db_test()
    if db.query(Note).filter(Note.idNote == id).first() is not None:
        db.query(Tags).filter(Tags.idNote == id).delete()
        db.query(EditNote).filter(EditNote.idNote == id).delete()
        db.query(Note).filter(Note.idNote == id).delete()
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

    def test_get_note(self):
        auth = ('user1','qwerty')
        response = self.client.get("/note/1",auth = auth)
        self.assertEqual(response.status_code,200)

    def test_get_note_bad_user(self):
        auth = ('user2','qwerty')
        response = self.client.get("/note/1",auth = auth)
        self.assertEqual(response.status_code,401)

    def test_get_note_bad_id(self):
        auth = ('user1','qwerty')
        response = self.client.get("/note/33",auth = auth)
        self.assertEqual(response.status_code,404)

    def test_create_note(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [1]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)

    def test_create_note_bad_tags(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [3]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,400)

    def test_create_note_bad_body(self):
        delete_note_if_present(3)
        obj = {
        "id":"4",
        "ownerId":1,
        "title": 1,
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,400)

    def test_create_note_bad_id(self):
        delete_note_if_present(3)
        obj = {
        "id":1,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,400)

    def test_create_note_bad_owner(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":4,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,404)

    def test_update_note(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obj = {
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [1]
        }
        auth = ('user1','qwerty')
        response = self.client.put("/note/3",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)
    def test_update_note_bad_tags(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obj = {
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [1,4]
        }
        auth = ('user1','qwerty')
        response = self.client.put("/note/3",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,404)
    
    def test_update_note_bad_body(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obj = {
        "title": 1,
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.put("/note/3",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,400)

    def test_update_note_bad_id(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obj = {
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.put("/note/4",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,404)
    def test_update_note_bad_user(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obj = {
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": []
        }
        auth = ('user2','qwerty')
        response = self.client.put("/note/3",auth = auth, json = obj)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,401)

    def test_delete_note(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        
        auth = ('user1','qwerty')
        response = self.client.delete("/note/3",auth = auth)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)

    def test_delete_note_bad_id(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        
        auth = ('user1','qwerty')
        response = self.client.delete("/note/4",auth = auth)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,404)

    def test_delete_note_bad_user(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        
        auth = ('user2','qwerty')
        response = self.client.delete("/note/3",auth = auth)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,401)

    def test_grant_access(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)
    
    def test_grant_access_no_user(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":33,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,404)
    
    def test_grant_access_already_has(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)
    def test_grant_access_bad_body(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":"wqew24",
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,400)

    def test_grant_access_bad_user(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        auth = ('user2','qwerty')
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,401)

    def test_not_grant_access(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.delete("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)
    
    def test_not_grant_access_no_user(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        obja = {
            "idUser":33,
            "idNote":3
        }
        response = self.client.delete("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)
    
    def test_not_grant_access_user_is_owner(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        obja = {
            "idUser":1,
            "idNote":3
        }
        response = self.client.delete("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,400)
    

    def test_not_grant_access_already_has(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        response = self.client.delete("/note/allowed",auth = auth, json = obja)
        response = self.client.delete("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,200)
    def test_not_grant_access_bad_body(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":"wqew24",
            "idNote":3
        }
        response = self.client.delete("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,400)

    def test_not_grant_access_bad_user(self):
        delete_note_if_present(3)
        obj = {
        "id":3,
        "ownerId":1,
        "title": "Trip to lviv",
        "isPublic": True,
        "text": "Today i was in Lviv. It was great!",
        "tags": [2]
        }
        auth = ('user1','qwerty')
        response = self.client.post("/note/",auth = auth, json = obj)
        obja = {
            "idUser":2,
            "idNote":3
        }
        response = self.client.post("/note/allowed",auth = auth, json = obja)
        auth = ('user2','qwerty')
        response = self.client.delete("/note/allowed",auth = auth, json = obja)
        delete_note_if_present(3)
        self.assertEqual(response.status_code,401)