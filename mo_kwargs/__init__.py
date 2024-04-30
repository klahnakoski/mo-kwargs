# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#


import sys
from functools import update_wrapper

from mo_dots import get_logger, is_data, to_data, is_many

KWARGS = str("kwargs")


def override(kwargs=None):
    """
    :param kwargs: Alternative argument name that will receive all parameters

    THIS DECORATOR WILL PUT ALL PARAMETERS INTO THE `kwargs` ARGUMENT AND
    THEN PUT ALL `kwargs` PARAMETERS INTO THE FUNCTION PARAMETERS. THIS HAS
    THE BENEFIT OF HAVING ALL PARAMETERS IN ONE PLACE (kwargs), PLUS ALL
    PARAMETERS ARE EXPLICIT FOR CLARITY.

    OF COURSE, THIS MEANS PARAMETER ASSIGNMENT MAY NOT BE UNIQUE: PARAMETER
    VALUES ARE CHOSEN IN THE FOLLOWING ORDER:
    1) EXPLICT CALL PARAMETERS
    2) PARAMETERS FOUND IN `kwargs`
    3) DEFAULT VALUES ASSIGNED IN FUNCTION DEFINITION
    """

    def output(func):
        func_name = func.__name__
        known_kwargs = get_function_arguments(func)[: func.__code__.co_argcount + func.__code__.co_kwonlyargcount]
        known_args = known_kwargs[: func.__code__.co_argcount]
        defaults = {k: v for k, v in zip(reversed(known_kwargs), reversed(func.__defaults__ or [])) if v is not None}

        def raise_error(e, a, k):
            packed = k.copy()
            packed.update(dict(zip(known_kwargs, a)))
            err = str(e)
            if func_name in err and (
                "takes at least" in err or "takes exactly " in err or "required positional argument" in err
            ):
                missing = [p for p in known_kwargs if str(p) not in packed]
                given = [p for p in known_kwargs if str(p) in packed]
                if not missing:
                    raise e
                else:
                    get_logger().error(
                        "Problem calling {func_name}:  Expecting parameter {missing}, given {given}",
                        func_name=func_name,
                        missing=missing,
                        given=given,
                        stack_depth=2,
                        cause=e,
                    )
            raise e

        if kwargs not in known_kwargs:
            # ADDING A kwargs PARAMETER TO SOME REGULAR METHOD
            def wo_kwargs(*given_args, **given_kwargs):
                settings = given_kwargs.get(kwargs, {})
                ordered_params = dict(zip(known_args, given_args))
                a, k = params_pack(known_kwargs, defaults, settings, given_kwargs, ordered_params)
                try:
                    return func(*a, **k)
                except TypeError as e:
                    raise_error(e, a, k)

            return update_wrapper(wo_kwargs, func)

        elif func_name in ("__init__", "__new__") or known_kwargs[0] in ("self", "cls"):

            def w_bound_method(*given_args, **given_kwargs):
                if len(given_args) == 2 and len(given_kwargs) == 0 and is_data(given_args[1]):
                    # ASSUME SECOND UNNAMED PARAM IS kwargs
                    a, k = params_pack(
                        known_kwargs, defaults, given_args[1], {known_kwargs[0]: given_args[0]}, given_kwargs,
                    )
                elif kwargs in given_kwargs and is_data(given_kwargs[kwargs]):
                    # PUT args INTO given_kwargs
                    a, k = params_pack(
                        known_kwargs, defaults, given_kwargs[kwargs], dict(zip(known_args, given_args)), given_kwargs,
                    )
                else:
                    a, k = params_pack(known_kwargs, defaults, dict(zip(known_args, given_args)), given_kwargs)
                try:
                    return func(*a, **k)
                except TypeError as e:
                    tb = getattr(e, "__traceback__", None)
                    if tb is not None:
                        trace = _parse_traceback(tb)
                    else:
                        trace = get_traceback(0)
                    raise_error(e, a, k)

            return update_wrapper(w_bound_method, func)

        else:

            def w_kwargs(*given_args, **given_kwargs):
                if len(given_args) == 1 and len(given_kwargs) == 0 and is_data(given_args[0]):
                    # ASSUME SINGLE PARAMETER IS kwargs
                    a, k = params_pack(known_kwargs, defaults, given_args[0])
                elif kwargs in given_kwargs and is_data(given_kwargs[kwargs]):
                    # PUT given_args INTO given_kwargs
                    a, k = params_pack(
                        known_kwargs, defaults, given_kwargs[kwargs], dict(zip(known_args, given_args)), given_kwargs,
                    )
                else:
                    # PULL kwargs OUT INTO PARAMS
                    a, k = params_pack(known_kwargs, defaults, dict(zip(known_args, given_args)), given_kwargs)
                try:
                    return func(*a, **k)
                except TypeError as e:
                    raise_error(e, a, k)

            return update_wrapper(w_kwargs, func)

    def params_pack(params, *args):
        """
        :param params:
        :param args:
        :return: (args, kwargs) pair
        """
        settings = {}
        for a in args:
            for k, v in a.items():
                settings[str(k)] = v
        settings[kwargs] = to_data(settings)

        if params and params[0] in ("self", "cls"):
            s = settings.get(params[0])
            if s is None:
                return (
                    [],
                    {k: settings[k] for k in params[1:] if k in settings},
                )
            else:
                return (
                    [s],
                    {k: settings[k] for k in params[1:] if k in settings},
                )
        else:
            return ([], {k: settings[k] for k in params if k in settings})

    if isinstance(kwargs, str):
        # COMPLEX VERSION @override(kwargs="other")
        return output
    elif kwargs == None:
        raise NotImplementedError("use @override without calling")
    else:
        # SIMPLE VERSION @override
        func, kwargs = kwargs, KWARGS
        return output(func)


def get_traceback(start):
    """
    SNAGGED FROM traceback.py

    RETURN list OF dicts DESCRIBING THE STACK TRACE
    """
    tb = sys.exc_info()[2]
    for i in range(start):
        tb = tb.tb_next
    return _parse_traceback(tb)


def _parse_traceback(tb):
    if is_many(tb):
        get_logger().error("Expecting a tracback object, not a list")
    trace = []
    while tb is not None:
        f = tb.tb_frame
        trace.append({
            "file": f.f_code.co_filename,
            "line": tb.tb_lineno,
            "method": f.f_code.co_name,
        })
        tb = tb.tb_next
    trace.reverse()
    return trace


def get_function_arguments(func):
    return func.__code__.co_varnames
