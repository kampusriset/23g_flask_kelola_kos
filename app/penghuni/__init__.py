from flask import Blueprint

penghuni_bp = Blueprint(
    'penghuni', __name__,
    template_folder='templates'
)

from . import routes