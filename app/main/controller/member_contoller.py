from flask import request
from flask_restplus import Resource

from app.main.utilities.dto import MemberDto
from ..service.member_service import *

api = MemberDto.api
_member = MemberDto.member


@api.route('/')
class MemberList(Resource):
    @api.response(201, 'Member successfully created.')
    @api.doc('create a new member')
    @api.expect(_member, validate=True)
    def post(self):
        """Creates a new Member """
        data = request.json
        return add_new_member(data=data)


@api.route('/<card_no>')
@api.param('card_no', 'The Member identifier')
@api.response(404, 'Member not found.')
class Member(Resource):
    @api.doc('get a member')
    @api.marshal_with(_member)
    def get(self, card_no):
        """get a member given its identifier"""
        member = get_a_member(card_no)
        if not member:
            api.abort(404)
        else:
            return member
