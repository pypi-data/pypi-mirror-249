import base64
import logging
import os
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import ClassVar


logger = logging.getLogger('panther')


class Singleton(object):
    _instances: ClassVar[dict] = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]


def load_env(env_file: str | Path, /) -> dict[str, str]:
    variables = {}

    if env_file is None or not Path(env_file).is_file():
        logger.critical(f'"{env_file}" is not valid file for load_env()')
        return variables

    with open(env_file) as file:
        for line in file.readlines():
            striped_line = line.strip()
            if not striped_line.startswith('#') and '=' in striped_line:
                key, value = striped_line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                variables[key] = value

                # Load them as system environment variable
                os.environ[key] = value
    return variables


def generate_secret_key() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).decode()


def round_datetime(dt: datetime, delta: timedelta):
    return datetime.min + round((dt - datetime.min) / delta) * delta


def generate_hash_value_from_string(string_value: str, /) -> str:
    # The point of this method is for maintenance, if we want to change
    # the hash algorithm in the future, it will be easy.
    return hashlib.sha256(string_value.encode('utf-8')).hexdigest()


def encrypt_password(password: str) -> str:
    return generate_hash_value_from_string(password)
