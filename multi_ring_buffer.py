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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QProgressBar

# Initialize Qt resources from file resources.py
from .resources_rc import *
# Import the code for the dialog
from .multi_ring_buffer_dialog import MultiRingBufferDialog
import os.path
from decimal import *

from qgis.core import *

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


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

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
        self.add_action(
            icon_path,
            text=self.tr(u'Multi Ring Buffer'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Multi Ring Buffer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run_buffer(self, geom, distance, segments):
        if geom is not None:
            buf = geom.buffer(distance, segments)
            return buf
        else:
            return None


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
        # Get list of vector layers
        layers = list(QgsProject.instance().mapLayers().values())

        # Check there is at least one vector layer.
        vlayer_count = 0
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                vlayer_count = vlayer_count + 1
        # Run the dialog event loop
        if vlayer_count > 0:
            # show the dialog
            self.dlg.show()
            self.dlg.isSomethingSelected()
            result = self.dlg.exec_()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning",
                                "No vecor layers.", QMessageBox.Ok)
            result = 0
            # See if OK was pressed

        if result == 1:
            buffering_layer = self.dlg.mMapLayerComboBox.currentLayer()

            # Either buffer with all features or just selected ones
            if self.dlg.selectedfeats.isChecked():
                sel_feats = buffering_layer.selectedFeatures()
            else:
                selecting_feats_iterator = buffering_layer.getFeatures()
                sel_feats = []
                for s_feat in selecting_feats_iterator:
                    sel_feats.append(s_feat)

            # Switch between sequential and central buffer styles.
            # A toggle was added, but it seems too complex of a question for most users.
            # buffer_style = "sequential"
            if self.dlg.central_style.isChecked():
                buffer_style = "central"
            else:
                buffer_style = "sequential"

            # Inputs from the dialog:
            if self.dlg.dissovle_button_2.isChecked():
                dissolve_bool = 1
            else:
                dissolve_bool = 0

            segments_to_approximate = self.dlg.segmentsToApproximate.value()

            # Check if regular buffers (no dissolving)
            if self.dlg.radioDonut.isChecked():
                clipper = True
            else:
                clipper = False

            run_csv_buffer = False

            # Check if rings and distance supplied or list of rings as csv
            if self.dlg.radioRings.isChecked():
                num_of_rings = self.dlg.numberOfRings.value()
                buffer_distance = self.dlg.bufferDistance.value()
                # If not dislving we want to start from the outside and come in
                # So smaller buffers will be on top of the bigger ones.
                # We will do this by creating a list
                if not clipper:
                    buffer_csv = []
                    buf_dist = buffer_distance
                    for i in range(num_of_rings):
                        buffer_csv.append(buf_dist)
                        buf_dist += buffer_distance
                    buffer_csv.sort(reverse=True)
                    run_csv_buffer = True

            else:
                buffer_csv = self.dlg.distancesCommaSep.text()
                # Parse csv into list of numbers
                buffer_csv = buffer_csv.split(",")
                try:
                    buffer_csv = [float(i) for i in buffer_csv]
                    run_csv_buffer = True
                    # Sort list small to large, or large to small if not disolving
                    if clipper:
                        buffer_csv.sort()
                    else:
                        buffer_csv.sort(reverse=True)
                except Exception as e:
                    QMessageBox.warning(self.iface.mainWindow(), "Warning",
                                        "Error in comma seperated numbers: {}.".format(e),
                                        QMessageBox.Ok)
                    result = 0

            add_old_attributes = 1

            # Create data provider for input layer to get fields.
            in_prov = buffering_layer.dataProvider()
            in_fields = in_prov.fields()

            buffer_crs_object = self.iface.activeLayer().crs()
            # Check the current CRS of the layer
            buffer_crs = buffer_crs_object.authid()
            # Apply that to the created layer if recognised
            buffer_input_crs = "Polygon?crs=%s" % buffer_crs
            # Create empty memory vector layer for buffers
            layer_name = buffering_layer.name()
            vl = QgsVectorLayer(buffer_input_crs,
                                "%s_MultiRingBuffer" % layer_name, "memory")
            vl_pr = vl.dataProvider()

            copy_atts = 0
            # Copy old attributes, only if not dissolving multiple features
            if (add_old_attributes == 1 and dissolve_bool == 0) or len(sel_feats) == 1:
                copy_atts = 1
                fields_to_add = []
                for field in in_fields:
                    fields_to_add.append(field)
                vl_pr.addAttributes(fields_to_add)
                vl.updateFields()
            else:
                copy_atts = 0
            # Distance feature for buffer distance
            vl_pr.addAttributes([QgsField("mrb_dist", QVariant.String)])
            vl.updateFields()

            # Dissolve the features if selected.
            if dissolve_bool == 1:
                sel2feats = []
                add_feat = self.dissolve(sel_feats)
                if copy_atts == 1:
                    new_attributes = []
                    for attributes in sel_feats[0].attributes():
                        new_attributes.append(attributes)
                    add_feat.setAttributes(new_attributes)
                # Our buffer loops require a list (as sel_feats originally is), so we append the features to a list.
                sel2feats.append(add_feat)
            else:
                sel2feats = sel_feats

            # Run if there are features in the layer
            if len(sel2feats) > 0 and result == 1:
                # Progress bar.
                progressMessageBar = self.iface.messageBar().createMessage("Buffering...")
                progress = QProgressBar()
                progress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                progressMessageBar.layout().addWidget(progress)
                self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
                if run_csv_buffer:
                    maximum_progress = len(sel2feats) * len(buffer_csv)
                else:
                    maximum_progress = len(sel2feats) * num_of_rings
                progress.setMaximum(maximum_progress)
                i = 0

                # Buffer a feature then buffer the buffer (used)
                if run_csv_buffer:
                    buffered = []
                    for each_feat in sel2feats:
                        to_clip = each_feat.geometry()

                        for j in buffer_csv:
                            geom = each_feat.geometry()
                            buff = self.run_buffer(geom, j, segments_to_approximate)
                            new_f = QgsFeature()
                            if clipper:
                                new_f_clipped = buff.difference(to_clip)
                            else:
                                new_f_clipped = buff

                            new_f.setGeometry(new_f_clipped)

                            if copy_atts == 1:
                                new_attributes = []
                                for attributes in each_feat.attributes():
                                    new_attributes.append(attributes)
                                new_attributes.append(i)
                                new_f.setAttributes(new_attributes)
                            else:
                                new_f.setAttributes([j])

                            buffered.append(new_f)

                            to_clip = to_clip.combine(buff)
                            i += 1
                            progress.setValue(i + 1)
                    vl_pr.addFeatures(buffered)
                    QgsProject.instance().addMapLayer(vl)


                elif buffer_style == "sequential":
                    num_attributes = len(sel2feats[0].attributes())
                    # fix_print_with_import
                    print(num_attributes)
                    new_buff_feats = []
                    distance = buffer_distance
                    while num_of_rings > 0:
                        to_buffer = []
                        for each_feat in sel2feats:
                            geom = each_feat.geometry()
                            buff = self.run_buffer(geom, buffer_distance, segments_to_approximate)
                            new_f = QgsFeature()
                            new_f.setGeometry(buff)
                            new_f_geom = new_f.geometry()
                            new_f_clipped = new_f_geom.difference(geom)
                            new_f2 = QgsFeature()
                            new_f2.setGeometry(new_f_clipped)
                            if copy_atts == 1:
                                new_attributes = []
                                for attributes in each_feat.attributes():
                                    new_attributes.append(attributes)
                                if len(new_attributes) > num_attributes:
                                    # Need to delete the distance field from
                                    # the previous run.
                                    new_attributes = new_attributes[:-1]
                                new_attributes.append(distance)
                                new_f2.setAttributes(new_attributes)
                                new_f.setAttributes(new_attributes)
                            else:
                                new_f2.setAttributes([distance])
                            new_buff_feats.append(new_f2)
                            i += 1
                            to_buffer.append(new_f)
                            progress.setValue(i + 1)
                        sel2feats = to_buffer
                        num_of_rings -= 1
                        distance = distance + buffer_distance
                    vl_pr.addFeatures(new_buff_feats)
                    QgsProject.instance().addMapLayer(vl)

                # Sequential buffers of the original feature with larger buffers
                elif buffer_style == "central":
                    orig_buffer_distance = buffer_distance
                    buffered = []
                    for each_feat in sel2feats:
                        num_to_buffer = num_of_rings
                        to_clip = each_feat.geometry()
                        buffer_distance = orig_buffer_distance

                        while num_to_buffer > 0:
                            geom = each_feat.geometry()
                            buff = self.run_buffer(geom, buffer_distance, segments_to_approximate)
                            new_f = QgsFeature()
                            new_f_clipped = buff.difference(to_clip)
                            new_f.setGeometry(new_f_clipped)

                            if copy_atts == 1:
                                new_attributes = []
                                for attributes in each_feat.attributes():
                                    new_attributes.append(attributes)
                                new_attributes.append(buffer_distance)
                                new_f.setAttributes(new_attributes)
                            else:
                                new_f.setAttributes([buffer_distance])

                            buffered.append(new_f)

                            buffer_distance = buffer_distance + orig_buffer_distance
                            num_to_buffer = num_to_buffer - 1
                            to_clip = to_clip.combine(buff)
                            i += 1
                            progress.setValue(i + 1)
                    vl_pr.addFeatures(buffered)
                    QgsProject.instance().addMapLayer(vl)

            self.iface.messageBar().clearWidgets()