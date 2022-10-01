from itertools import product
from flask import(
    Blueprint,
    render_template
)
from PANEL.model import(
    db,
    Product_sql,
)
from PANEL.util import(
    create_forms,
)

calculator = Blueprint('calculator', __name__)

@calculator.route('/list')
def list():
    products = Product_sql.query.all()
    return render_template('calculator/list.html', title='List Products', products=products)

@calculator.route("/create", methods=['GET','POST'])
@create_forms('bot_form')
def create(forms):
    forms_only_show = ['bot_form']
    if request.method == 'GET':
        pass
    elif bulk_validate(dict_except(forms, forms_only_show)):
        try:
            new_bot = form_to_db_fields(Bot_sql, forms['bot_form'])
            db.session.commit()
            flash(f"Bot {new_bot.Name} has been successfully added ", "success",)
            return redirect(url_for('.list'))
        except Exception as e: # pragma: no cover
            flash(f"Bot creation not successful.\nError: {e}", "danger")
    return render_template(
        'bot/edit.html',
        title='Create Bot',
        action_mode='Create',
        **forms
    )