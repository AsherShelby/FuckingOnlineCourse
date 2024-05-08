import time

from selenium.webdriver.common.by import By


def traversal_course(driver, ocr):
    while True:
        time.sleep(2)
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

        no_complete_course.find_element(By.CLASS_NAME, value="name").click()
        time.sleep(2)
        continueButton = driver.find_element(By.XPATH, value="/html/body/div[3]/div[2]/div/div[1]/div[2]/div[6]/div[1]/a")
        continueButton.click()
        time.sleep(2)

        videoSlot = driver.find_element(By.CLASS_NAME, value="detmain-navlist")
        videoList = videoSlot.find_elements(By.XPATH, value="./*")
        currVideoListIndex = 0
        currVideoIndex = 0

        for element in videoList:
            if element.get_attribute("class") == "group two  on":
                break
            else:
                currVideoListIndex += 1
        itemList = videoList[currVideoListIndex].find_element(By.CLASS_NAME, value="list").find_elements(By.CLASS_NAME,
                                                                                                         value="item")

        for video in itemList:
            if video.find_element(By.TAG_NAME, value="a").get_attribute("class") == "on":
                break
            else:
                currVideoIndex += 1
        print(f"""正在播放第{currVideoListIndex}章, 第{currVideoIndex}节...""")

        isNew = False
        for i in range(currVideoListIndex, len(videoList)):
            videoSlot = driver.find_element(By.CLASS_NAME, value="detmain-navlist")
            videoList = videoSlot.find_elements(By.XPATH, value="./*")
            itemList = videoList[i].find_element(By.CLASS_NAME, value="list").find_elements(By.CLASS_NAME, value="item")
            time.sleep(1)

            for j in range(currVideoIndex, len(itemList)):
                if j != currVideoIndex or isNew:
                    itemList[j].click()

                time.sleep(2)
                videoSlot = driver.find_element(By.CLASS_NAME, value="detmain-navlist")
                videoList = videoSlot.find_elements(By.XPATH, value="./*")
                itemList = videoList[i].find_element(By.CLASS_NAME, value="list").find_elements(By.CLASS_NAME,
                                                                                                value="item")

                playButton = driver.find_element(By.XPATH, value='//*[@id="videoContent"]/div/div[2]/div[1]/canvas')
                while True:
                    playButton.click()
                    time.sleep(1)
                    try:
                        dialog = driver.find_element(By.CSS_SELECTOR, value='[id^="layui-layer"]')
                        codeImg = driver.find_element(By.ID, value='codeImg').screenshot_as_png
                        res = ocr.classification(codeImg)
                        print(res)
                        vertify_input = dialog.find_element(By.CSS_SELECTOR, value='input:not([id="yzCode"])')
                        vertify_input.send_keys(res)
                        playButton2 = driver.find_element(By.LINK_TEXT, value='开始播放')
                        playButton2.click()
                        time.sleep(1.5)
                    except:
                        print('无需输入验证码')

                    detectPlayButton = driver.find_element(By.XPATH, value='//*[@id="videoContent"]/div/div[2]/div[1]')
                    videoStyle = detectPlayButton.get_attribute('style')
                    if 'none' in videoStyle:
                        print('开始播放...')
                        break
                    else:
                        time.sleep(1)

                while True:
                    detectPlayButton = driver.find_element(By.XPATH, value='//*[@id="videoContent"]/div/div[2]/div[1]')
                    videoStyle = detectPlayButton.get_attribute('style')
                    if 'block' in videoStyle:
                        print('播放完毕！')
                        break
                    else:
                        print('播放中...请勿触碰播放按钮...')
                    time.sleep(1)

                if j == len(itemList) - 1:
                    currVideoIndex = 0
                    time.sleep(1)
                    if i + 1 < len(videoList):
                        videoList[i + 1].click()
                        isNew = True
                        print('展开下一章')

                time.sleep(2)

            time.sleep(2)

        js = "window.location.replace('https://swxymooc.csuft.edu.cn/user')"
        driver.execute_script(js)
