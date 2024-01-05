import json
import pathlib
import tomllib

import pydantic

from oci_client import _helpers


class Config(pydantic.BaseModel):
    tenant: str
    user: str
    fingerprint: str
    region: str
    pem_private_key: bytes


async def _config_from_toml(file: _helpers.SupportsRead[bytes]):
    return Config(**tomllib.load(file))


async def read_toml(path_or_file: pathlib.Path | _helpers.SupportsRead[bytes]):
    if isinstance(path_or_file, pathlib.Path):
        with path_or_file.open(mode='rb') as f:
            return _config_from_toml(f)
    else:
        return _config_from_toml(path_or_file)


async def _config_from_json(file: _helpers.SupportsRead[str | bytes]):
    return Config(**json.load(file))


async def read_json(path_or_file: pathlib.Path | _helpers.SupportsRead[str | bytes]):
    if isinstance(path_or_file, pathlib.Path):
        with path_or_file.open(mode='r') as f:
            return _config_from_json(f)
    else:
        return _config_from_json(path_or_file)
