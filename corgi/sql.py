import os
from pathlib import Path

from six.moves import configparser as CP

import pandas as pd
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL

home = str(Path.home())

def get_odbc_engine(name, odbc_filename=None, database=None):
    """
    Looks up the connection details in an odbc file and returns a SQLAlchemy engine initialized with those details.
    """
    possible_locations = []
    if odbc_filename:
        possible_locations += [odbc_filename]
    possible_locations += [
        '/etc/odbc.ini',
        '%s/odbc.ini' % home,
    ]

    odbc_loc = None
    for loc in possible_locations:
        if os.path.exists(loc):
            odbc_loc = loc
            break
    if not odbc_loc:
        raise Exception('Could not find an odbc config file. Checked: \n%s' % "\n".join(possible_locations))

    parser = CP.ConfigParser()
    parser.read(odbc_loc)

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
