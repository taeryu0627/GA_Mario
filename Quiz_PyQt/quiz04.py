# 04. PyQt_key_event.py
# PyQt 키 이벤트

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(300, 300)

        self.setWindowTitle('My App')

        self.labelP = QLabel(self)
        self.labelR = QLabel(self)

        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        self.labelP.setText(str(key) + " press QLabel")
        self.labelP.setGeometry(0, 0, 300, 50)

    def keyReleaseEvent(self, event):
        key = event.key()
        self.labelR.setText(str(key) + " release QLabel")
        self.labelR.setGeometry(0, 20, 300, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())