from itertools import product
from flask import(
    Blueprint,
    render_template
)
from PANEL.model import(
    db,
    Product_sql,
)

calculator = Blueprint('calculator', __name__)

@calculator.route('/list')
def list():
    products = Product_sql.query.all()
    return render_template('panel/list.html', title='List Products', products=products)