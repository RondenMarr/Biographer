from flask import Blueprint

citizen = Blueprint('citizen', __name__)

from . import views
