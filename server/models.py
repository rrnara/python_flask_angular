from server      import db
from flask_login import UserMixin

ADMIN_ROLE = 'admin'
USER_ROLE  = 'user'

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id       = db.Column(db.Integer,    primary_key=True)
    name     = db.Column(db.String(120))
    username = db.Column(db.String(24), unique = True)
    password = db.Column(db.String(500))
    role     = db.Column(db.String(20))
    bookings = db.relationship("Bookings")

    def __init__(self, name, username, password, role):
        self.name     = name
        self.username = username
        self.password = password
        self.role     = role

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.username)

    def to_dict(self):
        return {
            "id":       self.id,
            "name":     self.name,
            "username": self.username,
            "role":     self.role
        }

    def commit(self):
        db.session.commit()

    def save(self):
        db.session.add(self)
        self.commit()
        return self


class Cleaners(db.Model):
    __tablename__ = 'cleaners'

    id       = db.Column(db.Integer, primary_key=True)
    badge    = db.Column(db.String(20), unique = True)
    name     = db.Column(db.String(120))
    bookings = db.relationship("Bookings")

    def __init__(self, badge, name):
        self.badge = badge
        self.name  = name

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name)

    def to_dict(self):
        return {
            "id":    self.id, 
            "badge": self.badge,
            "name":  self.name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class Bookings(db.Model):
    __tablename__ = 'bookings'
    # https://gist.github.com/asyd/3cff61ed09eabe187d3fbec2c8a3ee39
    __table_args__ = (
        db.UniqueConstraint('cleaner_id', 'date_booked', name='_cleaner_booking_uc'),
    )

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_booked    = db.Column(db.Date)
    cleaner_id     = db.Column(db.Integer, db.ForeignKey("cleaners.id"))
    user           = db.relationship("Users", back_populates="bookings")
    cleaner        = db.relationship("Cleaners", back_populates="bookings")

    def __init__(self, user, date_booked, cleaner):
        self.user_id = user.id
        self.date_booked = date_booked
        self.cleaner_id = cleaner.id

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.date_booked)

    def to_dict(self, withUser):
        result = {
            "id":          self.id, 
            "date_booked": self.date_booked,
            "cleaner":     self.cleaner.to_dict()
        }
        if withUser:
            result['user'] = self.user.to_dict()
        return result

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

