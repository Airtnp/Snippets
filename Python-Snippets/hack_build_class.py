import builtins
import sys
import dis

old_bc = builtins.__build_class__

def fake_build_class(cls_func, cls_name):
    print("Build class...")
    dis.dis(cls_func.__code__)
    print(cls_func.__code__.co_consts)
    print(cls_func.__code__.co_names)
    print(cls_name)
    print("Create class...")
    cls = old_bc(cls_func, cls_name)
    print("End of create class...")
    print(cls.__dict__['a'])

builtins.__build_class__ = fake_build_class

class A:
    a = 3
    def test():
        frame = sys._getframe(1)
        print(frame.f_locals['a'])
    test()

