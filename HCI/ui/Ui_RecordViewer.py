# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/RecordViewer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RecordViewer(object):
    def setupUi(self, RecordViewer):
        RecordViewer.setObjectName("RecordViewer")
        RecordViewer.resize(549, 372)
        self.verticalLayout = QtWidgets.QVBoxLayout(RecordViewer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.canvas = QtWidgets.QOpenGLWidget(RecordViewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setObjectName("canvas")
        self.verticalLayout.addWidget(self.canvas)
        self.widget = QtWidgets.QWidget(RecordViewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(RecordViewer)
        QtCore.QMetaObject.connectSlotsByName(RecordViewer)

    def retranslateUi(self, RecordViewer):
        _translate = QtCore.QCoreApplication.translate
        RecordViewer.setWindowTitle(_translate("RecordViewer", "Form"))
        self.label.setText(_translate("RecordViewer", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RecordViewer = QtWidgets.QWidget()
    ui = Ui_RecordViewer()
    ui.setupUi(RecordViewer)
    RecordViewer.show()
    sys.exit(app.exec_())
