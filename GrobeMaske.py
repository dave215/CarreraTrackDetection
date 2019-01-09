# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\samir\Documents\QtDesigner\GrobeMaske.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(731, 580)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 240, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 240, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 510, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(130, 510, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.Mask60 = QtWidgets.QGraphicsView(Dialog)
        self.Mask60.setGeometry(QtCore.QRect(10, 10, 321, 221))
        self.Mask60.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Mask60.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Mask60.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.Mask60.setObjectName("Mask60")
        self.Mask80 = QtWidgets.QGraphicsView(Dialog)
        self.Mask80.setGeometry(QtCore.QRect(400, 10, 321, 221))
        self.Mask80.setObjectName("Mask80")
        self.Mask100 = QtWidgets.QGraphicsView(Dialog)
        self.Mask100.setGeometry(QtCore.QRect(10, 280, 321, 221))
        self.Mask100.setObjectName("Mask100")
        self.Mask120 = QtWidgets.QGraphicsView(Dialog)
        self.Mask120.setGeometry(QtCore.QRect(400, 280, 321, 221))
        self.Mask120.setObjectName("Mask120")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Grobe Maske"))
        self.pushButton.setText(_translate("Dialog", "60"))
        self.pushButton_2.setText(_translate("Dialog", "80"))
        self.pushButton_3.setText(_translate("Dialog", "120"))
        self.pushButton_4.setText(_translate("Dialog", "100"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

