from flask_restplus import Api
from flask import Blueprint

from .main.controller.member_contoller import api as member_name_space
from .main.controller.member_contoller import api2 as member_name_space2

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FC Catering RESTFUL-API',
          version='1.0',
          description='a common flask restplus web service to interface between two kiosk terminals'
          )

api.add_namespace(member_name_space, path='/member')
api.add_namespace(member_name_space2)
