from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

"""
DB TABLES
"""
class Stage_sql(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), unique=True, nullable=False)
    Description = db.Column(db.Text, unique=False, nullable=True)

class Process_sql(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), unique=True, nullable=False)
    Description = db.Column(db.Text, unique=False, nullable=True)

class Product_sql(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), unique=True, nullable=False)
    Process = db.Column(db.Integer, db.ForeignKey(Process_sql.id), nullable=False)
    Stage = db.Column(db.Integer, db.ForeignKey(Process_sql.id), nullable=False)
    Machining = db.Column(db.Integer, nullable=False)
    Processing = db.Column(db.Integer, nullable=False)
    Packaging = db.Column(db.Integer, nullable=False)
    Shipping = db.Column(db.Integer, nullable=False)

class Settings_sql(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), unique=True, nullable=False)
    Value = db.Column(db.Integer, nullable=False)

"""
INIT DATABASE
"""

INIT_TABLES = [
    Process_sql,
    Stage_sql
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