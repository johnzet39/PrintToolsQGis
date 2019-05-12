# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrintTools
                                 A QGIS plugin
 Print Tools
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
import os.path
from PyQt5.QtCore import QObject, QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QDialogButtonBox, QColorDialog, QAction, QToolButton, QMenu
from qgis.core import  (Qgis, QgsFeature, QgsGeometry, QgsMapLayer, QgsSpatialIndex,
                        QgsFeatureRequest, QgsVectorLayer, QgsField, QgsProject,
                        QgsSimpleLineSymbolLayer, QgsSimpleMarkerSymbolLayer, QgsWkbTypes,
                        QgsRenderContext)

# Initialize Qt resources from file resources.py
from .resources_rc import *
# Import the code for the dialog

from .tools.comp_print.comp_print import CompPrint
from .tools.userLegend.userlegend import UserLegend
from .tools.fragmentPrint.fragment_print import FragmentPrint

class PrintTools:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PrintFragment_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = u'PrintMap'

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.toolButton = QToolButton()
        self.toolButton.setMenu(QMenu())
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolButton.setAutoRaise(True)
        
        self.toolBtnAdd = self.iface.addToolBarWidget(self.toolButton)

        self.fragment_action = QAction(QIcon(os.path.join(
                        self.plugin_dir, 'tools/fragmentPrint', 'icon.png')),
                                        u"Create layout with fragment map", 
                                        self.iface.mainWindow())
        self.iface.addPluginToMenu(u"&PrintMap", self.fragment_action)
        m = self.toolButton.menu()
        m.addAction(self.fragment_action)
        self.toolButton.setDefaultAction(self.fragment_action)
        self.fragment_action.triggered.connect(self.run_fragmentPrint)

        self.compPrint_action = QAction(QIcon(os.path.join(
                        self.plugin_dir, 'tools/comp_print', 'icon.png')),
                                        u"Create multipage layout",
                                        self.iface.mainWindow())
        self.iface.addPluginToMenu(u"&PrintMap", self.compPrint_action)
        m = self.toolButton.menu()
        m.addAction(self.compPrint_action)
        self.compPrint_action.triggered.connect(self.run_compPrint)

        self.legend_action = QAction(QIcon(os.path.join(
                        self.plugin_dir, 'tools/userLegend', 'icon.png')), 
                                        u"Add custom legend to Layout", 
                                        self.iface.mainWindow())
        self.iface.addPluginToMenu(u"&PrintMap", self.legend_action)
        m = self.toolButton.menu()
        m.addAction(self.legend_action)
        self.legend_action.triggered.connect(self.run_userLegend)


    def unload(self):
        self.iface.unregisterMainWindowAction(self.fragment_action)
        self.iface.removePluginMenu(u"&PrintMap", self.fragment_action)
        self.iface.removeToolBarIcon(self.fragment_action)

        self.iface.unregisterMainWindowAction(self.compPrint_action)
        self.iface.removePluginMenu(u"&PrintMap", self.compPrint_action)
        self.iface.removeToolBarIcon(self.compPrint_action)

        self.iface.unregisterMainWindowAction(self.legend_action)
        self.iface.removePluginMenu(u"&PrintMap", self.legend_action)
        self.iface.removeToolBarIcon(self.legend_action)

        self.iface.removeToolBarIcon(self.toolBtnAdd)

    def run_fragmentPrint(self):
        self.toolButton.setDefaultAction(self.fragment_action)
        FragmentPrint(self.iface).run()

    def run_compPrint(self):
        self.toolButton.setDefaultAction(self.compPrint_action)
        CompPrint(self.iface).run()

    def run_userLegend(self):
        UserLegend(self.iface).run()
