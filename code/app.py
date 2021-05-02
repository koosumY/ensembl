from flask import Flask
from flask_restful import Api
from resources.item import GeneSuggest
from db import db


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{username}:{password}@{server}/ensembl_website_102".format("anonymous", "", "ensembldb.ensembl.org")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anonymous:@ensembldb.ensembl.org/ensembl_website_102'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

#api.add_resource(GeneSuggest, '/gene_suggest/<string:name>')
api.add_resource(GeneSuggest, '/gene_suggest')
#api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
