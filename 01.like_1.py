from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pyautogui

import time

import pyperclip

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


x = pyautogui.prompt(text='', title='' , default='')

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
time.sleep(2)
naver_id = browser.find_element(By.CSS_SELECTOR,"#id")
naver_id.click()
pyperclip.copy("shoon199")
pyautogui.hotkey("ctrl", "v")
time.sleep(2)


# 비밀번호 입력창

naver_pw = browser.find_element(By.CSS_SELECTOR,"#pw")
naver_pw.click()
pyperclip.copy("1234")
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

# 로그인 버튼

login_btn = browser.find_element(By.CSS_SELECTOR,"#log\.login")
login_btn.click()

time.sleep(1)


url = f"https://m.blog.naver.com/FeedList.naver"
browser.get(url) 

time.sleep(1)



max_like_num = int(x)   #총 좋아요 개수
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


# while count<max_like_num:
#     like_buttons = browser.find_elements(By.CSS_SELECTOR,".u_likeit_list_btn._button.off")
#     count = len(like_buttons)

#     if count<max_like_num:
#         browser.find_element(By.CSS_SELECTOR,"body").send_keys(Keys.CONTROL + Keys.END)
#         time.sleep(2)

# like_buttons = browser.find_elements(By.CSS_SELECTOR,".u_likeit_list_btn._button.off")[:max_like_num]
# print(like_buttons)
# print(len(like_buttons))














