from app.main import db
from app.main.model.member import Member
from flask import session


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
        session.permanent = True
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
        session.permanent = True
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
        session.permanent = True
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def top_up_balance(employee_id, paid_in, pass_code):
    member_details = Member.query.filter_by(employee_id=employee_id).first()
    stored_password = member_details.pin_number
    pin_code_check = member_details.check_password(stored_password, pass_code)

    if pin_code_check:

       new_balance = member_details.balance + paid_in
       db.session.commit()
       response_object = {
                'status': 'success',
                'message': 'Successfully updated balance.',
                'Balance': str(new_balance)
        }
       return response_object, 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'Incorrect pin number entered, unable to update balance',
        }
        return response_object, 409


def modify_balance(employee_id, cost, pass_code):
    member_details = Member.query.filter_by(card_no=employee_id).first()
    stored_password = member_details.pin_number
    pin_code_check = member_details.check_password(stored_password, pass_code)

    if pin_code_check:
        amount_remaining = member_details.balance - cost
        if amount_remaining >= 0:
            db.session.commit()
            response_object = {
            'Status': 'success',
            'Message': 'Successfully bought goods.',
            'New balance': str(amount_remaining)
        }
            return response_object, 200

    elif pin_code_check:
         response_object ={
            'Status': 'Fail',
            'Message': 'Incorrect pin number entered, unable to purchase goods'
        }
         return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'Not enough funds in account',
            'balance': str(member_details.balance)
        }
        return response_object, 400
