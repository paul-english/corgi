from six.moves import configparser as CP
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import create_engine

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
