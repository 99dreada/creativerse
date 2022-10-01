from flask import (
    render_template,
)
from PANEL import app

"""
ROUTING
"""

@app.route('/')
def index():
    return render_template('index.html')