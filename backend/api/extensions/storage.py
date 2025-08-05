import os
import shutil
import logging
from api.libs.storage import LocalStorage

logger = logging.getLogger("ext.storage")


class Storage(object):

    def __init__(self) -> None:
        local_storage = LocalStorage()
        self.storages = {"local": local_storage}
        self.current_storage = local_storage

    def init_app(self, app):
        storage_type = app.config.get("STORAGE_TYPE")
        storage = self.storages.get(storage_type)
        if storage is None:
            raise ValueError(f"Not supported storage type {storage_type}")

        storage.init_app(app)
        self.current_storage = storage

    def exists(self, filename):
        return self.current_storage.exists(filename)

    def save(self, filename, data):
        return self.current_storage.save(filename, data)

    def load(self, filename, stream=False):
        return self.current_storage.load(filename, stream)

    def download(self, filename, target_filename):
        return self.current_storage.download(filename, target_filename)

    def delete(self, filename):
        return self.current_storage.delete(filename)


storage = Storage()


def init_app(app):
    storage.init_app(app)
