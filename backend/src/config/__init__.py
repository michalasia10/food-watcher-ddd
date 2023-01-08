from configparser import ConfigParser
from pathlib import Path


def read_config(config_path: str) -> ConfigParser:
    assert Path(config_path).is_file(), f"Config {config_path} doesn't exist!"
    config = ConfigParser()
    config.read(config_path)
    return config

def config_loggers():
    pass


def assemble(config_path:str):
    config = read_config(config_path)
    config_loggers()
    

