from flask import Blueprint, render_template, request
from coordinate_sys.form_temp import CheckBox
import coordinate_sys.models as md
import re

hello_bp = Blueprint('hello', __name__)



@hello_bp.route('/')
def hello():
    vin_list_all = md.read_database().columns.to_list()[3:]

    return render_template('hello.html', vin_list_all=vin_list_all)






@hello_bp.route('/form_temp', methods=['get', 'post'])
def form_temp():
    form = CheckBox()
    if form.validate_on_submit():
        a = form.aaaa.data
        b = form.bbbb.data
        c = form.cccc.name
        d = form.dddd.name
        return render_template('form_temp.html', form=form, a=a, b=b, c=c, d=d)
    return render_template('form_temp.html', form=form)


@hello_bp.route('/chart_fig', methods=['get', 'post'])
def chart_fig():
    vin_list1 = request.values.getlist('vin_list')

    point_input = request.values.get("point_select")
    point_input_upper = point_input.upper()
    pattern = '[A-Z]{2}\d{4}[A-Z]'
    point_select = re.findall(pattern, point_input_upper)

    direction = request.values.get('direction')

    df = md.read_database()
    column_head3 = ['特征点号', '方向', '名义值']
    vin_list = column_head3 + vin_list1
    chart_points = md.point_select(df, point_list=point_select, direction=direction, vin_list=vin_list)
    chart_response = md.chart_select_point(select_points_df=chart_points)
    return chart_response