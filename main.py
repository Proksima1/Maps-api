import os
import sys
from typing import List
import requests
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit


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

    def get_map(self, pos: List, scale: str):
        if (pos and scale) is not None:
            url_template = 'http://static-maps.yandex.ru/1.x/?ll= &spn= &l=map'
            try:
                os.remove(self.map_file)
                self.map_file = None
            except TypeError:
                pass
            coord = [','.join(pos)]
            self.position = list(map(float, pos))
            coord.append(','.join([scale, scale]))
            self.scale = int(scale)
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

    def data_prepare(self, lineEdit: QLineEdit, key=None):
        """Возвращает список из данных, которые были в lineEdit.
        Если передан ключ, то передано значение scale."""
        if not self.isEmpty(lineEdit):
            if key is None:
                if len(lineEdit.text().split(',')) == 1:
                    data = lineEdit.text().split()
                else:
                    data = list(map(lambda x: x.strip(), lineEdit.text().split(',')))
                lineEdit.setText(lineEdit.text().strip())
            else:
                if lineEdit.text().split(',') == 1:
                    lineEdit.setText(str(max(list(map(int, lineEdit.text().split())))))
                else:
                    lineEdit.setText(str(max(list(map(int,
                                                      list(map(lambda x: x.strip(),
                                                               lineEdit.text().split(','))))))))
                data = lineEdit.text()
        else:
            data = None
        return data

    def closeEvent(self, event):
        try:
            os.remove(self.map_file)
        except TypeError:
            pass

    def keyPressEvent(self, key):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        if key.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.get_map(self.data_prepare(self.lineEdit), self.data_prepare(self.lineEdit_2, key=True))
        if key.key() == QtCore.Qt.Key_PageUp:
            if self.scale < 90:
                self.scale += 1
            self.lineEdit_2.setText(str(round(self.scale)))
            self.get_map(self.data_prepare(self.lineEdit), self.data_prepare(self.lineEdit_2, key=True))
        if key.key() == QtCore.Qt.Key_PageDown:
            if self.scale > 0:
                self.scale -= 1
            self.lineEdit_2.setText(str(round(self.scale)))
            self.get_map(self.data_prepare(self.lineEdit), self.data_prepare(self.lineEdit_2, key=True))
        if key.key() == QtCore.Qt.Key_Up:
            if float(self.position[1]) < 70:
                self.position[1] += 0.5
            self.lineEdit.setText(' '.join(list(map(str, self.position))))
            self.get_map(self.data_prepare(self.lineEdit), self.data_prepare(self.lineEdit_2, key=True))
        if key.key() == QtCore.Qt.Key_Down:
            if float(self.position[1]) > -70:
                self.position[1] -= 0.5
            self.lineEdit.setText(' '.join(list(map(str, self.position))))
            self.get_map(self.data_prepare(self.lineEdit), self.data_prepare(self.lineEdit_2, key=True))
        if key.key() == QtCore.Qt.Key_Right:
            if int(self.position[0]) < 180:
                self.position[0] += 0.5
            self.lineEdit.setText(' '.join(list(map(str, self.position))))
            self.get_map(self.data_prepare(self.lineEdit), self.data_prepare(self.lineEdit_2, key=True))
        if key.key() == QtCore.Qt.Key_Left:
            if int(self.position[0]) > 0:
                self.position[0] -= 0.5
            self.lineEdit.setText(' '.join(list(map(str, self.position))))
            self.get_map(self.data_prepare(self.lineEdit), self.data_prepare(self.lineEdit_2, key=True))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    copy = Main()
    copy.show()
    sys.exit(app.exec())
