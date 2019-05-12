# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrintFragmentDialog
                                 A QGIS plugin
 Print Fragment
                             -------------------
        begin                : 2015-08-06
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

from PyQt5 import QtGui, uic, QtWidgets
from .print_fragment_dialog_base import Ui_PrintFragmentDialogBase

class PrintFragmentDialog(QtWidgets.QDialog, Ui_PrintFragmentDialogBase):
    def __init__(self):
        """Constructor."""
        super(PrintFragmentDialog, self).__init__()
        self.setupUi(self)
