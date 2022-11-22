from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc

from db import *
from schemas import *
from models import *

tag = Blueprint('tag', __name__, url_prefix='/tag')

@tag.route('/', methods=['POST'])
def tag_create():
    db = get_db()
    
    try:
        new_tag = TagSchema().load(request.json)
    except ValidationError:
        return jsonify({'Error': 'Invalid input for TagCreate'}), 400

    tag = Tag(idTag = new_tag['idTag'],text = new_tag['text'])

    db.add(tag)

    db.commit()

    return jsonify('successful creation of a tag')

@tag.route('/<int:id>', methods=['GET'])
def tag_get(id):
    db = get_db()
    
    tag = db.query(Tag).filter(Tag.idTag == id).first()

    if tag is None:
        return jsonify('Error, no such tag'),404

    tag_info = TagSchema().dump(tag)

    return jsonify(tag_info)
   

@tag.route('/<int:id>', methods=['PUT'])
def tag_update(id):
    db = get_db()

    tag = db.query(Tag).filter(Tag.idTag == id).first()

    if tag is None:
        return jsonify('Error, no such tag'),404

    try:
        new_tag = TagUpdateSchema().load(request.json)
    except ValidationError:
        return jsonify({'Error': 'Invalid input for TagUpdate'}), 400

    tag.text = new_tag['text']

    db.commit()

    return jsonify('Update successful'),200


@tag.route('/<int:id>', methods=['DELETE'])
def tag_delete(id):
    db = get_db()

    tag = db.query(Tag).filter(Tag.idTag == id).first()

    if tag is None:
        return jsonify('Error, no such tag'),404
   
    ctags = db.query(Tags).filter(Tags.idTag == id).all()

    for ctag in ctags:
        db.query(Tags).filter(Tags.idTag == ctag.idTag).delete()

    db.query(Tag).filter(Tag.idTag == id).delete()

    db.commit()
    return jsonify('Delete successful'),200
