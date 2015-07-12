# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multi_ring_buffer_dialog_base.ui'
#
# Created: Sun Jul 12 20:22:28 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(308, 200)
        Dialog.setSizeGripEnabled(False)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(130, 0))
        self.label_4.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.buffer_layer_name = QtGui.QLabel(Dialog)
        self.buffer_layer_name.setMinimumSize(QtCore.QSize(150, 0))
        self.buffer_layer_name.setObjectName(_fromUtf8("buffer_layer_name"))
        self.horizontalLayout_4.addWidget(self.buffer_layer_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(130, 0))
        self.label.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.bufferDistance = QtGui.QDoubleSpinBox(Dialog)
        self.bufferDistance.setMinimumSize(QtCore.QSize(150, 0))
        self.bufferDistance.setDecimals(10)
        self.bufferDistance.setMaximum(999999999.99)
        self.bufferDistance.setObjectName(_fromUtf8("bufferDistance"))
        self.horizontalLayout.addWidget(self.bufferDistance)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(130, 0))
        self.label_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.segmentsToApproximate = QtGui.QSpinBox(Dialog)
        self.segmentsToApproximate.setMinimumSize(QtCore.QSize(150, 0))
        self.segmentsToApproximate.setProperty("value", 25)
        self.segmentsToApproximate.setObjectName(_fromUtf8("segmentsToApproximate"))
        self.horizontalLayout_2.addWidget(self.segmentsToApproximate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(130, 0))
        self.label_3.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.numberOfRings = QtGui.QSpinBox(Dialog)
        self.numberOfRings.setMinimumSize(QtCore.QSize(150, 0))
        self.numberOfRings.setMaximum(999999999)
        self.numberOfRings.setProperty("value", 5)
        self.numberOfRings.setObjectName(_fromUtf8("numberOfRings"))
        self.horizontalLayout_3.addWidget(self.numberOfRings)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.selectedfeats = QtGui.QCheckBox(Dialog)
        self.selectedfeats.setEnabled(True)
        self.selectedfeats.setChecked(False)
        self.selectedfeats.setObjectName(_fromUtf8("selectedfeats"))
        self.verticalLayout_2.addWidget(self.selectedfeats)
        self.dissovle_button_2 = QtGui.QCheckBox(Dialog)
        self.dissovle_button_2.setChecked(True)
        self.dissovle_button_2.setObjectName(_fromUtf8("dissovle_button_2"))
        self.verticalLayout_2.addWidget(self.dissovle_button_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Multi Ring Buffer", None))
        self.label_4.setText(_translate("Dialog", "Layer to be buffered:", None))
        self.buffer_layer_name.setToolTip(_translate("Dialog", "Please select layer from the layers panel befopre buffering to change.", None))
        self.buffer_layer_name.setText(_translate("Dialog", "<html><head/><body><p>No layer found</p></body></html>", None))
        self.label.setText(_translate("Dialog", "Buffer Distance", None))
        self.bufferDistance.setToolTip(_translate("Dialog", "Buffer distance in your selected layers CRS units.", None))
        self.label_2.setText(_translate("Dialog", "Segments to Approximate", None))
        self.segmentsToApproximate.setToolTip(_translate("Dialog", "How smooth the resulting buffers will be.", None))
        self.label_3.setText(_translate("Dialog", "Number of Rings", None))
        self.numberOfRings.setToolTip(_translate("Dialog", "Number of rings.", None))
        self.selectedfeats.setText(_translate("Dialog", "Buffer only selected features", None))
        self.dissovle_button_2.setToolTip(_translate("Dialog", "Not dissolving may produce strange results with neighbouring features.", None))
        self.dissovle_button_2.setText(_translate("Dialog", "Dissolve features before buffering.", None))

