from .. import db, flask_bcrypt


class Member(db.Model):

    __tablename__ = "member"

    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    card_no = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Member '{}'>".format(self.name)
