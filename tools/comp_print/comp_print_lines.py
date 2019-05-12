from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant, Qt, QRectF, QSize
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import QDialogButtonBox, QColorDialog, QAction, QToolButton, QMenu, QMessageBox, QDialog
from PyQt5 import QtCore, QtGui
from qgis.core import *
import os.path

class CompLines:

    def __init__(self, iface, dlg):
        self.iface = iface
        self.dlg = dlg
        self.plugin_dir = os.path.dirname(__file__)

        self.smesh = self.dlg.spinBox_nalog.value()/2 * float(self.dlg.lineEdit.text()) / 1000
        self.length_line = 60 * float(self.dlg.lineEdit.text()) / 1000

        self.urilegend = os.path.join(self.plugin_dir, "lineLegend.qml")


    def getGroupLines(self):
        root = QgsProject.instance().layerTreeRoot()
        groupl = root.findGroup(u"_Компоновка - линии сводки")   
        if groupl == None:
            groupl = root.insertGroup(0, u"_Компоновка - линии сводки")
        return groupl


    def getFramesLayer(self):
        frameLayer = None
        layermap = QgsProject.instance().mapLayers()
        for name, layerold in layermap.items():
            if (layerold.type() == QgsMapLayer.VectorLayer and
                    layerold.name() == u"_Компоновка - границы листов"):
                frameLayer = layerold
                break
        return frameLayer


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


    def createSingleLineLayer(self, layername, group):
        groupl = group
        lineLayerName = layername

        LineLayer = None
        layermap = QgsProject.instance().mapLayers()
        for name, layerold in layermap.items():
            if (layerold.type() == QgsMapLayer.VectorLayer and
                    layerold.name() == lineLayerName):
                layerold.commitChanges()
                QgsProject.instance().removeMapLayer(layerold.id())
                break

        LineLayer = QgsVectorLayer("LineString", lineLayerName, "memory") 
        QgsProject.instance().addMapLayer(LineLayer, False)
        groupl.insertLayer(0, LineLayer)
        LineLayer.dataProvider().addAttributes(
            [QgsField("name", QVariant.String),
             QgsField("xpos", QVariant.Double),
             QgsField("ypos", QVariant.Double),
             QgsField("rpos", QVariant.Double)])
        LineLayer.updateFields()
        LineLayer.startEditing()
        self.iface.messageBar().clearWidgets()

        LineLayer.loadNamedStyle(self.urilegend)
        settings = LineLayer.labeling().clone().settings()
        frmt = settings.format()
        frmt.setSize(3*float(self.dlg.lineEdit.text()) / 1000)
        settings.setFormat(frmt)
        LineLayer.setLabeling(QgsVectorLayerSimpleLabeling(settings))

        return LineLayer


    def makeLines(self):
        """automatic creation connecting lines"""

        groupl = self.getGroupLines()
        frameLayer = self.getFramesLayer() # layer with frames
        if frameLayer is None:
            return

        if frameLayer.selectedFeatureCount() > 0:
            getfeat = frameLayer.selectedFeatures()
        else:
            getfeat = frameLayer.getFeatures()

        # создание или пересоздание линий стыковок
        # без надписей
        if not (self.dlg.checkBox_textLines.isChecked()):
            LineLayer = self.createSingleLineLayer(u"_Компоновка - линии сводки", groupl)

        for feat1 in getfeat:
            if self.dlg.checkBox_textLines.isChecked():
                uscale = feat1['frame_scale']
                
                if len(uscale) < 1:
                    uscale = self.dlg.lineEdit.text().strip()
                if not self.checkScaleText(uscale): return

                # создание или пересоздание слоя со стык.
                # линиями с надписями
                lineLayerName = u"_Компоновка - линии сводки - лист {0}".format(
                    str(feat1["frame_id"]))
                LineLayer = self.createSingleLineLayer(lineLayerName, groupl)

            if LineLayer is None:
                return

            fields = LineLayer.fields()
            angle = self.iface.mapCanvas().rotation() # угол канваса
            
            geom1 = QgsGeometry()
            geom1 = feat1.geometry()
            for feat2 in frameLayer.getFeatures():
                if feat2["frame_id"] != feat1["frame_id"]:
                    geom2 = QgsGeometry()
                    geom2 = feat2.geometry()
                    point1 = QgsGeometry()
                    point2 = QgsGeometry()
                    if geom1.intersects(geom2):
                        geom_inters = geom1.intersection(geom2)
                        center = geom_inters.centroid().asPoint()
                        # поворот полигона пересечения
                        geom_inters.rotate(angle, center)
                        geom_inters_box = geom_inters.boundingBox()
                        xmax = geom_inters_box.xMaximum()
                        xmin = geom_inters_box.xMinimum()
                        ymax = geom_inters_box.yMaximum()
                        ymin = geom_inters_box.yMinimum()

                        if (round(geom_inters_box.height(), 1) >
                                round(geom_inters_box.width(), 1)):#верт.прям.
                            
                            # задание длины линии на случай, 
                            # если линия не помещается в пересечение
                            if self.length_line > geom_inters_box.height() - self.smesh*3*2:
                                length = geom_inters_box.height() - self.smesh*3*2
                            else:
                                length = self.length_line

                            point1_x = (xmax + xmin)/2
                            point1_y = ymax - self.smesh*3
                            point2_x = (xmax + xmin)/2
                            point2_y = ymax - self.smesh*3 - length

                            newfeat = QgsFeature(fields)
                            # задание угла линии для правильной ориентации надписи
                            if geom1.centroid().asPoint().x()<geom2.centroid().asPoint().x():
                                newfeat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(point1_x, point1_y),
                                                                                QgsPointXY(point2_x+0.000000001, point2_y)]))
                            else:
                                newfeat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(point2_x-0.000000001, point2_y), 
                                                                                QgsPointXY(point1_x, point1_y)]))
                            newfeat.geometry().rotate(-angle, center)
                            if self.dlg.checkBox_textLines.isChecked():
                                newfeat['name'] = u'Линия сводки с Листом ' + str(feat2['frame_id'])
                            else:
                                newfeat['name'] = u''
                            LineLayer.dataProvider().addFeatures([newfeat])

                        elif round(geom_inters_box.height(),1) < round(geom_inters_box.width(), 1): #горизонтальный прямоугольник
                            if self.length_line > geom_inters_box.width() - self.smesh*3*2:
                                length = geom_inters_box.width() - self.smesh*3*2
                            else:
                                length = self.length_line

                            point1_x = xmin + self.smesh*3
                            point1_y = (ymax + ymin)/2

                            point2_x = xmin + self.smesh*3 + length
                            point2_y = (ymax + ymin)/2

                            newfeat = QgsFeature(fields)
                            if geom1.centroid().asPoint().y()<geom2.centroid().asPoint().y():
                                newfeat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(point1_x, point1_y), QgsPointXY(point2_x, point2_y)]))
                            else:
                                newfeat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(point2_x, point2_y), QgsPointXY(point1_x, point1_y)]))
                            newfeat.geometry().rotate(-angle, center)
                            if self.dlg.checkBox_textLines.isChecked():
                                newfeat['name'] = u'Линия сводки с Листом ' + str(feat2['frame_id'])
                            else:
                                newfeat['name'] = u''
                            LineLayer.dataProvider().addFeatures([newfeat])
                else:
                    continue

