# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from __future__ import absolute_import, division, unicode_literals

from mo_dots import get_logger, is_data, wrap, zip as dict_zip
from mo_future import get_function_arguments, get_function_defaults, get_function_name, text_type
from mo_logs import Except

KWARGS = str("kwargs")

def override(func):
    """
    THIS DECORATOR WILL PUT ALL PARAMETERS INTO THE `kwargs` PARAMETER AND
    THEN PUT ALL `kwargs` PARAMETERS INTO THE FUNCTION PARAMETERS. THIS HAS
    THE BENEFIT OF HAVING ALL PARAMETERS IN ONE PLACE (kwargs), PLUS ALL
    PARAMETERS ARE EXPLICIT FOR CLARITY.

    OF COURSE, THIS MEANS PARAMETER ASSIGNMENT MAY NOT BE UNIQUE: VALUES CAN
    COME FROM EXPLICIT CALL PARAMETERS, OR FROM THE kwargs PARAMETER. IN
    THESE CASES, PARAMETER VALUES ARE CHOSEN IN THE FOLLOWING ORDER:
    1) EXPLICT CALL PARAMETERS
    2) PARAMETERS FOUND IN kwargs
    3) DEFAULT VALUES ASSIGNED IN FUNCTION DEFINITION
    """

    func_name = get_function_name(func)
    params = get_function_arguments(func)
    if not get_function_defaults(func):
        defaults = {}
    else:
        defaults = {k: v for k, v in zip(reversed(params), reversed(get_function_defaults(func)))}

    def raise_error(e, packed):
        err = text_type(e)
        e = Except.wrap(e)
        if err.startswith(func_name) and ("takes at least" in err or "required positional argument" in err):
            missing = [p for p in params if str(p) not in packed]
            given = [p for p in params if str(p) in packed]
            if not missing:
                raise e
            else:
                get_logger().error(
                    "Problem calling {{func_name}}:  Expecting parameter {{missing}}, given {{given}}",
                    func_name=func_name,
                    missing=missing,
                    given=given,
                    stack_depth=2,
                    cause=e
                )
        raise e

    if KWARGS not in params:
        # WE ASSUME WE ARE ONLY ADDING A kwargs PARAMETER TO SOME REGULAR METHOD
        def wo_kwargs(*args, **kwargs):
            settings = kwargs.get(KWARGS, {})
            ordered_params = dict(zip(params, args))
            packed = params_pack(params, defaults, settings, kwargs, ordered_params)
            try:
                return func(**packed)
            except TypeError as e:
                raise_error(e, packed)
        return wo_kwargs

    elif func_name in ("__init__", "__new__"):
        def w_constructor(*args, **kwargs):
            if KWARGS in kwargs:
                packed = params_pack(params, defaults, kwargs[KWARGS], kwargs, dict_zip(params[1:], args[1:]))
            elif len(args) == 2 and len(kwargs) == 0 and is_data(args[1]):
                # ASSUME SECOND UNNAMED PARAM IS kwargs
                packed = params_pack(params, defaults, args[1])
            else:
                # DO NOT INCLUDE self IN kwargs
                packed = params_pack(params, defaults, kwargs, dict_zip(params[1:], args[1:]))
            try:
                return func(args[0], **packed)
            except TypeError as e:
                packed['self'] = args[0]  # DO NOT SAY IS MISSING
                raise_error(e, packed)
        return w_constructor

    elif params[0] == "self":
        def w_bound_method(*args, **kwargs):
            if len(args) == 2 and len(kwargs) == 0 and is_data(args[1]):
                # ASSUME SECOND UNNAMED PARAM IS kwargs
                packed = params_pack(params, defaults, args[1])
            elif KWARGS in kwargs and is_data(kwargs[KWARGS]):
                # PUT args INTO kwargs
                packed = params_pack(params, defaults, kwargs[KWARGS], dict_zip(params[1:], args[1:]), kwargs)
            else:
                packed = params_pack(params, defaults, dict_zip(params[1:], args[1:]), kwargs)
            try:
                return func(args[0], **packed)
            except TypeError as e:
                raise_error(e, packed)
        return w_bound_method

    else:
        def w_kwargs(*args, **kwargs):
            if len(args) == 1 and len(kwargs) == 0 and is_data(args[0]):
                # ASSUME SINGLE PARAMETER IS kwargs
                packed = params_pack(params, defaults, args[0])
            elif KWARGS in kwargs and is_data(kwargs[KWARGS]):
                # PUT args INTO kwargs
                packed = params_pack(params, defaults, kwargs[KWARGS], dict_zip(params, args), kwargs)
            else:
                # PULL kwargs OUT INTO PARAMS
                packed = params_pack(params, defaults, dict_zip(params, args), kwargs)
            try:
                return func(**packed)
            except TypeError as e:
                raise_error(e, packed)
        return w_kwargs


def params_pack(params, *args):
    settings = {}
    for a in args:
        for k, v in a.items():
            settings[str(k)] = v
    settings[KWARGS] = wrap(settings)

    output = {
        k: settings[k]
        for k in params
        if k in settings
    }
    return output
