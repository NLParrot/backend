import tomllib


# Global class for config
class Config:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.conf = tomllib.load(f)

    def get_model_path(self, name):
        return self.conf["model_path"][name]

    def get_db_path(self, name):
        return self.conf["db_path"][name]


config = Config("config/model.toml")
