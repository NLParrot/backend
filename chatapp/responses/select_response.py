import tomllib
import logging
import random
import pathlib
import os

class SelectResponse:
    def get_response(self, path, variables={}):
        try:
            base = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
            with open(base/(path+".toml"), "rb") as f:
                response = tomllib.load(f)

            for variable_name in response.get("variables", []):
                if variable_name not in variables:
                    raise AttributeError("variables not satisfied")

            chosen_response = random.choice(response.get("utter", []))
            return chosen_response.format(*variables)

        except Exception as e:
            logging.error(e)
            return "error"

