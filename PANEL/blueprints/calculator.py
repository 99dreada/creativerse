from flask import(
    Blueprint,
    render_template,
)

calculator = Blueprint('calculator', __name__)

@calculator.route('/')
def index():
    return render_template('calculator/index.html')