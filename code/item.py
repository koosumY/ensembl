from flask_restful import Resource, reqparse
import pymysql

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('species', type=str, default=False, required=False, help='Enable species filtering')


# parser.add_argument('limit', type=int)

class GeneSuggest(Resource):
    TABLE_NAME = 'gene_autocomplete'

    def get(self, name):
        args = parser.parse_args(strict=True)
        species = args['species']
        print("Nice to meet you %s" % species)
        item = self.find_by_gene(name, species)
        if item:
            return item
        return {'message': 'Gene not found'}, 404

    @classmethod
    def find_by_gene(cls, genesymbol, species):

        # Open database connection
        connection = pymysql.connect("ensembldb.ensembl.org", "anonymous", "", "ensembl_website_102")

        cursor = connection.cursor()

        if species:
            query = "SELECT * FROM {table} WHERE display_label LIKE %s AND species = %s".format(table=cls.TABLE_NAME)
            cursor.execute(query, (genesymbol + '%', species))
        else:
            query = "SELECT * FROM {table} WHERE display_label LIKE %s".format(table=cls.TABLE_NAME)
            cursor.execute(query, genesymbol + '%')

        results = cursor.fetchall()
        if results:
            items = []
            for row in results:
                items.append({'Gene Name': row[2], 'Species': row[0]})
            connection.close()
            return {'Genes': items}

        return {'message': "Gene '{}' not found.".format(genesymbol)}  # TODO better message
