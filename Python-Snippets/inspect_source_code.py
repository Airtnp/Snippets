import dis
import inspect



# pass f.__code__
# pass g.gi_code
def inspect_code_object(co_obj, indent=''):
    print(indent, "%s(lineno:%d)" % (co_obj.co_name, co_obj.co_firstlineno))
    
    def printl(tp):
  	    for i in range(len(tp)):
  		      print(i, tp[i])

    print('co_consts')
    printl(co_obj.co_consts)
    print('co_names')
    printl(co_obj.co_names)
    print('co_varnames')
    printl(co_obj.co_varnames)
    print('co_freevars')
    printl(co_obj.co_freevars)
    print('co_cellvars')
    printl(co_obj.co_cellvars)
    for name, param in inspect.signature(co_obj):
        print(param.kind, ':', name, '=', param.default)
    print(dis.dis(co_obj.co_code))

    for c in co_obj.co_consts:
        if isinstance(c, types.CodeType):
            inspect_code_object(c, indent + '  ')



def inspect_generator(g):
    sourcecode = open(g.gi_code.co_filename).readlines()
    gline = g.gi_code.co_firstlineno
    generator_code = inspect.getblock(sourcecode[gline-1:])

    output = "Generator %r from %r\n" % (g.gi_code.co_name, g.gi_code.co_filename)
    output += "".join("%4s: %s" % (idx+gline, line) for idx, line in enumerate(generator_code))

    output += "Local variables:\n"
    output += "".join("%s = %r\n" % (key,value) for key,value in g.gi_frame.f_locals.items())

    return output