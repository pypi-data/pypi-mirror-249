# dashbored

A simple dashboard framework created out of boredom. It provides a simple, tabular interface using a Python module that implements the defined specification.

## Usage

### Creating a dashbored module

The dashbored specification expects the following attributes.

* **fetch** (required) - A function that takes no arguments and returns a list of mappings of field names to values.
* **FORMAT** (optional, suggested) - This is a Python [format mini-language](https://docs.python.org/3/library/string.html?highlight=format%20mini%20string#format-specification-mini-language) string using columns from the data source as keywords.
* **FREQUENCY** (optional, suggested) - The frequency to fetch updated data using the `fetch` function

For convenience, it's also suggested to create an entry\_point within the `dashbored` group although it's not required as noted below.

### Command line interface

If a dashbored module provides the suggested defaults, then running one should be as easy as:

```python3
python3 -m dashbored <spec>
```

where specification is either a fully qualified module name or an entrypoint name within the `dashbored` group.

### Library interface

To be used as a library, simply provide the above mentioned arguments in the same positional order to the `create` functon in the `dashbored` module.

```python3
import dashbored

def myfetch():
    ...

dashbored.create("{field_a} {field_b}", myfetch, 1)
```
