
from flask import  url_for , redirect , Blueprint , request , jsonify
from requests import session

from backend import db ,bcrypt
from backend.auth.models import Resources, Role, User

install = Blueprint('install', __name__)

