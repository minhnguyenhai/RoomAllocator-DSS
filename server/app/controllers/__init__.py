from flask import Blueprint

main_api = Blueprint("main_api", __name__)

from . import main_controller