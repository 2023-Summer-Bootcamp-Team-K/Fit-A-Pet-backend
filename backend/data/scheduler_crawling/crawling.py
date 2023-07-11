import csv
import time
import os
from datetime import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium import webdriver

from data.models import Data


def import_csv_to_db(csv_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        next(csv_reader)
        next(csv_reader)

        for row in csv_reader:
            data = Data()
            data.device = row['장치']
            data.code = row['일련 번호']
            data.timestamp = datetime.strptime(row['장치 타임 스탬프'], '%Y-%m-%d %H:%M')
            data.record_type = int(row['기록 유형'])
            data.prev_bloodsugar = int(row['과거 혈당 mg/dL'])
            data.cur_bloodsugar = int(row['혈당 스캔 mg/dL'])

            data.save()

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

    # 인증코르 입력
    code_input = driver.find_element(By.ID, 'twoFactor-step2-code-input')
    code_input.send_keys('인증 키')
    time.sleep(100)

    # 확인 및 로그인 버튼 클릭
    next_button = driver.find_element(By.ID, 'twoFactor-step2-next-button')
    next_button.click()
    time.sleep(10)

    # 이름 선택하고 이름 입력
    first_name_button = driver.find_element(By.ID, 'table-header-search-button-firstName')
    first_name_button.click()
    first_name_input = driver.find_element(By.ID, 'table-header-search-input-firstName')
    first_name_input.send_keys("이름")

    # 성 선택하고 성 입력
    last_name_button = driver.find_element(By.ID, 'table-header-search-button-lastName')
    last_name_button.click()
    last_name_input = driver.find_element(By.ID, 'table-header-search-input-lastName')
    last_name_input.send_keys("성")

    # 제일 앞에있는 요소 더블 클릭
    row_element = driver.find_element(By.CLASS_NAME, 'row____3GNff')
    actions = ActionChains(driver)
    actions.click(row_element).perform()

    profile_button = driver.find_element(By.ID, 'profile-nav-button-container')
    profile_button.click()

    download_button = driver.find_element(By.ID, 'patient-profile-data-button')
    download_button.click()

    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'rc-anchor-container')))

    check_actions = ActionChains(driver)
    check_actions.move_to_element(checkbox).click().perform()

    downloaded_button = driver.find_element(By.ID, 'exportData-modal-download-button')
    downloaded_button.click()

    csv_file_path = "CSV파일 경로"

    import_csv_to_db(csv_file_path)

    driver.quit()
