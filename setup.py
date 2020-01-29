# encoding: utf-8
# THIS FILE IS AUTOGENERATED!
from __future__ import unicode_literals
from setuptools import setup
setup(
    description=u'More KWARGS! Let call parameters override kwargs',
    license=u'MPL 2.0',
    author=u'Kyle Lahnakoski',
    author_email=u'kyle@lahnakoski.com',
    long_description_content_type=u'text/markdown',
    include_package_data=True,
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"],
    install_requires=["mo-dots>=3.33.20028","mo-future>=3.32.20028","mo-logs>=3.38.20029"],
    version=u'3.38.20029',
    url=u'https://github.com/klahnakoski/mo-kwargs',
    zip_safe=False,
    packages=["mo_kwargs"],
    long_description=u'\n# More KWARGS!\n\n|Branch      |Status   |\n|------------|---------|\n|master      | [![Build Status](https://travis-ci.org/klahnakoski/mo-kwargs.svg?branch=master)](https://travis-ci.org/klahnakoski/mo-kwargs) |\n|dev         | [![Build Status](https://travis-ci.org/klahnakoski/mo-kwargs.svg?branch=dev)](https://travis-ci.org/klahnakoski/mo-kwargs)  [![Coverage Status](https://coveralls.io/repos/github/klahnakoski/mo-kwargs/badge.svg?branch=dev)](https://coveralls.io/github/klahnakoski/mo-kwargs?branch=dev)  |\n\n\n\n## Motivation\n\nExtensive use of dependency injection, plus managing the configuration for each of the components being injected, can result in some spectacularly complex system configuration. One way to reduce the complexity is to use configuration templates that contain useful defaults, and then overwrite the properties that need to be changed for the desired configuration. \n\n`@override` has been created to provide this templating system for Python function calls. It is mostly used for class constructors, but any method can benefit. The `@overrides` decorator adds a `kwargs` parameter which can be given a template of default parameters; but unlike `**kwargs`, it will not raise duplicate key exceptions.\n\n## Provide default values\n\nWe decorate the `login()` function with `@override`. In this case, `username` is a required parameter, and `password` will default to `None`. \n\n        @override\n        def login(username, password=None):\n            pass\n\nDefine some `dicts` for use with our `kwargs` parameter:\n\n        creds = {"userame": "ekyle", "password": "password123"}\n        alt_creds = {"username": "klahnakoski"}\n\n\nThe simplest case is when we use `kwargs` with no overrides\n\n        login(kwargs=creds)\n        # SAME AS\n        login(**creds)\n        # SAME AS\n        login(username="ekyle", password="password123")\n\nYou may override any property in `kwargs`: In this case it is `password`\n\n        login(password="123", kwargs=creds)\n        # SAME AS\n        login(username="ekyle", password="123")\n\nThere is no problem with overriding everything in `kwargs`:\n\n        login(username="klahnakoski", password="asd213", kwargs=creds)\n        # SAME AS\n        login(username="klahnakoski", password="asd213")\n\nYou may continue to use `**kwargs`; which provides a way to overlay one parameter template (`creds`) with another (`alt_creds`)\n\n        login(kwargs=creds, **alt_creds)\n        # SAME AS\n        login(username="klahnakoski", password="password123")\n\n## Handle too many parameters\n\nSometimes your method parameters come from a configuration file, or some other outside source which is outside your control. There may be more parameters than your method is willing to accept.  \n\n        creds = {"username": "ekyle", "password": "password123", "port":9000}\n        def login(username, password=None):\n             print(kwargs.get("port"))\n\nWithout `mo-kwargs`, passing the `creds` dictionary directly to `login()` would raise a key error\n\n        >>> login(**creds)\n        Traceback (most recent call last):\n          File "<stdin>", line 1, in <module>\n        TypeError: login() got an unexpected keyword argument \'port\'\n            \nThe traditional solution is to pass the parameters explicitly:\n\n        login(username=creds.username, password=creds.password)\n\nbut that can get get tedious when done often, or the parameter list get long. `mo-kwargs` allows you to pass the whole dictionary to the `kwargs` parameter; only the parameters used by the method are used:\n\n        @override\n        def login(username, password=None):\n            pass\n         \n        login(kwargs=creds)\n        # SAME AS\n        login(**creds)\n\n## Package all parameters\n\nYour method can accept `kwargs` as a parameter. If it does, ensure it defaults to `None` so that it\'s not required.\n\n        @override\n        def login(username, password=None, kwargs=None):\n            print(kwargs.get("username"))\n            print(kwargs.get("port"))\n\n`kwargs` will always be a dict, possibly empty, with the full set of parameters. This is different from using `**kwargs` which contains only the remainder of the keyword parameters.\n\n        >>> creds = {"username": "ekyle", "password": "password123", "port":9000}\n        >>> login(**creds)\n        ekyle\n        9000\n',
    name=u'mo-kwargs'
)