from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    citizens = db.relationship('Citizen', back_populates="creator")

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Citizen(db.Model):
    """
    Create a Citizen table
    """

    __tablename__ = 'citizens'

    RACES = ['Aasimar', 'Bugbear', 'Dragonborn', 'Dwarf', 'Halfling', 'Elf', 'Goblin', 'Gnoll', 'Gnome', 'Half-human', 'Hobgoblin', '', 'Human', 'Kobold', 'Lizardfolk', 'Ogre', 'Orc', 'Tiefling']
    SEXES = ['male', 'female', 'asexual', 'hermaphrodite', 'unspecified']
    ALLEGIANCES = ['dragonborn', 'human', 'dwarf', 'orc', 'unaligned']

    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(20), unique=True)
    firstname = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(20), unique=True)
    race = db.Column('race', db.Enum(*RACES))
    occupation = db.Column(db.String(30), unique=True)
    disposition = db.Column(db.String(20), unique=True)
    allegiance = db.Column('allegiance', db.Enum(*ALLEGIANCES))
    born = db.Column(db.Integer())
    died = db.Column(db.Integer())
    sex = db.Column('sex', db.Enum(*SEXES))

    description = db.Column(db.String(200))

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship("User", back_populates="citizens")

    def __repr__(self):
        return '<Citizen: {}>'.format(self.name)

