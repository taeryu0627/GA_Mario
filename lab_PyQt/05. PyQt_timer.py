# 05. pyqt_timer.py
# 타이머

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(300, 400)

        self.setWindowTitle('My App')

        self.label = QLabel(self)

        self.time = 0
        # 타이머 생성
        self.qtimer = QTimer(self)
        # 타이머에 호출될 함수 연결
        self.qtimer.timeout.connect(self.timer)
        # 1초마다 연결된 함수 실행
        self.qtimer.start(1000)

        self.show()

    def timer(self):
        self.time+=13
        self.label.setText(str(self.time))
        self.label.setGeometry(50, 50, 300, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())


