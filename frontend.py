# Github
# https://github.com/Werp1n/Davinci_Code.git

# GUI
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeyEvent, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QApplication

# System
import sys
import winsound

# Files
from backend import Tile
from event import Sets, Events

class Win(Tile, Sets, Events):
    def __init__(cls):
        super().__init__()

        super().init_Tile()

        cls.init_UI()
        
        entity_list = [cls.start_image, cls.start_button, cls.rule_image, cls.rule_button, 
                         cls.setting_image, cls.setting_button, cls.test_able_image_text, cls.test_able_image_able, cls.test_able_button, 
                         cls.black_pick_tile, cls.black_pick_tile_button, cls.white_pick_tile, cls.white_pick_tile_button]

        for _value in cls.tile_bundle.values():
            for _item in _value:
                entity_list.append(_item)
            
        super().the_init(cls.checker, *entity_list)

    # 창 초기화
    def init_UI(cls):
        cls.setWindowFlags(Qt.FramelessWindowHint) # 창 조절바 없애기

        cls.resize(720, 1000) # 라벨을 가운데로 맞추는 식 - 가로 : 360 - [( 라벨의 가로 크기 ) / 2]
        cls.set_center()

		# 안에서 처리하는데 필요한 변수
        cls.fullscreen = 0

        # 바탕 화면 로드 & 배치
        cls.background = QLabel(cls)
        cls.background.setPixmap(QPixmap('background'))

        # 모든 세팅 함수 호출
        cls.set_all_buttons()

        cls.checker = QLabel(cls)
        cls.checker.setPixmap(QPixmap('checker'))
        cls.checker.setVisible(False)

        cls.show()
        
    def set_all_buttons(self):
        self.set_start_button()
        self.set_rule_button()
        self.set_setting_button()

    def set_start_button(self):
        self.start_image = QLabel(self)
        self.start_button = QPushButton('', self)

        self.set_object(self.start_image, 'S t a r t', 'black', 'Times New Roman', 100, self.start_button, 0.0, 
                        lambda : self.pressed_event(self.start_image), lambda : self.released_start(self.start_image, 
                        self.black_pick_tile, self.black_pick_tile_button, self.white_pick_tile, self.white_pick_tile_button), [125, 70, 470, 100], True)

        # Pick Tile
        self.black_pick_tile = QLabel(self)
        self.black_pick_tile.setPixmap(QPixmap('black_tile'))

        self.black_pick_tile_button = QPushButton('', self)

        self.set_object(self.black_pick_tile, '', '', '', 1, self.black_pick_tile_button, 0.0, 
                        lambda : self.pressed_pick(self.black_pick_tile), 
                        lambda : self.released_pick(self.black_pick_tile, self.black_pick_tile_button, 'B'), [5, 430, 110, 140], False)
        
        self.white_pick_tile = QLabel(self)
        self.white_pick_tile.setPixmap(QPixmap('white_tile'))

        self.white_pick_tile_button = QPushButton('', self)

        self.set_object(self.white_pick_tile, '', '', '', 1, self.white_pick_tile_button, 0.0,
                        lambda : self.pressed_pick(self.white_pick_tile),
                        lambda : self.released_pick(self.white_pick_tile, self.white_pick_tile_button, 'W'), [605, 430, 110, 140], False)
        
        # All Tiles
        self.tile_bundle = {'black' : [], 'white': [], 'black_text' : [], 'white_text' : []}
        colors = (('black', 'white'), ('white', 'black'))
        #               black                white

        for i in range(0, 24): # -> 24까지 루프인 이유 : 0 ~ 11까지 타일이 2개(검정, 하양)가 있기 때문에 12 * 2 = 24.
            COLOR = colors[i % 2]
            TEXT = COLOR[0] + '_text'

            # Image
            image_label = QLabel(self)
            self.set_label(image_label, [5 + 120 * (i % 6), 200 + (i // 6) * 170, 110, 140], '', '', '', 1, True)
            image_label.setPixmap(QPixmap('{}_tile'.format(COLOR[0])))

            image_label.setVisible(False)

            # Text
            text_label = QLabel(self)
            self.set_label(text_label, [5 + 120 * (i % 6), 200 + (i // 6) * 170, 110, 140], str(i // 2), COLOR[1], '맑은 고딕', 40, True)

            text_label.setVisible(False)

            self.tile_bundle[COLOR[0]].append(image_label)
            self.tile_bundle[TEXT].append(text_label)

    def set_rule_button(self):
        self.rule_image = QLabel(self)
        self.rule_button = QPushButton('', self)

        self.set_object(self.rule_image, 'R u l e', 'black', 'Times New Roman', 100, self.rule_button, 0.0, 
                        lambda : self.pressed_event(self.rule_image), self.none_event, [160, 400, 400, 100], True)

    def set_setting_button(self):
        self.setting_image = QLabel(self)
        self.setting_button = QPushButton('', self)

        self.set_object(self.setting_image, 'S e t t i n g', 'black', 'Times New Roman', 100, self.setting_button, 0.0, 
                        lambda : self.pressed_event(self.setting_image), lambda : self.released_setting(self.setting_image, self.test_able_image_text, 
                                                                        self.test_able_image_able, self.test_able_button), [60, 740, 600, 160], True)
        
        self.test_able_image_text = QLabel(self)
        self.test_able_image_able = QLabel(self)

        self.test_able_button = QPushButton('', self)

        self.set_label(self.test_able_image_text, [60, 200, 300, 90], 'Test : ', 'black', 'Times New Roman', 80, False)
        self.set_object(self.test_able_image_able, 'Unable', 'red', 'Times New Roman', 80, self.test_able_button, 0.0, 
                        self.pressed_test, lambda : self.released_test(self.test_able_image_able, self.test_able_image_text, self.test_able_button), [340, 200, 330, 90], False)
    
    def keyPressEvent(self, e : QKeyEvent):
        if e.key() == Qt.Key_Escape:
            if self.home == True:
                # Quit
                winsound.Beep(345, 50)

                print("Closed")

                self.close()

            else:
                # Home
                winsound.Beep(293, 50)

                self.home = True

                self.set_visible(self.start_image, self.start_button, self.rule_image, self.rule_button, self.setting_image, self.setting_button)

                self.INIT_TILE()
        
        elif e.key() == Qt.Key_F11:
            if self.fullscreen == 0:
                self.showFullScreen()
                self.fullscreen = 1
            else:
                self.showNormal()
                self.fullscreen = 0
        
    def none_event(self):
        self.home = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()

    sys.exit(app.exec_())
