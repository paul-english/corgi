from six.moves import configparser as CP
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import create_engine
import os
import pandas as pd

def get_odbc_engine(name, odbc_filename='/etc/odbc.ini', database=None):
    """
    Looks up the connection details in an odbc file and returns a SQLAlchemy engine initialized with those details.
    """

    parser = CP.ConfigParser()
    parser.read(odbc_filename)

    cfg_dict = dict(parser.items(name))

    if database:
        cfg_dict['database'] = database

    connection_href = str(URL(**cfg_dict))

    engine = create_engine(connection_href)

    return engine

def cached_read_sql(name, engine, sql_loc='sql', out_data_loc='data', refresh=False):
    sql_fname = '%s/%s.sql' % (sql_loc, name)
    data_fname = '%s/%s.csv' % (out_data_loc, name)

    if os.path.isfile(data_fname):
        return pd.read_csv(data_fname)
    with open(sql_fname) as f:
        df = pd.read_sql(f.read(), engine)
    df.to_csv(data_fname, index=False)
    return df
