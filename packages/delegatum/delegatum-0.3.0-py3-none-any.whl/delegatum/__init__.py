"""
Simple cascading/nested scope/namespace manager

Delegatum walks a list of objects that can represent key/value
mappings and returns the first match found for a key.

- Supports dictionaries, argparse, configparser, mapping functions
- Most dictionary-like objects should work as well
- Python json and yaml parsers return dictionaries, and so are supported

Examples
--------

The following example searches, in order: command line arguments,
a config file, a json string, a yaml string, and the output of a
function.

.. code-block:: python

  import delegatum
  import json
  import yaml # Requires external package PyYAML
  j = json.loads('{"verbose": true, "output": "file.txt"}')
  y = yaml.safe_load(some_yaml_string)
  some_f = lambda x: x * x
  delegatus = delegatum.Delegatum([cmdline, configfile, j, y, some_f])
  print(delegatus['verbose'])
  print(delegatus['garbage'])

Attributes
----------
default : object
    Default value to return if no lookup succeeds

Raises
------
DelegatumError
    General library error; should only occur if misconfigured
DelegatumMissError
    Used internally for flow control

See Also
--------
Standard library:

- argparse
- configparser
- json
- tomllib

External modules:

- PyYAML
- https://pypi.org/project/nested-lookup/
"""

__author__ = """Brendan Strejcek"""
__email__ = 'brendan@datagazing.com'
__version__ = '0.3.0'

from .delegatum import Delegatum # noqa F401
