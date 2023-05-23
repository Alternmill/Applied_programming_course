from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc
import bcrypt
from db import *
from schemas import *
from models import *
from api.errors import StatusResponse
from api.note import note_delete
from flask_httpauth import HTTPBasicAuth

user = Blueprint('user', __name__, url_prefix='/user')
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    print("ouifhndgsuopgfhsdi")
    if username == '':
        print("ognfdgpids")

    print(username,password)
    db = get_db()
    user_r = db.query(User).filter(User.username == username).first()
    if user_r is None:
        return False
   
    if bcrypt.checkpw(password.encode('utf-8'),user_r.password.encode('utf-8')) == False:
        return False 
    print("Success")
    return username


@user.route('/check', methods=['GET'])
@auth.login_required
def check_user():
    return StatusResponse(code=200, response='Login successful')

@user.route('/', methods=['POST'])
def add_user():
    db = get_db()

    try:
        user = UserCreatingSchema().load(request.get_json())
    except ValidationError as err:
        return StatusResponse(err.messages, 400)

    username_r = db.query(User).filter(User.username == user['username']).first()

    if username_r:
        return StatusResponse(code=400, response='The username is used by other user')

    existsEmail = db.query(User).filter(User.email==user['email']).first()

    if existsEmail:
        return StatusResponse(code=400, response='The email is used by other user')

    print(user['password'])
    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'),salt = bcrypt.gensalt()).decode('utf-8')

    new_user = User(firstName=user['firstName'], lastName=user['lastName'], username=user['username'],
                     email=user['email'], password=hashed_password,userStatus = 1)

    db.add(new_user)

    db.commit()

    return get_user(user['username'])

@user.route('/<username>', methods=['GET'])
def get_user(username):
    db = get_db()

   
    username_r = db.query(User).filter(User.username == username).first()

    if username_r is None:
         return StatusResponse(code=404,response="No user with such username!")
    
    user = UserGetSchemaWithNotes().dump(username_r)

    user_notes = []

    notes = db.query(Note).filter(Note.ownerId == username_r.idUser).all()

    for note in notes: #pragma no cover
        add_note = NoteGetSchema().dump(note)

        tgs = []
        tags = db.query(Tags).filter(Tags.idNote == note.idNote).all()

        for tag in tags:
            tgs.append(TagSchema().dump(db.query(Tag).filter(Tag.idTag == tag.idTag).first()))

        add_note['tags']=tgs
        user_notes.append(add_note)

    user['notes']=user_notes
    print(user)
    return StatusResponse(code=200, response=user)

@user.route('/<username>', methods=['PUT'])
@auth.login_required
def update_user(username):
    db = get_db()

    username_r = db.query(User).filter(User.username == username).first()

    if username_r is None:
        return StatusResponse(code=404,response="No user with such username!")
    
    
    if username_r.username!=auth.username(): 
        check_admin = db.query(Admin).filter(Admin.username == auth.username()).first()
        if check_admin is None:
            return StatusResponse(response= 'Must be an admin', code = 401) 
    try:
        user = UserCreatingSchema().load(request.get_json())
    except ValidationError as err:
        return StatusResponse(err.messages, 400)

    username_r = db.query(User).filter(User.username == user['username']).first()

    
    if  username_r is not None and username_r.username != username:
        return StatusResponse(code=400, response='The username is used by other user')

    email_r = db.query(User).filter(User.email==user['email']).first()

    if email_r is not None and email_r.username != username:
        return StatusResponse(code=400, response='The email is used by other user')

    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'),salt = bcrypt.gensalt()).decode('utf-8')


    username_r = db.query(User).filter(User.username == username).first()
    username_r.firstName=user['firstName']
    username_r.lastName=user['lastName']
    username_r.username=user['username']
    username_r.email=user['email']
    username_r.password=hashed_password
    username_r.userStatus = 1
    
    db.commit()

    return StatusResponse(code=200, response='User succesfully updated')

@user.route('/<username>', methods=['DELETE'])
@auth.login_required
def delete_user(username):
    db = get_db()

    username_r = db.query(User).filter(User.username == username).first()

    if username_r is None:
        return StatusResponse(code=404,response="No user with such username!")
    
    if username_r.username!=auth.username(): 
        check_admin = db.query(Admin).filter(Admin.username == auth.username()).first()
        if check_admin is None:
            return StatusResponse(response= 'Must be an admin', code = 401) 
    for note in db.query(EditNote).filter(EditNote.idUser == username_r.idUser).all(): #pragma no cover
        note_delete(note.idNote)

    db.query(User).filter(User.username == username).delete()

    db.commit()

    return StatusResponse(code=200, response='User succesfully deleted')

@user.route('/stat/<username>', methods=['GET'])
@auth.login_required
def get_user_stat(username):
    db = get_db()

    username_r = db.query(User).filter(User.username == username).first()

    if username_r is None:
        return StatusResponse(code=404,response="No user with such username!")
    if username_r.username!=auth.username(): 
        check_admin = db.query(Admin).filter(Admin.username == auth.username()).first()
        if check_admin is None:
            return StatusResponse(response= 'Must be an admin', code = 401) 
    notes_edited = db.query(EditNote).filter(EditNote.idUser == username_r.idUser).all()
    notes_created = db.query(Note).filter(Note.ownerId == username_r.idUser).all()

    a = jsonify(idUser = username_r.idUser,numOfNotes = len(notes_created),numOfNotesEditing = len(notes_edited))
    
    return a,200
