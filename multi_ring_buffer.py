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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox, QProgressBar
from qgis.core import *
# Initialize Qt resources from file resources.py
import icon_rc
import resources_rc
# Import the code for the dialog
from multi_ring_buffer_dialog import MultiRingBufferDialog
from PyQt4.QtCore import *
import os.path
import time

class MultiRingBuffer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MultiRingBuffer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = MultiRingBufferDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Multi Ring Buffer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MultiRingBuffer')
        self.toolbar.setObjectName(u'MultiRingBuffer')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MultiRingBuffer', message)


    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True, status_tip=None, whats_this=None, parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Multi_Ring_Buffer/icon.svg'
        self.add_action(icon_path, text=self.tr(u'Multi Ring Buffer'), callback=self.run, parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(self.tr(u'&Multi Ring Buffer'), action)
            self.iface.removeToolBarIcon(action)

    def dissolve(self, input_feats):
        # Function to dissolve input features to allow for buffering of multiple features
        feats = []
        # Create and empty list of features and add all features to it.
        # We use feature 0 later and this ensures it exits.
        for each_feat in input_feats:
            feats.append(each_feat)
        # Do not run if geometry is empty, produce an error instead.
        if len(feats) > 0:
            # Need to create empty geometry to hold the dissolved features, we use the first feature to seed it.
            # Combine require a non-empty geometry to work (I could not get it to work).
            feat = feats[0]
            dissolved_geom = QgsGeometry()
            dissolved_geom = feat.geometry()
            # Progress bar for dissolving
            progressMessageBar = self.iface.messageBar().createMessage("Dissolving...")
            progress = QProgressBar()
            progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            progressMessageBar.layout().addWidget(progress)
            self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
            maximum_progress = len(feats)
            progress.setMaximum(maximum_progress)
            i = 0
            # Run through the features and dissolve them all.
            for each_feat in feats:
                geom = each_feat.geometry()
                dissolved_geom = geom.combine(dissolved_geom)
                i = i + 1
                progress.setValue(i + 1)
            return_f = QgsFeature()
            return_f.setGeometry(dissolved_geom)
            self.iface.messageBar().clearWidgets()
            return return_f
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                "No features to dissolve.", QMessageBox.Ok)
            return input_feats

    def run(self):
        # Plugin uses selected layer, hope to add layer selection later.
        active_vl = self.iface.activeLayer()
        # We check for selected features to auto-populate the "use selected feature" box in the dialog.
        sel_feats = ''
        if active_vl is not None:
            sel_feats = active_vl.selectedFeatures()
        result = 0
        """Run method that performs all the real work"""
        # Logic if to run the dialog
        if active_vl is None:
            sel_feats = ''
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                "No layer selected.", QMessageBox.Ok)
            result = 0
        elif active_vl.type() == QgsMapLayer.RasterLayer:
            sel_feats = ''
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                "Raster layer selected.", QMessageBox.Ok)
            result = 0
        elif active_vl.type() == QgsMapLayer.PluginLayer:
            sel_feats = ''
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                "Plugin layer selected, please save as a regular layer and try again.", QMessageBox.Ok)
            result = 0
        elif active_vl is not None:
            self.dlg.populatedialogue(active_vl.name())
            if len(sel_feats) == 0:
                # If selected layer has selected features populate the box.
                # If not make it impossible to populate the box.
                self.dlg.selectedfeats(0)
            else:
                self.dlg.selectedfeats(1)
            self.dlg.show()
            result = self.dlg.exec_()
        else:
            sel_feats = ''
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                "Could not process layer.", QMessageBox.Ok)
            result = 0

        # If ok was clicked in the dialog, continue:
        if result == 1:

            buffer_crs_object = self.iface.activeLayer().crs()
            # Check the current CRS of the layer
            buffer_crs = buffer_crs_object.authid()
            # Apply that to the created layer if recognised
            buffer_input_crs = "Polygon?crs=%s" % buffer_crs
            # Create empty memory vector layer for buffers
            layer_name = active_vl.name()
            vl = QgsVectorLayer(buffer_input_crs, "%s_MultiRingBuffer" % layer_name, "memory")
            vl_pr = vl.dataProvider()
            # Distance feature for buffer distance
            vl_pr.addAttributes([QgsField("distance", QVariant.String)])
            vl.updateFields()
            # Switch between sequential and central buffer styles.
            # A toggle was added, but it seems too complex of a question for most users.
            buffer_style = "sequential"
            #if self.dlg.ui.central.isChecked():
            #    buffer_style = "central"
            #else:
            #    buffer_style = "sequential"

            # Inputs from the dialog:
            dissolve_test = self.dlg.ui.dissovle_button_2.isChecked()
            if dissolve_test == 0:
                dissolve_bool = 0
            else:
                dissolve_bool = 1
            segments_to_approximate = self.dlg.ui.segmentsToApproximate.value()
            num_of_rings = self.dlg.ui.numberOfRings.value()
            buffer_distance = self.dlg.ui.bufferDistance.value()
            use_sel_feats_test = self.dlg.ui.selectedfeats.isChecked()
            if use_sel_feats_test == 0:
                use_sel_feats = 0
            else:
                use_sel_feats = 1

            # We use "sel_feats" to populate a box in the dialog, but if all features wanted, we need to re-populate it
            # with all the features in the layer.
            if use_sel_feats == 0:
                iterate = active_vl.getFeatures()
                sel_feats = []
                for feature in iterate:
                    sel_feats.append(feature)

            # Dissolve the features if selected.
            if dissolve_bool == 1:
                sel2feats = []
                add_feat = self.dissolve(sel_feats)
                # Our buffer loops require a list (as sel_feats originally is), so we append the features to a list.
                sel2feats.append(add_feat)
            else:
                sel2feats = sel_feats

            # Progress bar.
            progressMessageBar = self.iface.messageBar().createMessage("Buffering...")
            progress = QProgressBar()
            progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            progressMessageBar.layout().addWidget(progress)
            self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
            maximum_progress = len(sel2feats) * num_of_rings
            progress.setMaximum(maximum_progress)
            i = 0

            # Run if there are features in the layer
            if len(sel_feats) > 0:
                # Buffer a feature then buffer the buffer (used)
                if buffer_style == "sequential":
                    new_buff_feats = []
                    distance = buffer_distance
                    while num_of_rings > 0:
                        to_buffer = []
                        for each_feat in sel2feats:
                            geom = each_feat.geometry()
                            buff = geom.buffer(buffer_distance, segments_to_approximate)
                            new_f = QgsFeature()
                            new_f.setGeometry(buff)
                            to_buffer.append(new_f)

                            new_f_geom = new_f.geometry()
                            new_f_clipped = new_f_geom.difference(geom)
                            new_f2 = QgsFeature()
                            new_f2.setGeometry(new_f_clipped)
                            new_f2.setAttributes([distance])
                            new_buff_feats.append(new_f2)
                            i = i + 1
                            progress.setValue(i + 1)
                        sel2feats = to_buffer
                        num_of_rings = num_of_rings - 1
                        distance = distance + buffer_distance
                    vl_pr.addFeatures(new_buff_feats)
                    QgsMapLayerRegistry.instance().addMapLayer(vl)

                # Sequential buffers of the original feature with larger buffers
                if buffer_style == "central":
                    orig_buffer_distance = buffer_distance
                    buffered = []
                    for each_feat in sel2feats:
                        num_to_buffer = num_of_rings
                        to_clip = each_feat.geometry()
                        buffer_distance = orig_buffer_distance

                        while num_to_buffer > 0:
                            geom = each_feat.geometry()
                            buff = geom.buffer(buffer_distance, segments_to_approximate)
                            new_f = QgsFeature()
                            new_f_clipped = buff.difference(to_clip)
                            new_f.setGeometry(new_f_clipped)
                            new_f.setAttributes([buffer_distance])
                            buffered.append(new_f)

                            buffer_distance = buffer_distance + orig_buffer_distance
                            num_to_buffer = num_to_buffer - 1
                            to_clip = to_clip.combine(buff)
                            i = i + 1
                            progress.setValue(i + 1)

                    vl_pr.addFeatures(buffered)
                    QgsMapLayerRegistry.instance().addMapLayer(vl)

            self.iface.messageBar().clearWidgets()