import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    static_url = 'http://static-maps.yandex.ru/1.x/'

    def __init__(self):
        super().__init__()
        self.coords = [37.530887, 55.70311]
        self.scale = 0.002
        self.map_type = 'map'
        self.getImage()
        self.initUI()

    def getImage(self):
        params = {
            'll': ','.join(map(str, self.coords)),
            'spn': f'{self.scale},{self.scale}',
            'l': self.map_type
        }
        response = requests.get(self.static_url, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map = response.content

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.map, 'PNG')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())