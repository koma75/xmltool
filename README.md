xmltool
========================================================================

Simple XML handling cli tool

Installation
------------------------------------------------------------------------

* run `pip install git+https://github.com/koma75/xmltool` in commandline

Usage
------------------------------------------------------------------------

### Validate

~~~text
Usage: xmltool chk [OPTIONS] SCHEMA XML

  Validate XML against SCHEMA file

Options:
  -v, --verbose  output in verbose mode
  -h, --help     Show this message and exit.
~~~

### Convert to JSON

~~~text
Usage: xmltool json [OPTIONS] SCHEMA XML JSON

  Convert XML to JSON using Schema

Options:
  -o, --overwrite  overwrite existing file in JSON
  -v, --verbose    output in verbose mode
  -h, --help       Show this message and exit.
~~~

### Convert to YAML

~~~text
Usage: xmltool yaml [OPTIONS] SCHEMA XML YAML

  Convert XML to YAML using Schema

Options:
  -o, --overwrite  overwrite existing file in YAML
  -v, --verbose    output in verbose mode
  -h, --help       Show this message and exit.
~~~

Version Hitory
------------------------------------------------------------------------

* 0.1.0
    * Initial Version
