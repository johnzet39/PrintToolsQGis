# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
import psycopg2

import os.path


class NewUserLegend:

    def __init__(self, iface, layer_list, layout, border_left, border_top,
                 border_bottom, maph, mapw, curextent, size_legend, uscale,
                 layerHeaderState=False, legendName=''):
        """
        (список слоев, макет, левое поле,  верхн поле, нижнее поле,
        выс карты, шир карты, текущий эксцент, размер легенды, масштаб,
        название слоя - да нет,  Имя легенды (строка))
        """
        self.iface = iface
        self.layer_list = layer_list
        self.layout = layout
        self.border_left = border_left
        self.border_top = border_top
        self.border_bottom = border_bottom
        self.maph = maph
        self.mapw = mapw
        self.curextent = curextent
        self.size_legend = size_legend
        self.uscale = uscale
        self.layerHeaderState = layerHeaderState
        self.legendName = legendName

        global item_y
        global item_x
        global labelmaxwidth
        item_y = -6
        item_x = 0
        labelmaxwidth = 0


    def addUserLegend(self): 
        """
            add elements of user legend
        """

        # Header legend
        if len(self.legendName) > 0:
            self.addLegendName()
        # Add items of the legend
        for clayer in self.layer_list:
            legendElement = None
            if clayer.geometryType() == QgsWkbTypes.PointGeometry:
                print(1)
                legendElement = LegendElementPoint(
                    iface=self.iface, clayer=clayer, newcomp=self.layout,
                    border_left=self.border_left, border_top=self.border_top,
                    border_bottom=self.border_bottom, maph=self.maph,
                    mapw=self.mapw, curextent=self.curextent,
                    size_legend=self.size_legend, uscale=self.uscale,
                    layerHeaderState=self.layerHeaderState)
            if clayer.geometryType() == QgsWkbTypes.LineGeometry:
                print(2)
                legendElement = LegendElementLine(
                    iface=self.iface, clayer=clayer, newcomp=self.layout,
                    border_left=self.border_left, border_top=self.border_top,
                    border_bottom=self.border_bottom, maph=self.maph,
                    mapw=self.mapw, curextent=self.curextent,
                    size_legend=self.size_legend, uscale=self.uscale,
                    layerHeaderState=self.layerHeaderState)
            if clayer.geometryType() == QgsWkbTypes.PolygonGeometry:
                print(3)
                legendElement = LegendElementPolygon(
                    iface=self.iface, clayer=clayer, newcomp=self.layout,
                    border_left=self.border_left, border_top=self.border_top,
                    border_bottom=self.border_bottom, maph=self.maph,
                    mapw=self.mapw, curextent=self.curextent,
                    size_legend=self.size_legend, uscale=self.uscale,
                    layerHeaderState=self.layerHeaderState)

            if legendElement is not None:
                legendElement.createSymbol()


    def addLegendName(self):
        composerLabel_LegendHeader = QgsLayoutItemLabel(self.layout)
        composerLabel_LegendHeader.setPos(self.border_left,
                                          self.border_top+self.maph+4)
        composerLabel_LegendHeader_Font = QFont("Arial")
        composerLabel_LegendHeader_Font.setBold(True)
        composerLabel_LegendHeader_Font.setItalic(True)
        composerLabel_LegendHeader_Font.setPointSize(10)
        composerLabel_LegendHeader.setFont(composerLabel_LegendHeader_Font)
        composerLabel_LegendHeader.setText(self.legendName)
        composerLabel_LegendHeader.adjustSizeToText()
        self.layout.addLayoutItem(composerLabel_LegendHeader)


class LegendElement:
    """
        iface,clayer,newcomp,border_left,border_top,
        border_bottom,maph, mapw,curextent,size_legend,
        uscale,layerHeaderState,legendName):
    """

    def __init__(self, **kwargs):

        self.iface = kwargs.get("iface")
        self.clayer = kwargs.get("clayer")
        self.newcomp = kwargs.get("newcomp")
        self.border_left = kwargs.get("border_left")
        self.border_top = kwargs.get("border_top")
        self.border_bottom = kwargs.get("border_bottom")
        self.maph = kwargs.get("maph")
        self.mapw = kwargs.get("mapw")
        self.curextent = kwargs.get("curextent")
        self.size_legend = kwargs.get("size_legend")
        self.uscale = kwargs.get("uscale")
        self.layerHeaderState = kwargs.get("layerHeaderState")


    def createSymbol(self):
        self.selectSymbol()


    def selectSymbol(self):
        """# identify type of symbol and run calculation of symbols positions"""

        if self.clayer.renderer().type() == 'singleSymbol':
            self.calcSingleSymbol()
        elif self.clayer.renderer().type() == 'categorizedSymbol':
            self.calcCategorizedSymbol()
        elif self.clayer.renderer().type() == 'RuleRenderer':
            self.calcRuleSymbol()


    def calcSingleSymbol(self): #type = singleSymbol
        symindex = 0
        context = QgsRenderContext()
    
        for symbol in self.clayer.renderer().symbols(QgsRenderContext()):
            layerlabel = self.clayer.name()
            
            request = QgsFeatureRequest()
            request.setFilterRect(self.curextent)
            expclayer = self.clayer.getFeatures(request)
            isRecuest = None # попал в запрос?
            for feat in expclayer:
                isRecuest = True
                break
            if isRecuest:
                self.calcPositions(symbol, layerlabel)
            symindex += 1


    def calcCategorizedSymbol(self): #type = categorizedSymbol
        symindex = 0
        clayerHeaderShow = False
        context = QgsRenderContext()

        for symbol in self.clayer.renderer().symbols(QgsRenderContext()):
            if self.clayer.renderer().legendSymbolItemChecked(str(symindex)):
                layerlabel = self.clayer.renderer().categories()[symindex].label()
                
                cattrib = self.clayer.renderer().legendClassificationAttribute()
                cvalue = self.clayer.renderer().categories()[symindex].value()
                
                exp=QgsExpression('"'+cattrib+'"'+' = '+'\''+str(cvalue)+'\'')
                request_exp = QgsFeatureRequest(exp)
                request = QgsFeatureRequest()
                request.setFilterRect(self.curextent)
                expclayer = self.clayer.getFeatures(request)
                
                isRecuest = None # in query?
                for feat in expclayer:
                    if request_exp.acceptFeature(feat):
                        isRecuest = True
                        # Add layername Header (group)
                        if not clayerHeaderShow:
                            if self.layerHeaderState:
                                clayerHeaderShow = self.addLayerNameHeader()
                        break
                if isRecuest:
                    self.calcPositions(symbol, layerlabel)
                symindex += 1
            

    def calcRuleSymbol(self):  #type = RuleRenderer
        clayerHeaderShow = False
        context = QgsRenderContext()

        for child in (self.clayer.renderer().legendSymbolItems()):
            rulKey = child.ruleKey()
            rulChild = self.clayer.renderer().rootRule().findRuleByKey(rulKey)
            if (rulChild.isScaleOK(float(self.uscale)) and rulChild.active()):
                symbol = child.symbol()
                layerlabel = child.label()
                
                # проверяем, попадают ли в экстент объекты, отвечающие правилу
                ruleexp = rulChild.filterExpression() #правило
                exp = QgsExpression(ruleexp)
                request_exp = QgsFeatureRequest(exp)
                request = QgsFeatureRequest()
                request.setFilterRect(self.curextent)
                expclayer =  self.clayer.getFeatures(request)
                isRecuest= None # попал в запрос?
                for feat in expclayer:
                    if rulChild.isFilterOK(feat, QgsRenderContext()):
                        if request_exp.acceptFeature(feat):
                            isRecuest = True
                            # Add layername Header (group)
                            if not clayerHeaderShow:
                                if self.layerHeaderState:
                                    clayerHeaderShow = self.addLayerNameHeader()
                            break
                if isRecuest:
                    self.calcPositions(symbol, layerlabel)



    def calcPositions(self, symbol, layerlabel):
        """
        # calculate positions for legend symbol and label
        """
        global item_y
        global item_x
        global labelmaxwidth

        item_y += 5
        if ((self.border_top + self.maph + 8 + item_y) >
                (self.border_top + self.maph + self.size_legend - self.border_bottom)):
            item_y = 0
            item_x = item_x + 8 + labelmaxwidth
            labelmaxwidth = 0

        cshape_x = self.border_left+item_x
        cshape_y = self.border_top+self.maph+10+item_y
        composerLabel_layer_x = self.border_left+8+item_x
        composerLabel_layer_y = self.border_top+self.maph+10+item_y
        labelwidth = self.add_legend_item(self.newcomp, cshape_x, cshape_y,
                                          composerLabel_layer_x, composerLabel_layer_y,
                                          symbol, layerlabel, self.uscale)
        if labelwidth > labelmaxwidth:
            labelmaxwidth = labelwidth


    def add_legend_item(self, newcomp, cshape_x, cshape_y, composerLabel_layer_x,
                        composerLabel_layer_y, symbol, layerlabel, uscale):
        """# add legend symbol and label to layout"""
        raise NotImplementedError("Subclass must implement abstract method")


    def addLayerNameHeader(self):
        """# add layer header to layout"""

        global item_y
        global item_x
        global labelmaxwidth

        item_y += 5
        if ((self.border_top+self.maph+8+item_y) >
                (self.border_top + self.maph+self.size_legend - self.border_bottom)):
            item_y = 0
            item_x = item_x + 8 + labelmaxwidth
            labelmaxwidth = 0

        labelwidth = self.addLabelToLayout(self.newcomp, self.border_left+item_x,
                                           self.border_top+self.maph+10+item_y,
                                           self.clayer.name())
        if labelwidth > labelmaxwidth:
            labelmaxwidth = labelwidth
        clayerHeaderShow = True
        return clayerHeaderShow


    def addLabelToLayout(self, newcomp, Label_layer_x, Label_layer_y, layerlabel):
        composerLabel_layer = QgsLayoutItemLabel(newcomp)
        composerLabel_layer.setPos(Label_layer_x, Label_layer_y)
        composerLabel_layer_Font = QFont("Arial")
        composerLabel_layer_Font.setPointSize(10)
        composerLabel_layer.setFont(composerLabel_layer_Font)
        composerLabel_layer.setText(layerlabel.replace(u'•','').strip())
        composerLabel_layer.adjustSizeToText()
        newcomp.addLayoutItem(composerLabel_layer)
        labelwidth = composerLabel_layer.boundingRect().width()
        return labelwidth


class LegendElementPoint(LegendElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def add_legend_item(self, newcomp, cshape_x, cshape_y, Label_layer_x,
                        Label_layer_y, symbol, layerlabel, uscale):
        """# add legend symbol and label to layout"""

        cshape = QgsLayoutItemShape(newcomp)
        cshape.attemptSetSceneRect(QRectF(cshape_x, cshape_y, 7, 4))
        cshape.setShapeType(QgsLayoutItemShape.Rectangle)
        centroidFill = QgsCentroidFillSymbolLayer() # style
        fillSymbol = QgsFillSymbol()
        fillSymbol.changeSymbolLayer(0, centroidFill)
        sym = symbol.clone()
        fillSymbol.symbolLayer(0).setSubSymbol(sym) # set style to rectangle
        cshape.setSymbol(fillSymbol)

        newcomp.addLayoutItem(cshape)
        labelwidth = self.addLabelToLayout(newcomp, Label_layer_x,
                                           Label_layer_y, layerlabel)
        return labelwidth


class LegendElementLine(LegendElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def add_legend_item(self, newcomp, cshape_x, cshape_y, Label_layer_x,
                        Label_layer_y, symbol, layerlabel, uscale):
        """# add legend symbol and label to layout"""

        cline = QgsLayoutItemPolyline(QPolygonF([QPoint(0, 0), QPoint(6, 0)]),
                                                newcomp)
        cline.attemptSetSceneRect(QRectF(cshape_x, cshape_y+2, 7, 1))
        newSymbol = symbol.clone()
        cline.setSymbol(newSymbol)
        scale = uscale

        newcomp.addLayoutItem(cline)    
        labelwidth = self.addLabelToLayout(newcomp, Label_layer_x,
                                           Label_layer_y, layerlabel)
        return labelwidth


class LegendElementPolygon(LegendElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def add_legend_item(self, newcomp, cshape_x, cshape_y, Label_layer_x,
                        Label_layer_y, symbol, layerlabel, uscale):
        """# add legend symbol and label to layout"""

        cshape = QgsLayoutItemShape(newcomp)
        cshape.attemptSetSceneRect(QRectF(cshape_x, cshape_y, 7, 4))
        cshape.setShapeType(QgsLayoutItemShape.Rectangle)
        newSymbol = QgsFillSymbol()
        newSymbol = symbol.clone()
        cshape.setSymbol(newSymbol)

        newcomp.addLayoutItem(cshape)
        labelwidth = self.addLabelToLayout(newcomp, Label_layer_x,
                                           Label_layer_y, layerlabel)
        return labelwidth