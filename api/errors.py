from flask import Blueprint, jsonify, request, make_response
import sqlalchemy
import marshmallow 
from schemas import ResponseSchema
errors = Blueprint('errors', __name__)

def StatusResponse(response, code):
    end_response = make_response(jsonify(response = response,code = code),code)
    return end_response
