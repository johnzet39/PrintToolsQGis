# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrintFragment
                                 A QGIS plugin
 Print Fragment
                             -------------------
        begin                : 2015-08-06
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
    """Load PrintFragment class from file PrintFragment.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .print_tools import PrintTools
    return PrintTools(iface)
