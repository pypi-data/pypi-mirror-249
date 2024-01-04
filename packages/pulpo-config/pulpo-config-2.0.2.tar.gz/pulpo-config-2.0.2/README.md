# pulpo-config

[![Python CI](https://github.com/jasonray/pulpo-config/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/jasonray/pulpo-config/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/pulpo-config.svg)](https://badge.fury.io/py/pulpo-config)

# Overview
The `Config` class provides a robust and flexible way to manage configuration settings in Python applications. It offers a simple interface to load, retrieve, and set configuration parameters, making it ideal for projects that require dynamic configuration handling.

# Key Features
## Easy Initialization
* Initialize with a dictionary of options or a JSON file.
* Automatically loads options from a file if a file path is provided.
## Flexible Option Retrieval
* Retrieve configuration values with support for nested keys.
* Environment variable substitution for values starting with `$ENV`.
## Command-Line Argument Processing
* Seamlessly integrates with `argparse` to update configurations from command-line arguments.
* Accepts arguments as a dictionary or `argparse.Namespace` object.
## JSON and String Representation
* Convert configurations to a JSON string or a standard string representation for easy debugging and logging.
## Specialized Value Retrieval
* Get configuration values as boolean or integer types with `getAsBool` and `getAsInt`.
* Handles type conversion and validation internally.
## Dynamic Configuration Setting
* Set configuration values with support for nested keys.
* Automatically creates intermediate dictionaries if needed.
# Benefits
* `Flexibility`: Easily manage configurations with varying levels of complexity.
* `Simplicity`: Streamline configuration management without extensive boilerplate code.
* `Compatibility`: Works seamlessly with common Python libraries like `argparse`.
* `Extensibility`: Customize and extend for more complex use cases or specific project needs.

# Basic Usage
``` python
from pulpo_config import Config

# Can load values manually through a dictionary..
config = Config(options={"database": {"host": "localhost", "port": 3306}})

# Or can load values manually..
config.set("api_key", "your-api-key")
config.set('database.host', 'localhost')

# Or can load options from a JSON config file
config = Config(json_file_path="config.json")

# Or can load from command line parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--debug_mode', type=str)
config.process_args(parser)

# Retrieve a simple configuration value
api_key = config.get("api_key")

# Retrieve a simple configuration value
is_debug_mode = config.getAsBool("debug_mode")

# Retrieve a nested configuration value
db_host = config.get("database.host")
```

# API

# Terms: Config vs Options
In this library, I use the following terms:
* `config`: higher level class that offers ability to `set`/`get`, but also ability to load from a variety of sources or convenience methods
* `options`: low level dictionary of key-value pairs, used to initialize `Config`.  An `options` dictionary is used as the internal data store for the Config implementation

## Constructor
`Config` can be initialized with a dictionary or json formatted config file
* `Config(options: dict = None, json_file_path: str = None)`
  * With no parameters, will create a `Config` with no values
  * If `options` supplied, will initialize with the supplied key-value pairs.  Note that this does support nest key-value structures.
  * What if `options` is modified after being used to initialize `Config`?  Read [here]([url](https://github.com/jasonray/pulpo-config/issues/26)).
  * If `json_file_path` will load values from json formatted config file

## Load from sources
There are a set of methods to load from others sources.  Each for these will copy key-value pairs from parameter to `Config` and return the instance of `Config` (to support chain calls).  For example:
``` python
config = Config().fromOptions(options).fromKeyValue('k', 'v').fromJsonFile('config.json')
```

* `fromOptions(self, options: dict = None)`
  * load `Config` with the supplied key-value pairs.  Note that this does support nest key-value structures.
* `fromKeyValue(self, key: str, value: typing.Any)`
  * load `Config` with the supplied key-value pair.
* `fromJsonFile(self, file_path: str)`
  * load `Config` with the content from the supplied json file
* `fromYamlFile(self, file_path: str)`
  * load `Config` with the content from the supplied yaml file
* `fromArgumentParser(self, args: dict)`
  * load `Config` with command line arguments.
  * `args` can be either `argparser` or `argparser.namepspace` (the output from `argparser.parse()`)

## Load from sources
There are a set of methods to load from others sources.  Each for these will copy key-value pairs from parameter to `Config` and return the instance of `Config` (to support chain calls).  For example:
``` python
config = Config().fromOptions(options).fromKeyValue('k', 'v').fromJsonFile('config.json')
```

* `fromOptions(self, options: dict = None)`
  * load `Config` with the supplied key-value pairs.  Note that this does support nest key-value structures.
* `fromKeyValue(self, key: str, value: typing.Any)`
  * load `Config` with the supplied key-value pair.
* `fromKeyValueList(self, key_value_list)`
  * load `Config` with supplied key-value pairs.
* `fromJsonFile(self, file_path: str)`
  * load `Config` with the content from the supplied json file.
* `fromYamlFile(self, file_path: str)`
  * load `Config` with the content from the supplied yaml file.
* `fromArgumentParser(self, args: dict)`
  * load `Config` with command line arguments.
  * `args` can be either `argparser` or `argparser.namepspace` (the output from `argparser.parse()`)
 
## process_args
Passing a standard `argparser` or `argparser.namepspace` will integrate command line params into the config values
* `process_args(self, args: dict)`
 
## Set
* `set(key: str, value: typing.Any)`
  *  Will set key=value
  *  `value` can be of any type, and would be returned as set
  *  To set a nested value (such as if database option has child option of host), use a `.`: `config.set('database.host', 'localhost')`
  *  If nested value parent(s) (such as database in the above example) does not exist, those parent(s) will be created.

## Get
* `get(key: str, default_value: typing.Any = None)`
  * Will return the value associated the key
  * If there is not a set value, the the `default_value` is returned
  * To get a nested value, use a `.`: `config.get('database.host')`
* There are also specialized get methods to cast values to specific types
* `getAsBool(self, key: str, default_value: typing.Any = None) -> bool`
* `getAsInt(self, key: str, default_value: int = None) -> int`

## Keys, Values, Iterator
* `keys`: returns a list of keys.  If the options are nested, will return in dot notation (i.e. `['parent.k1', 'parent.k2']`)
* `values`: returns a dictionary with all key-value pairs.If the options are nested, will return in dot notation (i.e. `{'parent.k1': 'v1', 'parent.k2': 'v2'}`)
* `__iter__`: iterates over the list of keys (`for key in config`)

# More Usage Patterns

## Loading from dictionary

### Using fromOptions
``` python
from pulpo_config import Config
options={"api_key": "your-api-key", "database": {"host": "localhost", "port": 3306}}
config = Config().fromOptions(options)

api_key = config.get("api_key")    
host = config.get("database.host")   
```

### Using constructor
``` python
from pulpo_config import Config
config = Config(options={"api_key": "your-api-key", "database": {"host": "localhost", "port": 3306}}
api_key = config.get("api_key")    
host = config.get("database.host")    
```

## Manually setting config
``` python
from pulpo_config import Config
config = Config()
config.set("api_key", "your-api-key")
config.set("database.host", "localhost")
config.set("database.port", 3306)
api_key = config.get("api_key")
host = config.get("database.host")    
```

## Loading from json config file
Most use cases will utilize a config file to store options.  Below is a sample config
``` json
{
    "api_key": "your-api-key",
    "database": {
        "host": "localhost",
        "port": 3306
    }
}
```
Load this config file named `config.json` using the following:
```
from pulpo_config import Config
config = Config().fromJsonFile(file_path='config.json')
api_key = config.get("api_key")
host = config.get("database.host")    
```

## Loading from command line parameters
In a scenario in which you are using commandline params with `argparser`, use the following:
```
from pulpo_config import Config
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--api_key', type=str)
config = Config().fromArgumentParser(parser)
api_key = config.get("api_key")
```

## Get bool values
The `getAsBool` will cast the value to a bool.  For this purpose, the following are considered `true`: `[True, 'TRUE', 'T', '1', 1]` (case-insensitive)
```
if config.getAsBool("enable_feature_x"):
   # do stuff
```

## Get in values
The `getAsInt` will cast the value to an int.
```
port = config.getAsInt("database.host")
```

## Extending the Config class
For many application, I prefer to create an application-specific config class, extending from the provided config class.  Example:

``` python
class MyApplicationConfig(Config):

    def __init__(self, options: dict = None, json_file_path: str = None):
        super().__init__(options=options, json_file_path=json_file_path)

    @property
    def api_key(self: Config) -> str:
        return self.get('api_key')

    @property
    def debug_mode(self: Config) -> str:
        return self.getAsBool('debug_mode', False)
```

# Installation
Pulpo-config is avaiable on PyPi: https://pypi.org/project/pulpo-config/  
Install using
```
pip install pulpo-config
```
