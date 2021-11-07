# GUI
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QDesktopWidget, QGraphicsOpacityEffect

# System
import time
import winsound

# File
from backend_backup import Tile
T = Tile()

class Sets(QWidget):
    def __init__(cls):
        super().__init__()
        
    # 창 위치를 가운데로 배치
    def set_center(self):
        frame_info = self.frameGeometry()
        display_center = QDesktopWidget().availableGeometry().center()
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())
    
    # 버튼의 투명도를 정함
    def set_transparency(self, button : QPushButton, transparency : float):
        opacity_effect = QGraphicsOpacityEffect(button)
        opacity_effect.setOpacity(transparency)
        button.setGraphicsEffect(opacity_effect)

    # QLabel만 사용 할 수 있기에, set_object 함수로 QPushButton도 사용 할 수 있기에 각각 따로 만든다.
    # QLabel
    def set_label(self, image : QLabel, position_image : list[int], image_text : str, image_text_color : str, font_family : str, font_size : int, visible : bool = False):
        image.setGeometry(position_image[0], position_image[1], position_image[2], position_image[3])

        # 폰트 (Font)
        font = QFont()
        font.setFamily(font_family)
        font.setPointSize(font_size)
        font.setBold(True)
        image.setFont(font)

        image.setText(image_text)
        image.setStyleSheet('color : {};'.format(image_text_color.lower()))
        image.setAlignment(Qt.AlignCenter)

        image.setVisible(visible)

    # QPushButton
    def set_button(self, button : QPushButton, position_button : list[int], transparency : float, pressed_event, released_event, visible : bool = False):
        button.setGeometry(position_button[0], position_button[1], position_button[2], position_button[3])
        self.set_transparency(button, transparency)
        button.pressed.connect(pressed_event)
        button.released.connect(released_event)

        button.setVisible(visible)
    
    # 메뉴, 타일 등 모든 버튼을 배치
    def set_object(self, image : QLabel, image_text : str, image_text_color : str, font_family : str, font_size : int,
                   button : QPushButton, transparency : float, pressed_event, released_event, position : list[int], visible : bool = False):
        # Image
        self.set_label(image, position, image_text, image_text_color, font_family, font_size, visible)
        
        # Button
        self.set_button(button, position, transparency, pressed_event, released_event, visible)

class Events(QWidget):
    def __init__(cls):
        super().__init__()
    
    def the_init(cls, checker : QLabel, *all_object):
        FONT = QFont()
        FONT.setFamily('Times New Roman')
        FONT.setPointSize(100) # 왜냐면 이 함수를 쓸 QLabel들은 다 font_size가 100이기 떄문
        FONT.setBold(True)
        cls.setFont(FONT)

        cls.home = True
        cls.test = False
        cls.turn = 'HUMAN'

        cls.checker = checker

        cls.all_objects_list = []
        for _object in all_object:
            cls.all_objects_list.append(_object)
        
        T.init_Tile()
    
    def set_visible(self, *objects):
        for _object in self.all_objects_list:
            _object.setVisible(False)
        
        for _object in objects:
            _object.setVisible(True)

    def pressed_event(self, image : QLabel):
        winsound.Beep(293, 50)

        image.setStyleSheet('color : grey;')
    
    def released_event(self, image : QLabel, *visibles):
        time.sleep(0.05) # For saving motion

        image.setStyleSheet('color : black;')

        self.home = False

        self.set_visible(*visibles)

    # Start
    def released_start(self, image : QLabel, *visibles):
        self.released_event(image, *visibles)

    
    def pressed_pick(self, image : QLabel):
        winsound.Beep(493, 50)

        self.checker.setGeometry(image.geometry())

        self.checker.setVisible(True)
    
    def released_pick(self, image : QLabel, button : QPushButton, color : str):
        time.sleep(0.05)

        self.checker.setVisible(False)

        T.pick_random(1, color, self.turn)
        self.turn = self.turn = 'HUMAN' if self.turn == 'AI' else 'AI'

        if len(T.tiles_will_pick) == 0:
            image.setVisible(False)
            button.setVisible(False)
        
        print(T.order('human'), T.order('AI'))
    
    def INIT_TILE(self):
        T.init_Tile()
    
    # Setting
    def released_setting(self, image : QLabel, *visibles):
        self.released_event(image, *visibles)
    
    def pressed_test(self):
        winsound.Beep(261, 50)

    def released_test(self, image : QLabel, *visibles):
        self.set_visible(image, *visibles)

        if self.test == True:
            Sets().set_label(image, [340, 200, 330, 90], 'Unable', 'red', 'Times New Roman', 80, True)
            self.test = False

        elif self.test == False:
            Sets().set_label(image, [340, 200, 330, 90], 'Enable', 'green', 'Times New Roman', 80, True)
            self.test = True
        
        image.setAlignment(Qt.AlignCenter)
