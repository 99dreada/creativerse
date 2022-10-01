from flask import(
    request,
)
from flask_sqlalchemy import inspect
from functools import wraps
from PANEL import app
from PANEL.model import(
    db,
    Product_sql,
)
from PANEL.forms import(
    Product_Form
)

@app.template_filter('dict_but')
def dict_but(d, **kwargs):
    return { **d, **kwargs }

@app.template_filter('dict_except')
def dict_except(d, excepting):
    return { k: d[k] for k in d if k not in excepting }

def bulk_validate(forms):
    """
    Takes dictionary of forms in the request and returns whether each has
    validated.
    Terminal condition on first validation failure, or successful completion
    """
    # while an `all` would work, this is more debuggable
    for name, form in forms.items():
        if not form.validate():
            # print('FORM FAILED:', name, form.errors)
            return False
    return True

"""
Retrieve data from database
"""
def retrieve_data(*tables):
    def _inner(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            def retrieve_products(**kwargs):
                products = (db.session.query(Product_sql).all())
                return products
            def retrieve_current_product(id, **kwargs):
                return Product_sql.query.get_or_404(id)
            mapping = {
                'list_products': retrieve_products,
                'current_product': retrieve_current_product,
            }
            stored_records={}
            for table in tables:
                stored_records[table]=mapping[table](**kwargs)
            return f(*args, dbvalues=stored_records, **kwargs)
        return _wrapper
    return _inner   

def create_forms(*forms):
    def _inner(f):
        @wraps(f)
        def _wrapper(*args,**kwargs):
            def create_product_form(**kwargs):
                product_form = Product_Form(request.form)
                return product_form
            mapping = {'product_form': create_product_form,
                      }
            formObjs = {}
            for form in forms:
                formObjs[form] = mapping[form](**kwargs)
            return f(*args, forms=formObjs, **kwargs)
        return _wrapper
    return _inner

def natural_to_surrogate_key(SQLAlchemy_Obj, natural_kwname, natural_colname=None, surrogate_kwname=None, surrogate_colname='id'):
    if surrogate_kwname is None: surrogate_kwname = surrogate_colname
    if natural_colname is None: natural_colname = natural_kwname
    def _inner(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            nk_value = kwargs[natural_kwname]
            kwargs[surrogate_kwname] = get_surrogate_key_from_natural_key(SQLAlchemy_Obj, nk_value, natural_colname, surrogate_colname)
            return f(*args, **kwargs)
        return _wrapper
    return _inner

def get_surrogate_key_from_natural_key(SQLAlchemy_Obj, natural_key, natural_colname, surrogate_colname='id'):
    result = SQLAlchemy_Obj.query.filter_by(
        **{natural_colname: natural_key},
    ).first_or_404()
    return result.__getattribute__(surrogate_colname)

def form_to_db_fields(SQLAlchemy_Obj, WTForm_Obj, excludes=[], **kwargs):
    try:
        localdict = WTForm_Obj.data
        columns = inspect(inspect(SQLAlchemy_Obj).mapper).columns.keys()
        localdict = {k: v
            for k, v in localdict.items()
                if k not in excludes
                    and k in columns
                    and k not in kwargs
        }
        new = SQLAlchemy_Obj(
            **kwargs,
            **localdict,
        )
        db.session.add(new)
        db.session.flush()
        return new
    except Exception as e: # pragma: no cover
        raise Exception(f"Failed to create {SQLAlchemy_Obj}\nError: {e}")

def row_to_dict(row):
    return {k: row.__getattribute__(k)
        for k in inspect(inspect(row).mapper).columns.keys()
    }

def form_from_db_fields(SQLAlchemy_Obj, WTForm_Obj, excludes=[]):
    try:
        localdict = row_to_dict(SQLAlchemy_Obj)
        localdict = {k: v
            for k, v in localdict.items()
                if k not in excludes and WTForm_Obj.__contains__(k)
        }
        for k, v in localdict.items():
            WTForm_Obj[k].data = v
    except Exception as e: # pragma: no cover
        raise Exception(f"Failed to retrieve {SQLAlchemy_Obj}\nError: {e}")