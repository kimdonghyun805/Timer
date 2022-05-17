
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDesktopWidget, 
                             QAction, QToolBar, QVBoxLayout, QScrollArea,
                             QPushButton, QDialog, QLabel, QTextEdit, QLineEdit)
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtCore import QSize, QPoint, Qt, pyqtSignal

from Timer import Timer

# 메인 윈도우는 자체 레이아웃을 사용하여 레이아웃을 지정할 수 없음
# central widget이 필요하며, central widget에 레이아웃 지정
class MainWindow (QMainWindow) :
    saveSignal = pyqtSignal()

    def __init__(self, icon_list) :
        super().__init__(None, Qt.WindowTitleHint 
                         | Qt.WindowMinimizeButtonHint
                         | Qt.WindowCloseButtonHint
                         )

        self.main_width = 440
        self.main_height = 380
        self.main_min_height = 220
        self.window_title = "타이머"

        self.widget_width = 420
        self.widget_height = 12

        self.icon_list = icon_list
        self.icon_add = icon_list["add"]
        self.icon_save = icon_list["save"]
        self.icon_setting = icon_list["setting"]

        self.num_timer = 0
        self.timer_width = 400
        self.timer_height = 150
        self.timer_order = 1
        self.timer_dic = {}

        self.makeWindow()

        self.toolbar = self.makeToolbar()
        self.addToolBar(self.toolbar)

        self.scroll = QScrollArea()

        self.widget = self.makeWidget()

        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.main_font = QFont("Arial", 10, QFont.Bold) #12
        self.main_font.setPixelSize(16)

        (self.dialog_add, self.title_add, self.min_add, self.sec_add, self.ok_add) = self.makeTimerDialog()
        (self.dialog_edit, self.title_edit, self.min_edit, self.sec_edit, self.ok_edit) = self.makeTimerDialog()
        (self.dialog_delete, self.title_delete, self.ok_delete) = self.makeDeleteDialog()
        self.dialog_setting = self.makeSettingDialog()

    # 메인 윈도우 제작 관련 함수
    def makeWindow(self) :
        # 창을 모니터 중심으로 이동
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center() # 모니터 중앙의 정보 가져옴
        frame.moveCenter(center)

        # 창 설정
        self.setWindowTitle(self.window_title) # 창 이름 설정
        self.resize(QSize(self.main_width, self.main_height)) # 창 크기 설정
        self.setFixedWidth(self.main_width)
        self.setMinimumHeight(self.main_min_height)

    def makeToolbar(self) :
        # 툴바 - add, save 와 setting 버튼 존재
        action_add = QAction(self.icon_add, "새로운 타이머 추가", self)
        # 타이머 생성 시 기본값으로 New Timer, 0, 0 을 지정
        action_add.triggered.connect(self.execAddDialog)

        action_save = QAction(self.icon_save, "저장", self)
        action_save.triggered.connect(self.saveSignal.emit)

        action_setting = QAction(self.icon_setting, "설정", self)
        action_setting.triggered.connect(self.execSettingDialog)

        icon_size = 40
        toolbar = QToolBar("도구 모음")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(icon_size, icon_size))
        toolbar.addAction(action_add)
        toolbar.addSeparator()
        toolbar.addAction(action_save)
        toolbar.addSeparator()
        toolbar.addAction(action_setting)

        return toolbar

    def makeScrollWidget (self) :
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setEnabled(True)
        return scroll

    def makeWidget(self) :
        widget = QWidget()
        widget.resize(QSize(self.widget_width, self.widget_height))
        widget.setFixedWidth(self.widget_width)
        widget.setFixedHeight(self.widget_height)
        return widget


    # add, edit 수행을 위한 다이얼로그 관련 함수
    def makeTimerDialog (self) :
        
        dialog = QDialog(None, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("dialog")
        dialog.setFixedSize(300, 200)

        label_title = QLabel("타이머 이름   :", dialog)
        label_title.setFont(self.main_font)
        label_title.move(30, 30)

        text_title = QLineEdit("", dialog)
        text_title.setFont(self.main_font)
        text_title.setFixedSize(100, 30)
        text_title.setMaxLength(15)
        text_title.move(150, 25)

        label_min = QLabel("분   :", dialog)
        label_min.setFont(self.main_font)
        label_min.move(30, 80)

        text_min = QLineEdit("", dialog)
        text_min.setFont(self.main_font)
        text_min.setFixedSize(40, 30)
        text_min.setMaxLength(3)
        text_min.setValidator(QIntValidator(0, 999, self))
        text_min.move(80, 75)

        label_sec = QLabel("초   :", dialog)
        label_sec.setFont(self.main_font)
        label_sec.move(150, 80)

        text_sec = QLineEdit("", dialog)
        text_sec.setFont(self.main_font)
        text_sec.setFixedSize(40, 30)
        text_sec.setMaxLength(2)
        text_sec.setValidator(QIntValidator(0, 59, self))
        text_sec.move(200, 75)

        button_ok = QPushButton("확인", dialog)
        button_ok.setFont(self.main_font)
        button_ok.setFixedSize(100, 30)
        button_ok.move(70, 150)

        button_cancel = QPushButton("취소", dialog)
        button_cancel.setFont(self.main_font)
        button_cancel.setFixedSize(100, 30)
        button_cancel.move(180, 150)

        text_min.textChanged.connect(lambda : self.valueValidationCheck(text_min, 1000))
        text_sec.textChanged.connect(lambda : self.valueValidationCheck(text_sec, 60))
        button_cancel.clicked.connect(dialog.close)

        return (dialog, text_title, text_min, text_sec, button_ok)

    def execAddDialog (self) :
        if self.num_timer >= 10 :
            print("더 이상 타이머를 추가할 수 없음")
        else :
            frame = self.frameGeometry()
            pos = frame.topLeft()
            pos.setX(pos.x() + 50)
            pos.setY(pos.y() + 50)
            self.dialog_add.move(pos)

            self.dialog_add.setWindowTitle("새로운 타이머 추가")
            self.title_add.setText("타이머 " + str(self.timer_order))
            self.min_add.setText("0")
            self.sec_add.setText("0")
            self.ok_add.disconnect() # 기존의 연결된 함수 제거
            self.ok_add.clicked.connect(lambda : self.addExecution(self.dialog_add, self.title_add, self.min_add, self.sec_add))

            self.dialog_add.exec()

    def execEditDialog (self, order) :
        frame = self.frameGeometry()
        pos = frame.topLeft()
        pos.setX(pos.x() + 50)
        pos.setY(pos.y() + 50)
        self.dialog_edit.move(pos)

        timer = self.timer_dic[order][1]
        title = timer.getName()
        (min, sec) = timer.getTime()

        self.dialog_edit.setWindowTitle("타이머 수정")
        self.title_edit.setText(title)
        self.min_edit.setText(str(min))
        self.sec_edit.setText(str(sec))
        self.ok_edit.disconnect() # 기존의 연결된 함수 제거
        self.ok_edit.clicked.connect(lambda : self.editExecution(self.dialog_edit, self.title_edit, self.min_edit, self.sec_edit, timer))

        self.dialog_edit.exec()
        

    # delete 수행을 위한 다이얼로그 함수
    def makeDeleteDialog (self) :
        dialog = QDialog(None, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("타이머 삭제")
        dialog.setFixedSize(300, 150)

        label_title = QLabel("Timer Name", dialog)
        label_title.setFont(self.main_font)
        label_title.move(20, 20)

        label_question = QLabel("타이머를 삭제하시겠습니까?", dialog)
        label_question.setFont(self.main_font)
        label_question.move(40, 55)

        button_ok = QPushButton("확인", dialog)
        button_ok.setFont(self.main_font)
        button_ok.setFixedSize(100, 30)
        button_ok.move(70, 100)

        button_cancel = QPushButton("취소", dialog)
        button_cancel.setFont(self.main_font)
        button_cancel.setFixedSize(100, 30)
        button_cancel.move(180, 100)

        button_cancel.clicked.connect(dialog.close)

        return (dialog, label_title, button_ok)

    def execDeleteDialog(self, order) :
        frame = self.frameGeometry()
        pos = frame.topLeft()
        pos.setX(pos.x() + 50)
        pos.setY(pos.y() + 50)
        self.dialog_delete.move(pos)

        timer = self.timer_dic[order][1]
        title = timer.getName()
        title_len = len(title)
        title = "\"" + title + "\""
        self.title_delete.setText(title)
        self.title_delete.adjustSize()

        if title_len in range(14, 16) :
            self.title_delete.move(20, 20)
        elif title_len in range(10, 14) :
            self.title_delete.move(50, 20)
        elif title_len in range(5, 10) :
            self.title_delete.move(80, 20)
        else :
            self.title_delete.move(110, 20)

        self.ok_delete.disconnect()
        self.ok_delete.clicked.connect(lambda : self.deleteExecution(self.dialog_delete, order))

        self.dialog_delete.exec()


    def makeSettingDialog (self) :
        dialog = QDialog(None, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("설정")
        dialog.setFixedSize(300, 270)

        label_a = QLabel("배포일 : 22.02.24", dialog)
        label_a.setFont(self.main_font)
        label_a.move(20, 235)

        label_b = QLabel("주의 사항", dialog)
        label_b.setFont(self.main_font)
        label_b.move(20, 10)

        label_c = QLabel("1. 설정 가능한 최대 시간은 999:59", dialog)
        label_c.setFont(self.main_font)
        label_c.move(20, 40)

        label_d = QLabel("2. 타이머는 최대 10개 까지 생성됨", dialog)
        label_d.setFont(self.main_font)
        label_d.move(20, 65)

        label_e = QLabel("3. 진행중인 타이머는 파란색,\n    10초 이하로 남은 타이머는\n    빨간색으로 표시", dialog)
        label_e.setFont(self.main_font)
        label_e.move(20, 90)

        label_f = QLabel("4. 프로그램 시작시 자동으로\n    저장 데이터를 불러옴", dialog)
        label_f.setFont(self.main_font)
        label_f.move(20, 155)

        label_g = QLabel("5. 자동으로 저장되지 않음", dialog)
        label_g.setFont(self.main_font)
        label_g.move(20, 200)

        button_cancel = QPushButton("닫기", dialog)
        button_cancel.setFont(self.main_font)
        button_cancel.setFixedSize(100, 30)
        button_cancel.move(180, 230)

        button_cancel.clicked.connect(dialog.close)
        return dialog

    def execSettingDialog (self) :
        frame = self.frameGeometry()
        pos = frame.topLeft()
        pos.setX(pos.x() + 50)
        pos.setY(pos.y() + 50)
        self.dialog_setting.move(pos)

        self.dialog_setting.exec()

    # 다이얼로그를 통해 결정된 add, edit, delete를 수행하는 함수
    def addExecution(self, dialog, title_edit, min_edit, sec_edit) :
        title = title_edit.text()
        if not title : 
            title = "이름 없음"
        elif len(title) > 15 :
            title = title[0:15]

        min = min_edit.text()
        if not min : min = 0
        else : min = int(min)
        if min >= 1000 : min = 999
        elif min < 0 : min = 0

        sec = sec_edit.text()
        if not sec : sec = 0
        else : sec = int(sec)
        if sec >= 60 : sec = 59
        elif sec < 0 : sec = 0

        self.addTimer(title, min, sec, self.timer_order)
        dialog.close()

    def editExecution (self, dialog, title_edit, min_edit, sec_edit, timer) :
        title = title_edit.text()
        if not title : 
            title = "이름 없음"
        elif len(title) > 15 :
            title = title[0:15]

        min = min_edit.text()
        if not min : min = 0
        else : min = int(min)
        if min >= 1000 : min = 999
        elif min < 0 : min = 0

        sec = sec_edit.text()
        if not sec : sec = 0
        else : sec = int(sec)
        if sec >= 60 : sec = 59
        elif sec < 0 : sec = 0

        if timer.time_thread.is_playing :
            timer.timerPause()
        timer.setName(title)
        timer.setTime(min, sec)
        print("타이머 수정 :", title, timer.order)
        dialog.close()

    def deleteExecution (self, dialog, order) :
        self.deleteTimer(order)
        dialog.close()

    def valueValidationCheck(self, text_edit, top) :
        if text_edit :
            val = text_edit.text()
            if not val :
                val = 0
            else :
                val = int(val)
            if val >= top :
                val = top - 1
                text_edit.setText(str(val))


    # add, delete 수행 마다 central widget의 크기를 조정하는 함수
    def setWidgetHeight(self, height) :
        self.widget_height = height
        self.widget.setFixedSize(QSize(self.widget_width, self.widget_height))


    # 실제 add, delete 연산을 수행하는 함수
    def addTimer(self, name, min, sec, order) :
        if self.num_timer >= 10 :
            print("더 이상 타이머를 추가할 수 없음 :", name)
        else :
            self.num_timer += 1
            # timer_dic은 index를 order로 가지며 (name, timer object) 형태의 튜플로 구성
            timer = Timer(name, order, min, sec, self.icon_list)
            timer_name = timer.getName()
            timer_order = timer.getOrder()
            self.timer_dic[timer_order] = (timer_name, timer)
            self.timer_order += 1

            self.setWidgetHeight(self.widget_height + self.timer_height)
            self.layout.addWidget(timer)

            timer.deleteSignal.connect(lambda : self.execDeleteDialog(timer_order))
            timer.editSignal.connect(lambda : self.execEditDialog(timer_order))
            print("타이머 추가 :", timer_name, timer_order)


    def deleteTimer (self, order) :
        if self.num_timer <= 0 :
            print("제거할 타이머가 없음")
        else :
            if order not in self.timer_dic :
                print("제거할 타이머가 존재하지 않음 :", order)
            else :
                self.timer_dic[order][1].deleteWidget()
                self.layout.removeWidget(self.timer_dic[order][1])
                self.setWidgetHeight(self.widget_height - self.timer_height)

                del self.timer_dic[order]
                self.num_timer -= 1
                print("타이머 제거 :", order)


    # 현재 프로그램의 설정 정보를 전달하는 함수 - 저장 기능에 사용
    def getInfo (self) :
        timer_info = []
        if self.timer_dic :
            for t_order, timer in self.timer_dic.items() :
                name = timer[1].getName()
                order = timer[1].getOrder()
                (min, sec) = timer[1].getTime()

                timer_info.append({"name":name, "order":order, "min":min, "sec":sec})

        return (self.num_timer, self.timer_order, timer_info)
