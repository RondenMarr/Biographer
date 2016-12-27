from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Citizen


class CitizenForm(FlaskForm):
    """
    Form for admin to add or edit a citizen
    """
    firstname = StringField('First Name', validators=[])
    lastname = StringField('Surname', validators=[DataRequired()])
    title = StringField('Title')
#    race =  ChoicesSelect(choices=Citizen.RACES.items()),
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

