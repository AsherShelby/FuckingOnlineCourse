import ddddocr
import time
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service

from traversal import traversal_course


def find_school_value(school_name, driver):
    school_selector = driver.find_element(by=By.XPATH, value='//*[@id="schoolId"]')
    school_list = school_selector.find_elements(By.XPATH, value='./*')
    for school in school_list:
        if school.text == school_name:
            return school.get_attribute('value')


def login(school, username, password, ocr, driver):
    school_value = find_school_value(school, driver)
    schoolSelector = driver.find_element(by=By.XPATH, value='//*[@id="schoolId"]')
    Select(schoolSelector).select_by_value(school_value)

    username_input = driver.find_element(By.XPATH, value='//*[@id="username"]')
    username_input.send_keys(username)

    password_input = driver.find_element(By.XPATH, value='//*[@id="password"]')
    password_input.send_keys(password)

    while True:
        time.sleep(2)
        vertifyImage = driver.find_element(By.ID, value='codeImg')
        image = vertifyImage.screenshot_as_png
        res = ocr.classification(image)
        vertify_input = driver.find_element(By.XPATH, value='//*[@id="code"]')
        vertify_input.send_keys(res)
        loginButton = driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div/div[6]/div/input[2]')
        loginButton.click()
        time.sleep(2)

        try:
            errorButton = driver.find_element(By.LINK_TEXT, value='确定')
            errorButton.click()
        except NoSuchElementException as e:
            print('\n登录成功')
            break


def initial(platform):
    ocr = ddddocr.DdddOcr()
    driver = uc.Chrome(driver_executable_path="./chromedriver.exe")
    print(platform)
    if platform == '英华学堂':
        driver.get('https://mooc.yinghuaonline.com/user/login')
    elif platform == '仓辉教育科技':
        driver.get('https://shixun.canghuikeji.com/user/login')
    driver.implicitly_wait(3)

    return driver, ocr


def begin(dic):
    school = dic['school']
    username = dic['id']
    password = dic['password']
    platform = dic['platform']
    print('声明：本工具完全免费，如果您是通过购买途径获得本工具，说明您已经上当受骗！')
    print('本工具由林科大涉外神秘人士制作')


    # school = input("请输入学校名称：")
    # username = input("请输入学号：")
    # password = input("请输入密码：")
    print('正在启动......')
    driver, ocr = initial(platform)
    login(school, username, password, ocr, driver)
    traversal_course(driver, ocr)
    # except Exception as ex:
    #     print('脚本执行出错')

