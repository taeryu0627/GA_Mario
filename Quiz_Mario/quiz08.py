import retro
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
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
        self.tiles_width = 448
        self.tiles_height = 480
        # 키배열 : B, NULL, SELECT, START, U, D, L, R, A
        self.button = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        # 화면 가져오기
        self.screen = self.env.get_screen()

        # 창의 크기 고정
        self.setFixedSize(1080, 480)
        # 창 제목
        self.setWindowTitle('GA Mario')

        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(1080-448, 0, 1080, self.height)

        # 타이머 생성
        qtimer = QTimer(self)
        # 타이머 호출
        qtimer.timeout.connect(self.game_timer)
        qtimer.start(1000//self.game_speed)

        # 창 띄우기
        self.show()

    def paintEvent(self, event):

        ram = self.env.get_ram()

        full_screen_tiles = ram[0x0500:0x069F + 1]

        full_screen_tile_count = full_screen_tiles.shape[0]

        full_screen_page1_tile = full_screen_tiles[:full_screen_tile_count // 2].reshape((13, 16))
        full_screen_page2_tile = full_screen_tiles[full_screen_tile_count // 2:].reshape((13, 16))

        full_screen_tiles = np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1).astype(np.int)

        # 페이지 속 현재 화면 위치
        screen_position = ram[0x071C]
        # 0x071A	Current screen (in level)
        # 현재 화면이 속한 페이지 번호
        current_screen_page = ram[0x071A]
        # 0x071C	ScreenEdge X-Position, loads next screen when player past it?

        # 화면 오프셋
        screen_offset = (256 * current_screen_page + screen_position) % 512
        # 타일 화면 오프셋
        screen_tile_offset = screen_offset // 16
        # 현재 보이는 화면에서 x 좌표
        player_x = ram[0x03AD]

        player_y = ram[0x03B8]
        width = 32
        height = 13
        set_screen = screen_tile_offset % 16
        player_tile_position_x = (player_x + 8) // 16
        player_tile_position_y = (player_y + 8) // 16 - 1
        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

        # 사각형 그리기
        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        print("[", player_x , ", " , player_y , "]")
        for h in range(height):
            for w in range(width):
                # 현재 위치 바꿔주기
                painter.setBrush(QBrush(Qt.blue))
                painter.drawRect((screen_tile_offset + 16) % 32 * 15, (h) * 15, 15, 15)
                painter.setBrush(QBrush(Qt.blue))
                painter.drawRect((screen_tile_offset) % 32 * 15, (h) * 15, 15, 15)
                painter.setBrush(QBrush(Qt.blue))
                painter.drawRect((screen_tile_offset + player_tile_position_x) % 32 * 15, (player_tile_position_y) * 15, 15,
                                 15)
                if full_screen_tiles[h][w] == 0:
                    painter.setBrush(QBrush(Qt.gray))
                    painter.drawRect(w * 15, h * 15, 15, 15)
                # 바닥 및 벽
                elif full_screen_tiles[h][w] == 84 or full_screen_tiles[h][w] == 97 \
                        or full_screen_tiles[h][w] == 82 or full_screen_tiles[h][w] == 99:
                    painter.setBrush(QColor(58, 134, 255))
                    painter.drawRect(w * 15, h * 15, 15, 15)
                # 배관
                elif full_screen_tiles[h][w] >= 16 and full_screen_tiles[h][w] <= 33:
                    painter.setBrush(QColor(131, 56, 236))
                    painter.drawRect(w * 15, h * 15, 15, 15)
                # 빈 박스
                elif full_screen_tiles[h][w] == 81:
                    painter.setBrush(QColor(251, 86, 7))
                    painter.drawRect(w * 15, h * 15, 15, 15)
                # 아이템 or 골드 박스
                elif full_screen_tiles[h][w] == 192 or full_screen_tiles[h][w] == 193 or full_screen_tiles[h][w] == 196:
                    painter.setBrush(QColor(255, 0, 110))
                    painter.drawRect(w * 15, h * 15, 15, 15)
                # 그냥 골드
                elif full_screen_tiles[h][w] == 194:
                    painter.setBrush(QBrush(Qt.white))
                    painter.drawRect(w * 15, h * 15, 15, 15)



        painter.end()

    def update_screen(self):
        screen = self.env.get_screen()
        screen_qimage = QImage(screen, screen.shape[1], screen.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(screen_qimage)
        pixmap = pixmap.scaled(self.width, self.height, Qt.IgnoreAspectRatio)
        self.screen_label.setPixmap(pixmap)

    def game_timer(self):
        self.env.step(np.array(self.button))
        self.update_screen()
        self.update()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())
