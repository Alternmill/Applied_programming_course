from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc
from sqlalchemy.sql import func
from db import *
from schemas import *
import bcrypt
from models import *
from api.errors import StatusResponse
from flask_httpauth import HTTPBasicAuth

note = Blueprint('note', __name__, url_prefix='/note')

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    db = get_db()
    user_r = db.query(User).filter(User.username == username).first()
    if user_r is None:
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt = bcrypt.gensalt())
    if (user_r is None) or (bcrypt.checkpw(user_r.password.encode('utf-8') , hashed_password)):
        return False 
    return username


@note.route('/', methods=['POST'])
@auth.login_required
def note_create():
    db = get_db()

    try:
        new_note = NoteCreatingSchema().load(request.json)
    except ValidationError:
        return StatusResponse(response= 'Error : Invalid input for NoteCreate', code = 400) 

    
    user = db.query(User).filter(User.idUser == new_note['ownerId']).first()
    if user is None:
        return 


    note = db.query(Note).filter(Note.idNote == new_note['id']).first()
    if note is not None:
        return StatusResponse(response= 'Error : Invalid input for NoteCreate, id already exists', code = 400) 

    note = Note(idNote = new_note['id'],ownerId = new_note['ownerId'],title = new_note['title'],
        isPublic = new_note['isPublic'], text = new_note['text'],dateOfEditing = func.now() 
    )

    tags = new_note['tags']

    for tag in tags:
        print(tag)
        ch = db.query(Tag).filter(Tag.idTag == tag).first()
        if ch is None:
            return jsonify('No such tags exist'),400
        tag_note = Tags(idNote = note.idNote,idTag=tag)
        db.add(tag_note)

    editnote = EditNote(idUser = new_note['ownerId'],idNote = new_note['id'])
    
    db.add(note)
    db.commit()

    db.add(editnote)
    db.commit()
    
    return StatusResponse(response= 'Successful creation of a note', code = 200) 

@note.route('/<int:id>', methods=['GET'])
@auth.login_required
def note_get(id):
    db = get_db()
    
    note = db.query(Note).filter(Note.idNote == id).first()

    if note is None:
        return StatusResponse(response= 'Error, no such note id', code = 200) 
    
    note_info = NoteGetSchemaWithAuthors().dump(note)

    authors = db.query(EditNote).filter(EditNote.idNote == id).all()
    au = []

    for aut in authors:
        au.append(UserGetSchema().dump(db.query(User).filter(User.idUser == aut.idUser).first()))
    
    note_info['authors']=au

    tgs = []
    tags = db.query(Tags).filter(Tags.idNote == id).all()

    for tag in tags:
        tgs.append(TagSchema().dump(db.query(Tag).filter(Tag.idTag == tag.idTag).first()))

    note_info['tags']=tgs

    return StatusResponse(response= note_info, code = 200) 


@note.route('/<int:id>', methods=['PUT'])
@auth.login_required
def note_update(id):
    db = get_db()
    
    note = db.query(Note).filter(Note.idNote == id).first()

    if note is None:
        return StatusResponse(response= 'Error, no such note id', code = 200) 
    try:
        new_note = NoteCreatingSchema().load(request.json)
    except ValidationError:
        return StatusResponse(response= 'Error, invalid input', code = 400) 

    for tag in new_note['tags']:
        print(tag)
        ch = db.query(Tag).filter(Tag.idTag == tag).first()
        if ch is None:
            return StatusResponse(response= 'Error, no such tag id', code = 404) 

    note.title = new_note['title']
    note.isPublic = new_note['isPublic']
    note.text = new_note['text']
    old_tags = db.query(Tags).filter(Tags.idNote == id).all()

    for i in old_tags:
        db.query(Tags).filter(Tags.idNote == id and Tags.idTag == i).delete()

    db.commit()
    
    for i in new_note['tags']:
        tag =Tags(idNote = id, idTag =i)
        t = db.query(Tags).filter(Tags.idNote == id and Tags.idTag == i)
        if t is not None:
            db.add(tag)
       
    db.commit()

    return StatusResponse(response= 'Update successful', code = 200) 


@note.route('/<int:id>', methods=['DELETE'])
@auth.login_required
def note_delete(id):
    db = get_db()
    
    note = db.query(Note).filter(Note.idNote == id).first()

    if note is None:
        return StatusResponse(response= 'Error, no such note id', code = 200) 

    
    db.query(Tags).filter(Tags.idNote == id).delete()
    db.query(EditNote).filter(EditNote.idNote == id).delete()


    db.query(Note).filter(Note.idNote == id).delete()

    db.commit()

    return StatusResponse(response= 'Delete successful', code = 200) 


@note.route('/allowed', methods=['POST'])
@auth.login_required
def note_allow_change():
    db = get_db()
    
    try:
        new_allow = AllowSchema().load(request.json)
    except ValidationError as err:
        return StatusResponse(response= err, code = 400) 


    allow = db.query(EditNote).filter(EditNote.idNote == new_allow['idNote'], EditNote.idUser == new_allow['idUser']).first()

    if allow is not None:
        return StatusResponse("User already has access",200)

    allow = EditNote(idNote = new_allow['idNote'],idUser = new_allow['idUser'])
    db.add(allow)
    db.commit()

    return StatusResponse("User now has access to modify",200)

@note.route('/allowed', methods=['DELETE'])
@auth.login_required
def note_disallow_change():
    db = get_db()
    
    try:
        old_allow = AllowSchema().load(request.json)
    except ValidationError as err:
         return StatusResponse(response= err, code = 400) 



    allow = db.query(EditNote).filter(EditNote.idNote == old_allow['idNote'], EditNote.idUser == old_allow['idUser']).first()

    if allow is None:
        return StatusResponse("User already has access",200)
    
    note = db.query(Note).filter(Note.idNote == old_allow['idNote']).first()
    if note.ownerId == old_allow['idUser']:
        return StatusResponse("User is an owner of a note",400)
      
    db.query(EditNote).filter(EditNote.idNote == old_allow['idNote'], EditNote.idUser == old_allow['idUser']).delete()
    db.commit()

    return StatusResponse("User now does not have access to modify",200)
