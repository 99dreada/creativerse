from flask import(
    Blueprint,
    render_template,
)

sales_stats = Blueprint('sales_stats', __name__)

@sales_stats.route('/')
def index():
    return render_template('sales_stats/index.html')