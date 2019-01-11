# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\samir\Documents\QtDesigner\GrobeMaske.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog1(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(2000,1410)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(400, 630, 140, 50))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 1310, 140, 50))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(1360, 630, 140, 50))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(1360, 1310, 140, 50))
        self.pushButton_4.setObjectName("pushButton_4")

        self.label60 = QtWidgets.QLabel(Dialog)
        self.label60.setGeometry(QtCore.QRect(40, 50, 900, 530))
        self.label60.setText("")
        self.label60.setScaledContents(True)
        self.label60.setObjectName("Mask60")

        self.label80 = QtWidgets.QLabel(Dialog)
        self.label80.setGeometry(QtCore.QRect(40, 730, 900, 530))
        self.label80.setText("")
        self.label80.setScaledContents(True)
        self.label80.setObjectName("Mask80")

        self.label100 = QtWidgets.QLabel(Dialog)
        self.label100.setGeometry(QtCore.QRect(980, 50, 900, 530))
        self.label100.setText("")
        self.label100.setScaledContents(True)
        self.label100.setObjectName("Mask100")

        self.label120 = QtWidgets.QLabel(Dialog)
        self.label120.setGeometry(QtCore.QRect(980, 730, 900, 530))
        self.label120.setText("")
        self.label120.setScaledContents(True)
        self.label120.setObjectName("Mask120")

        # self.Mask120 = QtWidgets.QGraphicsView(Dialog)
        # self.Mask120.setGeometry(QtCore.QRect(400, 280, 321, 221))
        # self.Mask120.setObjectName("Mask120")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Grobe Maske"))
        self.pushButton.setText(_translate("Dialog", "60"))
        self.pushButton_2.setText(_translate("Dialog", "80"))
        self.pushButton_3.setText(_translate("Dialog", "100"))
        self.pushButton_4.setText(_translate("Dialog", "120"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog1()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

