from flask import Flask
from flask_restful import Api
from resources.gene import GeneSuggest
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anonymous:@ensembldb.ensembl.org/ensembl_website_102'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

api.add_resource(GeneSuggest, '/gene_suggest')

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
