import os
import sys
import time

import pymysql
from PyQt5 import uic
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView, QMessageBox
from matplotlib import font_manager
from db import *
from datetime import datetime, timedelta
import time

# path = os.getcwd()
# font_path = path + "\Pretendard-Light.otf"
# font = font_manager.FontProperties(fname=font_path).get_name()

form_class = uic.loadUiType("main.ui")[0]

# 메인 윈도우
class WindowClass(QMainWindow, form_class):
    user = None
    today = datetime.now().date().strftime('%Y-%m-%d')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_style()

    def set_style(self):
        # style.css 파일의 내용을 텍스트로 읽고 스타일시트로 적용
        with open("style.css", 'r') as f:
            self.setStyleSheet(f.read())

    # 초기 화면 설정
        self.mainWidget.setCurrentWidget(self.intro_page)
        yesterday = datetime.strptime(self.today, '%Y-%m-%d') - timedelta(days=1)
        self.label_yesterday.setText(f'({yesterday.strftime("%Y.%m.%d")}기준)')


    # 로그인 / 로그아웃
        self.btn_login.clicked.connect(self.login)
        self.btn_logout.clicked.connect(self.logout)

    # 입실 / 퇴실 / 외출 버튼
        self.btn_entrance.clicked.connect(self.click_btn)
        self.btn_checkout.clicked.connect(self.click_btn)
        self.btn_out.clicked.connect(self.click_btn)

    # 로그인 함수
    def login(self):
        id = self.lt_id.text()
        pw = self.lt_pw.text()
        if id == '' or pw == '':
            self.login_msg.setText('아이디와 비밀번호를 입력해주세요')
        else:
            result, msg, name = login(id, pw)
            if result == False:
                self.login_msg.setText(msg)
            elif result == True:
                print(msg)
                self.user = name
                self.set_mainpage()

    def set_mainpage(self):
        self.mainWidget.setCurrentWidget(self.main_page)
        self.user_msg.setText(f'{self.user}님 환영합니다.')
        self.set_timestamp()
        list_up_attendance(self.user, self.today)

    def set_timestamp(self):
        data = today_attendance(self.user, self.today)
        text = lambda x : x if x != None else ''

        # 상태 표시
        if data[2] != None and data[5] != None:
            self.label_status.setText('퇴실')
        elif data[5] != None:
            self.label_status.setText('입실')

        # 입실 - 외출 - 복귀 - 퇴실 시간 표시
        self.tl_entrance.setText(f'{text(data[2])}')
        self.tl_out.setText(f'{text(data[3])}')
        self.tl_comeback.setText(f'{text(data[4])}')
        self.tl_check.setText(f'{text(data[5])}')

        if data[3] != None and data[4] != None:
            self.btn_out.setEnabled(False)
        elif data[3] != None:
            self.btn_out.setEnabled(True)
            self.btn_out.setText('복귀')
        else:
            self.btn_checkout.hide()
            self.btn_out.hide()



    # 로그아웃 함수
    def logout(self):
        self.mainWidget.setCurrentWidget(self.intro_page)
        self.user = None
        self.lt_id.setText('')
        self.lt_pw.setText('')
        self.login_msg.setText('')

    def click_btn(self):
        btn = self.sender().text()
        print(f'@ {btn}')
        option = {'입실': 2, '외출': 3, '복귀': 4, '퇴실': 5}

        # 현재 상태 확인 - 시간 입력
        data = today_attendance(self.user, self.today)
        if data[option[btn]] == None :
            now = time.strftime('%H:%M:%S')
            reply = QMessageBox.information(self, '알림', f'현재 시각 {now}, {btn}하시겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                timestamp(self.user, btn, now, self.today)
        else:
            QMessageBox.information(self, '알림', f'{data[option[btn]]}에 이미 {btn}했습니다.')

        self.set_timestamp()

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    mainWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    mainWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()