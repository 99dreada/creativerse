from flask import(
    Blueprint,
    render_template,
)

product_inv = Blueprint('product_inv', __name__)

@product_inv.route('/')
def index():
    return render_template('product_inv/index.html')