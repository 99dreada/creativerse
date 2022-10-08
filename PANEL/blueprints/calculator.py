from flask import(
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from PANEL.model import(
    db,
    Product_sql,
)
from PANEL.util import(
    bulk_validate,
    create_forms,
    dict_except,
    form_from_db_fields,
    form_to_db_fields,
    natural_to_surrogate_key,
    retrieve_data,
)

calculator = Blueprint('calculator', __name__)

@calculator.route('/list')
@retrieve_data('list_products')
def list(dbvalues):
    return render_template('calculator/list.html', title='List Products', products=dbvalues['list_products'])

@calculator.route("/create", methods=['GET','POST'])
@create_forms('product_form')
def create(forms):
    forms_only_show = ['product_form']
    if request.method == 'GET':
        pass
    elif bulk_validate(dict_except(forms, forms_only_show)):
        try:
            new_product = form_to_db_fields(Product_sql, forms['product_form'])
            db.session.commit()
            flash(f"Product {new_product.Name} has been successfully added ", "success",)
            return redirect(url_for('.list'))
        except Exception as e: # pragma: no cover
            flash(f"Product creation not successful.\nError: {e}", "danger")
    return render_template(
        'calculator/edit.html',
        title='Create Product',
        action_mode='Create',
        **forms
    )

@calculator.route('/<Name>/edit', methods=['GET','POST'])
@natural_to_surrogate_key(Product_sql, 'Name')
@retrieve_data('current_product')
@create_forms('product_form')
def edit(Name, id, forms, dbvalues):
    forms_only_show = ['product_form']
    if request.method == 'GET':
        form_from_db_fields(dbvalues['current_product'], forms['product_form'])
    elif bulk_validate(dict_except(forms, forms_only_show)):
        forms['product_form'].populate_obj(dbvalues['current_product'])
        try:
            db.session.commit()
            flash(f"product {Name} has been sucessfully amended", "success")
            return redirect(url_for('.list'))
        except Exception as e:
            flash(f"product amendment was unsuccessful.\nerror: {e}", "danger")
    return render_template(
        'calculator/edit.html',
        title='Edit product',
        action_mode='Edit',
        name=Name,
        **forms
    )

@calculator.route('/<Name>/delete', methods=['POST'])
@natural_to_surrogate_key(Product_sql, 'Name')
def delete(Name, id):
    product = Product_sql.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(f'product has been deleted', 'success')
    return redirect(url_for('.list'))