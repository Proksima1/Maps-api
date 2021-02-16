import os
import sys
import requests
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QHBoxLayout
from modules import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map_api.ui', self)
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
        url_template = f'http://static-maps.yandex.ru/1.x/?ll= &spn= &l=map'
        self.lineEdit.setText(self.lineEdit.text().strip())
        try:
            os.remove(self.map_file)
            self.map_file = None
        except TypeError:
            pass
        if not (self.isEmpty(self.lineEdit) and self.isEmpty(self.lineEdit_2)):
            coord = [','.join(self.lineEdit.text().split(' '))]
            self.position = coord
            print(self.position)
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
            print(self.scale)
            self.lineEdit_2.setText(str(round(self.scale)))
            self.get_map()
        if key.key() == QtCore.Qt.Key_Up:
            if int(self.position[1]) < 70:
                self.position[1] += 0.5
            print(self.position)
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