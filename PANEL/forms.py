from wtforms_alchemy import ModelForm
from PANEL.model import(
    Product_sql,
)

class Product_Form(ModelForm):
    class Meta:
        model = Product_sql