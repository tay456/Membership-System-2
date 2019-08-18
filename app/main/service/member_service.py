from app.main import db
from app.main.model.member import Member


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


# need to look at possibly changing this to something else at some point
def get_a_member(card_no):
    return Member.query.filter_by(card_no=card_no).first()


# top up

# edit balance by paying for something


def update(card_no, money):
    update_this = Member.query.filter_by(card_no=card_no).first()
    update_this.balance += money
    db.session.commit()
    value = True

    if value:
        response_object = {
            'status': 'success',
            'message': 'Successfully updated balance.'
        }
        return response_object, 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'Member unable to update balance',
        }
        return response_object, 409


def modify_balance(card_no, purchase):
    take_away = Member.query.filter_by(card_no=card_no).first()
    left = take_away.balance - purchase
    if take_away.balance > 0 and left >= 0:
        take_away.balance -= purchase
        db.session.commit()
        value = True
    else:
        response_object ={
            'status': 'fail',
            'message': 'Not enough funds in account'
        }
        return response_object, 400

    if value:
        response_object = {
            'status': 'success',
            'message': 'Successfully bought goods.'
        }
        return response_object, 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'Member unable to make purchase',
        }
        return response_object, 409

