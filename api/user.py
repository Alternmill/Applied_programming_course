from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc
import bcrypt
from db import *
from schemas import *
from models import *
from api.errors import StatusResponse
from api.note import note_delete
user = Blueprint('user', __name__, url_prefix='/user')

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

    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'),salt = bcrypt.gensalt()).decode('utf-8')

    print(hashed_password)

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

    for note in notes:
        add_note = NoteGetSchema().dump(note)

        tgs = []
        tags = db.query(Tags).filter(Tags.idNote == note.idNote).all()

        for tag in tags:
            tgs.append(TagSchema().dump(db.query(Tag).filter(Tag.idTag == tag.idTag).first()))

        add_note['tags']=tgs
        user_notes.append(add_note)

    user['notes']=user_notes

    return jsonify(user)

@user.route('/<username>', methods=['PUT'])
def update_user(username):
    db = get_db()

    try:
        user = UserCreatingSchema().load(request.get_json())
    except ValidationError as err:
        return StatusResponse(err.messages, 400)

    username_r = db.query(User).filter(User.username == user['username']).first()

    if username_r is not None and username_r.username != username:
        return StatusResponse(code=400, response='The username is used by other user')

    email_r = db.query(User).filter(User.email==user['email']).first()

    if email_r is not None and email_r.username != username:
        return StatusResponse(code=400, response='The email is used by other user')

    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'),salt = bcrypt.gensalt()).decode('utf-8')

    username_r.firstName=user['firstName']
    username_r.lastName=user['lastName']
    username_r.username=user['username']
    username_r.email=user['email']
    username_r.password=hashed_password
    username_r.userStatus = 1
    
    db.commit()

    return StatusResponse(code=200, response='User succesfully updated')

@user.route('/<username>', methods=['DELETE'])
def delete_user(username):
    db = get_db()

    username_r = db.query(User).filter(User.username == username).first()

    if username_r is None:
        return StatusResponse(code=404,response="No user with such username!")
    
    for note in db.query(EditNote).filter(EditNote.idUser == username_r.idUser).all():
        note_delete(note.idNote)

    db.query(User).filter(User.username == username).delete()

    db.commit()

    return StatusResponse(code=200, response='User succesfully deleted')

@user.route('/stat/<username>', methods=['GET'])
def get_user_stat(username):
    db = get_db()

    username_r = db.query(User).filter(User.username == username).first()

    if username_r is None:
        return StatusResponse(code=404,response="No user with such username!")
    
    notes_edited = db.query(EditNote).filter(EditNote.idUser == username_r.idUser).all()
    notes_created = db.query(Note).filter(Note.ownerId == username_r.idUser).all()

    a = jsonify(idUser = username_r.idUser,numOfNotes = len(notes_created),numOfNotesEditing = len(notes_edited))
    
    return a,200
