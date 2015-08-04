from flask import Blueprint
            
comment = Blueprint(__name__,'comment',url_prefix='/comment')
            
from .views import *
from .models import *
