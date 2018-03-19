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

from PyQt5 import uic
from PyQt5 import QtWidgets

from qgis.core import QgsMapLayerProxyModel

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'multi_ring_buffer_dialog_base.ui'))


class MultiRingBufferDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MultiRingBufferDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.HasGeometry)
        self.radioDistances.toggled.connect(self.commaSelected)
        self.radioRings.toggled.connect(self.ringSelected)
        self.radioNoDonut.toggled.connect(self.regBufferSelected)
        self.radioDonut.toggled.connect(self.donutSelected)
        self.sequential_style.toggled.connect(self.seqSelected)
        self.central_style.toggled.connect(self.centSelected)

        self.mMapLayerComboBox.layerChanged.connect(self.isSomethingSelected)

    def seqSelected(self):
        self.radioNoDonut.setEnabled(0)

    def centSelected(self):
        self.radioNoDonut.setEnabled(1)

    def commaSelected(self):
        self.distancesCommaSep.setEnabled(1)
        self.bufferDistance.setEnabled(0)
        self.numberOfRings.setEnabled(0)
        self.sequential_style.setChecked(0)
        self.central_style.setChecked(1)
        self.sequential_style.setEnabled(0)

    def ringSelected(self):
        self.bufferDistance.setEnabled(1)
        self.numberOfRings.setEnabled(1)
        self.distancesCommaSep.setEnabled(0)
        self.sequential_style.setEnabled(1)

    def regBufferSelected(self):
        self.sequential_style.setChecked(0)
        self.central_style.setChecked(1)
        self.sequential_style.setEnabled(0)

    def donutSelected(self):
        self.sequential_style.setEnabled(1)

    def isSomethingSelected(self):
        vlayer = self.mMapLayerComboBox.currentLayer()
        if vlayer is not None:
            if not vlayer.selectedFeatures():
                self.selectedfeats.setChecked(0)
                self.selectedfeats.setEnabled(0)
                self.selectedfeats.setToolTip("No features selected in layer")
            else:
                self.selectedfeats.setEnabled(1)
                self.selectedfeats.setToolTip("Use only selected features")
                # self.selectedfeats.setChecked(1)
        else:
            pass
