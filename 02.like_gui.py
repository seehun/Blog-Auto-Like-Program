from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pyautogui

import time

import pyperclip

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

UI_PATH = r"07.project3/design.ui"

class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self,None)
        uic.loadUi(UI_PATH, self)
    
        # 1) 버튼 클릭 이벤트
        #self.객체이름.clicked.connect(self.실행할함수이름)
        self.start_btn.clicked.connect(self.start)
        self.quit_btn.clicked.connect(self.quit)
        self.like_number.valueChanged.connect(self.number)
    
    def number(self):
        self.number_label.setText(f"{self.like_number.value()}")

    def start(self):
        id_input = self.id_input.text()
        pw_input = self.pw_input.text()
        like_number = self.like_number.value()

        if id_input=="" or pw_input=="":
                self.status.append("빈칸을 모두 채워주셈")
                return 0

        self.status.append("로그인 진행중..")
        QApplication.processEvents()

        
        browser = self.login(id_input,pw_input)

        if browser ==0:
            self.status.append("로그인 실패.. ")
            return 
        else:
            self.status.append("로그인 성공")
            QApplication.processEvents()
            time.sleep(1)
            self.status.append("자동화 진행중..")
            QApplication.processEvents()
            self.push_like_button(browser, like_number)
            browser.close()
            self.status.append("자동화 완료")
            




    def login(self,id_input,pw):
        #브라우저 꺼짐 방지
        chrome_options = Options()
        chrome_options.add_experimental_option("detach",True)

        #불필요한 에러메세지 제거
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


        #크롬드라이버를 자동으로 설치해서 서비스를 만들어냄
        service = Service(executable_path=ChromeDriverManager().install())


        # 크롬 드라이버 연결
        browser = webdriver.Chrome("C:/chromedriver.exe", service = service,options=chrome_options)

        browser.implicitly_wait(10) # 페이지가 로딩될때까지 최대 10초 기다려줌

        # 1.로그인
        url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"

        browser.get(url) # 페이지 열기

        browser.maximize_window() # 화면 최대화

        # 아이디 입력창
        time.sleep(3)
        naver_id = browser.find_element(By.CSS_SELECTOR,"#id")
        naver_id.click()
        pyperclip.copy(id_input)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2)


        # 비밀번호 입력창

        naver_pw = browser.find_element(By.CSS_SELECTOR,"#pw")
        naver_pw.click()
        pyperclip.copy(pw)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2)

        # 로그인 버튼

        login_btn = browser.find_element(By.CSS_SELECTOR,"#log\.login")
        login_btn.click()
        time.sleep(1)

        #로그인 완료
        #로그인 성공 시 드라이버 반환

        #로그인 실패시 드라이버 종료 후에 숫자 0을 반환 

        check = browser.find_elements(By.CSS_SELECTOR, "#minime")
        #로그인 하게 되면 #minime라는 태그가 생김 -> check에 [iframe ~~~]
    
        if(len(check)>0): #로그인 성공
            return browser
        else:
            browser.close()
            return 0
        
    def push_like_button(self,browser, like_number):
        url = f"https://m.blog.naver.com/FeedList.naver"
        browser.get(url) 

        time.sleep(1)
        max_like_num = like_number   #총 좋아요 개수
        count = 0 #현재 좋아요 신청 개수


        while count<max_like_num:
            like_buttons = browser.find_elements(By.CSS_SELECTOR,".u_likeit_list_btn._button.off")
            
            #더 이상 누를 좋아요 버튼이 없다면
            #반목문 종료
            if len(like_buttons)==0:
                break

            # 좋아요가 안 눌린 첫번째 게시물 클릭
            like_buttons[0].click()

            # 현재 좋아요 신청개수 +1
            count+=1
            time.sleep(1)


    def quit(self):
        sys.exit()
    
    

QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())

