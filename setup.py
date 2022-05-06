# encoding: utf-8
# THIS FILE IS AUTOGENERATED!
from __future__ import unicode_literals
from setuptools import setup
setup(
    author='Kyle Lahnakoski',
    author_email='kyle@lahnakoski.com',
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)","Programming Language :: Python :: 3.6","Programming Language :: Python :: 3.7","Programming Language :: Python :: 3.9"],
    description='Object destructuring of function parameters for Python!',
    extras_require={"tests":["mo-testing","mo-times","mo-json","mo-threads"]},
    include_package_data=True,
    install_requires=["mo-dots==9.173.22126","mo-future==6.2.21303"],
    license='MPL 2.0',
    long_description='\n# More KWARGS!\n\nObject destructuring of function parameters for Python!\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/mo-kwargs.svg)](https://pypi.org/project/mo-kwargs/)\n[![Build Status](https://app.travis-ci.com/klahnakoski/mo-kwargs.svg?branch=master)](https://travis-ci.com/github/klahnakoski/mo-kwargs)\n [![Coverage Status](https://coveralls.io/repos/github/klahnakoski/mo-kwargs/badge.svg?branch=dev)](https://coveralls.io/github/klahnakoski/mo-kwargs?branch=dev)\n[![Downloads](https://pepy.tech/badge/mo-kwargs)](https://pepy.tech/project/mo-kwargs)\n\n\n## Motivation\n\nJavascript has [object destructuring](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment#object_destructuring), and it can be used for function parameters. This has a couple of benefts over Python\'s keyword arguments:\n\n* Extra caller parameters are ignored (eg `f({a, b, c})`)\n* Duplicate parameters are handled elegantly (eg `f({a, a})`) \n\nThe `mo-kwargs` library provides this functionality with the `@override` decorator, with additional benefits:\n \n * required parameters throw an error if missing, just like regular Python\n * all parameters, even ones not in the argument list, are passed in the optional `kwargs` parameter \n \nThe `@override` decorator adds a `kwargs` argument which can be passed a dict of call parameters; but unlike `**kwargs`, it will not raise duplicate key exceptions.\n\n## Provide default values\n\nWe decorate the `login()` function with `@override`. `username` is a required parameter, and `password` will default to `None`. \n\n        @override\n        def login(username, password=None):\n            pass\n\nDefine some `dicts` for use with our `kwargs` parameter:\n\n        creds = {"userame": "ekyle", "password": "password123"}\n        alt_creds = {"username": "klahnakoski"}\n\n\nThe simplest case is when we use `kwargs` with no overrides\n\n        login(kwargs=creds)\n        # SAME AS\n        login(**creds)\n        # SAME AS\n        login(username="ekyle", password="password123")\n\nYou may override any property in `kwargs`: In this case it is `password`\n\n        login(password="123", kwargs=creds)\n        # SAME AS\n        login(username="ekyle", password="123")\n\nThere is no problem with overriding everything in `kwargs`:\n\n        login(username="klahnakoski", password="asd213", kwargs=creds)\n        # SAME AS\n        login(username="klahnakoski", password="asd213")\n\nYou may continue to use `**kwargs`; which provides a way to overlay one parameter template (`creds`) with another (`alt_creds`)\n\n        login(kwargs=creds, **alt_creds)\n        # SAME AS\n        login(username="klahnakoski", password="password123")\n\n## Handle too many parameters\n\nSometimes your method parameters come from a configuration file, or some other outside source which is outside your control. There may be more parameters than your method is willing to accept.  \n\n        creds = {"username": "ekyle", "password": "password123", "port":9000}\n        def login(username, password=None):\n             print(kwargs.get("port"))\n\nWithout `mo-kwargs`, passing the `creds` dictionary directly to `login()` would raise a key error\n\n        >>> login(**creds)\n        Traceback (most recent call last):\n          File "<stdin>", line 1, in <module>\n        TypeError: login() got an unexpected keyword argument \'port\'\n            \nThe traditional solution is to pass the parameters explicitly:\n\n        login(username=creds.username, password=creds.password)\n\nbut that can get get tedious when done often, or the parameter list get long. `mo-kwargs` allows you to pass the whole dictionary to the `kwargs` parameter; only the parameters used by the method are used:\n\n        @override\n        def login(username, password=None):\n            pass\n         \n        login(kwargs=creds)\n        # SAME AS\n        login(username=creds.username, password=creds.password)\n\n## Package all parameters\n\nYour method can accept `kwargs` as a parameter. If it does, ensure it defaults to `None` so that it\'s not required.\n\n        @override\n        def login(username, password=None, kwargs=None):\n            print(kwargs.get("username"))\n            print(kwargs.get("port"))\n\n`kwargs` will always be a dict, possibly empty, with the full set of parameters. This is different from using `**kwargs` which contains only the remainder of the keyword parameters.\n\n        >>> creds = {"username": "ekyle", "password": "password123", "port":9000}\n        >>> login(**creds)\n        ekyle\n        9000\n',
    long_description_content_type='text/markdown',
    name='mo-kwargs',
    packages=["mo_kwargs"],
    url='https://github.com/klahnakoski/mo-kwargs',
    version='7.173.22126',
    zip_safe=False
)