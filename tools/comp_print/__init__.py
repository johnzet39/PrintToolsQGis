# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CompPrint
                                 A QGIS plugin
 Print composition consists of extent parts
                             -------------------
        begin                : 2015-11-09
        copyright            : (C) 2015 by Zlatanov Evgeniy
        email                : johnzet@yandex.ru
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CompPrint class from file CompPrint.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .comp_print import CompPrint
    return CompPrint(iface)
