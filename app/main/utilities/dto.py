from flask_restplus import Namespace, fields


class MemberDto:
    api = Namespace('member', description='user related operations')
    member = api.model('member_post', {
        'employee_id': fields.String(required= True, description='employee unique id'),
        'name': fields.String(required=True, description='employee name'),
        'card_no': fields.String(description='employee top up card number'),
        'email': fields.String(required=True, description='employee email address'),
        'mobile_number': fields.Integer(required=True, description='employee contact number'),
        'pin_number': fields.String(required=True, description='employee passcode'),
    })


class MemberDetailsDto:
    api = Namespace('member', description='user related operations')
    member = api.model('member_get', {
        'name': fields.String(required=True, description='member name'),
        'card_no': fields.String(description='user Identifier'),
        'email': fields.String(required=True, description='member email address'),
        'mobile_number': fields.Integer(required=True, description='employee contact number'),
        'balance': fields.Integer(required=False)
    })


class MemberBalanceDto:
    api = Namespace('member', description='user related operations')
    member = api.model('member_top_up_and_purchase', {
        'employee_id': fields.String(required=True, description='employee unique id'),
        'pin_number': fields.String(required=True, description='employee passcode'),
        'money': fields.Integer(required=True),
    })

# add a DTO for mapping revoked tickets to database in both logout requests

# also add a DTO for checking user has provided token?
