# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\samir\Documents\QtDesigner\Modellbahnerkennung.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QMainWindow(object):
    def setupUi(self, QMainWindow):
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.resize(729, 620)
        self.centralwidget = QtWidgets.QWidget(QMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 160, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 80, 531, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 40, 91, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(590, 80, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.ImgStrecke = QtWidgets.QGraphicsView(self.centralwidget)
        self.ImgStrecke.setGeometry(QtCore.QRect(40, 210, 651, 361))
        self.ImgStrecke.setObjectName("ImgStrecke")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 120, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 120, 531, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        QMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(QMainWindow)
        self.statusbar.setObjectName("statusbar")
        QMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(QMainWindow)
        QtCore.QMetaObject.connectSlotsByName(QMainWindow)
        QMainWindow.setTabOrder(self.comboBox, self.lineEdit)
        QMainWindow.setTabOrder(self.lineEdit, self.pushButton)

    def retranslateUi(self, QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        QMainWindow.setWindowTitle(_translate("QMainWindow", "Modellbahnerkennung"))
        self.pushButton.setText(_translate("QMainWindow", "Start"))
        self.comboBox.setItemText(0, _translate("QMainWindow", "Camera"))
        self.comboBox.setItemText(1, _translate("QMainWindow", "Picture"))
        self.pushButton_2.setText(_translate("QMainWindow", "Select Picture"))
        self.pushButton_3.setText(_translate("QMainWindow", "Save Result"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()
    ui = Ui_QMainWindow()
    ui.setupUi(QMainWindow)
    QMainWindow.show()
    sys.exit(app.exec_())

