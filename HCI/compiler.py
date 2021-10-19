# -*- coding: UTF-8 -*-

from PyQt5 import uic
from os import listdir

print ("[compiler.py] Called")

for filename in listdir("ui"):
    if filename.endswith(".ui"):
        ui =  "ui/" + filename
        py = "ui/Ui_" + filename.replace(".ui", ".py")

        #uic.

        with open(py, mode="w") as file:
            uic.compileUi(ui, file)#, execute=True)
    