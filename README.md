xmltool
========================================================================

Simple XML handling cli tool

Installation
------------------------------------------------------------------------

* not registered in python registry.  Install by cloning the repository
* after cloning the project, do `pip install`.

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
  -v, --verbose  output in verbose mode
  -h, --help     Show this message and exit.
~~~

Version Hitory
------------------------------------------------------------------------

* 0.1.0
    * Initial Version
