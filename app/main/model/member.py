from .. import db, flask_bcrypt


class Member(db.Model):

    __tablename__ = "member"

    employee_id = db.Column(db.String(7), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    card_no = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    mobile_number = db.Column(db.Integer, unique=True)
    pin_number = db.Column(db.String(4), nullable=False, unique=True)
    balance = db.Column(db.Integer, default=0)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.pin_number = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.pin_number, password)

    def __repr__(self):
        return "<Member '{}'>".format(self.name)
