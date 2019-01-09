# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\samir\Documents\QtDesigner\GenaueMaske.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(721, 701)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 210, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 440, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(120, 670, 75, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(510, 670, 75, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(510, 440, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(510, 210, 75, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.Mask1 = QtWidgets.QGraphicsView(Dialog)
        self.Mask1.setGeometry(QtCore.QRect(20, 11, 281, 191))
        self.Mask1.setObjectName("Mask1")
        self.Mask4 = QtWidgets.QGraphicsView(Dialog)
        self.Mask4.setGeometry(QtCore.QRect(410, 10, 281, 191))
        self.Mask4.setObjectName("Mask4")
        self.Mask2 = QtWidgets.QGraphicsView(Dialog)
        self.Mask2.setGeometry(QtCore.QRect(20, 241, 281, 191))
        self.Mask2.setObjectName("Mask2")
        self.Mask5 = QtWidgets.QGraphicsView(Dialog)
        self.Mask5.setGeometry(QtCore.QRect(410, 240, 281, 191))
        self.Mask5.setObjectName("Mask5")
        self.Mask3 = QtWidgets.QGraphicsView(Dialog)
        self.Mask3.setGeometry(QtCore.QRect(20, 471, 281, 191))
        self.Mask3.setObjectName("Mask3")
        self.Mask6 = QtWidgets.QGraphicsView(Dialog)
        self.Mask6.setGeometry(QtCore.QRect(410, 470, 281, 191))
        self.Mask6.setObjectName("Mask6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Genaue Maske"))
        self.pushButton.setText(_translate("Dialog", "1"))
        self.pushButton_2.setText(_translate("Dialog", "2"))
        self.pushButton_3.setText(_translate("Dialog", "3"))
        self.pushButton_4.setText(_translate("Dialog", "6"))
        self.pushButton_5.setText(_translate("Dialog", "5"))
        self.pushButton_6.setText(_translate("Dialog", "4"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

