from flask import request
from flask_restplus import Resource

from app.main.utilities.dto import MemberDto, MemberDetailsDto, MemberBalanceDto
from ..service.member_service_handler import *

api = MemberDto.api
_member = MemberDto.member

api2 = MemberDetailsDto.api
_member2 = MemberDetailsDto.member

api3 = MemberBalanceDto.api
_member_balance = MemberBalanceDto.member


@api.route('/')
class MemberList(Resource):
    @api.response(201, 'Member successfully created.')
    @api.doc('create a new member')
    @api.expect(_member, validate=True)
    def post(self):
        """Creates a new Member """
        data = request.json
        return add_new_member(data=data)


@api.route('/cardNo:<card_no>/<int:cost>')
@api.response(201, 'Member balance deducted.')
class MemberPurchase(Resource):
    @api.doc('purchase goods')
    def put(self, card_no, cost):
        """"deducts cost of goods from member balance"""
        return modify_balance(card_no, cost)


@api2.route('/<card_no>/memberDetails')
class Member(Resource):
    @api2.marshal_with(_member2)
    def get(self, card_no):
        """get a member given its identifier"""
        return get_member_details(card_no)


@api3.route('/topUp/<card_no>/<int:money>')
@api3.response(201, 'Member balance updated.')
class MemberTopUp(Resource):
    @api3.doc('update member balance')
    def put(self, card_no, money):
        """"tops up the money on a member card"""
        return update_balance(card_no, money)


