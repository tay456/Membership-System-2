from flask_restplus import Namespace, fields


class MemberDto:
    api = Namespace('member', description='user related operations')
    member = api.model('member', {
        'name': fields.String(required=True, description='member name'),
        'card_no': fields.String(description='user Identifier'),
        'email': fields.String(required=True, description='member email address'),
        'password_hash': fields.String(required=True, description='member password'),
    })


class MemberDetailsDto:
    api = Namespace('member', description='user related operations')
    member = api.model('member', {
        'name': fields.String(required=True, description='member name'),
        'card_no': fields.String(description='user Identifier'),
        'email': fields.String(required=True, description='member email address'),
        'balance': fields.Integer(required=False)
    })


