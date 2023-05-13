from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from PANEL.model import (
    db,
    Settings_sql,
)
from PANEL.util import (
    create_forms,
    bulk_validate,
    dict_except,
    form_from_db_fields,
    retrieve_data,
)
from PANEL import app
import PANEL.blueprints

"""
ROUTING
"""

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(PANEL.blueprints.calculator, url_prefix='/calculator')
app.register_blueprint(PANEL.blueprints.material_inv, url_prefix='/material_inv')