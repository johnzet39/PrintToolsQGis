# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CompPrint
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
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5 import QtCore, QtGui
from qgis.core import *
from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import (QSettings, QTranslator, qVersion,
                          QCoreApplication, QVariant, Qt, QRectF, QSize)
from PyQt5.QtWidgets import (QDialogButtonBox, QColorDialog, QAction,
                             QToolButton, QMenu, QMessageBox, QDialog)

from .comp_print_frame import (CompFrame, CompFrameMoveRight,
                               CompFrameMoveLeft, CompFrameMoveUp, 
                               CompFrameMoveDown)
from .comp_print_dialog import CompPrintDialog
from .comp_print_lines import CompLines
import os.path
import codecs
import tempfile


class CompPrint:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        self.iface = iface

        self.pL = None
        self.lM = None
        self.layoutItemsList = []

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.path1 = os.path.join(self.plugin_dir, u'tools', 'stamps_list.ini')
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CompPrint_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        self.dlg = CompPrintDialog()
        
        self.dlg.pushButton_5.clicked.connect(self.showFrame)
        self.dlg.pushButton_4.clicked.connect(self.moveRight)
        self.dlg.pushButton_2.clicked.connect(self.moveLeft)
        self.dlg.pushButton.clicked.connect(self.moveUp)
        self.dlg.pushButton_3.clicked.connect(self.moveDown)
        self.dlg.pushButton_7.clicked.connect(self.makeComposer)
        self.dlg.pushButton_6.clicked.connect(self.createFeature)
        self.dlg.pushButton_8.clicked.connect(self.makeLines)
        self.dlg.pushButton_9.clicked.connect(self.resetAll)
        self.dlg.pushButton_edit.clicked.connect(self.editComposer)

        # Declare instance attributes
        self.actions = []
        # TODO: We are going to let the user set this up in a future iteration


    def createFeature(self):
        CompFrame(self.iface, self.dlg).createFrame()


    def moveRight(self):
        CompFrameMoveRight(self.iface, self.dlg).createFrame()


    def moveLeft(self):
        CompFrameMoveLeft(self.iface, self.dlg).createFrame()


    def moveUp(self):
        CompFrameMoveUp(self.iface, self.dlg).createFrame()


    def moveDown(self):
        CompFrameMoveDown(self.iface, self.dlg).createFrame()
    

    def alert(self, msg, title, buttons, icon=QMessageBox.Information):
        d = QMessageBox()
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                         QtCore.Qt.WindowMinMaxButtonsHint)
        d.setWindowTitle(title)
        d.setText(msg)
        for button in buttons:
            d.addButton(button)
        res = d.exec_()
        if res == QMessageBox.Yes:
            return True
        else:
            return False


    def resetAll(self):
        """ remove layers with frames and lines """

        result = self.alert(u"Удалить все слои, связанные с компоновками?",
                            u"Подтверждение",
                            [QMessageBox.Yes,
                            QMessageBox.No],
                            QMessageBox.Question)
        if result:
            layermap = QgsProject.instance().mapLayers()
            for name, layerold in layermap.items():
                if (layerold.type() == QgsMapLayer.VectorLayer and
                        layerold.name() == u"_Компоновка - границы листов"):
                    layerold.rollBack(True)
                    QgsProject.instance().removeMapLayer(layerold.id())
                elif (layerold.type() == QgsMapLayer.VectorLayer and
                        u"_Компоновка - линии сводки" in layerold.name()):
                    layerold.rollBack(True)
                    QgsProject.instance().removeMapLayer(layerold.id())

            root = QgsProject.instance().layerTreeRoot()
            groupl = root.findGroup(u"_Компоновка - линии сводки")   
            if groupl != None:
                root.removeChildNode(groupl)

            self.dlg.spinBox_nalog.setValue(8.0)


    def makeLines(self):
        compLines = CompLines(self.iface, self.dlg)
        compLines.makeLines()


    def countNameLay(self, name):
        """count layout with same names (without last numbers)"""

        count = 0
        for cView in QgsProject.instance().layoutManager().layouts():
            if ((cView.name() == name) or
                    (cView.name()[:-1].strip() == name) or
                    (cView.name()[:-2].strip() == name)):
                count += 1
        return count


    def addFrame(self, border_left, border_top,
                 mapw, maph,  pagenum=-1):
        ramka = QgsLayoutItemShape(self.pL)
        ramka.setShapeType(QgsLayoutItemShape.Rectangle) 
        ramka.attemptSetSceneRect(QRectF(border_left, border_top,
                                         mapw, maph))
        symbol_layer = QgsFillSymbol()
        symbol_layer.symbolLayers()[0].setBrushStyle(Qt.NoBrush)
        symbol_layer.symbolLayers()[0].setStrokeWidth(0.3)
        ramka.setSymbol(symbol_layer)
        ramka.setLocked(True)
        if not pagenum < 0:
            ramka.attemptMove(QgsLayoutPoint(ramka.pos()), page=pagenum-1)
        ramka.setId("___PAMKA___ лист "+str(pagenum))
        self.pL.addLayoutItem(ramka)
        return ramka


    def getStampProperties(self):
        f = codecs.open(self.path1, 'r', encoding='cp1251')
        data = f.readlines()
        line = data[self.dlg.comboBox_Stamps.currentIndex()].strip()
        words = line.split(';')
        f.close()
        # if stamp is selected in edited stamps,
        # than myFile - path to temporary file
        if self.dlg.comboBox_layoutStamp.currentIndex() > 0:
            cur_indexLS = self.dlg.comboBox_layoutStamp.currentIndex()
            layouts = self.lM.printLayouts()
            stamp_pL = layouts[cur_indexLS-1]
            context = QgsReadWriteContext()
            myDocument = QDomDocument()
            template_file = os.path.join(tempfile.gettempdir(), u"template.qpt")
            stamp_pL.saveAsTemplate(template_file, context)
            myFile = template_file
        else: #  else myFile - path from ini-file
            myFile = os.path.join(self.plugin_dir, words[1].strip())
        stampWidth = words[2]
        stampHeight = words[3]

        return myFile, stampWidth, stampHeight


    def getFramesList(self, templayer):
        fts = []
        if templayer.selectedFeatureCount() < 1:
            if self.dlg.radioButton_5.isChecked(): # многостран
                fts = templayer.getFeatures()
            elif self.dlg.radioButton_3.isChecked(): # постр
                last = QgsFeature()
                for f in templayer.getFeatures():
                    last = f
                fts = [last]
        elif templayer.selectedFeatureCount() > 0:
            fts = templayer.selectedFeatures()

        return fts


    def getPageSize(self, frame_size):
        if  frame_size == u"A4":
            size_a, size_b = 210, 297
        elif frame_size == u"A3":
            size_a, size_b = 297, 420
        elif frame_size ==  u"A2":
            size_a, size_b = 420, 594
        elif frame_size == u"A1":
            size_a, size_b = 594, 841
        elif frame_size == u"A0":
            size_a, size_b = 841, 1189
        return size_a, size_b


    def createPage(self, feature, cnt, myFile, stampWidth, stampHeight):
        """ createPage(FilePath_stamp, stampWidth, stampHeight,
            feature, page_index) """

        uscale = feature['frame_scale']   
        angle = feature['frame_rotation']           

        frame_size = feature['frame_size']
        size_a, size_b = self.getPageSize(frame_size)

        if feature['frame_orient'] == 'Landscape':
            if size_a < size_b:
                size_a, size_b = size_b, size_a
        else:
            if size_b < size_a:
                size_a, size_b = size_b, size_a

        page = QgsLayoutItemPage(self.pL)
        page.setPageSize(QgsLayoutSize (float(size_a), float(size_b)))
        self.pL.pageCollection().addPage(page)

        border_left = feature['border_left']
        border_top = feature['border_top']
        border_right = feature['border_right']
        border_bottom = feature['border_bottom']
            
        outGeom = QgsGeometry()
        outGeom = QgsGeometry(feature.geometry())
        center = outGeom.centroid().asPoint()
        
        self.iface.mapCanvas().refresh()
        self.iface.mapCanvas().setCenter(center)
        extent = self.iface.mapCanvas().extent()
        
        mapw = size_a - border_left - border_right
        maph = size_b - border_top - border_bottom

        composerMap = QgsLayoutItemMap(self.pL)
        composerMap.setRect(QRectF(border_left, border_top, mapw, maph))
        composerMap.setExtent(extent)
        composerMap.attemptSetSceneRect(QRectF(border_left, border_top, mapw, maph))
        composerMap.setScale(float(uscale))
        composerMap.setMapRotation(self.iface.mapCanvas().rotation())
        composerMap.setMapRotation(angle)
        composerMap.attemptMove(QgsLayoutPoint(composerMap.pos()), page=cnt-1)
        self.pL.addLayoutItem(composerMap)

        # read stamp from file 
        if self.dlg.groupBox_Stamps.isChecked():
            if not (self.dlg.check_onlyFirstPage.isChecked() and cnt > 1):
                myTemplateFile = open(myFile, 'rt', encoding="utf8")
                myTemplateContent = myTemplateFile.read()
                myTemplateFile.close()
                myDocument = QDomDocument()
                myDocument.setContent(myTemplateContent, False)

                context = QgsReadWriteContext()
                self.pL.loadFromTemplate(myDocument, context, clearExisting=False) 

                for item in self.pL.items():
                    if (item.type() == QgsLayoutItemRegistry.LayoutLabel or
                            item.type() == QgsLayoutItemRegistry.LayoutPicture or
                            item.type() == QgsLayoutItemRegistry.LayoutPolyline or
                            item.type() == QgsLayoutItemRegistry.LayoutScaleBar or
                            item.type() == QgsLayoutItemRegistry.LayoutShape):
                        if item not in self.layoutItemsList:
                            self.layoutItemsList.append(item)
                            xi = item.pos().x()
                            yi = item.pos().y()
                            item.attemptMove(QgsLayoutPoint(xi+size_a-float(stampWidth)-border_right,
                                                            yi+size_b-float(stampHeight)-border_bottom),
                                                            page=cnt-1)
                            if item.type() == QgsLayoutItemRegistry.LayoutScaleBar:
                                item.setLinkedMap(composerMap)
        else:
            # add scale
            composerScaleBar = QgsLayoutItemScaleBar(self.pL)
            composerScaleBar.setStyle('Numeric')
            composerScaleBar.setAlignment(QgsScaleBarSettings.AlignRight)
            composerScaleBar.setLinkedMap(composerMap)
            composerScaleBar_Font = QFont("Arial")
            composerScaleBar_Font.setPointSize(11)
            composerScaleBar_Font.setItalic(True)
            composerScaleBar_Font.setBold(True)
            composerScaleBar.setFont(composerScaleBar_Font)
            composerScaleBar.setFixedSize(QgsLayoutSize(composerScaleBar.rectWithFrame().width(), 6))
            composerScaleBar.setPos(mapw+border_left-0.15-composerScaleBar.rectWithFrame().width(),
                                    border_top+maph-0.15-6)
            composerScaleBar.setBackgroundEnabled(True)
            composerScaleBar.attemptMove(QgsLayoutPoint(composerScaleBar.pos()), page=cnt-1)
            self.pL.addLayoutItem(composerScaleBar)
        self.pL.moveItemToBottom(composerMap)

        if self.dlg.checkBox_Frame.isChecked() == False:
            composerMap.setFrameEnabled(True)
        else:
            # separate frame
            ramka = self.addFrame(border_left, border_top, mapw, maph, cnt)
            self.layoutItemsList.append(ramka)    


    def makeComposer(self):
        exist = False
        layermap = QgsProject.instance().mapLayers()
        for name, layerold in layermap.items():
            if (layerold.type() == QgsMapLayer.VectorLayer and
                    layerold.name() == u"_Компоновка - границы листов"):
                layerold.commitChanges()
                
                exist = True
                templayer = layerold
                cnt_frames = sum(1 for i in templayer.getFeatures())
                break
        if exist != True:
            self.iface.messageBar().pushMessage(u"Не выполнено",
                                                u"Создайте начальную рамку", 
                                                duration=5,
                                                level=1)
            return
        composerName = u"Компоновка многостраничная: [{0} лст]".format(str(cnt_frames))
        compCount = self.countNameLay(composerName)
        if compCount > 0:
            composerName = composerName + ' ' + str(compCount)

        self.lM = QgsProject.instance().layoutManager()
        self.pL = QgsPrintLayout(QgsProject.instance())
        self.pL.setName(composerName)
        self.lM.addLayout(self.pL)

        cnt = 0
        fts = self.getFramesList(templayer)

        # set stamp file path
        myFile = ''
        stampWidth = .0
        stampHeight = .0
        if self.dlg.groupBox_Stamps.isChecked():
            myFile, stampWidth, stampHeight = self.getStampProperties()

        for feature in fts:
            cnt = cnt + 1
            self.createPage(feature, cnt, myFile, stampWidth, stampHeight)

        self.hideFrame()
        self.pL.refresh()
        self.iface.openLayoutDesigner(self.pL)


    def editComposer(self):
        """edit (load) selected stamp"""

        composerName = u"ШТАМП {0}".format(self.dlg.comboBox_Stamps.currentText())
        compCount = self.countNameLay(composerName)
        if compCount > 0:
            composerName = composerName+' '+str(compCount)

        self.lM = QgsProject.instance().layoutManager()
        self.pL = QgsPrintLayout(QgsProject.instance())
        self.pL.setName(composerName)
        self.lM.addLayout(self.pL)

        # load stamp from ini file
        f = codecs.open(self.path1, 'r', encoding='cp1251')
        data = f.readlines()
        line = data[self.dlg.comboBox_Stamps.currentIndex()].strip()
        words = line.split(';')
        f.close()
        myFile = os.path.join(self.plugin_dir, words[1].strip())

        myTemplateFile = open(myFile, 'rt', encoding="utf8")
        myTemplateContent = myTemplateFile.read()
        myTemplateFile.close()
        myDocument = QDomDocument()
        myDocument.setContent(myTemplateContent, False)

        context = QgsReadWriteContext()
        self.pL.loadFromTemplate(myDocument, context, clearExisting=False) 
        self.pL.refresh()

        self.populate_layouts()

        index_composer = self.dlg.comboBox_layoutStamp.findText(composerName)
        self.dlg.comboBox_layoutStamp.setCurrentIndex(index_composer)
        self.iface.openLayoutDesigner(self.pL)


    def showFrame(self):
        root = QgsProject.instance().layerTreeRoot()
        layermap = QgsProject.instance().mapLayers()
        templayer = None
        for name, layerold in layermap.items():
            if (layerold.type() == QgsMapLayer.VectorLayer and
                    layerold.name() == u"_Компоновка - границы листов"):
                templayer = layerold
                if root.findLayer(templayer.id()).itemVisibilityChecked():
                    # self.hideFrame()
                    root.findLayer(templayer.id()).setItemVisibilityChecked(False)
                    break
                else:
                    root.findLayer(templayer.id()).setItemVisibilityChecked(True)
                    self.iface.mapCanvas().refresh()
                    break


    def hideFrame(self):
        layermap = QgsProject.instance().mapLayers()
        for name, layerold in layermap.items():
            if (layerold.type() == QgsMapLayer.VectorLayer and
                    layerold.name() == u"_Компоновка - границы листов"):
                templayer = layerold
                root = QgsProject.instance().layerTreeRoot()
                root.findLayer(templayer.id()).setItemVisibilityChecked(False)


    def populate_templates(self, p):
        self.dlg.comboBox_Stamps.clear()
        f = codecs.open(p, 'r', encoding='cp1251')
        data = f.readlines()
        for line in data:
            line = line.strip()
            words = line.split(';')
            self.dlg.comboBox_Stamps.addItem(words[0])
        f.close()


    def populate_layouts(self):
        wdgt=self.dlg.comboBox_layoutStamp
        wdgt.clear()
        wdgt.addItem('')

        lM = QgsProject.instance().layoutManager()
        for l in lM.printLayouts():
            wdgt.addItem(l.name())


    def run(self):
        self.populate_templates(self.path1)
        self.populate_layouts() # layouts with stamps
        self.showFrame()
        
        self.dlg.setWindowFlags(self.dlg.windowFlags() |
                                QtCore.Qt.WindowStaysOnTopHint |
                                QtCore.Qt.WindowMinMaxButtonsHint)
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass