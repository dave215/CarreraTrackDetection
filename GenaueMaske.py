# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\samir\Documents\QtDesigner\GenaueMaske.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1320, 1609)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(270, 453, 140, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 956, 140, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(270, 1509, 140, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(910, 453, 140, 50))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(910, 956, 140, 50))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(910, 1509, 140, 50))
        self.pushButton_6.setObjectName("pushButton_6")

        self.label1 = QtWidgets.QLabel(Dialog)
        self.label1.setGeometry(QtCore.QRect(40, 50, 600, 353))
        self.label1.setText("")
        self.label1.setScaledContents(True)
        self.label1.setObjectName("Mask1")

        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(40, 553, 600, 353))
        self.label2.setText("")
        self.label2.setScaledContents(True)
        self.label2.setObjectName("Mask2")

        self.label3 = QtWidgets.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(40, 1056, 600, 353))
        self.label3.setText("")
        self.label3.setScaledContents(True)
        self.label3.setObjectName("Mask3")

        self.label4 = QtWidgets.QLabel(Dialog)
        self.label4.setGeometry(QtCore.QRect(680, 50, 600, 353))
        self.label4.setText("")
        self.label4.setScaledContents(True)
        self.label4.setObjectName("Mask4")

        self.label5 = QtWidgets.QLabel(Dialog)
        self.label5.setGeometry(QtCore.QRect(680, 553, 600, 353))
        self.label5.setText("")
        self.label5.setScaledContents(True)
        self.label5.setObjectName("Mask5")

        self.label6 = QtWidgets.QLabel(Dialog)
        self.label6.setGeometry(QtCore.QRect(680, 1056, 600, 353))
        self.label6.setText("")
        self.label6.setScaledContents(True)
        self.label6.setObjectName("Mask6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Genaue Maske"))
        self.pushButton.setText(_translate("Dialog", "1"))
        self.pushButton_2.setText(_translate("Dialog", "2"))
        self.pushButton_3.setText(_translate("Dialog", "3"))
        self.pushButton_4.setText(_translate("Dialog", "4"))
        self.pushButton_5.setText(_translate("Dialog", "5"))
        self.pushButton_6.setText(_translate("Dialog", "6"))


# if __name__ == "__main__":
import sys
app2 = QtWidgets.QApplication(sys.argv)
Dialog2 = QtWidgets.QDialog()
ui2 = Ui_Dialog2()
ui2.setupUi(Dialog2)
# Dialog2.show()
# sys.exit(app2.exec_())

