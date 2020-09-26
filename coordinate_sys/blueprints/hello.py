from flask import Blueprint, render_template, Response, render_template_string

hello_bp = Blueprint('hello', __name__)


@hello_bp.route('/')
def hello():
    return render_template('point_select_chart.html')


from coordinate_sys.models import chart_response
@hello_bp.route('/pygal')
def pygal():
    # return chart_response
    return Response(response='<body><h1>response string</h1></body>', content_type="text/html")