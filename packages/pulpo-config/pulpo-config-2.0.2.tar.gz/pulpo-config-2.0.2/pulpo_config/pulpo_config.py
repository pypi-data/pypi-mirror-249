import typing
import json
import argparse
import os
import copy
import yaml


class Config():
    __options = None

    UTF8 = 'UTF-8'

    def __init__(self, options: dict = None, json_file_path: str = None, yaml_file_path: str = None):
        self.__options = {}

        if options:
            if isinstance(options, dict):
                self.__options = copy.deepcopy(options)
            elif isinstance(options, Config):
                self.__options = options.__options

        if json_file_path:
            self.fromJsonFile(file_path=json_file_path)

        if yaml_file_path:
            self.fromYamlFile(file_path=yaml_file_path)

    def __str__(self):
        return self.to_string()

    def __iter__(self):
        return iter(self.keys())

    def to_string(self):
        return str(self.__options)

    def to_json(self):
        return json.dumps(self.__options)

    def fromOptions(self, options: dict = None) -> 'Config':
        # this is necessary to get the nest config keys
        sourceConfig = Config(options=options)
        sourceKeys = sourceConfig.keys()

        for key in sourceKeys:
            value = sourceConfig.get(key)
            self.set(key, value)
        return self

    def fromKeyValue(self, key: str, value: typing.Any) -> 'Config':
        self.set(key, value)
        return self

    def fromKeyValueList(self, key_value_list) -> 'Config':
        for key, value in key_value_list:
            self.set(key, value)
        return self

    def fromJsonFile(self, file_path: str) -> 'Config':
        return self.fromOptions(self._load_options_from_json_file(json_file_path=file_path))

    def _load_options_from_json_file(self, json_file_path: str = None) -> dict:
        options = None
        with open(json_file_path, "r", encoding=self.UTF8) as f:
            options = json.load(f)
        return options

    def fromYamlFile(self, file_path: str) -> 'Config':
        return self.fromOptions(self._load_options_from_yaml_file(yaml_file_path=file_path))

    def _load_options_from_yaml_file(self, yaml_file_path: str = None) -> dict:
        options = None
        with open(yaml_file_path, "r", encoding=self.UTF8) as f:
            options = yaml.safe_load(f)
        return options

    def fromArgumentParser(self, args: dict) -> 'Config':
        if args:
            if isinstance(args, argparse.ArgumentParser):
                args = args.parse_args()
            if isinstance(args, argparse.Namespace):
                args = vars(args)

            for arg in args:
                # value = getattr(args, arg)
                value = args.get(arg)
                if value:
                    self.set(arg, value)
        return self

    def keys(self):
        return self._build_key_list(self.__options, None)

    def values(self):
        return self._build_value_list(self.keys())

    def _build_key_list(self, options: dict, parent_key_list=None):
        if not parent_key_list:
            parent_key_list = []

        key_list = []
        for key in options:
            key_parts = parent_key_list.copy()
            key_parts.append(key)
            full_key_name = ".".join(key_parts)
            value = self.get(full_key_name)
            if isinstance(value, dict):
                child_keys = self._build_key_list(options=value, parent_key_list=key_parts)
                key_list += child_keys
            else:
                key_list.append(full_key_name)
        return key_list

    def _build_value_list(self, keys):
        values = {}
        for key in keys:
            value = self.get(key)
            values[key] = value
        return values

    def get(self, key: str, default_value: typing.Any = None):
        keys = key.split('.')

        value = self.__options
        for subkey in keys:
            if value:
                if subkey in value:
                    value = value[subkey]
                else:
                    value = None
            else:
                value = None

        if not value:
            value = default_value

        value = self._get_handle_env(value)

        return value

    def _get_handle_env(self, value):
        Environment_Variable_Prefix = '$ENV.'
        if value:
            if isinstance(value, str):
                if value.startswith(Environment_Variable_Prefix):
                    env_var_key = value[len(Environment_Variable_Prefix):]
                    value = os.getenv(env_var_key)
        return value

    def getAsBool(self, key: str, default_value: typing.Any = None) -> bool:
        value_raw = self.get(key=key, default_value=default_value)
        value = None
        true_values = [True, 'TRUE', 'T', '1', 1]
        if isinstance(value_raw, str):
            value_raw = value_raw.upper()
        value = value_raw in true_values
        return value

    def getAsInt(self, key: str, default_value: int = None) -> int:
        value_raw = self.get(key=key, default_value=default_value)
        try:
            value = int(value_raw)
        except Exception as ex:
            raise Exception(f'Invalid config value (expected numeric value) [key={key}][value={value_raw}]') from ex
        return value

    # support key=a.b.c where it will create intermediate dictionaries
    def set(self, key: str, value: typing.Any):
        keys = key.split('.')

        parent = self.__options
        for key_number in range(0, len(keys) - 1):
            key = keys[key_number]
            if not key in parent:
                parent[key] = {}
            parent = parent.get(key)

        last_key = keys[len(keys) - 1]
        parent[last_key] = value
