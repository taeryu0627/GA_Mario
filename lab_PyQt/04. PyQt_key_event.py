# 04. PyQt_key_event.py
# PyQt 키 이벤트

import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1024, 768)

        self.setWindowTitle('GA Mario')

        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        print(str(key)+' press')

    def keyReleaseEvent(self, event):
        key = event.key()
        print(str(key) + ' release')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())