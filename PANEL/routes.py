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
    form_to_db_fields,
)
from PANEL import app
import PANEL.blueprints

"""
ROUTING
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET','POST'])
@create_forms('settings_form')
def settings(forms):
    forms_only_show = ['settings_form']
    if request.method == 'GET':
        pass
    elif bulk_validate(dict_except(forms, forms_only_show)):
        try:
            new_setting = form_to_db_fields(Settings_sql, forms['settings_form'])
            db.session.commit()
            flash(f"Settings have been updated", "success")
            return redirect(url_for('.settings'))
        except Exception as e: # pragma: no cover
            flash(f"Settings not updated.\nError: {e}", "danger")
    return render_template(
        'settings.html',
        title='Settings',
        **forms
    )

app.register_blueprint(PANEL.blueprints.calculator, url_prefix='/calculator')