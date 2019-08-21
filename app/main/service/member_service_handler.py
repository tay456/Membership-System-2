from app.main import db
from app.main.model.member import Member
from app.main.utilities.dto import MemberDetailsDto
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


def check_if_member_is_registered(data):
    member = Member.query.filter_by(card_no=data['card_no']).first()
    if not member:
        response_object = {
            'Status': 'Fail',
            'Message': 'This card is not registered, please register'
        }
        return response_object, 409
    else:
        response_object = {
            'Status': 'Success',
            'Message': 'Welcome ' + member.name
        }
        return response_object, 201


def registering_a_new_member(data):
    member = Member.query.filter_by(card_no=data['card_no']).first()
    if not member:
        new_member = Member(
            employee_id=data['employee_id'],
            name=data['name'],
            card_no=data['card_no'],
            email=data['email'],
            mobile_number=data['mobile_number'],
            pin_number=data['pin_number'],
            balance=0
        )
        save_changes(new_member)
        response_object = {
            'Status': 'Success',
            'Message': 'Successfully registered. ' + new_member.name
        }
        return response_object, 201
    else:
        response_object = {
            'Status': 'Fail',
            'Message': 'Looks like your already registered, welcome ' + member.name
        }
        return response_object, 409


def login(employee_id, pass_code):
    current_user = Member.query.filter_by(employee_id=employee_id).first()
    if not current_user:
        response_object = {
            'Status': 'Fail',
            'Message': 'This card is not registered, please register'
        }
        return response_object, 409

    elif current_user:
        stored_password = current_user.pin_number
        pin_code_check = current_user.check_password(stored_password, pass_code)

        if pin_code_check:
            access_token = create_access_token(identity=current_user.employee_id)
            refresh_token = create_refresh_token(identity=current_user.employee_id)
            response_object = {
                'Status': 'Success',
                'Message': 'Logged in as {}'.format(current_user.name),
                'Access_token': access_token,
                'Refresh_token': refresh_token
            }
            return response_object, 201
    else:
        response_object = {
            'Status': 'Fail',
            'Message': 'Wrong credentials'
        }
        return response_object, 409


def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    renewed_token = {
            'token': create_access_token(identity=current_user)
    }
    response_object = {
        'Status': 'Token renewed',
        'access_token': renewed_token
    }
    return response_object, 200

# def check_user_has_token():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return (logged_in_as=current_user), 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def get_member_details(card_no):
    member = Member.query.filter_by(card_no=card_no).first()
    if not member:
        response_object = {
            'status': 'unsuccessful',
            'message': 'Member does not exist, please register.'
        }
        return response_object, 404
    else:
        response_object = {
            'Member': map(MemberDetailsDto, member)
        }
        return response_object, 200


def update_balance(card_no, paid_in):
    member_details = Member.query.filter_by(card_no=card_no).first()
    new_balance = member_details.balance + paid_in
    db.session.commit()
    value = True

    if value:
        response_object = {
            'status': 'success',
            'message': 'Successfully updated balance.',
            'Balance': str(new_balance)
        }
        return response_object, 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'Member unable to update balance',
        }
        return response_object, 409


def modify_balance(card_no, cost):
    member_details = Member.query.filter_by(card_no=card_no).first()
    amount_remaining = member_details.balance - cost
    if amount_remaining >= 0:
        db.session.commit()
        response_object = {
            'Status': 'success',
            'Message': 'Successfully bought goods.',
            'New balance': str(amount_remaining)
        }
        return response_object, 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'Not enough funds in account',
            'balance': str(member_details.balance)
        }
        return response_object, 400
