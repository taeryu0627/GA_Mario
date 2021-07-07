# 01.PyQt_basic
# PyQt 기본 기능

import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 크기 고정
        self.setFixedSize(400, 400)
        # 창 제목 설정
        self.setWindowTitle('GA_Mario')
        # 창 띄우기
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())

