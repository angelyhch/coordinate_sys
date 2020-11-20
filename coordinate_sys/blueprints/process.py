from flask import url_for, render_template, Blueprint


process_bp = Blueprint('process', __name__, url_prefix='/process')

@process_bp.route('/')
def stations():
    pass
    return render_template('process/stations.html')
