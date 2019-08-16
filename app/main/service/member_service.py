from app.main import db
from app.main.model.member import Member


def add_new_member(data):
    member = Member.query.filter_by(card_no=data['card_no']).first()
    if not member:
        new_member = Member(
            name=data['name'],
            card_no=data['card_no'],
            email=data['email'],
            password=data['password_hash']
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


# need to look at possibly changing this to something else at some point
def get_a_member(card_no):
    return Member.query.filter_by(card_no=card_no).first()


def get_balance(card_no):
    response = Member
