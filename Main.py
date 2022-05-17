import os
import sys
import pickle

from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget)
from PyQt5.QtGui import QIcon, QFont

from Window import MainWindow


def checkFolder (path) :
    if path :
        print("폴더 확인 :", path)
        if not os.path.exists(path) :
            print("폴더가 존재하지 않음, 프로그램 종료")
            sys.exit(0)
        else :
            print("폴더가 존재 :", path)
    else :
        print("경로가 지정되지 않음, 프로그램 종료")
        sys.exit(0)


def checkIcon (icon_path, icon_type) :
    try :
        file_list = os.listdir(icon_path)
        icon_list = list(b for b in file_list if b.endswith(icon_type))
    except :
        print("아이콘 폴더 접근 불가능, 프로그램 종료")
        sys.exit(0)

    # 아이콘 이미지가 모두 존재하는지 확인
    # 필요 버튼 (8) : add, delete, edit, pause, play, refresh, save, setting
    requiring_icon = ["add", "delete", "edit", "pause", "play", "refresh", "save", "setting"]
    lost_icon = []
    for name in requiring_icon :
        name = name + icon_type
        if not name in icon_list :
            lost_icon.append(name)

    # 이미지가 없는 아이콘이 있는 경우 종료
    if lost_icon :
        print("아이콘 이미지 손실, 프로그램 종료", lost_icon)
        sys.exit(0)

    # 아이콘의 주소를 딕셔너리로 저장
    icon_location = {}
    for name in requiring_icon :
        location = icon_path + "\\" + name + icon_type
        icon_location[name] = location

    del lost_icon
    del requiring_icon
    del icon_list
    del file_list
    return icon_location


def loadIcon (icon_loc) :
    icon_list = {}

    icon_add = QIcon(icon_loc["add"])
    icon_delete = QIcon(icon_loc["delete"])
    icon_edit = QIcon(icon_loc["edit"])
    icon_pause = QIcon(icon_loc["pause"])
    icon_play = QIcon(icon_loc["play"])
    icon_refresh = QIcon(icon_loc["refresh"])
    icon_save = QIcon(icon_loc["save"])
    icon_setting = QIcon(icon_loc["setting"])

    icon_list["add"] = icon_add
    icon_list["delete"] = icon_delete
    icon_list["edit"] = icon_edit
    icon_list["pause"] = icon_pause
    icon_list["play"] = icon_play
    icon_list["refresh"] = icon_refresh
    icon_list["save"] = icon_save
    icon_list["setting"] = icon_setting

    return icon_list


def checkWindowIcon (icon_path, icon_type) :
    try :
        file_list = os.listdir(icon_path)
        icon_list = list(b for b in file_list if b.endswith(icon_type))
    except :
        print("아이콘 폴더 접근 불가능, 프로그램 종료")
        sys.exit(0)

    path = ""
    name = "timer" + icon_type

    # 윈도우 아이콘 이미지 timer.ico가 존재하는지 확인
    if name not in icon_list :
        # 윈도우 아이콘이 없는 경우 프로그램 종료
        print("윈도우 아이콘 이미지 손실, 프로그램 종료", name)
        sys.exit(0)
    else :
        path = icon_path + "\\" + name
    
    return path


def saveInfo (folder_path, file_name, file_type, main_window) :
    savefile_path = folder_path + "\\" + file_name + file_type
    savefile = None

    if folder_path :
        if not os.path.exists(savefile_path) :
            try :
                # 기존 저장 파일이 없으므로, 새로운 저장 파일 생성
                savefile = open(savefile_path, "wb")
                print("저장 파일 생성 :", savefile_path)
            except :
                if savefile :
                    savefile.close()
                print("저장 파일 생성 불가능, 실행 종료")
                return
        else :
            try :
                # 기존 저장 파일 내용을 비우고 쓰기모드로 열기
                savefile = open(savefile_path, "wb")
                print("기존 저장 파일 존재, 파일을 덮어 씀")
            except :
                if savefile :
                    savefile.close()
                print("저장 파일을 열 수 없음, 실행 종료")
                return
    else :
        print("저장 파일 경로가 지정되지 않음, 실행 종료")
        return

    # 타이머의 정보 가져오기
    (timer_num, timer_order, timer_info) = main_window.getInfo()

    #print("save file info")
    #print("timer_num :", timer_num)
    #print("timer_order :", timer_order)
    #print("timer_info :", timer_info)

    try :
        pickle.dump(timer_num, savefile)
        pickle.dump(timer_order, savefile)
        pickle.dump(timer_info, savefile)
        print("파일 저장 완료 :", savefile_path)
        savefile.close()
    except :
        if savefile :
            savefile.close()
        print("파일 덤프 불가능, 프로그램 종료")
        sys.exit(0)


def loadInfo (folder_path, file_name, file_type, main_window) :
    savefile_path = folder_path + "\\" + file_name + file_type
    savefile = None

    if folder_path :
        if not os.path.exists(savefile_path) :
            try :
                # 기존 저장 파일이 없으므로, 실행 종료
                print("저장 파일이 없음, 실행 종료 :", savefile_path)
                return
            except :
                print("저장 파일 접근 불가능, 실행 종료")
                return
        else :
            try :
                # 기존 저장 파일을 열기
                savefile = open(savefile_path, "rb")
                print("저장 파일 접근 성공")
            except :
                if savefile :
                    savefile.close()
                print("저장 파일을 열 수 없음, 프로그램 종료")
                return
    else :
        print("저장 파일 경로가 지정되지 않음, 프로그램 종료")
        sys.exit(0)

    try :
        timer_num = pickle.load(savefile)
        timer_order = pickle.load(savefile)
        timer_info = pickle.load(savefile)
        print("저장 파일 불러오기 성공")
        savefile.close()
    except :
        if savefile :
            savefile.close()
        print("파일 불러오기 불가능, 프로그램 종료")
        return

    #print("load file info")
    #print("timer_num :", timer_num)
    #print("timer_order :", timer_order)
    #print("timer_info :", timer_info)
    
    invalid = 0 # 데이터 손상을 확인하는 변수, invalid가 0 이면 오류 없음

    # num은 timer_info의 요소 개수와 같아야 함
    if type(timer_num) is int :
        if type(timer_info) is list :
            if len(timer_info) != timer_num :
                print("저장 파일 손상됨, num - 1")
                invalid += 1
        else :
            print("저장 파일 손상됨, num - 2")
            invalid += 1
    else :
        print("저장 파일 손상됨, num - 3")
        invalid += 1

    # order는 0 이하일 수 없음
    if type(timer_order) is int :
        if timer_order <= 0 :
            print("저장 데이터가 손상됨, order - 1")
            invalid += 1
    else :
        print("저장 데이터가 손상됨, order - 2")
        invalid += 1

    # 각 타이머의 정보를 확인
    for info in timer_info :
        # name은 0자 이하, 15자 초과할 수 없음
        if type(info["name"]) is str :
            length = len(info["name"])
            if (length <= 0) or (length > 15) :
                print("저장 데이터가 손상됨, info - name - 1")
                invalid += 1
        else :
            print("저장 데이터가 손상됨, info - name - 2")
            invalid += 1

        # 각 타이머의 order는 메인의 order 보다 크거나 같을 수 없음
        if type(info["order"]) is int :
            if info["order"] >= timer_order :
                print("저장 데이터가 손상됨, info - order - 1")
                invalid += 1
        else :
            print("저장 데이터 손상됨, info - order - 2")
            invalid += 1
        
        # min은 0 미만이면서 1000 이상일 수 없음
        if type(info["min"]) is int :
            if (info["min"] < 0) or (info["min"] >= 1000) :
                print("저장 데이터 손상됨, info - min - 1")
                invalid += 1
        else : 
            print("저장 데이터 손상됨, info - min - 2")
            invalid += 1

        # sec은 0 미만이면서 60 이상일 수 없음
        if type (info["sec"]) is int :
            if (info["sec"] < 0) or (info["sec"] >= 60) :
                print("저장 데이터 손상됨, info - sec - 1")
                invalid += 1
        else :
            print("저장 데이터 손상됨, info - sec - 2")
            invalid += 1

    if invalid != 0 :
        print("저장 데이터 손상 총", invalid, "개 확인됨, 실행 종료")
        return
    else :
        print("저장 데이터 손상 없음")

    # 불러온 데이터를 메인윈도우에 적용
    for info in timer_info :
        main_window.addTimer(info["name"], info["min"], info["sec"], info["order"])
        
    main_window.timer_order = timer_order

    if main_window.num_timer != timer_num :
        print("타이머 개수 불일치, ", main_window.num_timer, timer_num)
    else :
        print("타이머 개수 일치, ", main_window.num_timer, timer_num)


if __name__ == "__main__" :

    # C 드라이브 내에 리소스 생성시 경로
    #resource_path = "C:\\Timer"

    # 실행파일과 같은 파일에 리소스 생성시 경로
    resource_path = "resource"

    icon_path = resource_path + "\\icon"
    #font_path = resource_path + "\\font"
    savefolder_path = resource_path

    icon_type = ".png"
    savefile_name = "savefile"
    savefile_type = ".bin" #.p

    checkFolder(resource_path)
    checkFolder(icon_path)
    #checkFolder(font_path)
    #checkFolder(savefile_path) # 리소스 폴더와 경로가 같으므로 현재는 사용하지 않음

    # 아이콘 확인
    icon_location = checkIcon(icon_path, icon_type)
    # 윈도우 아이콘 확인
    window_icon_location = checkWindowIcon(icon_path, ".ico")
    
    # 창 띄우기
    window = QApplication(sys.argv)
    
    # 아이콘 로딩
    icon_list = loadIcon(icon_location)

    # 윈도우 아이콘 생성
    window_icon = QIcon(window_icon_location)

    # 메인 윈도우 제작 및 화면에 표시
    main = MainWindow(icon_list)
    main.setWindowIcon(window_icon)
    #main.show()
    
    # 저장 파일 확인 후 불러오기
    loadInfo(savefolder_path, savefile_name, savefile_type, main)

    # 저장 시그널과 저장 함수 연결
    main.saveSignal.connect(lambda : saveInfo(savefolder_path, savefile_name, savefile_type, main))

    main.show()

    sys.exit(window.exec_())