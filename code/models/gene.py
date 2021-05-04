import pymysql

from db import db


class GeneModel(db.Model):
    __tablename__ = 'gene_autocomplete'

    # SQLAlchemy ORM requires at least one column denoted as a primary key column in a table,
    # To circumvent this issue, we use the primary_key=True flag on display_label and species columns
    display_label = db.Column(db.String(128), primary_key=True)
    species = db.Column(db.String(255), primary_key=True)

    def __init__(self, gene, species):
        self.display_label = gene
        self.species = species

    def json(self):
        return {'gene': self.display_label, 'species': self.species}

    @classmethod
    def find_by_gene(cls, genesymbol, species, pagesize):
        res = cls.query.filter(cls.display_label.like(genesymbol + '%'))
        if species is not None:
            res = res.filter(cls.species == species)

        # all() will remove duplicates in the returned ORM instances
        # based on the primary key identity
        if res:
            hitcount = res.count()
            return [{'request': [{'hitCount': hitcount,
                                  'version': 1.0,
                                  'pageSize': pagesize}

                                 ],
                     'resultList': list(map(lambda x: x.json(), res.limit(pagesize).all()))}]

        return {'message': "Gene '{}' not found.".format(genesymbol)}
