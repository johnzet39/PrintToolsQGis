# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CompPrintDialog
                                 A QGIS plugin
 Print composition consists of extent parts
                             -------------------
        begin                : 2015-11-09
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Zlatanov Evgeniy
        email                : johnzet@yandex.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import QtGui, uic, QtCore, QtWidgets
from .resources import *
from .comp_print_dialog_base import Ui_CompPrintDialogBase

class CompPrintDialog(QtWidgets.QDialog, Ui_CompPrintDialogBase):
    def __init__(self):
        """Constructor."""
        super(CompPrintDialog, self).__init__()
        self.setupUi(self)
