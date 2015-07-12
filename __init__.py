# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MultiRingBuffer
                                 A QGIS plugin
 A simple plugin to buffer selected features
                              -------------------
        begin                : 2014-10-23
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Heikki Vesanto
        email                : heikki.vesanto@thinkwhere.com
        thanks               : Matthew Walsh and Neil Benny
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MultiRingBuffer class from file MultiRingBuffer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .multi_ring_buffer import MultiRingBuffer
    return MultiRingBuffer(iface)
