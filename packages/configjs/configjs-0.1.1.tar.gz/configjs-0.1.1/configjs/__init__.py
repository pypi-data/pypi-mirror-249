"""
configjs is a Python package designed to simplify the process of reading and accessing configuration settings stored in a JSON file.
With configjs, you can effortlessly load a "config.json" file from the working directory and access its contents using the package name as attributes.
"""

import json
from collections import namedtuple


__version__ = "0.1.0"


class Config:
    """
    Config is a class for reading configuration settings from a JSON file and
    providing easy access to these settings using attribute syntax.

    Parameters:
    - filename (str, optional): The name of the JSON file to read. Default is "config.json".

    Attributes:
    - _config (namedtuple): A nested named tuple containing the configuration settings.

    Example Usage:
    ```python
    # Assuming the "config.json" file has the structure mentioned in the README
    config = Config()

    # Access configuration settings using the package name as attributes
    db_host = config.database.host
    db_port = config.database.port
    db_username = config.database.username
    db_password = config.database.password
    api_key = config.api_key

    # Print the configuration settings
    print(f"Database Host: {db_host}")
    print(f"Database Port: {db_port}")
    print(f"Database Username: {db_username}")
    print(f"Database Password: {db_password}")
    print(f"API Key: {api_key}")
    ```

    Note:
    - The structure of the "config.json" file is assumed to be as described in the README.
    """

    def __init__(self, filename: str = "config.json", **kwargs) -> None:
        """
        Initialize the Config instance by loading configuration settings from a JSON file.

        Parameters:
        - filename (str, optional): The name of the JSON file to read. Default is "config.json".
        """

        if kwargs:
            self._config = self._json_object_hook(kwargs)
        else:
            with open(filename, "r") as file:
                config_data = json.load(file)
            self._config = self._json_object_hook(config_data)

    def _json_object_hook(self, d):
        """
        Convert a JSON object into a nested named tuple recursively.

        Parameters:
        - d (dict): The JSON object to convert.

        Returns:
        - namedtuple: A nested named tuple representing the JSON data.
        """

        return namedtuple("Config", d.keys())(
            *[
                self._json_object_hook(v) if isinstance(v, dict) else v
                for v in d.values()
            ]
        )

    def __getattr__(self, name):
        """
        Allow attribute access using the package name itself.

        Parameters:
        - name (str): The name of the attribute to access.

        Returns:
        - Any: The value of the accessed attribute.
        """

        return getattr(self._config, name)

    def __repr__(self) -> str:
        return repr(self._config)

    def __str__(self) -> str:
        return str(self._asdict())

    def _asdict(self) -> dict:
        d = self._config._asdict()

        for k in d.keys():
            if hasattr(d[k], '_asdict'):
                d[k] = d[k]._asdict()

        return d


# Example usage:
if __name__ == "__main__":

    # Assuming the "config.json" file has the structure mentioned in the README
    config = Config()

    # Access configuration settings using the package name as attributes
    print(f"repr(config): {repr(config)}")
    print(f"str(config): {config}")
    print(f"config.database.host: {config.database.host}")
    print(f"config.database.port: {config.database.port}")
    print(f"config.database.username: {config.database.username}")
    print(f"config.database.password: {config.database.password}")
    print(f"config.api_key: {config.api_key}")

    config = Config(database=Config(host='localhost', port=5432,
                                    username='user', password='secret'), api_key='your_api_key')

    print(f"repr(config): {repr(config)}")
    print(f"str(config): {config}")
    print(f"config._asdict(): {config._asdict()}")
