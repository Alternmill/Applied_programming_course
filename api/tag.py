from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc
import bcrypt
from db import *
from schemas import *
from models import *
from api.errors import StatusResponse
from flask_httpauth import HTTPBasicAuth
tag = Blueprint('tag', __name__, url_prefix='/tag')

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    db = get_db()
    user_r = db.query(User).filter(User.username == username).first()
    if user_r is None:
        return False
   
    if bcrypt.checkpw(password.encode('utf-8'),user_r.password.encode('utf-8')) == False:
        return False 
    return username


@tag.route('/', methods=['POST'])
@auth.login_required
def tag_create():
    db = get_db()
    try:
        new_tag = TagSchema().load(request.json)
    except ValidationError:
        return StatusResponse(response= 'Error : Invalid input for TagCreate', code = 400) 

    check = db.query(Tag).filter(Tag.idTag == new_tag['idTag']).first()

    if check is not None:
        return StatusResponse(response= 'Error : tag with this id already exists', code = 400) 


    tag = Tag(idTag = new_tag['idTag'],text = new_tag['text'])

    db.add(tag)

    db.commit()

    return StatusResponse(response= 'Successful creation of a tag', code = 200) 

@tag.route('/<int:id>', methods=['GET'])
def tag_get(id):
    db = get_db()
    tag = db.query(Tag).filter(Tag.idTag == id).first()

    if tag is None:
        return StatusResponse('Error, no such tag', code = 404) 

    tag_info = TagSchema().dump(tag)

    return StatusResponse(response= tag_info, code = 200) 
   

@tag.route('/<int:id>', methods=['PUT'])
@auth.login_required
def tag_update(id):
    db = get_db()

    tag = db.query(Tag).filter(Tag.idTag == id).first()

    if tag is None:
        return StatusResponse('Error, no such tag', code = 404) 
    check_admin = db.query(Admin).filter(Admin.username == auth.username()).first()
    if check_admin is None:
        return StatusResponse(response= 'Must be an admin', code = 401) 
    try:
        new_tag = TagUpdateSchema().load(request.json)
    except ValidationError:
       return StatusResponse(response= 'Error : Invalid input for TagUpdate', code = 400) 

    tag.text = new_tag['text']

    db.commit()

    return StatusResponse(response= new_tag, code = 200) 


@tag.route('/<int:id>', methods=['DELETE'])
@auth.login_required
def tag_delete(id):
    db = get_db()

    tag = db.query(Tag).filter(Tag.idTag == id).first()
    check_admin = db.query(Admin).filter(Admin.username == auth.username()).first()
    if check_admin is None:
        return StatusResponse(response= 'Must be an admin', code = 401) 
    if tag is None:
        return StatusResponse('Error, no such tag', code = 404)
    ctags = db.query(Tags).filter(Tags.idTag == id).all()

    for ctag in ctags:
        db.query(Tags).filter(Tags.idTag == ctag.idTag).delete() # pragma: no cover

    db.query(Tag).filter(Tag.idTag == id).delete()

    db.commit()
    return StatusResponse(response= 'Delete successful', code = 200) 
