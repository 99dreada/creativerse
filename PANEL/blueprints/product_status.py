from flask import(
    Blueprint,
    render_template,
)

product_status = Blueprint('product_status', __name__)

@product_status.route('/')
def index():
    return render_template('product_status/index.html')