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


@api.route('/registration')
class RegisteringMember(Resource):
    @api.response(201, 'Member successfully created.')
    @api.doc('create a new member')
    @api.expect(_member, validate=True)
    def post(self):
        """Registers a new Member """
        data = request.json
        return registering_a_new_member(data=data)


@api2.route('/check_registration_status')
class CheckMemberRegistrationStatus(Resource):
    @api2.expect('card_no', validate=True)
    @api2.doc('checking if member is already registered using card_no')
    def get(self, card_no):
        return check_if_member_is_registered(self, card_no)


@api3.route('/cardNo:<employee_id>/<int:cost>/<pin_number>')
@api3.response(201, 'Member balance deducted.')
class MemberPurchase(Resource):
    @api3.doc('purchase goods')
    def put(self, card_no, cost, pin_number):
        """"deducts cost of goods from member balance"""
        return modify_balance(card_no, cost, pin_number)


@api3.route('/topUp/<employee_id>/<int:money>,<pin_number>')
@api3.response(201, 'Member balance updated.')
class MemberTopUp(Resource):
    @api3.doc('update member balance')
    def put(self, card_no, money, pin_number):
        """"tops up the money on a member card"""
        return top_up_balance(card_no, money, pin_number)

