from flask import Blueprint

bp = Blueprint('api', __name__)

from cctwin.api import simulator, config_provider
