import os

from wpc.config.config import configurator
from shutil import copyfile


def bootstrap():
    _make_working_dir()
    _make_database()


def _make_working_dir():
    d = configurator.data_path
    if not os.path.exists(d):
        os.makedirs(d)


def _make_database():
    db_empty = os.path.join(configurator.data_path, "res", "wpc-empty.db")
    db = os.path.join(configurator.data_path, "wpc.db")
    if not os.path.exists(db):
        copyfile(db_empty, db)
