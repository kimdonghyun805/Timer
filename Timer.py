import sys
import time

from PyQt5.QtWidgets import (QWidget, QGroupBox, QGridLayout, QLabel, QAction,
                             QPushButton)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QThread

class Timer (QGroupBox) :
    deleteSignal = pyqtSignal()
    editSignal = pyqtSignal()

    def __init__ (self, name, order, min, sec, icon_list) :
        super().__init__()

        self.name = name # string type
        self.order = order # int type

        self.weight = 400
        self.height = 150

        # 타이머에게 설정된 분, 초
        self.origin_min = min # int type
        self.origin_sec = sec # int type

        # 타이머가 작동을 시작한 분, 초
        self.start_min = min
        self.start_sec = sec
        # 현재 타이머에 표시되는 분, 초
        self.now_min = min
        self.now_sec = sec

        self.icon_delete = icon_list["delete"]
        self.icon_edit = icon_list["edit"]
        self.icon_pause = icon_list["pause"]
        self.icon_play = icon_list["play"]
        self.icon_refresh = icon_list["refresh"]

        self.title_font = QFont("Arial", 10, QFont.Bold) #15
        self.title_font.setPixelSize(20)
        self.time_font = QFont("Arial", 10, QFont.ExtraBold) #50
        self.time_font.setPixelSize(70)

        self.color_black = "Color : black"
        self.color_red = "Color : red"
        self.color_blue = "Color : blue"
        self.color_gray = "Color : gray"
        self.default_color = self.color_black
        self.accent_color = self.color_red
        self.playing_color = self.color_blue
        self.accent_bound = 10

        self.setFixedSize(QSize(self.weight, self.height))
        #self.setStyleSheet("border-style : solid;"
        #                   "border-width : 2px;"
        #                   "border-color : #000000;")

        self.time_thread = TimeThread()
        self.time_thread.passTimeSignal.connect(self.timeAdjustment)

        self.title = self.makeTitle(self.name)
        (self.min, self.sec) = self.makeTime(self.origin_min, self.origin_sec)

        self.button_delete = self.makeDelete()
        self.button_play = self.makePlay()
        self.button_pause = self.makePause()
        self.button_refresh = self.makeRefresh()
        self.button_edit = self.makeEdit()

        self.button_play.clicked.connect(self.timerPlay)
        self.button_pause.clicked.connect(self.timerPause)
        self.timerPause()

        self.button_delete.clicked.connect(self.deleteSignal.emit)
        self.button_edit.clicked.connect(self.editSignal.emit)
        self.button_refresh.clicked.connect(self.timerRefresh)

       
    def makeGrid (self) :
        grid = QGridLayout()
        return grid
        
    def makeTitle (self, name) :
        # 타이틀 객체 생성하여 리턴
        title = QLabel(name, self)
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet(self.default_color)
        title.move(15, 15)
        
        return title

    def makeTime (self, min, sec) :
        min = QLabel(str(min) + ":", self)
        min.setFont(self.time_font)
        min.setAlignment(Qt.AlignRight)
        min.setStyleSheet(self.default_color)
        min.resize(160, 70)
        min.move(20, 50)

        sec = QLabel(str(sec), self)
        sec.setFont(self.time_font)
        sec.setAlignment(Qt.AlignRight)
        sec.setStyleSheet(self.default_color)
        sec.resize(120, 70)
        sec.move(140, 50)

        return (min, sec)
        
    
    def makeDelete (self) :
        button_delete = QPushButton("", self)
        button_delete.setIcon(self.icon_delete)
        button_delete.setIconSize(QSize(30, 30))
        button_delete.move(340, 10)
        button_delete.setToolTip("이 타이머를 삭제합니다.")
        return button_delete

    def makePlay (self) :
        button_play = QPushButton("", self)
        button_play.setIcon(self.icon_play)
        button_play.setIconSize(QSize(80, 30))
        button_play.move(290, 55)
        button_play.setToolTip("타이머를 재생합니다.")
        return button_play

    def makePause (self) :
        button_pause = QPushButton("", self)
        button_pause.setIcon(self.icon_pause)
        button_pause.setIconSize(QSize(80, 30))
        button_pause.move(290, 55)
        button_pause.setToolTip("타이머를 정지합니다.")
        return button_pause

    def makeRefresh (self) :
        button_refresh = QPushButton("", self)
        button_refresh.setIcon(self.icon_refresh)
        button_refresh.setIconSize(QSize(30, 30))
        button_refresh.move(290, 100)
        button_refresh.setToolTip("타이머를 초기화 합니다.")
        return button_refresh

    def makeEdit (self) :
        button_edit = QPushButton("", self)
        button_edit.setIcon(self.icon_edit)
        button_edit.setIconSize(QSize(30, 30))
        button_edit.move(340, 100)
        button_edit.setToolTip("타이머의 정보를 수정합니다.")
        return button_edit


    def timerPlay (self) :
        if (self.now_min == 0) and (self.now_sec == 0) :
            return
        else :
            self.button_play.setDisabled(True)
            self.button_play.hide()

            self.start_min = self.now_min
            self.start_sec = self.now_sec
            # 남은 시간이 accent_bount 초 이하인 경우, 분, 초를 강조색으로 변경
            if (self.now_min == 0) and (self.now_sec <= self.accent_bound) :
                self.min.setStyleSheet(self.accent_color)
                self.sec.setStyleSheet(self.accent_color)
            else :
                # 아닌 경우, 분, 초를 진행색으로 변경
                self.min.setStyleSheet(self.playing_color)
                self.sec.setStyleSheet(self.playing_color)

            self.time_thread.threadStart()

            self.button_pause.setEnabled(True)
            self.button_pause.show()

    def timerPause (self) :
        self.button_pause.setDisabled(True)
        self.button_pause.hide()
        
        self.time_thread.threadStop()

        self.button_play.setEnabled(True)
        self.button_play.show()

    def timerRefresh (self) :
        if self.time_thread.is_playing :
            self.timerPause()
        self.setTime(self.origin_min, self.origin_sec)


    # 쓰레드의 passTimeSignal에 의해 실행되는 함수
    def timeAdjustment (self, passed_time) :
        # start time에서 passed time 만큼 흐른 시간을 now time으로 설정
        start_time = 60 * self.start_min + self.start_sec
        now_time = start_time - passed_time
        if now_time < 0 :
            now_time = 0
        min = now_time // 60
        sec = now_time % 60
        self.now_min = min
        self.now_sec = sec
        self.min.setText(str(self.now_min) + ":")
        self.sec.setText(str(self.now_sec))
        # 남은시간이 accent_bound 초 이하인 경우, 분, 초를 강조색으로 변경
        if (min == 0) and (sec == self.accent_bound) :
            self.min.setStyleSheet(self.accent_color)
            self.sec.setStyleSheet(self.accent_color)
        # 시간이 모두 흐른 경우, 타이머를 중지
        if (self.now_min == 0) and (self.now_sec == 0) :
            self.timerPause()


    # 타이머 정보를 전달하는 함수
    def getName(self) :
        return self.name

    def getTime(self) :
        return (self.origin_min, self.origin_sec)

    def getOrder(self) :
        return self.order


    def setName(self, name) :
        # 타이머의 이름을 변경
        self.name = name
        self.title.setText(self.name)
        self.title.adjustSize()

    def setTime (self, min, sec) :
        # 타이머의 분, 초를 변경
        self.origin_min = min
        self.origin_sec = sec
        self.start_min = min
        self.start_sec = sec
        self.now_min = min
        self.now_sec = sec
        self.min.setText(str(self.origin_min) + ":")
        self.sec.setText(str(self.origin_sec))
        # 분, 초를 검은색으로 변경
        self.min.setStyleSheet(self.default_color)
        self.sec.setStyleSheet(self.default_color)


    def deleteWidget(self) :
        # 위젯 삭제
        self.title.deleteLater()
        self.min.deleteLater()
        self.sec.deleteLater()
        # 객체 및 리스트 삭제
        del self.icon_delete
        del self.icon_edit
        del self.icon_pause
        del self.icon_play
        del self.icon_refresh

        del self.button_delete
        del self.button_edit
        del self.button_pause
        del self.button_play
        del self.button_refresh

        del self.title_font
        del self.time_font
        # 쓰레드 중지 및 삭제
        if self.time_thread.is_playing :
            self.time_thread.threadStop()
        del self.time_thread
        # 타이머 본체 삭제
        self.deleteLater()
        del self



class TimeThread (QThread) :

    passTimeSignal = pyqtSignal(int) # 인자로 지난 시간을 전달 

    def __init__(self) :
        super().__init__()

        self.is_playing = False

        self.start_time = 0 # 타이머를 시작한 시점의 시간, 실행마다 초기화
        self.passed_time = 0 # 타이머 시작 이후 지난 시간, 실행마다 초기화


    def run(self) :
        while self.is_playing :
            now_time = time.time()
            t = int(now_time - self.start_time)

            if self.passed_time != t :
                self.passed_time = t
                # 흐른 시간의 초 단위가 변한 경우 시그널을 발생하여 알림
                self.passTimeSignal.emit(self.passed_time)

            time.sleep(0.1)


    def threadStart (self) :
        self.is_playing = True
        self.start_time = time.time()
        self.passed_time = 0
        self.start()

    def threadStop (self) :
        self.is_playing = False
        self.passed_time = 0
        self.quit()

