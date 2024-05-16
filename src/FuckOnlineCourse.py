import matplotlib
import ddddocr
import time
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import frozen_dir
from traversal import traversal_course

matplotlib.use('Agg')


def find_school_value(school_name, driver):
    school_selector = driver.find_element(by=By.XPATH, value='//*[@id="schoolId"]')
    school_list = school_selector.find_elements(By.XPATH, value='./*')
    for school in school_list:
        if school.text == school_name:
            return school.get_attribute('value')


def login(school, username, password, ocr, driver):
    xpath = '//*[@id="loginForm"]/div/div[6]/div/input[2]'
    try:
        school_value = find_school_value(school, driver)
        schoolSelector = driver.find_element(by=By.XPATH, value='//*[@id="schoolId"]')
        Select(schoolSelector).select_by_value(school_value)
    except NoSuchElementException:
        print("无需选择学校")
        xpath = '//*[@id="loginForm"]/div/div[5]/div/input[2]'

    username_input = driver.find_element(By.XPATH, value='//*[@id="username"]')
    username_input.send_keys(username)

    password_input = driver.find_element(By.XPATH, value='//*[@id="password"]')
    password_input.send_keys(password)

    while True:
        time.sleep(1)
        url = driver.current_url
        vertifyImage = driver.find_element(By.ID, value='codeImg')
        image = vertifyImage.screenshot_as_png
        res = ocr.classification(image)
        vertify_input = driver.find_element(By.XPATH, value='//*[@id="code"]')
        vertify_input.send_keys(res)
        loginButton = driver.find_element(By.XPATH, value=xpath)
        loginButton.click()
        time.sleep(1)
        if url == driver.current_url:
            errorButton = driver.find_element(By.LINK_TEXT, value='确定')
            errorButton.click()
        else:
            break


def initial(platform):
    ocr = ddddocr.DdddOcr()
    driver = uc.Chrome(driver_executable_path=frozen_dir.app_path() + '\\bin\\chromedriver.exe')
    print(platform)
    # if platform == '英华学堂':
    #     driver.get('https://mooc.yinghuaonline.com/user/login')
    # elif platform == '仓辉教育科技':
    #     driver.get('https://shixun.canghuikeji.com/user/login')
    driver.get(platform)
    driver.implicitly_wait(5)

    return driver, ocr


def begin(dic):
    school = dic['school']
    username = dic['id']
    password = dic['password']
    platform = dic['platform']

    driver, ocr = initial(platform)
    login(school, username, password, ocr, driver)
    traversal_course(driver, ocr, dic['platform'])

    driver.quit()

