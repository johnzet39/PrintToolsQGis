from PyQt5.QtCore import (QSettings, QTranslator, qVersion,
                          QCoreApplication, QObject, pyqtSignal, 
                          QVariant)
from PyQt5.QtGui import  QIcon
from PyQt5.QtWidgets import QAction, QToolButton, QMenu, QMessageBox
from qgis.core import QgsField, QgsVectorLayer

from .unique_field_dialog import UniqueFieldDialog


class FilterLayer:

    def __init__(self, iface):
        self.iface = iface
        self.dlg_unique = UniqueFieldDialog()


    def filtershow(self, mlayer = None):

        if mlayer is None:
            mlayer = self.iface.activeLayer()

        if mlayer != None:
            fcount = mlayer.selectedFeatureCount()

            filterstr = ''
            if  fcount == 0:
                filterstr = ''  #метка
            else:
                if mlayer.providerType() == u'memory':
                    first = True
                    gidstr = ''
                    for feat in mlayer.selectedFeatures():
                        gidstr += (', \'' if not first else '\'') + str(feat.id()) +'\''
                        first = False
                    filterstr = '$id in ('+ gidstr +')'
                else:
                    mfields = mlayer.fields()
                    fname = None
                    for mfield in mfields:
                        if mfield.name().lower() == u'gid':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'id':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'keyid':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'object_id':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'kad_no':
                            fname = mfield.name()
                            break

                    if fname is None:
                        # print('There is no unique field')
                        self.dlg_unique.mFieldComboBox.setLayer(mlayer)
                        self.dlg_unique.show()
                        result = self.dlg_unique.exec_()
                        if result:
                            if len(self.dlg_unique.mFieldComboBox.currentField()) > 0:
                                fname = self.dlg_unique.mFieldComboBox.currentField()

                    if fname is not None:
                        first = True
                        gidstr = ''
                        for feat in mlayer.selectedFeatures():
                            gidstr += (', \'' if not first else '\'') + str(feat[fname]) +'\''
                            first = False
                        filterstr = fname+' in ('+ gidstr +')'
                    else:
                        self.iface.messageBar().pushMessage(
                                u"Не выполнено",
                                u"Отсутствуют заданные ключевые поля в атрибутах слоя",
                                duration=5,
                                level=2)
                        return

            mlayer.setSubsetString(filterstr)  #метка
            self.iface.mainWindow().statusBar().showMessage(u'Фильтр: '+filterstr)

        else:
            pass

    def filterhide(self):
        mlayer = self.iface.activeLayer()
        
        if  (mlayer != None) and (mlayer.isEditable()):
            self.iface.messageBar().pushMessage(
                    u"Не выполнено",
                    u"Отключите режим редактирования активного слоя",
                    duration=5,
                    level=2)
            return
        
        if mlayer != None:
            fcount = mlayer.selectedFeatureCount()

            filterstr = ''
            if  fcount == 0:
                return
            else:
                if mlayer.providerType() == u'memory':
                    if len((mlayer.subsetString()).strip()) == 0:
                        gidnum = 0
                        gidstr = ''
                        for feat in mlayer.selectedFeatures():
                            gidnum += 1
                            if gidnum > 1:
                                gidstr = gidstr + ', \''+ str(feat.id())+'\''
                            else:
                                gidstr = '\''+str(feat.id())+'\''
                        filterstr = '$id not in ('+ gidstr +')'
                    else:
                        lenfname = len(u'$id')
                        filterstr = mlayer.subsetString().strip()
                        if filterstr[lenfname:lenfname+7].strip() == u'not in':
                            fname = filterstr.split(' ')[0]
                            filterstr = filterstr[:-1]
                            for feat in mlayer.selectedFeatures():
                                filterstr = filterstr + ', \'' + str(feat.id())+'\''
                            filterstr = filterstr + ')'
                        elif filterstr[lenfname:lenfname+3].strip() == u'in':
                            mlayer.invertSelection()
                            self.filtershow()
                            return
                else:
                    mfields = mlayer.fields()
                    fname = None
                    for mfield in mfields:
                        if mfield.name().lower() == u'gid':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'id':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'keyid':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'object_id':
                            fname = mfield.name()
                            break
                        elif mfield.name().lower() == u'kad_no':
                            fname = mfield.name()
                            break

                    if fname is not None:
                        if len((mlayer.subsetString()).strip()) == 0: #если фильтр слоя пустой
                            gidnum = 0
                            gidstr = ''
                            for feat in mlayer.selectedFeatures():
                                gidnum += 1
                                if gidnum > 1:
                                    gidstr = gidstr + ', \''+ str(feat[fname])+'\''
                                else:
                                    gidstr = '\'' + str(feat[fname]) + '\''
                            filterstr = fname+' not in ('+ gidstr +')'
                        else:
                            lenfname = len(fname)
                            filterstr = mlayer.subsetString().strip()
                            if filterstr[lenfname:lenfname+7].strip() == u'not in':
                                fname = filterstr.split(' ')[0]
                                filterstr = filterstr[:-1]
                                for feat in mlayer.selectedFeatures():
                                    filterstr = filterstr + ', \''+str(feat[fname])+'\''
                                filterstr = filterstr + ')'
                            elif filterstr[lenfname:lenfname+3].strip() == u'in':
                                mlayer.invertSelection()
                                self.filtershow()
                                return

                    else:
                        self.iface.messageBar().pushMessage(
                                u"Не выполнено", 
                                u"Отсутствуют заданные ключевые поля в атрибутах слоя", 
                                duration=5, 
                                level=2)
            mlayer.setSubsetString(filterstr)  #метка
            self.iface.mainWindow().statusBar().showMessage(u'Фильтр: '+filterstr)
        else:
            pass