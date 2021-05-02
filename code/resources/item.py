from flask_restful import Resource, reqparse
from models.item import ItemModel

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('query', type=str, default=False, required=False, help='Provide gene suggestions')
parser.add_argument('species', type=str, default=False, required=False, help='Enable species filtering')
parser.add_argument('limit', type=int, default=25, required=False, help='Limit number of suggestions returned')


# parser.add_argument('limit', type=int)

class GeneSuggest(Resource):

    def get(self):
        args = parser.parse_args(strict=True)
        gene = args['query']
        species = args['species']
        limit = args['limit']
        item = ItemModel.find_by_gene(gene, species, limit)
        if item:
            return item
        return {'message': 'Gene not found'}, 404

