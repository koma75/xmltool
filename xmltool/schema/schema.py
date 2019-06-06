#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""exif sort implementation"""

# BSD 2-Clause License
#
# Copyright (c) 2019, Yasuhiro Okuno (Koma)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import os
from enum import IntEnum

import click
import xmlschema
import yaml


class Level(IntEnum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

def pout(msg=None, verbose=0, level=Level.INFO, newline=True):
    """stdout support method

    Keyword Arguments:
        msg {string} -- message to print (default: {None})
        verbose {bool} -- Set True to print DEBUG message (default: {False})
        level {Level} -- Set message level for coloring (default: {Level.INFO})
        newline {bool} -- set to False if trailing new line is not needed (default: {True})
    """
    error=False
    if level in {Level.NOTSET, Level.DEBUG}:
        # DEBUG messages
        if verbose < 2: # should print if larger than 2 -vv
            return
        fg = 'magenta'
    elif level == Level.INFO:
        fg = 'green' # always print
    elif level == Level.WARNING:
        if verbose < 1: # should print if larger than 1 -v
            return
        fg = 'yellow'
        error=True
    elif level in {Level.ERROR, Level.CRITICAL}:
        fg = 'red'
        error=True
    else:
        pass
    click.echo(click.style(str(msg), fg=fg), nl=newline, err=error)
    return

def validate(kwargs):
    """Validate xml against xsd schema file

    Arguments:
        kwargs {Object} -- Keyword arguments parsed by Click library
    """
    # validate xml against xsd schema file
    rt = True
    pout(kwargs, kwargs["verbose"], Level.DEBUG)
    try:
        pout("Schema: {file}".format(file=kwargs["schema"]), kwargs["verbose"], Level.DEBUG)
        mySchema = xmlschema.XMLSchema(kwargs["schema"])
        try:
            pout("XML: {file}".format(file=kwargs["xml"]), kwargs["verbose"], Level.DEBUG)
            mySchema.validate(kwargs["xml"])
        except Exception as e:
            pout("validation failed", kwargs["verbose"], Level.WARNING)
            pout("{msg}".format(msg=str(e)), kwargs["verbose"], Level.ERROR)
            rt = False
    except Exception as e:
        pout("XML Schema load failed.", kwargs["verbose"], Level.WARNING)
        pout("{msg}".format(msg=str(e)), kwargs["verbose"], Level.ERROR)
        rt = False
    if rt:
        pout("XML Schema valid!", kwargs["verbose"], Level.INFO)
    return

def toJson(kwargs):
    """Export xml file to JSON

    Arguments:
        kwargs {Object} -- Keyword arguments parsed by Click library
    """
    # export xml file to json
    pout(kwargs, kwargs["verbose"], Level.DEBUG)
    err = False
    try:
        pout("Schema: {file}".format(file=kwargs["schema"]), kwargs["verbose"], Level.DEBUG)
        mySchema = xmlschema.XMLSchema(kwargs["schema"], validation='lax')
        try:
            pout("XML: {file}".format(file=kwargs["xml"]), kwargs["verbose"], Level.DEBUG)
            xmlJson = json.dumps(mySchema.to_dict(kwargs["xml"], decimal_type=str), indent=4)
            pout("{out}".format(out=xmlJson), kwargs["verbose"], Level.DEBUG)
        except Exception as e:
            pout("validation failed", kwargs["verbose"], Level.WARNING)
            pout("{msg}".format(msg=str(e)), kwargs["verbose"], Level.ERROR)
            err = True
    except Exception as e:
        pout("XML Schema load failed.", kwargs["verbose"], Level.WARNING)
        pout("{msg}".format(msg=str(e)), kwargs["verbose"], Level.ERROR)
        err = True
    if not err:
        # Successfully read xml file. output to kwargs["json"]
        try:
            fileexists = os.path.exists(kwargs["json"])
            if kwargs["overwrite"] or not fileexists:
                if fileexists:
                    pout("overwriting {fname}".format(fname=kwargs["json"]), kwargs["verbose"], Level.WARNING)
                outfile = open(kwargs["json"], "w")
                outfile.write("{output}".format(output=xmlJson))
            else:
                pout("cannot overwrite {fname}".format(fname=kwargs["json"]), kwargs["verbose"], Level.ERROR)
        except:
            pout("could not write to file: {fname}".format(fname=kwargs["json"]), kwargs["verbose"], Level.ERROR)
    return

def toYAML(kwargs):
    """Export xml file to YAML

    Arguments:
        kwargs {Object} -- Keyword arguments parsed by Click library
    """
    pout(kwargs, kwargs["verbose"], Level.DEBUG)
    err = False
    try:
        pout("Schema: {file}".format(file=kwargs["schema"]), kwargs["verbose"], Level.DEBUG)
        mySchema = xmlschema.XMLSchema(kwargs["schema"], validation='lax')
        try:
            pout("XML: {file}".format(file=kwargs["xml"]), kwargs["verbose"], Level.DEBUG)
            xmlYAML = yaml.dump(mySchema.to_dict(kwargs["xml"], decimal_type=str), sort_keys=False)
            pout("{out}".format(out=xmlYAML), kwargs["verbose"], Level.DEBUG)
        except Exception as e:
            pout("validation failed", kwargs["verbose"], Level.WARNING)
            pout("{msg}".format(msg=str(e)), kwargs["verbose"], Level.ERROR)
            err = True
    except Exception as e:
        pout("XML Schema load failed.", kwargs["verbose"], Level.WARNING)
        pout("{msg}".format(msg=str(e)), kwargs["verbose"], Level.ERROR)
        err = True
    if not err:
        # Successfully read xml file. output to kwargs["yaml"]
        try:
            fileexists = os.path.exists(kwargs["yaml"])
            if kwargs["overwrite"] or not fileexists:
                if fileexists:
                    pout("overwriting {fname}".format(fname=kwargs["yaml"]), kwargs["verbose"], Level.WARNING)
                outfile = open(kwargs["yaml"], "w")
                outfile.write("{output}".format(output=xmlYAML))
            else:
                pout("cannot overwrite {fname}".format(fname=kwargs["yaml"]), kwargs["verbose"], Level.ERROR)
        except:
            pout("could not write to file: {fname}".format(fname=kwargs["yaml"]), kwargs["verbose"], Level.ERROR)
    return
