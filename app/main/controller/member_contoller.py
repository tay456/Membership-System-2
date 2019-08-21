from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app.main.model import revoked_token_model

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


@api2.route('/check_registration')
class CheckMemberRegistrationStatus(Resource):
    @api2.doc('checking if member is already registered using card_no')
    def get(self):
        return check_if_member_is_registered(self)


@api2.route('/login')
class Login(Resource):
    def post(self):
        return login(self)


@api.route('/refresh')
@jwt_refresh_token_required
class RefreshToken(Resource):
    def post(self):
        return refresh()


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = revoked_token_model(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500



@api.route('/cardNo:<card_no>/<int:cost>')
@api.response(201, 'Member balance deducted.')
class MemberPurchase(Resource):
    @jwt_required
    @api.doc('purchase goods')
    def put(self, card_no, cost):
        """"deducts cost of goods from member balance"""
        return modify_balance(card_no, cost)


@api2.route('/<card_no>/memberDetails')
class Member(Resource):
    @jwt_required
    @api2.marshal_with(_member2)
    def get(self, card_no):
        """get a member given its identifier"""
        return get_member_details(card_no)


@api3.route('/topUp/<card_no>/<int:money>')
@api3.response(201, 'Member balance updated.')
class MemberTopUp(Resource):
    @jwt_required
    @api3.doc('update member balance')
    def put(self, card_no, money):
        """"tops up the money on a member card"""
        return update_balance(card_no, money)

