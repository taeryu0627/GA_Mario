
import retro
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')

        # 새 게임 시작
        self.env.reset()

        self.width = 448
        self.height = 480
        self.game_speed = 60
        self.screen_size = 1

        # 키배열 : B, NULL, SELECT, START, U, D, L, R, A
        self.button = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        # 화면 가져오기
        self.screen = self.env.get_screen()

        # 창의 크기 고정
        self.setFixedSize(self.width, self.height)
        # 창 제목
        self.setWindowTitle('GA Mario')

        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.width * self.screen_size, self.height * self.screen_size)

        # 타이머 생성
        qtimer = QTimer(self)
        # 타이머 호출
        qtimer.timeout.connect(self.game_timer)
        qtimer.start(1000//self.game_speed)

        # 창 띄우기
        self.show()

    def update_screen(self):
        screen = self.env.get_screen()
        screen_qimage = QImage(screen, screen.shape[1], screen.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(screen_qimage)
        pixmap = pixmap.scaled(self.width, self.height, Qt.IgnoreAspectRatio)
        self.screen_label.setPixmap(pixmap)

    def game_timer(self):
        self.env.step(np.array(self.button))
        self.update_screen()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.button[4] = 1
        if key == Qt.Key_Down:
            self.button[5] = 1
        if key == Qt.Key_Left:
            self.button[6] = 1
        if key == Qt.Key_Right:
            self.button[7] = 1
        if key == Qt.Key_Z:
            self.button[8] = 1
        if key == Qt.Key_X:
            self.button[0] = 1

    def keyReleaseEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.button[4] = 0
        if key == Qt.Key_Down:
            self.button[5] = 0
        if key == Qt.Key_Left:
            self.button[6] = 0
        if key == Qt.Key_Right:
            self.button[7] = 0
        if key == Qt.Key_Z:
            self.button[8] = 0
        if key == Qt.Key_X:
            self.button[0] = 0
        if key == Qt.Key_R:
            self.env.reset()
        if key == Qt.Key_P:
            self.game_speed += 30
        if key == Qt.Key_O:
            self.game_speed -= 30


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())
