from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc

from db import *
from schemas import *
from models import *
from api.errors import StatusResponse

tag = Blueprint('tag', __name__, url_prefix='/tag')

@tag.route('/', methods=['POST'])
def tag_create():
    db = get_db()

    try:
        new_tag = TagSchema().load(request.json)
    except ValidationError:
        return StatusResponse(response= 'Error : Invalid input for TagCreate', code = 400) 

    check = db.query(Tag).filter(Tag.idTag == new_tag['idTag']).all()

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
def tag_update(id):
    db = get_db()

    tag = db.query(Tag).filter(Tag.idTag == id).first()

    if tag is None:
        return StatusResponse('Error, no such tag', code = 404) 

    try:
        new_tag = TagUpdateSchema().load(request.json)
    except ValidationError:
       return StatusResponse(response= 'Error : Invalid input for TagUpdate', code = 400) 

    tag.text = new_tag['text']

    db.commit()

    return StatusResponse(response= new_tag, code = 200) 


@tag.route('/<int:id>', methods=['DELETE'])
def tag_delete(id):
    db = get_db()

    tag = db.query(Tag).filter(Tag.idTag == id).first()

    if tag is None:
        return StatusResponse('Error, no such tag', code = 404)
    ctags = db.query(Tags).filter(Tags.idTag == id).all()

    for ctag in ctags:
        db.query(Tags).filter(Tags.idTag == ctag.idTag).delete()

    db.query(Tag).filter(Tag.idTag == id).delete()

    db.commit()
    return StatusResponse(response= 'Delete successful', code = 200) 
