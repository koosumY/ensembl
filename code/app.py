from flask import Flask
from flask_restful import Api
from item import GeneSuggest

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

api.add_resource(GeneSuggest, '/gene_suggest/<string:name>')
#api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)
