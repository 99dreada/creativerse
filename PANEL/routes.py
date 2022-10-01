from flask import (
    render_template,
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