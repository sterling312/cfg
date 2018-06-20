import os
import yaml
from contextlib import contextmanager

connection_string_format = '{dbapi}://{user}:{password}@{host}:{port}/{db}?application_name={app_name}'
gdal_postgres_format = 'PG:dbname={db} host={host} user={user} password={password} port={port}'

@contextmanager
def use_config_directory(path):
    pwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(pwd)

class Environment(dict):
    def __init__(self, environment=None):
        if environment is None:
            environment = os.environ['PYTHONENV']
        self.load_yaml(f'{environment}.yaml')

    def load_yaml(self, filename):
        with open(filename) as fh:
            self.__dict__ = yaml.load(fh)
            super().__init__(vars(self)) 

    @property
    def database_url(self):
        app_name = os.environ.get('HOSTNAME', '')
        return connection_string_format.format(app_name=app_name, **self.Database)

    @property
    def gdal_postgres_string(self):
        return gdal_postgres_format.format(**self.Database)

    @classmethod
    def get_config(cls, environment=None, path=None):
        if path is None:
            path = os.environ['CONFIG_PATH']
        with use_config_directory(path):
            return cls(environment)
