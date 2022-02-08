
# More KWARGS!

Object destructuring of function parameters for Python!

[![PyPI Latest Release](https://img.shields.io/pypi/v/mo-kwargs.svg)](https://pypi.org/project/mo-kwargs/)
[![Build Status](https://app.travis-ci.com/klahnakoski/mo-kwargs.svg?branch=master)](https://travis-ci.com/github/klahnakoski/mo-kwargs)
 [![Coverage Status](https://coveralls.io/repos/github/klahnakoski/mo-kwargs/badge.svg?branch=dev)](https://coveralls.io/github/klahnakoski/mo-kwargs?branch=dev)
[![Downloads](https://pepy.tech/badge/mo-kwargs)](https://pepy.tech/project/mo-kwargs)


## Motivation

Javascript has [object destructuring](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment#object_destructuring), and it can be used for function parameters. This has a couple of benefts over Python's keyword arguments:

* Extra caller parameters are ignored (eg `f({a, b, c})`)
* Duplicate parameters are handled elegantly (eg `f({a, a})`) 

The `mo-kwargs` library provides this functionality with the `@override` decorator, with additional benefits:
 
 * required parameters throw an error if missing, just like regular Python
 * all parameters, even ones not in the argument list, are passed in the optional `kwargs` parameter 
 
The `@override` decorator adds a `kwargs` argument which can be passed a dict of call parameters; but unlike `**kwargs`, it will not raise duplicate key exceptions.

## Provide default values

We decorate the `login()` function with `@override`. `username` is a required parameter, and `password` will default to `None`. 

        @override
        def login(username, password=None):
            pass

Define some `dicts` for use with our `kwargs` parameter:

        creds = {"userame": "ekyle", "password": "password123"}
        alt_creds = {"username": "klahnakoski"}


The simplest case is when we use `kwargs` with no overrides

        login(kwargs=creds)
        # SAME AS
        login(**creds)
        # SAME AS
        login(username="ekyle", password="password123")

You may override any property in `kwargs`: In this case it is `password`

        login(password="123", kwargs=creds)
        # SAME AS
        login(username="ekyle", password="123")

There is no problem with overriding everything in `kwargs`:

        login(username="klahnakoski", password="asd213", kwargs=creds)
        # SAME AS
        login(username="klahnakoski", password="asd213")

You may continue to use `**kwargs`; which provides a way to overlay one parameter template (`creds`) with another (`alt_creds`)

        login(kwargs=creds, **alt_creds)
        # SAME AS
        login(username="klahnakoski", password="password123")

## Handle too many parameters

Sometimes your method parameters come from a configuration file, or some other outside source which is outside your control. There may be more parameters than your method is willing to accept.  

        creds = {"username": "ekyle", "password": "password123", "port":9000}
        def login(username, password=None):
             print(kwargs.get("port"))

Without `mo-kwargs`, passing the `creds` dictionary directly to `login()` would raise a key error

        >>> login(**creds)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        TypeError: login() got an unexpected keyword argument 'port'
            
The traditional solution is to pass the parameters explicitly:

        login(username=creds.username, password=creds.password)

but that can get get tedious when done often, or the parameter list get long. `mo-kwargs` allows you to pass the whole dictionary to the `kwargs` parameter; only the parameters used by the method are used:

        @override
        def login(username, password=None):
            pass
         
        login(kwargs=creds)
        # SAME AS
        login(username=creds.username, password=creds.password)

## Package all parameters

Your method can accept `kwargs` as a parameter. If it does, ensure it defaults to `None` so that it's not required.

        @override
        def login(username, password=None, kwargs=None):
            print(kwargs.get("username"))
            print(kwargs.get("port"))

`kwargs` will always be a dict, possibly empty, with the full set of parameters. This is different from using `**kwargs` which contains only the remainder of the keyword parameters.

        >>> creds = {"username": "ekyle", "password": "password123", "port":9000}
        >>> login(**creds)
        ekyle
        9000
