from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant, Qt, QRectF, QSize
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import QDialogButtonBox, QColorDialog, QAction, QToolButton, QMenu, QMessageBox, QDialog
from PyQt5 import QtCore, QtGui
from qgis.core import *
import os.path

class CompFrame:

    def __init__(self, iface, dlg):
        self.iface = iface
        self.dlg = dlg
        self.plugin_dir = os.path.dirname(__file__)


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


    def findOrCreateLayer(self):
        layermap = QgsProject.instance().mapLayers()
        for name, layerold in layermap.items():
            if (layerold.type() == QgsMapLayer.VectorLayer and
                    layerold.name() == u"_Компоновка - границы листов"):
                if self.alert(u"Сбросить существующий слой с рамками компоновок?",
                              u"Подтверждение",
                              [QMessageBox.Yes, QMessageBox.No],
                              QMessageBox.Question):
                    layerold.rollBack(True)
                    QgsProject.instance().removeMapLayer(layerold.id())
                else:
                    return None
        templayer = QgsVectorLayer("Polygon",
                                   u"_Компоновка - границы листов",
                                   "memory")
        QgsProject.instance().addMapLayer(templayer, False)
        root = QgsProject.instance().layerTreeRoot()
        root.insertLayer(0, templayer)
        templayer.startEditing()
        templayer.dataProvider().addAttributes(
            [QgsField("frame_id", QVariant.Int),
             QgsField("frame_size", QVariant.String),
             QgsField("frame_orient", QVariant.String), 
             QgsField("frame_scale", QVariant.Double),
             QgsField("frame_rotation", QVariant.Double),
             QgsField("border_left", QVariant.Double),
             QgsField("border_top", QVariant.Double),
             QgsField("border_right", QVariant.Double),
             QgsField("border_bottom", QVariant.Double)])
        templayer.commitChanges()
        templayer.startEditing()
        # стили
        urilegend = os.path.join(self.plugin_dir, "frameLegend.qml")
        templayer.loadNamedStyle(urilegend)
        symbol_layer = QgsSimpleFillSymbolLayer()
        symbol_layer.setStrokeColor(QColor('#000000'))
        symbol_layer.setStrokeWidth(0.7)
        symbol_layer.setStrokeStyle(2)
        symbol_layer.setBrushStyle(0)
        templayer.renderer().symbols(QgsRenderContext())[0].changeSymbolLayer(0, symbol_layer)
        templayer.setOpacity(.4)
        self.iface.layerTreeView().refreshLayerSymbology(templayer.id())
        self.iface.messageBar().clearWidgets()

        return templayer

    # recreate frame
    def createFrame(self):
        #check scale
        uscale = self.dlg.lineEdit.text().strip()
        angle = self.iface.mapCanvas().rotation() # angle canvas
        if not self.checkScaleText(uscale): return

        # find or create layer with frames
        templayer = self.findOrCreateLayer()
        if templayer == None:
            return

        # get number of features in frameLayer
        num = self.getNumFeatures(templayer)
        x1, x2, y1, y2, center = self.getXY(templayer)

        feat = QgsFeature(templayer.fields())
        feat['frame_id'] = num
        feat['frame_size'] = self.listSize(self.dlg.horizontalSlider.value())
        feat['frame_orient'] = self.listOrientation()
        feat['frame_scale'] = uscale
        feat['frame_rotation'] = angle
        feat['border_left'] = self.dlg.spinBox_Left.value()
        feat['border_top'] = self.dlg.spinBox_Top.value()
        feat['border_right'] = self.dlg.spinBox_Right.value()
        feat['border_bottom'] = self.dlg.spinBox_Bottom.value()

        poly_geometry = QgsGeometry.fromPolygonXY([[QgsPointXY(x1,y1),
                                                    QgsPointXY(x2,y1),
                                                    QgsPointXY(x2,y2),
                                                    QgsPointXY(x1,y2)]])
        poly_geometry.rotate(-angle, center)   # rotate frame
        feat.setGeometry(poly_geometry)
        templayer.dataProvider().addFeatures([feat])
        templayer.triggerRepaint()
        templayer.updateExtents()
        self.iface.setActiveLayer(templayer)
        self.iface.mapCanvas().setCenter(poly_geometry.boundingBox().center())
        self.iface.mapCanvas().refresh()


    def checkScaleText(self, uscale):
        try:
            float(uscale)
            return True
        except:
            self.alert(u"Введите целое число в поле со значением величины Mасштаба",
                       u"Внимание",
                       [QMessageBox.Ok],
                       QMessageBox.Information)
            self.dlg.lineEdit.selectAll()
            self.dlg.lineEdit.setFocus()
            return False

    def getNumFeatures(self, templayer):
        return 1


    def getXY(self, templayer):
        extent = self.iface.mapCanvas().extent()
        center = extent.center()
        vsize, hsize = self.calculateSize(center)
        x1 = center.x() - hsize/2
        x2 = center.x() + hsize/2
        y1 = center.y() - vsize/2
        y2 = center.y() + vsize/2
        return x1,x2,y1,y2,center


    def calculateSize(self, center):
        if self.dlg.radioButton.isChecked():
            border_left = self.dlg.spinBox_Left.value()
            border_top = self.dlg.spinBox_Top.value()
            border_right = self.dlg.spinBox_Right.value()
            border_bottom = self.dlg.spinBox_Bottom.value()
        if self.dlg.radioButton_2.isChecked():
            border_left = self.dlg.spinBox_Top.value()
            border_top = self.dlg.spinBox_Right.value()
            border_right = self.dlg.spinBox_Bottom.value()
            border_bottom = self.dlg.spinBox_Left.value()
        vlength_orig = 210
        hlength_orig = 297

        sliderValue = self.dlg.horizontalSlider.value()
        if sliderValue == 0: # A4
            vlength = vlength_orig - border_top - border_bottom
            hlength = hlength_orig - border_left - border_right
        elif sliderValue == 1: # A3
            vlength = hlength_orig - border_top - border_bottom
            hlength = vlength_orig*2-border_left-border_right
        elif sliderValue == 2: # A2
            vlength = vlength_orig*2 - border_top - border_bottom
            hlength = hlength_orig*2 - border_left-border_right
        elif sliderValue == 3: # A1
            vlength = hlength_orig*2 - border_top - border_bottom
            hlength = vlength_orig*4 - border_left-border_right
        elif sliderValue == 4: # A0
            vlength = vlength_orig*4 - border_top - border_bottom
            hlength = hlength_orig*4 - border_left-border_right

        # orientation
        if self.dlg.radioButton_2.isChecked():
            lengthtmp = vlength
            vlength = hlength
            hlength = lengthtmp
        vsize = (vlength)* float(self.dlg.lineEdit.text()) / 1000
        hsize = (hlength)* float(self.dlg.lineEdit.text()) / 1000
        return vsize, hsize


    def listOrientation(self):
        if self.dlg.radioButton.isChecked():
            return('Landscape')
        if self.dlg.radioButton_2.isChecked():
            return('Portrait')


    def listSize(self, slidervalue):
        """# listsize text to attribute table"""
        if slidervalue == 0: # A4
            frameSize = u"A4"
        elif slidervalue == 1: # A3
            frameSize = u"A3"
        elif slidervalue == 2: # A2
            frameSize = u"A2"
        elif slidervalue == 3: # A1
            frameSize = u"A1"
        elif slidervalue == 4: # A0
            frameSize = u"A0"
        return frameSize


class CompFrameMove(CompFrame):
    """Abstract class"""

    def __init__(self, iface, dlg):
        super().__init__(iface, dlg)

    def findOrCreateLayer(self):
        exist = False
        layermap = QgsProject.instance().mapLayers()
        for name, layerold in layermap.items():
            if (layerold.type() == QgsMapLayer.VectorLayer and
                    layerold.name() == u"_Компоновка - границы листов" and
                    layerold.providerType() == u"memory"):
                exist = True
                templayer = layerold
                return templayer
        self.iface.messageBar().pushMessage(u"Не выполнено",
                                            u"Создайте начальную рамку",
                                            duration=5,
                                            level=1)
        return None


    def getNumFeatures(self, templayer):
        num = 1
        for fnum in templayer.getFeatures():
            num = num + 1
        return num


    def getXY(self, templayer):
        raise NotImplementedError("Subclass must implement abstract method")


    def getCenterOutGeom(self, layer):
        last = QgsFeature()
        for f in layer.getFeatures():
            last = f
        if last != None:
            outGeom = QgsGeometry()
            outGeom = QgsGeometry(last.geometry())
            center = outGeom.centroid().asPoint()
            return center, outGeom


class CompFrameMoveRight(CompFrameMove):

    def __init__(self, iface, dlg):
        super().__init__(iface, dlg)


    def getXY(self, templayer):
        outGeom = QgsGeometry()
        center, outGeom = self.getCenterOutGeom(templayer)
        vsize, hsize = self.calculateSize(center)
        angle = self.iface.mapCanvas().rotation()
        outGeom.rotate(angle, center)

        v2size = outGeom.boundingBox().height() # sizes previous frame
        h2size = outGeom.boundingBox().width() # sizes previous frame
        
        naloj = self.dlg.spinBox_nalog.value() * float(self.dlg.lineEdit.text()) / 1000
        x1 = (center.x() + h2size/2 - naloj)
        x2 = (center.x() + h2size/2 - naloj + hsize)
        y1 = center.y() - vsize/2
        y2 = center.y() + vsize/2
        return x1, x2, y1, y2, center


class CompFrameMoveLeft(CompFrameMove):

    def __init__(self, iface, dlg):
        super().__init__(iface, dlg)


    def getXY(self, templayer):
        outGeom = QgsGeometry()
        center, outGeom = self.getCenterOutGeom(templayer)
        vsize, hsize = self.calculateSize(center)
        angle = self.iface.mapCanvas().rotation()
        outGeom.rotate(angle, center)

        v2size = outGeom.boundingBox().height() # sizes previous frame
        h2size = outGeom.boundingBox().width() # sizes previous frame

        naloj = self.dlg.spinBox_nalog.value() * float(self.dlg.lineEdit.text()) / 1000
        x1 = (center.x() - h2size/2 + naloj - hsize/2 - hsize/2)
        x2 = (center.x() - h2size/2 + naloj - hsize/2 + hsize/2)
        y1 = center.y() - vsize/2
        y2 = center.y() + vsize/2
        return x1, x2, y1, y2, center

class CompFrameMoveUp(CompFrameMove):
    def __init__(self, iface, dlg):
        super().__init__(iface, dlg)

    def getXY(self, templayer):
        outGeom = QgsGeometry()
        center, outGeom = self.getCenterOutGeom(templayer)
        vsize, hsize = self.calculateSize(center)
        angle = self.iface.mapCanvas().rotation()
        outGeom.rotate(angle, center) 

        v2size = outGeom.boundingBox().height()# sizes previous frame
        h2size = outGeom.boundingBox().width()# sizes previous frame

        naloj = self.dlg.spinBox_nalog.value() * float(self.dlg.lineEdit.text()) / 1000
        x1 = (center.x() - hsize/2 )
        x2 = (center.x() + hsize/2)
        y1 = center.y() + v2size/2 - naloj
        y2 = center.y() + v2size/2 - naloj + vsize
        return x1, x2, y1, y2, center


class CompFrameMoveDown(CompFrameMove):

    def __init__(self, iface, dlg):
        super().__init__(iface, dlg)


    def getXY(self, templayer):
        outGeom = QgsGeometry()
        center, outGeom = self.getCenterOutGeom(templayer)
        vsize, hsize = self.calculateSize(center)
        angle = self.iface.mapCanvas().rotation()
        outGeom.rotate(angle, center) 

        v2size = outGeom.boundingBox().height() # sizes previous frame
        h2size = outGeom.boundingBox().width() # sizes previous frame
        
        naloj = self.dlg.spinBox_nalog.value() * float(self.dlg.lineEdit.text()) / 1000
        x1 = (center.x() - hsize/2 )
        x2 = (center.x() + hsize/2)
        y1 = center.y() - v2size/2 + naloj - vsize 
        y2 = center.y() - v2size/2 + naloj
        return x1, x2, y1, y2, center

