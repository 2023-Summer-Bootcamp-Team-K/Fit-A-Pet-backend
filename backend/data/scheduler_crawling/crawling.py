import csv
import time
import os
import pytz
from datetime import datetime

from django.contrib.auth.models import User
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium import webdriver

from data.models import Data


def import_csv_to_db(file_name):
    current_directory = os.getcwd()
    csv_file_path = os.path.join(current_directory, 'data/scheduler_crawling/csv_file', file_name)
    # fieldnames = ['장치', '일련 번호', '장치 타임 스탬프', '장치 타임 스탬프', '기록 유형', '과거 혈당 mg/dL', '혈당 스캔 mg/dL']
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        next(file)
        next(file)
        csv_reader = csv.DictReader(file)
        print(csv_reader.fieldnames)

        korea = pytz.timezone('Asia/Seoul')

        for row in csv_reader:
            data = Data()
            data.device = row['장치']
            data.code = row['일련 번호']
            data.timestamp = datetime.strptime(row['장치 타임스탬프'], '%Y-%m-%d %H:%M')
            data.timestamp = korea.localize(data.timestamp)
            data.record_type = int(row['기록 유형'])
            data.bloodsugar = int(row['과거 혈당 mg/dL']) if row['과거 혈당 mg/dL'] else None
            data.scan_bloodsugar = int(row['혈당 스캔 mg/dL']) if row['혈당 스캔 mg/dL'] else None

            data.save()

def run_libreView_process(user_id):

    user = User.objects.get(pk=user_id)
    first_name = user.first_name
    last_name = user.last_name
    chrome_options = Options()
    download_dir = os.path.join(os.getcwd(), 'data/scheduler_crawling/csv_file')
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')
    # Selenium 웹 드라이버 설정
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(3)


    # 웹 페이지로 이동
    driver.get('https://www.libreview.com/')
    time.sleep(2)

    # 모달 창 선택
    modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'truste-consent-track')))
    time.sleep(1)

    # 동의 버튼 클릭
    consent_button = modal.find_element(By.ID, 'truste-consent-button')
    consent_button.click()

    # 나라 선택 모달 클릭
    open_modal_button = driver.find_element(By.ID, 'country-select')
    open_modal_button.click()
    time.sleep(2)

    # '한국' 선택
    country_select = Select(driver.find_element(By.ID, 'country-select'))
    country_select.select_by_value('KR')

    time.sleep(1)

    # 완료 버튼 클릭
    confirm_button = driver.find_element(By.ID, 'submit-button')
    confirm_button.click()

    time.sleep(1)

    # 이메일 넣기
    email_input = driver.find_element(By.ID, 'loginForm-email-input')
    email_input.send_keys(os.getenv('LIBRE_ID'))

    password_input = driver.find_element(By.ID, 'loginForm-password-input')
    password_input.send_keys(os.getenv('LIBRE_PASSWORD'))

    login_button = driver.find_element(By.ID, 'loginForm-submit-button')
    login_button.click()

    time.sleep(3)

    dropdown = Select(driver.find_element(By.ID, "2fa-method-select"))
    dropdown.select_by_value("email")
    time.sleep(3)

    code_send_button = driver.find_element(By.ID, 'twoFactor-step1-next-button')
    code_send_button.click()
    time.sleep(3)

    # 2차 코드가 Google 이메일로 전송되는 새로운 창 열기
    driver.execute_script("window.open('about:blank', 'google_window')")
    driver.switch_to.window("google_window")

    # Google 검색 페이지 열기
    driver.get("https://www.google.com")

    gmail_button = driver.find_element(By.XPATH, "//a[@aria-label='Gmail (새 탭에서 열기)']")
    gmail_button.click()

    login_button = driver.find_element(By.XPATH, "//a[@data-label='header' and text()='로그인']")
    login_button.click()

    time.sleep(3)

    email_input_google = driver.find_element(By.ID, 'identifierId')
    email_input_google.clear()
    email_input_google.send_keys(os.getenv('GOOGLE_ID'))

    time.sleep(1)

    next_button = driver.find_element(By.ID, 'identifierNext')
    next_button.click()

    time.sleep(3)

    password_input_google = driver.find_element(By.CSS_SELECTOR, '#password input')
    password_input_google.clear()
    password_input_google.send_keys(os.getenv('GOOGLE_PASSWORD'))

    time.sleep(1)

    next_button_2 = driver.find_element(By.ID, 'passwordNext')
    next_button_2.click()

    time.sleep(60)

    driver.refresh()

    time.sleep(3)

    element = driver.find_element(By.CSS_SELECTOR, ".zA.zE")
    element.click()

    driver.refresh()
    time.sleep(3)

    text = driver.find_element(By.CSS_SELECTOR, "td[style*='padding-top:25px']").text
    security_code = ''.join(filter(str.isdigit, text))

    driver.switch_to.window(driver.window_handles[0])

    # 인증코드 입력
    code_input = driver.find_element(By.ID, 'twoFactor-step2-code-input')
    code_input.send_keys(security_code)
    time.sleep(3)

    # 확인 및 로그인 버튼 클릭
    next_button = driver.find_element(By.ID, 'twoFactor-step2-next-button')
    next_button.click()
    time.sleep(3)

    name_search = driver.find_element(By.ID, 'main-header-patient-search-wrapper')
    name_search.send_keys(user.last_name + " " + user.first_name)

    time.sleep(3)

    name_result = driver.find_element(By.ID, 'patient-result-button-9ae61ff0-f67d-11ed-ba5b-0242ac110009')
    name_result.click()

    time.sleep(3)

    profile_button = driver.find_element(By.ID, 'profile-nav-button-container')
    profile_button.click()
    time.sleep(15)

    download_button = driver.find_element(By.ID, 'patient-profile-data-download-button')
    download_button.click()
    time.sleep(15)

    # frame = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'a-kdd93qcd3n5w')))

    # check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'a-kdd93qcd3n5w')))
    # check_box.click()

    # # reCAPTCHA 프레임을 찾습니다.
    # frame = driver.find_element(By.NAME, 'a-kdd93qcd3n5w')
    # driver.switch_to.frame(frame)
    # time.sleep(5)

    # # "확인란"을 클릭합니다.
    # element = driver.find_element(By.ID, 'recaptcha-anchor')
    # element.click()

    # driver.switch_to.default_content()

    downloaded_button = driver.find_element(By.ID, 'exportData-modal-download-button')
    downloaded_button.click()
    time.sleep(15)

    file_name = f"{user.first_name}{user.last_name}_glucose_{datetime.now().strftime('%Y-%-m-%-d')}.csv"

    import_csv_to_db(file_name)

    driver.quit()
