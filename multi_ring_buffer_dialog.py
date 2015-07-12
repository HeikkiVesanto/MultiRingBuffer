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

import os

from PyQt4 import QtGui, uic
from multi_ring_buffer_dialog_base import Ui_Dialog


class MultiRingBufferDialog(QtGui.QDialog):
    def __init__(self):
        """Constructor."""
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.accepted.connect(self.accept)

    def populatedialogue(self, layername):
        self.ui.buffer_layer_name.clear()
        self.ui.buffer_layer_name.setText(layername)

    def selectedfeats(self, yes):
        if yes == 1:
            self.ui.selectedfeats.setEnabled(1)
            self.ui.selectedfeats.setCheckable(1)
            self.ui.selectedfeats.setChecked(1)
            self.ui.selectedfeats.setToolTip("Use only selected features?")
        else:
            self.ui.selectedfeats.setChecked(0)
            self.ui.selectedfeats.setCheckable(0)
            self.ui.selectedfeats.setToolTip("No features selected")
            self.ui.selectedfeats.setEnabled(0)
