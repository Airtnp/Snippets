import dis
import inspect



# pass f.__code__
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
    print(dis.dis(co_obj.co_code))

    for c in co_obj.co_consts:
        if isinstance(c, types.CodeType):
            inspect_code_object(c, indent + '  ')



