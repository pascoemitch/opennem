"""
    settings files - read settings from env and from config.yml



"""


import os
from urllib.parse import urlparse

import yaml
from dotenv import load_dotenv

load_dotenv()

MODULE_DIR = os.path.dirname(__file__)

MYSQL_HOST_URL = os.getenv("MYSQL_HOST_URL", default=False)

DATABASE_HOST_URL = os.getenv("DATABASE_HOST_URL", default=False)


def load_config_yaml():
    config_file = os.path.join(MODULE_DIR, "config.yml")

    if not os.path.isfile(config_file):
        raise Exception(f"No config file found at {config_file}")

    with open(config_file, "r") as ymlfile:
        config = yaml.safe_load(ymlfile)

    return config


def get_mysql_host(db_name=None):
    """
        read the database connection url from env and optionally replace the database name

    """
    db_url = None

    if not MYSQL_HOST_URL:
        raise Exception("MYSQL_HOST_URL not defined")

    db_url = MYSQL_HOST_URL

    if not db_name:
        return db_url

    db_url = replace_database_in_url(db_url, db_name)

    return db_url


def get_database_host():
    if DATABASE_HOST_URL:
        return DATABASE_HOST_URL
    raise Exception("DATABASE_HOST_URL not defined")


def replace_database_in_url(db_url, db_name):
    """
        replaces the database portion of a database connection URL with db_name

        @param db_name database name to replace with
    """

    db_url_parsed = urlparse(db_url)
    db_url_parsed = db_url_parsed._replace(path=f"/{db_name}")

    return db_url_parsed.geturl()
