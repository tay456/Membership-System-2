from app.main import db
from app.main.model.member import Member
from app.main.utilities.dto import MemberDetailsDto


def add_new_member(data):
    member = Member.query.filter_by(card_no=data['card_no']).first()
    if not member:
        new_member = Member(
            name=data['name'],
            card_no=data['card_no'],
            email=data['email'],
            password=data['password_hash'],
            balance=0
        )
        save_changes(new_member)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Member already exists. Please Log in.',
        }
        return response_object, 409


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
        response_object ={
            'status': 'fail',
            'message':'Not enough funds in account',
            'balance': str(member_details.balance)
        }
        return response_object, 400