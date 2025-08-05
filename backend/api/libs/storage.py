import os
import shutil
import logging

logger = logging.getLogger("libs.storage")


class LocalStorage(object):

    def __init__(self) -> None:
        self.folder = ""

    def init_app(self, app):
        self.folder = app.config.get("STORAGE_LOCAL_PATH")
        if not self.folder:
            raise ValueError("STORAGE_LOCAL_PATH is not set")

        self.chunk_size = int(app.config.get("FILE_CHUNK_SIZE", 4096))

        if not os.path.isabs(self.folder):
            self.folder = os.path.join(app.root_path, self.folder)

    def exists(self, filename):
        filename = os.path.join(self.folder, filename)
        if not os.path.exists(filename):
            logger.error('file "%s" not found', filename)
            raise FileNotFoundError("File not found")
        return filename

    def save(self, filename, data):
        filename = os.path.join(self.folder, filename)
        folder = os.path.dirname(filename)
        os.makedirs(folder, 0o755, exist_ok=True)

        with open(filename, "wb") as fp:
            fp.write(data)

    def load(self, filename, stream=False):
        filename = self.exists(filename)
        if stream:
            return self._load_stream(filename)
        else:
            return self._load_file(filename)

    def download(self, filename, target_filename):
        filename = self.exists(filename)
        shutil.copyfile(filename, target_filename)

    def delete(self, filename):
        try:
            filename = self.exists(filename)
            os.remove(filename)
        except FileNotFoundError:
            pass

    def _load_file(self, filename):
        with open(filename, "rb") as fp:
            data = fp.read()

        return data

    def _load_stream(self, filename):
        with open(filename, "rb") as fp:
            # https://peps.python.org/pep-0572/#syntax-and-semantics
            while chunk := fp.read(self.chunk_size):
                yield chunk
