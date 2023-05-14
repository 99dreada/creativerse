from flask import(
    Blueprint,
    render_template,
)

material_inv = Blueprint('material_inv', __name__)

@material_inv.route('/')
def index():
    return render_template('material_inv/index.html')