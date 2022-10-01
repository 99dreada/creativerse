from re import S
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

"""
DB TABLES
"""

class Product_sql(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), unique=True, nullable=False)

"""
INIT DATABASE
"""

INIT_TABLES = [

]

INIT_DIRECTORY_NAME = "PANEL/db/initial"

TABLES_TO_SAVE = [

]

def create_db():
    try: db.drop_all()
    except: pass
    db.create_all()
    import csv
    import os
    for table in INIT_TABLES:
        filename = table.__name__ + '.csv'
        filename = os.path.join(INIT_DIRECTORY_NAME, filename)
        with open(filename, newline='') as file:
            for row in csv.DictReader(file):
                db.session.add(table(**row))
    db.session.commit()