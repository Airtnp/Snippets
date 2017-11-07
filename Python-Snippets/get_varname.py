import sys
import dis
import types
from opcode import *
import inspect

# ref: https://nedbatchelder.com/blog/200804/wicked_hack_python_bytecode_tracing.html
def hack_line_numbers(f):
    """ Replace a code object's line number information to claim that every
        byte of the bytecode is a new line.  Returns a new code object.
        Also recurses to hack the line numbers in nested code objects.
    """
    code = f.__code__
    n_bytes = len(code.co_code)
    new_lnotab = "\x01\x01" * (n_bytes-1)
    new_consts = []
    for const in code.co_consts:
        if type(const) == types.CodeType:
            new_consts.append(hack_line_numbers(const))
        else:
            new_consts.append(const)
    new_code = types.CodeType(
        code.co_argcount, code.co_kwonlyargcount, code.co_nlocals, code.co_stacksize, code.co_flags,
        code.co_code, tuple(new_consts), code.co_names, code.co_varnames,
        code.co_filename, code.co_name, 0, str.encode(new_lnotab), code.co_freevars, code.co_cellvars
        )  
    f.__code__ = new_code
    f.__is_lineno_hacked__ = True
    return f

def get_variable_name_easy(**kwargs):
    for arg_name in kwargs:
        return kwargs[arg_name], arg_name

def get_variable_name_simple(var):
    loc = sys._getframe(1).f_locals
    names = []
    for k, v in loc.items():
        if v == var:
            names.append(k)
    return names

# Don't work with REPL, nothing named after f_globals['<module>']
# Need to redirect a frame
# If not handled with hacked lineno, 
# We must use 1-level nested no-argument function 
# which directly ref to ordered variable
def get_variable_name(var):
    last_frame = sys._getframe(1)
    last_code = last_frame.f_code
    last_func_name = last_code.co_name
    last_func = None
    if last_func_name in last_frame.f_globals.keys():
        last_func = last_frame.f_globals[last_func_name]
    elif last_func_name in last_frame.f_locals.keys():
        last_func = last_frame.f_globals[last_func_name]
    else:
        # nested support
        if last_func_name in last_frame.f_back.f_globals.keys():
            last_func = last_frame.f_back.f_globals[last_func_name]
        elif last_func_name in last_frame.f_back.f_locals.keys():
            last_func = last_frame.f_back.f_locals[last_func_name]
    is_lineno_hacked = False;
    if not last_func:
        print("Holy crap. Assume we have hacked our lineno")
        is_lineno_hacked = True
    elif '__is_lineno_hacked__' in last_func.__dict__.keys():
        is_lineno_hacked = True
    if is_lineno_hacked:
        last_code_arr = bytearray(last_code.co_code)
        call_lineno = last_frame.f_lineno
        # last_code_arr[last_frame.f_lineno] = opmap['CALL_FUNCTION']
        attr_name = []
        pos_code = 2
        pos_off = 1
        load_var_op = last_code_arr[call_lineno - pos_code]
        load_var_pos = last_code_arr[call_lineno - pos_off]
        while load_var_op == opmap['LOAD_ATTR']:
            attr_name.append(last_code.co_names[load_var_pos])
            load_var_op = last_code_arr[call_lineno - pos_code]
            load_var_pos = last_code_arr[call_lineno - pos_off]
            pos_code += 2
            pos_off += 2
        if load_var_op == opmap['LOAD_FAST']:
            attr_name.append(last_code.co_varnames[load_var_pos])
            return '.'.join(attr_name)
        elif load_var_op == opmap['LOAD_GLOBAL'] or load_var_op == opmap['LOAD_NAME']:
            attr_name.append(last_code.co_names[load_var_pos])
            return '.'.join(attr_name)
        elif load_var_op == opmap['LOAD_DEREF']:
            attr_name.append(last_code.co_freevars[load_var_pos])
            return '.'.join(attr_name)

        print("I don't know, maybe just consts")
        return None
    else:
        last_func = hack_line_numbers(last_func)
        sys._getframe(0).f_locals[last_func_name] = last_func
        return last_func()
        # sys._getframe(0).f_back = last_frame.f_back
        # last_frame.clear()

def do_nothing():
    pass

@hack_line_numbers
def f():
    a_var = 'str'
    print(get_variable_name(a_var)) # a_var


def g():
    ar = 1
    arrrrrgggghhhhhh = 1
    do_nothing()
    do_nothing()
    do_nothing()
    do_nothing()
    name = None
    def nested_get_varname():
        return get_variable_name(arrrrrgggghhhhhh)
    name = nested_get_varname()
    print(name) # arrrrrgggghhhhh

class A:
    pass

def h():
    test = A()
    test.t = A()
    test.t.t = 1
    return get_variable_name(test.t.t) # test.t.t

def u():
    return get_variable_name(1)

def test_all():
    f()
    g()
    print(h())
    print(u())