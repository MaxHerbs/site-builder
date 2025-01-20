import os

import yaml


class ConfigManager:
    def __init__(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file could not be found at {config_path}")
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
