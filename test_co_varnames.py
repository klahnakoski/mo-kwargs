# Test various function signatures
def func1(a, b, c):
    pass

def func2(a, b, *args):
    pass

def func3(a, b, **kwargs):
    pass

def func4(a, b, *args, **kwargs):
    pass

def func5(a, b, c=10, *args, d=20, **kwargs):
    pass

def test_func(func):
    code = func.__code__
    print(f"\n{func.__name__}:")
    print(f"  co_varnames: {code.co_varnames}")
    print(f"  co_argcount: {code.co_argcount}")
    print(f"  co_kwonlyargcount: {code.co_kwonlyargcount}")
    print(f"  co_flags: {code.co_flags:08b} (decimal: {code.co_flags})")
    print(f"  co_flags & 0x04 (VAR_POSITIONAL/*args): {bool(code.co_flags & 0x04)}")
    print(f"  co_flags & 0x08 (VAR_KEYWORD/**kwargs): {bool(code.co_flags & 0x08)}")

    # Calculate positions
    argcount = code.co_argcount
    kwonlyargcount = code.co_kwonlyargcount
    has_varargs = bool(code.co_flags & 0x04)
    has_varkw = bool(code.co_flags & 0x08)

    print(f"\n  Breakdown:")
    print(f"    Position 0-{argcount-1}: positional args = {code.co_varnames[:argcount]}")
    if kwonlyargcount > 0:
        print(f"    Position {argcount}-{argcount+kwonlyargcount-1}: keyword-only args = {code.co_varnames[argcount:argcount+kwonlyargcount]}")

    varargs_index = argcount + kwonlyargcount
    if has_varargs:
        print(f"    Position {varargs_index}: *args name = {code.co_varnames[varargs_index]}")

    varkw_index = varargs_index + int(has_varargs)
    if has_varkw:
        print(f"    Position {varkw_index}: **kwargs name = {code.co_varnames[varkw_index]}")

    print(f"    Position {varkw_index + int(has_varkw)}-end: local variables = {code.co_varnames[varkw_index + int(has_varkw):]}")

for func in [func1, func2, func3, func4, func5]:
    test_func(func)

