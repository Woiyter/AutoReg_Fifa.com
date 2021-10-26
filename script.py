from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import string
import time
import random
import calendar
import imaplib
from email.parser import Parser
from bs4 import BeautifulSoup


def get_fifa_code(login, password, imap_server):
    try:
        server = imaplib.IMAP4_SSL(imap_server)
        server.login(login, password)
        server.select("inbox")
        result, data = server.search(None, "ALL")
        ids = data[0]
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, data = server.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = raw_email.decode("utf-8")
        parsed_mail = Parser().parsestr(email_message)
        content = parsed_mail.get_payload(decode=True).decode("utf-8")
        if content.find("FIFA") > -1:
            soup = BeautifulSoup(content, 'lxml')
            span_with_code = soup.findAll("span", {"id": "BodyPlaceholder_UserVerificationEmailBodySentence2"})[0]
            code = span_with_code.text.split(":")[1]
            print(f'Код получен: {code}')
            return code
        else:
            print("Не удалось найти письмо от FIFA")
    except Exception as err:
        print("Ошибка во время получения кода")
        print(err)


def wait_for_element(driver, selector):
    try:
        action_element = WebDriverWait(driver, 15).until(ec.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        return action_element
    except Exception as err:
        print(err)


def select_option(driver, select_tag_selector, option):
    try:
        select = Select(driver.find_element(By.CSS_SELECTOR, select_tag_selector))
        select.select_by_visible_text(option)
    except Exception as err:
        print(err)


# MAIN PAGE SELECTORS
ok_cookies_selector = "#onetrust-accept-btn-handler"
login_in_selector = "#__next > div > div.d-none.d-lg-block.fc-layout_headerMargin__YO7ab > header" \
                    " > nav.fc-header_mainNav__Ayaqb > div > a:nth-child(2)"
register_btn_selector = "#create_button_link"

# 1 STEP SELECTORS
screen_name_selector = "#screenName"
email_selector = "#email"
password_selector = "#newPassword"
retype_password_selector = "#reenterPassword"
firstname_selector = "#givenName"
last_name_selector = "#surname"
country_select = "#country"
lang_select = "#preferredLanguage"
birth_day_selector = "#dateOfBirth_day"
birth_month_selector = "#dateOfBirth_month"
birth_year_selector = "#dateOfBirth_year"
first_step_next_btn = "#step1Next"

# 2 STEP SELECTORS
second_step_next_btn = "#step2Next"

# 3 STEP SELECTORS
scroll_div_selector = "#attributeList > ul > li.CheckboxMultiSelect.step3 > div.attrEntry > div.fifa_tos"
third_step_next_btn = "#step3Next"

# 4 STEP SELECTORS
fourth_step_next_btn = "#step4Next"

# 5 STEP SELECTORS
send_code_btn = "#email_ver_but_send"
input_code_selector = "#email_ver_input"
verify_code_btn = "#email_ver_but_verify"
continue_btn = "#continue"

check_register_selector = "#__next > div > div.d-none.d-lg-block.fc-layout_headerMargin__YO7ab > " \
                          "header > nav.fc-header_mainNav__Ayaqb > div > a:nth-child(2) > div"


def register_account(mail, password,
                     first_name, last_name,
                     country, date_of_birth,
                     mail_password, imap_server, proxy):
    # INITIALIZE DRIVER
    options = ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--unsafely-treat-insecure-origin-as-secure")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-web-security")
    options.add_argument('--disable-gpu')
    options.add_argument(f'--proxy-server={proxy}')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # GENERATING RANDOM LOGIN
    random_login = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))

    bd_list = date_of_birth.split(".")
    try:
        # MAIN PAGE
        driver.get("https://www.fifa.com")
        time.sleep(random.triangular(2, 3))
        wait_for_element(driver, ok_cookies_selector).click()
        time.sleep(random.triangular(1, 3))
        wait_for_element(driver, login_in_selector).click()
        time.sleep(random.triangular(2, 6))
        wait_for_element(driver, register_btn_selector).click()
        time.sleep(random.triangular(1, 3))

        # 1 STEP
        wait_for_element(driver, screen_name_selector).send_keys(random_login)
        time.sleep(random.triangular(2, 4))
        driver.find_element(By.CSS_SELECTOR, email_selector).send_keys(mail)
        time.sleep(random.triangular(1, 3))
        driver.find_element(By.CSS_SELECTOR, password_selector).send_keys(password)
        time.sleep(random.triangular(1, 3))
        driver.find_element(By.CSS_SELECTOR, retype_password_selector).send_keys(password)
        time.sleep(random.triangular(1, 3))
        driver.find_element(By.CSS_SELECTOR, firstname_selector).send_keys(first_name)
        time.sleep(random.triangular(1, 3))
        driver.find_element(By.CSS_SELECTOR, last_name_selector).send_keys(last_name)
        time.sleep(random.triangular(1, 3))
        select_option(driver, country_select, country)
        time.sleep(random.triangular(1, 3))
        select_option(driver, lang_select, "English")
        time.sleep(random.triangular(1, 3))
        select_option(driver, birth_day_selector, str(int(bd_list[0])))
        time.sleep(random.triangular(1, 3))
        select_option(driver, birth_month_selector, calendar.month_name[int(bd_list[1])])
        time.sleep(random.triangular(1, 3))
        select_option(driver, birth_year_selector, bd_list[2])
        time.sleep(random.triangular(1, 3))
        driver.find_element(By.CSS_SELECTOR, first_step_next_btn).click()

        # 2 STEP
        wait_for_element(driver, second_step_next_btn).click()
        time.sleep(random.triangular(2, 6))

        # 3 STEP
        scroll_div_element = wait_for_element(driver, scroll_div_selector)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_div_element)
        time.sleep(random.triangular(2, 3))
        driver.find_element(By.CSS_SELECTOR, third_step_next_btn).click()
        time.sleep(random.triangular(1, 3))

        # 4 STEP
        wait_for_element(driver, fourth_step_next_btn).click()
        time.sleep(random.triangular(1, 3))

        # 5 STEP
        driver.find_element(By.CSS_SELECTOR, send_code_btn).click()
        time.sleep(random.triangular(30, 45))
        code = get_fifa_code(login=mail, password=mail_password, imap_server=imap_server)
        time.sleep(random.triangular(3, 4))
        driver.find_element(By.CSS_SELECTOR, input_code_selector).send_keys(code)
        time.sleep(random.triangular(2, 3))
        driver.find_element(By.CSS_SELECTOR, verify_code_btn).click()
        time.sleep(random.triangular(3, 4))
        driver.find_element(By.CSS_SELECTOR, continue_btn).click()
        time.sleep(random.triangular(7, 10))
        sing_in_name = wait_for_element(driver, check_register_selector)
        if sing_in_name:
            print("Регистрация успешна")
            driver.close()
            driver.quit()
            return random_login
        else:
            print("Регистрация неудалась")
            driver.close()
            driver.quit()
            exit()
    except Exception as err:
        print(err)
        driver.close()
        driver.quit()
        exit()

