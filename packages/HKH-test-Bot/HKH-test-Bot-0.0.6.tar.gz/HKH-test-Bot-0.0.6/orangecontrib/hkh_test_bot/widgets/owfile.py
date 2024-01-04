import sys
import os
import sys

import Orange.data
from Orange.widgets.utils.signals import Input, Output
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

"""
Ce widget permet de modifier des variables globales et de spécifier des opérations à effectuer sur ces variables en utilisant une interface utilisateur. 
Il charge également des données en entrée et les renvoie en sortie.
"""
class VariableEditor(widget.OWWidget):
    name = "Variable Editor"
    description = "Edit global variable"
    icon = "icons/Emblem_of_Napoleon_Bonaparte.svg"
    priority = 10
    # astuce jcm
    ecriture_fichier_sortie=False
    dossier_du_script = os.path.dirname(os.path.abspath(__file__))
    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        data_out = Output("Data", Orange.data.Table)