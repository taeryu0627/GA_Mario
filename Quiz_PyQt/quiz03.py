# 03. pyqt_paint_event.py
# PyQt Paint Event
import sys
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 300)
        self.setWindowTitle('GA Mario')
        self.show()

    def paintEvent(self, event):
        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

# 사각형 그리기
        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        # 하얀색 사각형
        painter.drawRect(50, 0, 50, 50)

        # 파랑색 사각형
        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(0, 0, 50, 50)
        # 빨간색 사각형
        painter.setBrush(QBrush(Qt.red))
        painter.drawRect(50, 50, 50, 50)

# 선 그리기
        painter.setPen(QPen(Qt.red, 2.0, Qt.SolidLine))
        painter.drawLine(25, 175, 85, 275)
        painter.drawLine(145, 175, 85, 275)
        painter.setPen(QPen(Qt.blue, 2.0, Qt.SolidLine))
        painter.drawLine(85, 175, 85, 275)

# 원 그리기
        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        # 하얀색 원
        painter.setBrush(QBrush(QColor.fromRgb(255, 255, 255)))
        painter.drawEllipse(60, 150, 50, 50)
        # 청록색 원
        painter.setBrush(QBrush(QColor.fromRgb(0, 255, 255)))
        painter.drawEllipse(0, 150, 50, 50)
        painter.drawEllipse(120, 150, 50, 50)
        # 회색 원
        painter.setBrush(QBrush(QColor.fromRgb(125, 125, 125)))
        painter.drawEllipse(60, 250, 50, 50)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())