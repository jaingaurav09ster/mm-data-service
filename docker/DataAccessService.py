from docker.SQLConnector import SQLConnector
from docker.AlchemyEncoder import AlchemyEncoder
from sqlalchemy.ext.automap import automap_base
from docker.config import DATABASE_CONFIG
from sqlalchemy.orm import Session
import json
from sqlalchemy import inspect


# The Data Transformation controller, transforms the data from various datasources into standardised JSON format


class DataAccessService:

    def __init__(self):
        self.Base = automap_base()

        # engine, suppose it has two tables 'user' and 'address' set up
        db = SQLConnector()
        self.engine = db.engine
        self.session = Session(self.engine)
        # reflect the tables
        self.Base.prepare(self.engine, reflect=True)

    def get_tables(self):
        inspector = inspect(self.engine)
        return json.dumps(inspector.get_table_names(), indent=4, sort_keys=True, cls=AlchemyEncoder)

    def get_columns(self):
        columns = {}
        # mapped classes are now created with names by default
        # matching that of the table name.
        table = self.Base.classes[DATABASE_CONFIG['TABLE_NAME']]
        for column in table.__table__.columns:
            column_description = str(column.type)
            columns[column.name] = column_description
        return columns

    def get_data_records(self, columns):
        table = self.Base.classes[DATABASE_CONFIG['TABLE_NAME']]
        records = self.session.query(table).all()

        return json.dumps(records, indent=4, sort_keys=True, cls=AlchemyEncoder)

    def get_queried_results(self):
        with self.engine.connect() as con:
            records = con.execute(DATABASE_CONFIG['QUERY'])
            record_dict = [dict(row) for row in records]
            return json.dumps(record_dict, indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    dataAccessService = DataAccessService()
    rows = dataAccessService.get_tables()
    print(rows)


