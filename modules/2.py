import os
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(990, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 0, 631, 551))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 291, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setStyleSheet("border: 1px solid rgb(160, 160, 160)")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setStyleSheet("border: 1px solid rgb(160, 160, 160)")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout.addWidget(self.radioButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 990, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Введите координаты:"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Введите масштаб:"))
        self.radioButton.setText(_translate("MainWindow", "Схема"))
        self.radioButton_2.setText(_translate("MainWindow", "Спутник"))
        self.radioButton_3.setText(_translate("MainWindow", "Гибрид"))
        self.pushButton.setText(_translate("MainWindow", "Переместиться"))
        self.pushButton.clicked.connect(self.get_map)
        self.map_file = None
        self.position = [37.615370, 55.756936]
        self.scale = 5

    def isEmpty(self, lineEdit: QLineEdit):
        if lineEdit.text() == '':
            lineEdit.setStyleSheet('border: 1px solid red;')
            return True
        else:
            lineEdit.setStyleSheet('border: 1px solid rgb(160, 160, 160);')
        return False

    def get_map(self):
        if self.radioButton.isChecked():
            url_template = f'http://static-maps.yandex.ru/1.x/?ll= &spn= &l=map'
        elif self.radioButton_2:
            url_template = f'http://static-maps.yandex.ru/1.x/?ll= &spn= &l=sat'
        else:
            url_template = f'http://static-maps.yandex.ru/1.x/?ll= &spn= &l=skl'
        self.lineEdit.setText(self.lineEdit.text().strip())
        try:
            os.remove(self.map_file)
            self.map_file = None
        except TypeError:
            pass
        if not (self.isEmpty(self.lineEdit) and self.isEmpty(self.lineEdit_2)):
            coord = [','.join(self.lineEdit.text().split(' '))]
            self.position = coord
            if len(self.lineEdit_2.text().strip().split(' ')) == 1:
                coord.append(','.join([self.lineEdit_2.text().strip(), self.lineEdit_2.text().strip()]))
                self.scale = float(self.lineEdit_2.text().strip())
            else:
                max_scale = str(max(list(map(float, self.lineEdit_2.text().strip().split(' ')))))
                self.lineEdit_2.setText(max_scale)
                self.scale = float(max_scale)
                coord.append(','.join([max_scale, max_scale]))
            for i in coord:
                url_template = url_template.replace(' ', i, 1)
            response = requests.get(url_template)
            if not response:
                print(f'error {response.text}')
            else:
                self.map_file = "map.png"
                with open(self.map_file, "wb") as file:
                    file.write(response.content)
            pixmap = QPixmap(self.map_file)
            self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        """"""
        try:
            os.remove(self.map_file)
        except TypeError:
            pass

    def keyPressEvent(self, key):
        if key.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.get_map()
        if key.key() == QtCore.Qt.Key_PageUp:
            if self.scale < 90:
                self.scale += 1
            self.lineEdit_2.setText(str(round(self.scale)))
            self.get_map()
        if key.key() == QtCore.Qt.Key_PageDown:
            if self.scale > 0:
                self.scale -= 1
            self.lineEdit_2.setText(str(round(self.scale)))
            self.get_map()
        if key.key() == QtCore.Qt.Key_Up:
            if int(self.position[1]) < 70:
                self.position[1] += 0.5
            self.lineEdit.setText(' '.join(list(map(str, self.position))))
            self.get_map()
        if key.key() == QtCore.Qt.Key_Right:
            #if int(self.position[0]) <
            self.position[0] += 0.5
            self.lineEdit.setText(' '.join(list(map(str, self.position))))
            self.get_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    copy = Main()
    copy.show()
    sys.exit(app.exec())