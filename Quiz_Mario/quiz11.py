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
        # 게임 화면 크기
        width = 448
        height = 480
        # 게임 속도 조절
        game_speed = 60
        # 키배열 : B, NULL, SELECT, START, U, D, L, R, A
        self.button = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 화면 가져오기
        self.screen = self.env.get_screen()
        # 창의 크기 고정
        self.setFixedSize(1080, 480)
        # 창 제목
        self.setWindowTitle('GA Mario')

        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(1080-width, 0, 1080, height)

        # 타이머 생성
        qtimer = QTimer(self)
        # 타이머 호출
        qtimer.timeout.connect(self.game_timer)
        qtimer.start(1000//game_speed)

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

        # 현재 화면 추출
        screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:,
                       screen_tile_offset:screen_tile_offset + 16]

        # 현재 화면 속 플레이어 x 좌표
        player_x = ram[0x03AD]
        # 현재 화면 속 플레이어 y 좌표
        player_y = ram[0x03B8]
        player_tile_position_x = (player_x + 8) // 16
        player_tile_position_y = (player_y + 8) // 16 - 1

        # 0x006E-0x0072	Enemy horizontal position in level
        # 자신이 속한 화면 페이지 번호
        enemy_horizon_position = ram[0x006E:0x0072 + 1]
        # 0x0087-0x008B	Enemy x position on screen
        # 자신이 속한 페이지 속 x 좌표
        enemy_screen_position_x = ram[0x0087:0x008B + 1]
        # 0x00CF-0x00D3	Enemy y pos on screen
        enemy_position_y = ram[0x00CF:0x00D3 + 1]
        # 적 x 좌표
        enemy_position_x = (enemy_horizon_position * 256 + enemy_screen_position_x) % 512

        # 적 타일 좌표
        enemy_tile_position_x = (enemy_position_x + 8) // 16
        enemy_tile_position_y = (enemy_position_y - 8) // 16 - 1

        enemy_drawn = ram[0x000F:0x0013 + 1]

        max_enemy = 5
        enemy_count = 0

        for drawn in range(max_enemy):
            if enemy_drawn[drawn] == 1:
                enemy_count += 1

        print(enemy_count)

        print(enemy_tile_position_x, enemy_tile_position_y)
        map_width = 32
        map_height = 13
        screen_width = 16
        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

        # 사각형 그리기
        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))

        for h in range(map_height):
            for w in range(map_width):
                painter.setBrush(QBrush(Qt.blue))
                painter.drawRect((screen_tile_offset + 16) % 32 * 15, h * 15, 15, 15)
                painter.setBrush(QBrush(Qt.blue))
                painter.drawRect(screen_tile_offset % 32 * 15, h * 15, 15, 15)
                painter.setBrush(QBrush(Qt.red))
                painter.drawRect((screen_tile_offset + player_tile_position_x) % 32 * 15, player_tile_position_y * 15, 15, 15)
                if full_screen_tiles[h][w] == 0:
                    painter.setBrush(QBrush(Qt.gray))
                    painter.drawRect(w * 15, (h * 15), 15, 15 )
                # 바닥 및 벽
                elif full_screen_tiles[h][w] != 0 and full_screen_tiles[h][w] != 194:
                    painter.setBrush(QColor(58, 134, 255))
                    painter.drawRect(w * 15, (h * 15), 15, 15 )
                # 그냥 골드
                elif full_screen_tiles[h][w] == 194:
                    painter.setBrush(QBrush(Qt.white))
                    painter.drawRect(w * 15, (h * 15), 15, 15)
        for count in range(enemy_count):
            painter.setBrush(QBrush(Qt.yellow))
            painter.drawRect(enemy_tile_position_x[count] * 15, enemy_tile_position_y[count] * 15, 15, 15)
        for h in range(map_height):
            for w in range(screen_width):
                painter.setBrush(QBrush(Qt.red))
                painter.drawRect(player_tile_position_x % 16 * 15, (player_tile_position_y * 15) + 200, 15, 15)
                if screen_tiles[h][w] == 0:
                    painter.setBrush(QBrush(Qt.gray))
                    painter.drawRect(w * 15, (h * 15) + 200, 15, 15 )
                # 바닥 및 벽
                elif screen_tiles[h][w] != 0 and screen_tiles[h][w] != 194:
                    painter.setBrush(QColor(58, 134, 255))
                    painter.drawRect(w * 15, (h * 15) + 200, 15, 15 )
                # 그냥 골드
                elif screen_tiles[h][w] == 194:
                    painter.setBrush(QBrush(Qt.white))
                    painter.drawRect(w * 15, (h * 15) + 200, 15, 15)

        painter.end()

    def update_screen(self):
        screen = self.env.get_screen()
        qimage = QImage(screen, screen.shape[1], screen.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(448, 480, Qt.IgnoreAspectRatio)
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
