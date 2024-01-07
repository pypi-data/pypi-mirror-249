#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Miles"


def getName():
    return "Hello World"


def setName(name):
    if isinstance(name, str) and name != "":
        return name
    else:
        return None
