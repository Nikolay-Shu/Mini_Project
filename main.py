import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt

COEFF_SCALING = 2

class NoMapException(BaseException):
    pass

class Example(QWidget):
    static_url = 'http://static-maps.yandex.ru/1.x/'

    def __init__(self):
        super().__init__()
        self.coords = [37.530887, 55.70311]
        self.scale = 0.002
        self.map_type = 'map'
        uic.loadUi("interface.ui", self)
        self.getImage(self.coords, self.scale)


    def getImage(self, coords, scale):
        params = {
            'll': ','.join(map(str, coords)),
            'spn': f'{scale},{scale}',
            'l': self.map_type
        }
        response = requests.get(self.static_url, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            raise NoMapException

        pixmap = QPixmap()
        pixmap.loadFromData(response.content, 'PNG')
        self.image.setPixmap(pixmap)

    def keyPressEvent(self, a0):
        key = a0.key()
        if key in (Qt.Key_PageUp, Qt.Key_PageDown):
            if key == Qt.Key_PageUp:
                new_scale = self.scale / COEFF_SCALING
            else:
                new_scale = self.scale * COEFF_SCALING
            try:
                self.getImage(self.coords, new_scale)
            except NoMapException:
                pass
            else:
                self.scale = new_scale
        elif key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            new_coords = self.coords[:]
            if key == Qt.Key_Left:
                new_coords[0] -= self.scale
            elif key == Qt.Key_Right:
                new_coords[0] += self.scale
            elif key == Qt.Key_Up:
                new_coords[1] += self.scale
            elif key == Qt.Key_Down:
                new_coords[1] -= self.scale
            try:
                self.getImage(new_coords, self.scale)
            except NoMapException:
                pass
            else:
                self.coords = new_coords





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())