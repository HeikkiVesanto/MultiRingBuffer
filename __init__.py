# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FeatureBuffer
                                 A QGIS plugin
 A simple plugin to buffer selected features
                             -------------------
        begin                : 2014-10-23
        copyright            : (C) 2014 by thinkWhere
        email                : matthew.walsh@thinkwhere.com
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
    """Load FeatureBuffer class from file FeatureBuffer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .feature_buffer import FeatureBuffer
    return FeatureBuffer(iface)
