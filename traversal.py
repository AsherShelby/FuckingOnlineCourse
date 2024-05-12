import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class link_changed(Exception):
    def __init__(self, message):
        super().__init__(message)


class traversal_over(Exception):
    def __init__(self, message):
        super().__init__(message)


def traversal_course(driver, ocr, platform):
    while True:

        courseL = driver.find_element(By.CLASS_NAME, value="user-course")
        courseList = courseL.find_elements(By.CLASS_NAME, value="item")
        no_complete_course = courseList[0]
        has_no_complete_course = False
        for course in courseList:
            if course.find_element(By.CLASS_NAME, value="txt").text != "100%":
                print(course.find_element(By.CLASS_NAME, value="txt").text)
                no_complete_course = course
                has_no_complete_course = True
                break

        if not has_no_complete_course:
            print('所有课程都已完成，无待刷课程')
            break

        no_complete_course.find_element(By.CLASS_NAME, value="name").find_element(By.TAG_NAME, value="a").click()

        continueButton = driver.find_element(By.XPATH,
                                             value="/html/body/div[3]/div[2]/div/div[1]/div[2]/div[6]/div[1]/a")
        continueButton.click()

        while True:
            try:
                browser_url = driver.current_url

                videoSlot = driver.find_element(By.CLASS_NAME, value="detmain-navlist")
                videoList = videoSlot.find_elements(By.XPATH, value="./*")
                currVideoListIndex = 0
                currVideoIndex = 0

                for element in videoList:
                    if element.get_attribute("class") == "group two  on":
                        break
                    else:
                        currVideoListIndex += 1

                itemList = videoList[currVideoListIndex].find_element(By.CLASS_NAME, value="list").find_elements(By.CLASS_NAME, value="item")
                for video in itemList:
                    if video.find_element(By.TAG_NAME, value="a").get_attribute("class") == "on":
                        break
                    else:
                        currVideoIndex += 1

                if browser_url != driver.current_url:
                    raise link_changed("页面已跳转")

                print(f"""正在播放第{currVideoListIndex + 1}章, 第{currVideoIndex + 1}节...""")

                isNew = False
                for i in range(currVideoListIndex, len(videoList)):
                    videoSlot = driver.find_element(By.CLASS_NAME, value="detmain-navlist")
                    videoList = videoSlot.find_elements(By.XPATH, value="./*")
                    itemList = videoList[i].find_element(By.CLASS_NAME, value="list").find_elements(By.CLASS_NAME, value="item")

                    if browser_url != driver.current_url:
                        raise link_changed("页面已跳转")

                    for j in range(currVideoIndex, len(itemList)):
                        if j != currVideoIndex or isNew:
                            itemList[j].click()
                        elif browser_url != driver.current_url:
                            raise link_changed("页面已跳转")

                        videoSlot = driver.find_element(By.CLASS_NAME, value="detmain-navlist")
                        videoList = videoSlot.find_elements(By.XPATH, value="./*")
                        itemList = videoList[i].find_element(By.CLASS_NAME, value="list").find_elements(By.CLASS_NAME, value="item")
                        playButton = driver.find_element(By.XPATH, value='//*[@id="videoContent"]/div/div[2]/div[1]/canvas')

                        while True:
                            playButton.click()
                            time.sleep(1)
                            if browser_url != driver.current_url:
                                raise link_changed("页面已跳转")
                            try:
                                dialog = driver.find_element(By.CSS_SELECTOR, value='[id^="layui-layer"]')
                                codeImg = driver.find_element(By.ID, value='codeImg').screenshot_as_png
                                res = ocr.classification(codeImg)
                                print(res)
                                vertify_input = dialog.find_element(By.CSS_SELECTOR, value='input:not([id="yzCode"])')
                                vertify_input.send_keys(res)
                                time.sleep(1)
                                playButton2 = driver.find_element(By.LINK_TEXT, value='开始播放')
                                playButton2.click()
                            except:
                                print('已开始播放')
                                break

                        while True:
                            try:
                                if browser_url != driver.current_url:
                                    raise link_changed("页面已跳转")

                                playingTimeElement = driver.find_element(By.XPATH, value="//*[starts-with(@class, 'timetext')]")
                                playingTimeText = playingTimeElement.text
                                textList = playingTimeText.split()
                                if len(textList) == 0:
                                    pass
                                elif textList[0] == textList[2]:
                                    print('播放完毕！')
                                    break
                            except NoSuchElementException as e:
                                print('找不到播放时间元素')

                        if j == len(itemList) - 1:
                            currVideoIndex = 0

                            if browser_url != driver.current_url:
                                raise link_changed("页面已跳转")
                            if i + 1 < len(videoList):
                                videoList[i + 1].click()
                                isNew = True
                                print('展开下一章')
                            else:
                                raise traversal_over("已刷完")

            except link_changed as e:
                print('页面已跳转')
                continue
            except traversal_over as o:
                print('已刷完一门网课')
                js = "window.location.replace('https://swxymooc.csuft.edu.cn/user')"
                if platform == '仓辉教育科技':
                    js = "window.location.replace('https://swxyzxshixun.canghuikeji.com/user')"
                driver.execute_script(js)
                break
