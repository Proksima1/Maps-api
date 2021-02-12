import os
import sys
import requests
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map_api.ui', self)
        self.pushButton.clicked.connect(self.get_map)
        self.map_file = None

    def isEmpty(self, lineEdit: QLineEdit):
        if lineEdit.text() == '':
            lineEdit.setStyleSheet('border: 1px solid red;')
            return True
        else:
            lineEdit.setStyleSheet('border: 1px solid rgb(160, 160, 160);')
        return False

    def get_map(self):
        url_template = 'http://static-maps.yandex.ru/1.x/?ll= &spn= &l=map'
        try:
            os.remove(self.map_file)
            self.map_file = None
        except TypeError:
            pass
        if not (self.isEmpty(self.lineEdit) and self.isEmpty(self.lineEdit_2)):
            spis = [','.join(self.lineEdit.text().split(' '))]
            if len(self.lineEdit_2.text().strip().split(' ')) == 1:
                spis.append(','.join([self.lineEdit_2.text().strip(), self.lineEdit_2.text().strip()]))
            else:
                spis.append(','.join(self.lineEdit_2.text().strip().split(' ')))
            for i in spis:
                url_template = url_template.replace(' ', i, 1)
            response = requests.get(url_template)
            if not response:
                print('error')
            else:
                self.map_file = "map.png"
                with open(self.map_file, "wb") as file:
                    file.write(response.content)
            pixmap = QPixmap(self.map_file)
            self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        try:
            os.remove(self.map_file)
        except TypeError:
            pass

    def keyPressEvent(self, key):
        if key.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.get_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    copy = Main()
    copy.show()
    sys.exit(app.exec())