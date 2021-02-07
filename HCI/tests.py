# -*- coding: utf-8 -*-

from sys import argv


if len(argv) != 2:

    print("")
    print("This script is a class test launcher. You should provide the name of the class to test such as in this example :")
    print("$ python tests.py CLASSNAME")
    print("")

else:

    from config import *
    from compiler import *
    CLASSNAME = argv[1]

    exec(f"import lib.{CLASSNAME} as classModule")
    exec(f"Class = classModule.{CLASSNAME}")

    Class.test(CONFIG)