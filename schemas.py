from marshmallow import Schema, fields, post_load, base

class TagSchema(Schema):
    idTag = fields.Integer()
    text = fields.String()
    
class ResponseSchema(Schema):
    code = fields.Integer()
    response = fields.String()

class AllowSchema(Schema):
    idNote = fields.Integer()
    idUser = fields.Integer()

class TagUpdateSchema(Schema):
    text = fields.String(required=True)

class UserCreatingSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    firstName = fields.String(required=True) 
    lastName = fields.String(required=True)

class UserGetSchema(Schema):
    idUser = fields.Integer()
    username = fields.String(required=True)
    email = fields.String(required=True)
    firstName = fields.String(required=True) 
    lastName = fields.String(required=True)
    userStatus = fields.Integer()



class NoteGetSchema(Schema):
    idNote = fields.Integer()
    ownerId = fields.Integer()
    title = fields.String()
    isPublic = fields.Boolean()
    text = fields.String()
    tags = fields.List(fields.Nested(TagSchema))
    dateOfEditing = fields.Date()

class NoteCreatingSchema(Schema):
    id = fields.Integer()
    ownerId = fields.Integer()
    title = fields.String()
    isPublic = fields.Boolean()
    text = fields.String()
    tags = fields.List(fields.Integer())

class UserGetSchemaWithNotes(Schema):
    idUser = fields.Integer()
    username = fields.String(required=True)
    email = fields.String(required=True)
    firstName = fields.String(required=True) 
    lastName = fields.String(required=True)
    userStatus = fields.Integer()
    authors = fields.List(fields.Nested(NoteGetSchema))

class NoteGetSchemaWithAuthors(Schema):
    idNote = fields.Integer()
    ownerId = fields.Integer()
    title = fields.String()
    isPublic = fields.Boolean()
    text = fields.String()
    tags = fields.List(fields.Nested(TagSchema))
    authors = fields.List(fields.Nested(UserGetSchema))
    dateOfEditing = fields.Date()