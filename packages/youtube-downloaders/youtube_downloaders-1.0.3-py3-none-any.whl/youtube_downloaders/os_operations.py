import os


class operations:
    def __init__(self) -> None:
        self.path = None

    def is_dir_exist(self, path):
        self.path = path
        return os.path.isdir(self.path)

    def create_directory(self, path):
        return os.makedirs(path)
