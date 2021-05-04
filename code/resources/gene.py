from flask_restful import Resource, reqparse
from models.gene import GeneModel

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('query', type=str, default=False, required=True, help='Query for a gene, for e.g query=wnt4')
parser.add_argument('species', type=str, default=False, required=False, help='Enable species filtering')
parser.add_argument('limit', type=int, default=25, required=False, help='Limit the number of suggestions returned')


class GeneSuggest(Resource):
    def get(self):
        args = parser.parse_args(strict=True)
        gene_arg = args['query']
        species_arg = args['species']
        limit_arg = args['limit']
        gene = GeneModel.find_by_gene(gene_arg, species_arg, limit_arg)
        if gene:
            return gene
        return {'message': 'Gene not found'}, 404
