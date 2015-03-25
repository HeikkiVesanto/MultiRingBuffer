# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FeatureBuffer
                                 A QGIS plugin
 A simple plugin to buffer selected features
                              -------------------
        begin                : 2014-10-23
        git sha              : $Format:%H$
        copyright            : (C) 2014 by thinkWhere
        email                : matthew.walsh@thinkwhere.com
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
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from qgis.core import *
# Initialize Qt resources from file resources.py
import icon_rc
# Import the code for the dialog
from feature_buffer_dialog import FeatureBufferDialog
import os.path


class FeatureBuffer:
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
            'FeatureBuffer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = FeatureBufferDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Feature Buffer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'FeatureBuffer')
        self.toolbar.setObjectName(u'FeatureBuffer')
        # Create empty vector layer for buffers
        #self.vl = QgsVectorLayer('Polygon', "Temp buffers", "memory")

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
        return QCoreApplication.translate('FeatureBuffer', message)


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
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/FeatureBuffer/icon.png'
        self.add_action(icon_path, text=self.tr(u'Buffer Feature'), callback=self.run, parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&Feature Buffer'), action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        #print "THE PLUGIN IS NOT WORKING!!!!!!!!!!!!!!"
        # Create empty vector layer for buffers


        active_vl = self.iface.activeLayer()

        buffer_crs_object = self.iface.activeLayer().crs()

        buffer_crs = buffer_crs_object.authid()

        buffer_input_crs = 'Polygon?crs=%s' % buffer_crs

        vl = QgsVectorLayer(buffer_input_crs, "Temp buffers", "memory")

        sel_feats = active_vl.selectedFeatures()
        if len(sel_feats) > 0:
            # Create
            vl_pr = vl.dataProvider()

            # Create empty list for buffer features
            new_buff_feats = []

            # Loop through all features, buffer and append to list
            for each_feat in sel_feats:
                geom = each_feat.geometry()
                buff = geom.buffer(1500, 20)
                new_f = QgsFeature()
                new_f.setGeometry(buff)
                new_buff_feats.append(new_f)

            # Add features to mem layer then add to canvas
            vl_pr.addFeatures(new_buff_feats)
            QgsMapLayerRegistry.instance().addMapLayer(vl)
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning", "No features selected.", QMessageBox.Ok)




