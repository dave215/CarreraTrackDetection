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
        QMainWindow.resize(2000, 1600)
        self.centralwidget = QtWidgets.QWidget(QMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 380, 150, 60))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 140, 1660, 50))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 40, 200, 60))
        self.comboBox.setObjectName("comboBox")
        icon = QtGui.QIcon.fromTheme("Kamera")
        self.comboBox.addItem(icon, "")
        icon = QtGui.QIcon.fromTheme("Bild")
        self.comboBox.addItem(icon, "")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1720, 140, 200, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 500, 1800, 1060))
        self.label.setText("")
#         self.label.setPixmap(QtGui.QPixmap("test2.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("ImgStrecke")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1720, 250, 200, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 250, 1660, 50))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(1)
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
        self.comboBox.setItemText(0, _translate("QMainWindow", "Kamera"))
        self.comboBox.setItemText(1, _translate("QMainWindow", "Bild"))
        self.pushButton_2.setText(_translate("QMainWindow", "Bild wählen"))
        self.pushButton_3.setText(_translate("QMainWindow", "Strecke speichern"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()
    ui = Ui_QMainWindow()
    ui.setupUi(QMainWindow)
    QMainWindow.show()
    sys.exit(app.exec_())

