# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from PyQt5 import QtCore, QtGui

from .user_legend_dialog import UserLegendDialog
from .newuserlegend import NewUserLegend

import os.path
import codecs

class UserLegend:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PrintFragment_{}.qm'.format(locale))

        self.dlgUL = UserLegendDialog()

        self.dlgUL.composerList.itemSelectionChanged.connect(self.selectComposer)
        self.dlgUL.layerList.itemSelectionChanged.connect(self.checkOk)
        self.dlgUL.lineEdit_scale.editingFinished.connect(self.populateLayerList)
        self.dlgUL.pushButton.clicked.connect(self.populateLayerList)

        self.OK = self.dlgUL.buttonBox.button( QDialogButtonBox.Ok )


    def checkOk(self):
        if (len(self.dlgUL.layerList.selectedItems()) < 1 or
                len(self.dlgUL.composerList.selectedItems()) < 1):
            self.OK.setEnabled(False)
        else:
            self.OK.setEnabled(True)


    def populateComposerList(self):
        wdgt=self.dlgUL.composerList
        wdgt.clear()

        lM = QgsProject.instance().layoutManager()
        self.layouts_dict = {l: l.name() for l in lM.printLayouts()}

        for cView in self.layouts_dict.values():
            item=QListWidgetItem()
            item.setText(cView)
            wdgt.addItem(item)


    def populateLayerList(self):
        uscale = self.dlgUL.lineEdit_scale.text()

        wdgt=self.dlgUL.layerList
        wdgt.clear()
        for clayer in self.iface.mapCanvas().layers():
            if clayer.type() == QgsMapLayer.VectorLayer:
                if clayer.hasScaleBasedVisibility():
                    if not (clayer.minimumScale()>float(uscale) and
                            clayer.maximumScale()<float(uscale)):
                        continue
                item=QListWidgetItem()
                item.setText(clayer.name())
                wdgt.addItem(item)
        wdgt.sortItems()


    def selectComposer(self):
        keys = list(self.layouts_dict.keys())
        cView = keys[self.dlgUL.composerList.selectedIndexes()[0].row()]
        for item in cView.items():
            if item.type() ==  QgsLayoutItemRegistry.LayoutMap:
                uscale = item.scale()
                self.dlgUL.lineEdit_scale.setText(str(int(round(uscale))))
                self.populateLayerList()
                break


    def getVectorLayerByName( self, myName ):
        layermap = QgsProject.instance().mapLayers()
        for name, layer in layermap.items():
            if (layer.type() == QgsMapLayer.VectorLayer and
                    layer.name() == myName):
                if layer.isValid():
                    return layer
                else:
                    return None


    def run(self):
        self.dlgUL.setWindowFlags(self.dlgUL.windowFlags() |
                                  Qt.WindowStaysOnTopHint |
                                  Qt.WindowMinMaxButtonsHint)

        self.populateComposerList()
        self.dlgUL.layerList.clear()
        self.dlgUL.lineEdit_scale.setText(
            str(int(round(self.iface.mapCanvas().scale()))))
        self.checkOk()

        self.dlgUL.show()

        result = self.dlgUL.exec_()
        if result:
            self.doIfResult()


    def doIfResult(self):
        layer_list = []
        for layer_item in self.dlgUL.layerList.selectedItems():
            layer = self.getVectorLayerByName(layer_item.text())
            layer_list.append(layer)

            pL = QgsPrintLayout(QgsProject.instance())
            keys = list(self.layouts_dict.keys())
            cView = keys[self.dlgUL.composerList.selectedIndexes()[0].row()]

            for item in cView.items():
                if item.type() == QgsLayoutItemRegistry.LayoutMap:
                    pL = cView

                    curextent = QgsRectangle(item.extent())
                    cHeight = pL.pageCollection().page(item.page()).pageSize().height()
                    cWidth = pL.pageCollection().page(item.page()).pageSize().width()
                    uscale = item.scale()
                    break

        if pL != None:
            _newUserLegend = NewUserLegend(iface=self.iface,
                                           layer_list=layer_list,
                                           layout=pL,
                                           border_left=cWidth+10,
                                           border_top=0,
                                           border_bottom=0,
                                           maph=0,
                                           mapw=0,
                                           curextent=curextent,
                                           size_legend=cHeight,
                                           uscale=uscale,
                                           layerHeaderState=False,
                                           legendName='')
            _newUserLegend.addUserLegend()

            self.iface.openLayoutDesigner(pL)
