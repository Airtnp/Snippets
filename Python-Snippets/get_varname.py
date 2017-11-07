import sys
import dis
import types
from opcode import *

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

# don't work with REPL
# the caller function should hack line number to get accurate lineno
def get_variable_name(var):
    last_frame = sys._getframe(1)
    frame = sys._getframe(0)
    last_code = sys._getframe(1).f_code
    last_code_arr = bytearray(last_code.co_code)
    call_lineno = last_frame.f_lineno
    # last_code_arr[last_frame.f_lineno] = opmap['CALL_FUNCTION']
    load_var_op = last_code_arr[call_lineno - 2]
    load_var_pos = last_code_arr[call_lineno - 1]
    if load_var_op == opmap['LOAD_NAME'] or load_var_op == opmap['LOAD_FAST']:
        return last_code.co_varnames[load_var_pos]
    if load_var_op == opmap['LOAD_GLOBAL']:
        return last_code.co_names[load_var_pos]
    print("I don't know, maybe just consts")
    return None

def do_nothing():
    pass

@hack_line_numbers
def g():
    ar = 1
    arrrrrgggghhhhhh = 1
    do_nothing()
    do_nothing()
    do_nothing()
    do_nothing()
    n = get_variable_name(arrrrrgggghhhhhh)
    print(n)

