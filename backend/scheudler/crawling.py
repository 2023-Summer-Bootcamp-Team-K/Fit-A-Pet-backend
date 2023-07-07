import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium import webdriver

def run_libreView_process():
    # Selenium 웹 드라이버 설정
    driver = webdriver.Chrome()  # 크롬 드라이버 경로를 지정해주세요
    time.sleep(3)


    # 웹 페이지로 이동
    driver.get('https://www.libreview.com/')
    time.sleep(5)

    # 모달 창 선택
    modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'truste-consent-track')))
    time.sleep(1)

    # 동의 버튼 클릭
    consent_button = modal.find_element(By.ID, 'truste-consent-button')
    consent_button.click()

    # 나라 선택 모달 클릭
    open_modal_button = driver.find_element(By.ID, 'country-select')
    open_modal_button.click()
    time.sleep(5)

    # '한국' 선택
    country_select = Select(driver.find_element(By.ID, 'country-select'))
    country_select.select_by_value('KR')

    # 완료 버튼 클릭
    confirm_button = driver.find_element(By.ID, 'submit-button')
    confirm_button.click()

    time.sleep(5)

    # 이메일 넣기
    email_input = driver.find_element(By.ID, 'loginForm-email-input')
    email_input.send_keys(os.getenv('LIBRE_ID'))

    password_input = driver.find_element(By.ID, 'loginForm-password-input')
    password_input.send_keys(os.getenv('LIBRE_PASSWORD'))

    login_button = driver.find_element(By.ID, 'loginForm-submit-button')
    login_button.click()

    code_send_button = driver.find_element(By.ID, 'twoFactor-step1-next-button')
    code_send_button.click()

    time.sleep(10)

    driver.quit()
