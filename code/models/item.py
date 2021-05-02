import pymysql

from db import db


class ItemModel(db.Model):
    __tablename__ = 'gene_autocomplete'

    TABLE_NAME = 'gene_autocomplete'

    display_label = db.Column(db.String(128), primary_key=True)
    species = db.Column(db.String(255), primary_key=True)

    # SQLAlchemy ORM requires at least one column denoted as a primary key column,
    # dummy column added to circumvent this error
    # column_not_exist_in_db = db.Column(db.Integer, primary_key=True)

    def __init__(self, gene, species):
        self.display_label = gene
        self.species = species

    def json(self):
        return {'gene': self.display_label, 'species': self.species}

    @classmethod
    def find_by_gene_original(cls, genesymbol, species):

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

        return {'message': "Gene '{}' not found.".format(genesymbol)}

    @classmethod
    def find_by_gene(cls, genesymbol, species, pagesize):
        res = cls.query.filter(cls.display_label.like(genesymbol + '%'))
        if species is not None:
            res = res.filter(cls.species == species)

        # all() when used to return ORM instances will de-duplicate
        # based on primary key identity as those instances come in
        if res:
            return {'items': list(map(lambda x: x.json(), res.limit(pagesize).all()))}

        return {'message': "Gene '{}' not found.".format(genesymbol)}