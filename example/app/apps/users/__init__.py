from flask import Blueprint
            
user = Blueprint(__name__,'user',url_prefix='/user')

from .views import *
from .models import *
