from wtforms import(
    SelectField,
    validators,
)
from wtforms_alchemy import ModelForm
from PANEL.model import(
    Product_sql,
)

class Product_Form(ModelForm):
    class Meta:
        model = Product_sql
    Process = SelectField('Process', [validators.InputRequired()], render_kw={"placeholder": "Select Process"}, coerce=int)
    Stage = SelectField('Stage', [validators.InputRequired()], render_kw={"placeholder": "Select Process"}, coerce=int)