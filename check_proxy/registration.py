#!/usr/bin/env python

places_map = {}
checks_map = {}


def register(name, where_to_register):
    def func_wrapper(func):
        if where_to_register == 'places':
            places_map[name] = func
        elif where_to_register == 'checks':
            checks_map[name] = func
        return func

    return func_wrapper
