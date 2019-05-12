# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrintTools
                                 A QGIS self.plugin
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QDialogButtonBox, QColorDialog, QAction,
                             QToolButton, QMenu, QDialog)
from qgis.core import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtXml import QDomDocument

# Initialize Qt resources from file resources.py
# Import the code for the dialog

from .print_fragment_dialog import PrintFragmentDialog
from ..userLegend.newuserlegend import NewUserLegend
from .filter_layer import FilterLayer

import os.path
import codecs
import psycopg2


class FragmentPrint:


    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        self.lM = None # layout Manager
        self.pL = None # page Layout
        self.border_left = .0
        self.border_top = .0
        self.border_right = .0
        self.border_bottom = .0
        self.mapw = .0
        self.maph = .0
        self.size_a = .0 # page size a
        self.size_b = .0 # page size b
        self.size_legend = .0
        self.header_height = 0

        # initialize self.plugin directory
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

        # Create the dialog (after translation) and keep reference
        self.dlg = PrintFragmentDialog()

        self.dlg.radio_userPrint.clicked.connect(self.radio_userPrint_clicked)
        self.dlg.radio_shablonPrint.clicked.connect(self.radio_shablonPrint_clicked)
        self.dlg.radioButton_legendauto.clicked.connect(self.user_auto_clicked)
        self.dlg.radioButton_legenduser.clicked.connect(self.user_auto_clicked)

        self.dlg.comboBox_2.currentIndexChanged.connect(self.populate_form_user_sizes)
        self.dlg.comboBox.currentIndexChanged.connect(self.clear_headers)
        self.dlg.lineEdit_4.textEdited.connect(self.populate_form_user_header)
        self.dlg.lineEdit_5.textEdited.connect(self.populate_form_user_header)

        self.populate_listsizes()


    # legend type
    def user_auto_clicked(self):
        if self.dlg.radioButton_legendauto.isChecked():
            self.dlg.frame_user.setEnabled(False)
        elif self.dlg.radioButton_legenduser.isChecked():
            self.dlg.frame_user.setEnabled(True)


    def radio_userPrint_clicked(self):
        if self.dlg.radio_userPrint.isChecked() is False:
            self.dlg.radio_userPrint.setChecked(True)
        self.dlg.groupBox_userPrint.setCollapsed(False)
        self.dlg.groupBox_ShablonPrint.setEnabled(False)
        self.dlg.groupBox_userPrint.setEnabled(True)
        self.dlg.adjustSize()


    def radio_shablonPrint_clicked(self):
        if not self.dlg.radio_shablonPrint.isChecked():
            self.dlg.radio_shablonPrint.setChecked(True)
        self.dlg.groupBox_userPrint.setCollapsed(True)
        self.dlg.groupBox_ShablonPrint.setEnabled(True)
        self.dlg.groupBox_userPrint.setEnabled(False)
        self.dlg.adjustSize()


    def populate_form_user_header(self):
        if (len(self.dlg.lineEdit_4.text()) > 0 or
                len(self.dlg.lineEdit_5.text()) > 0):
            self.dlg.comboBox.setCurrentIndex(0)


    def clear_headers(self):
        if self.dlg.comboBox.currentIndex() != 0:
            self.dlg.lineEdit_4.setText('')
            self.dlg.lineEdit_5.setText('')


    # import composer from file
    def import_composer(self, pathfile):
        f = codecs.open(pathfile, 'r', encoding = 'cp1251')
        data = f.readlines()
        line = data[self.dlg.comboBox_3.currentIndex()].strip()
        words = line.split(';')
        f.close()

        composerName = self.getComposerName(words[0])
        isAtlas = words[2]

        layoutTemplateDocument = self.getLayoutTemplateDocument(words[1])
        self.lM = QgsProject.instance().layoutManager()
        self.pL = QgsPrintLayout(QgsProject.instance())
        context = QgsReadWriteContext()
        self.lM.addLayout(self.pL)
        self.pL.loadFromTemplate(layoutTemplateDocument, context)
        self.pL.setName(composerName)

        extent = self.iface.mapCanvas().extent()
        scale = self.iface.mapCanvas().scale()

        # get list of all map items in layout
        maps = [item for item in self.pL.items() if item.type() ==
                QgsLayoutItemRegistry.LayoutMap]

        layoutMap = self.configureMapItem(maps, extent, scale)
        if layoutMap is not None:
            self.activateAtlas(layoutMap, isAtlas)

        self.iface.openLayoutDesigner(self.pL)


    def getLayoutTemplateDocument(self, pathTemplate):
        myFile = os.path.join(self.plugin_dir, pathTemplate.strip())
        myTemplateFile = open(myFile, 'rt', encoding="utf8")
        myTemplateContent = myTemplateFile.read()
        myTemplateFile.close()
        myDocument = QDomDocument()
        myDocument.setContent(myTemplateContent, False)
        return myDocument


    def activateAtlas(self, compmap, isatlas):
        isAtlas = isatlas.strip()
        # activate atlas if ini-key = 1
        if isAtlas == '1':
            curlayer = self.iface.activeLayer()
            # show only selected features
            FilterLayer(self.iface).filtershow(curlayer)
            atlas = self.pL.atlas()
            atlas.setCoverageLayer(curlayer)
            compmap.setAtlasDriven(True)
            atlas.setEnabled(True)

    def configureMapItem(self, maps, extent, scale):
        compmap = None
        if len(maps) > 0:
            compmap = maps[0]
            compmap.setLayers([layer for layer in self.iface.mapCanvas().layers()])
            compmap.update()
            compmap_pagePos = compmap.pagePos()
            compmap_rect = compmap.boundingRect()
            compmap.setKeepLayerSet(False)
            compmap.setExtent(extent)
            compmap.setScale(scale)
            compmap.attemptSetSceneRect(QRectF(compmap_pagePos.x(), compmap_pagePos.y(), 
                                               compmap_rect.width(), compmap_rect.height()))
        return compmap


    def getComposerName(self, name):
        compCount = self.countNameLay(name)
        if compCount > 0:
            return name + ' ' + str(compCount)
        return name


    # count layouts with same names
    def countNameLay(self, name):
        count = 0
        for cView in QgsProject.instance().layoutManager().layouts():
            if ((cView.name() == name) or
                    (cView.name()[:-1].strip() == name) or
                    (cView.name()[:-2].strip() == name)):
                count+=1
        return count


    # CREATE USER PRINT LAYEOUT
    def create_fragment(self, pathfile):
        header, subheader = self.getHeaders(pathfile)

        uscale = self.dlg.spinBox_scale.value()
        extent = self.iface.mapCanvas().extent()

        self.setPageSize()
        self.setBorders()
        self.setLegendSize()
        self.createAndAddLayout()

        self.mapw = self.size_a - self.border_left - self.border_right
        self.maph = self.size_b - self.border_top - self.border_bottom - self.size_legend

        composerMap = self.addMap(extent, uscale)
        curextent = QgsRectangle(composerMap.extent())
        self.addHeader(header)
        self.addSubHeader(subheader)
        self.addScalebar(composerMap)
        self.addLegend(curextent, uscale, composerMap)
        self.setMapFrame(composerMap)

        self.iface.openLayoutDesigner(self.pL)


    def getHeaders(self, pathfile):
        if len(self.dlg.lineEdit_4.text()) > 0 or len(self.dlg.lineEdit_5.text()) > 0:
            header = self.dlg.lineEdit_4.text()
            subheader = self.dlg.lineEdit_5.text()
        else:
            f = codecs.open(pathfile, 'r', encoding = 'cp1251')
            data = f.readlines()
            line = data[self.dlg.comboBox.currentIndex()].strip()
            words = line.split(';')
            f.close()

            header = words[1].strip()
            subheader = words[2].strip()
        return header, subheader


    def setMapFrame(self, composerMap):
        # own frame
        if self.dlg.checkBox_Frame.isChecked() is False:
            composerMap.setFrameEnabled(True)
        # single frame
        else:
            composerMap.setFrameEnabled(False)
            self.addFrame()


    def addLegend(self, curextent, uscale, composerMap):
        if self.dlg.groupBox_Legend.isChecked() is True:
            # Creating QgsComposerLegend
            if self.dlg.radioButton_legendauto.isChecked() is True:
                self.addLegendAuto(composerMap)
            # Creating legend by code
            elif self.dlg.radioButton_legenduser.isChecked() is True: 
                # set list of layers for legend
                layer_list = []
                for clayer in self.iface.mapCanvas().layers():
                    if clayer.type() == QgsMapLayer.VectorLayer:
                        if clayer.hasScaleBasedVisibility():
                            if not (clayer.minimumScale() > float(uscale) and
                                    clayer.maximumScale() < float(uscale)):
                                continue
                        layer_list.append(clayer)
                layerHeaderState = self.dlg.checkBox_Layer_Header.isChecked()
                legendName = 'Условные обозначения:'
                newUserLegend = NewUserLegend(iface=self.iface,
                                              layer_list=layer_list,
                                              layout=self.pL,
                                              border_left=self.border_left,
                                              border_top=self.border_top,
                                              border_bottom=self.border_bottom,
                                              maph=self.maph,
                                              mapw=self.mapw,
                                              curextent=curextent,
                                              size_legend=self.size_legend,
                                              uscale=uscale,
                                              layerHeaderState=layerHeaderState,
                                              legendName=legendName)
                newUserLegend.addUserLegend()


    def addScalebar(self, composerMap):
        composerScaleBar = QgsLayoutItemScaleBar(self.pL)
        composerScaleBar.setStyle('Numeric')
        composerScaleBar.setAlignment( QgsScaleBarSettings.AlignRight)
        composerScaleBar.setLinkedMap(composerMap)
        composerScaleBar_Font = QFont("Arial")
        composerScaleBar_Font.setPointSize(11)
        composerScaleBar_Font.setItalic(True)
        composerScaleBar_Font.setBold(True)
        composerScaleBar.setFont(composerScaleBar_Font)
        composerScaleBar.setReferencePoint(QgsLayoutItem.LowerRight)
        composerScaleBar.setFixedSize(QgsLayoutSize(composerScaleBar.rectWithFrame().width(), 6))
        composerScaleBar.setPos(
                self.mapw + self.border_left - 0.15 - composerScaleBar.rectWithFrame().width(), 
                self.border_top + self.maph-0.15-6)
        composerScaleBar.setBackgroundEnabled(True)
        self.pL.addLayoutItem(composerScaleBar)


    def addSubHeader(self, subheader):
        if len(subheader) > 0:
            composerLabel_2 = QgsLayoutItemLabel(self.pL)
            composerLabel_2.setHAlign(Qt.AlignRight)
            composerLabel_2.setText(subheader)
            composerLabel_2.attemptSetSceneRect(QRectF(
                    2*self.border_left+self.mapw+self.border_right-210+0.15,
                    self.border_top+self.header_height,
                    210-self.border_right-self.border_left-0.3,
                    7))
            composerLabel_2.setHAlign(Qt.AlignHCenter)
            composerLabel_2_Font = QFont("Arial")
            composerLabel_2_Font.setPointSize(10)
            composerLabel_2_Font.setItalic(True)
            composerLabel_2.setFont(composerLabel_2_Font)
            composerLabel_2.setBackgroundEnabled(True)
            self.pL.addLayoutItem(composerLabel_2)
            self.header_height = self.header_height + 7


    def addHeader(self, header):
        if len(header) > 0:
            composerLabel_1 = QgsLayoutItemLabel(self.pL)
            composerLabel_1.setHAlign(Qt.AlignRight)
            composerLabel_1.setText(header)
            composerLabel_1.attemptSetSceneRect(QRectF(
                    2*self.border_left+self.mapw+self.border_right-210+0.15,
                    self.border_top+0.15,
                    210-self.border_right-self.border_left-0.3,
                    7))
            composerLabel_1.setHAlign(Qt.AlignHCenter)
            composerLabel_1_Font = QFont("Arial")
            composerLabel_1_Font.setPointSize(12)
            composerLabel_1_Font.setItalic(True)
            composerLabel_1_Font.setBold(True)
            composerLabel_1.setFont(composerLabel_1_Font)
            composerLabel_1.setBackgroundEnabled(True)
            self.header_height = 7
            self.pL.addLayoutItem(composerLabel_1)


    def addMap(self, extent, uscale):
        composerMap = QgsLayoutItemMap(self.pL)
        composerMap.setRect(QRectF(self.border_left, self.border_top, 
                                   self.mapw, self.maph))
        composerMap.setExtent(extent)
        composerMap.attemptSetSceneRect(QRectF(self.border_left, self.border_top, 
                                               self.mapw, self.maph))
        composerMap.setScale(float(uscale))
        composerMap.setFrameEnabled(True)
        self.pL.addLayoutItem(composerMap)
        return composerMap


    def createAndAddLayout(self):
        self.lM = QgsProject.instance().layoutManager()
        self.pL = QgsPrintLayout(QgsProject.instance())
        layoutName = self.lM.generateUniqueTitle(QgsMasterLayoutInterface.PrintLayout)
        self.pL.setName(layoutName)
        page = QgsLayoutItemPage(self.pL)
        page.setPageSize(QgsLayoutSize (float(self.size_a), float(self.size_b)))
        self.pL.pageCollection().addPage(page)
        self.lM.addLayout(self.pL)


    def setLegendSize(self):
        if self.dlg.groupBox_Legend.isChecked() and self.dlg.radioButton_legenduser.isChecked():
            self.size_legend = self.dlg.spinBox.value()
        else:
            self.size_legend = 0


    def setBorders(self):
        self.border_left = self.dlg.spinBox_Left.value()
        self.border_top = self.dlg.spinBox_Top.value()
        self.border_right = self.dlg.spinBox_Right.value()
        self.border_bottom = self.dlg.spinBox_Bottom.value()


    def setPageSize(self):
        try:
            self.size_a = float(self.dlg.lineEdit_2.text().strip())
            self.size_b = float(self.dlg.lineEdit_3.text().strip())
        except:
            self.size_a = 210.0
            self.size_b = 297.0

        if self.dlg.radioButton.isChecked():
            if self.size_a > self.size_b:
                sizetmp = self.size_a
                self.size_a = self.size_b
                self.size_b = sizetmp
        if self.dlg.radioButton_2.isChecked():
            if self.size_b > self.size_a:
                sizetmp = self.size_a
                self.size_a = self.size_b
                self.size_b = sizetmp


    # legend auto
    def addLegendAuto(self, composerMap):
        composerLegend = QgsLayoutItemLegend (self.pL)
        composerLegend.setLinkedMap(composerMap)
        composerLegend.setLegendFilterByMapEnabled(True)
        composerLegend.setTitle(u"Условные обозначения:")
        composerLegend.setResizeToContents(True)
        itemFont = QFont("Arial", 10)
        newFont = QFont("Arial", 11)
        composerLegend.setStyleFont(QgsLegendStyle.Title, newFont)
        composerLegend.setStyleFont(QgsLegendStyle.Group, newFont)
        composerLegend.setStyleFont(QgsLegendStyle.Subgroup, itemFont)
        composerLegend.setStyleFont(QgsLegendStyle.SymbolLabel, itemFont)
        composerLegend.setAutoUpdateModel(False)
        composerLegend.setSplitLayer(True)
        composerLegend.setReferencePoint(QgsLayoutItem.UpperRight)
        composerLegend.setPos(self.size_a, self.border_top)
        self.pL.addLayoutItem(composerLegend)


    def addFrame(self):
        ramka = QgsLayoutItemShape(self.pL)
        ramka.setShapeType(QgsLayoutItemShape.Rectangle) 
        ramka.attemptSetSceneRect(QRectF(self.border_left, self.border_top,
                                         self.mapw, self.maph))
        symbol_layer = QgsFillSymbol()
        symbol_layer.symbolLayers()[0].setBrushStyle(Qt.NoBrush)
        symbol_layer.symbolLayers()[0].setStrokeWidth(0.3)
        ramka.setSymbol(symbol_layer)
        ramka.setId("___РАМКА___")
        ramka.setLocked(True)
        self.pL.addLayoutItem(ramka)

    def populate_shablons(self, p):
        f = codecs.open(p,'r', encoding='cp1251')
        data = f.readlines()
        for line in data:
            line = line.strip()
            words = line.split(';')
            self.dlg.comboBox_3.addItem(words[0])
        f.close()


    def populate_form_user( self, p ):
        self.dlg.spinBox_scale.setValue(float(round(self.iface.mapCanvas().scale())))
        f = codecs.open(p,'r', encoding='cp1251')
        data = f.readlines()
        for line in data:
            line = line.strip()
            words = line.split(';')
            self.dlg.comboBox.addItem(words[0])
        f.close()


    def populate_listsizes(self):
        self.dlg.comboBox_2.clear()
        self.dlg.comboBox_2.addItem(u"A4 (210х297)")
        self.dlg.comboBox_2.addItem(u"A3 (297х420)")
        self.dlg.comboBox_2.addItem(u"A2 (420х594)")
        self.dlg.comboBox_2.addItem(u"A1 (594х841)")
        self.dlg.comboBox_2.addItem(u"A0 (841х1189)")
        self.dlg.comboBox_2.addItem(u"Other")
        self.dlg.comboBox_2.setCurrentIndex(0)
        

    def populate_form_user_sizes(self):
        cbindex = self.dlg.comboBox_2.currentIndex()
        self.dlg.lineEdit_2.setEnabled(False)
        self.dlg.lineEdit_3.setEnabled(False)
        if cbindex == 0:
            self.dlg.lineEdit_2.setText("297")
            self.dlg.lineEdit_3.setText("210")
        elif cbindex == 1:
            self.dlg.lineEdit_2.setText("420")
            self.dlg.lineEdit_3.setText("297")
        elif cbindex == 2:
            self.dlg.lineEdit_2.setText("594")
            self.dlg.lineEdit_3.setText("420")
        elif cbindex == 3:
            self.dlg.lineEdit_2.setText("841")
            self.dlg.lineEdit_3.setText("594")
        elif cbindex == 4:
            self.dlg.lineEdit_2.setText("1189")
            self.dlg.lineEdit_3.setText("841")
        elif cbindex == 5:
            self.dlg.lineEdit_2.setText("")
            self.dlg.lineEdit_3.setText("")
            self.dlg.lineEdit_2.setEnabled(True)
            self.dlg.lineEdit_3.setEnabled(True)


    def run(self):
        self.dlg.setWindowFlags(self.dlg.windowFlags() |
                                Qt.WindowStaysOnTopHint |
                                Qt.WindowMinMaxButtonsHint)

        path1 = os.path.join(self.plugin_dir, 'fragment_print.ini')
        path2 = os.path.join(self.plugin_dir, 'fragment_user.ini')

        self.dlg.comboBox_3.clear()
        self.dlg.comboBox.clear()
        self.populate_shablons(path1)
        self.populate_form_user(path2)
        self.radio_userPrint_clicked()

        self.dlg.show()

        self.dlg.groupBox_Legend.setCollapsed(True)
        self.dlg.groupBox_Headers.setCollapsed(True)
        self.dlg.adjustSize()

        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            if self.dlg.radio_shablonPrint.isChecked():
                self.import_composer(path1)
            elif self.dlg.radio_userPrint.isChecked():
                self.create_fragment(path2)


    def showEvent(event):
        self.dlg.adjustSize()