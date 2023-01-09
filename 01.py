import os
import sys
import pymysql
from PyQt5 import uic
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView
from matplotlib import font_manager

# path = os.getcwd()
# font_path = path + "\Pretendard-Light.otf"
# font = font_manager.FontProperties(fname=font_path).get_name()

form_class = uic.loadUiType("main.ui")[0]

# 메인 윈도우
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 초기 화면 설정
        self.mainWidget.setCurrentWidget(self.intro_page)

    # 로그인 화면 설정


    # ui


    # 슬롯
        self.btn_login.clicked.connect(self.login)
        self.btn_logout.clicked.connect(self.logout)

    def login(self):
        self.mainWidget.setCurrentWidget(self.main_page)
    def logout(self):
        self.mainWidget.setCurrentWidget(self.intro_page)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    mainWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    mainWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()