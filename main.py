from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
# Version: 2.0
# 浏览器驱动版本：114.0.5735.90

# 获取人名列表函数定义
def GettingNames(wd):
    # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
    wd.maximize_window()
    wd.get('https://www.qmsjmfb.com/')

    # 搜索名字
    elements = [element.text for element in wd.find_elements(By.XPATH, "//div/ul/li")]
    return elements

# 填写身份信息函数定义
def FulfillInfo(wd, name):
    # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
    wd.maximize_window()
    wd.get('https://www.jscdc.cn/KABP2011/business/index1.jsp?tdsourcetag=s_pcqq_aiomsg')

    # 通过 Select 对象选中南京市，栖霞区，马群街道以及填入姓名
    Select(wd.find_element(By.ID, "zone3")).select_by_visible_text("南京市")
    Select(wd.find_element(By.ID, "zone4")).select_by_visible_text("栖霞区")
    Select(wd.find_element(By.ID, "zone5")).select_by_visible_text("马群街道")
    wd.find_element(By.ID, 'name').send_keys(name)

    # 通过 Select 对象选中0～15岁以下，男，小学，学生，小学3~4年级
    Select(wd.find_element(By.ID, "ageGroup")).select_by_visible_text("0～15岁以下")
    Select(wd.find_element(By.ID, "sex")).select_by_visible_text("男")
    Select(wd.find_element(By.ID, "educationStatus")).select_by_visible_text("小学")
    Select(wd.find_element(By.ID, "metier")).select_by_visible_text("学生")
    Select(wd.find_element(By.ID, "studentLevel")).select_by_visible_text("小学3~4年级")

    # 点击开始按钮
    wd.find_element(By.ID, 'log_img').click()

# 回答问题函数定义
def AnsweringQuestions(wd):
    # 获取答案
    # 获取题数
    num = wd.find_element(By.ID, "__subjectCount")
    num = int(num.text)

    # 获取所有input的元素构成一个list
    answers = wd.find_elements(By.XPATH, "//*[@id=\"subject\"]/input")

    # 填充答案
    for i in range(num):
        answer = answers[i].get_attribute('value').split(",")[1]
        wd.find_element(By.CSS_SELECTOR, "#KWait" + str(i + 1) + " input[value=\"" + answer + str(i + 1) + "\"]").click()

    wd.find_element(By.ID, "btnAct" + str(num) + "").click()
    wd.switch_to.alert.accept()

# Main Part
# 创建 WebDriver 对象，指明使用chrome浏览器驱动
# webDriver = webdriver.Chrome(service=Service(r'd:\tools\chromedriver.exe'))
webDriver = webdriver.Chrome(service=Service(r'114.0.5735.90\chromedriver.exe'))
nameList = GettingNames(webDriver)

# 开始循环答题
for i in range(1):
    name = nameList[i]
    FulfillInfo(webDriver, name)
    AnsweringQuestions(webDriver)

    # 等到网页加载完毕后截屏保存
    time.sleep(1)

    # 检测截图文件夹是否存在
    if not os.path.exists('Screenshots/'):
        os.makedirs('Screenshots/')
    
    # 创建截图文件
    if(webDriver.get_screenshot_as_file('Screenshots/' + str(i+1) + '.png') ):
        print("Screenshots/" + str(i+1) + ".png is saved successfully.")
    else:
        print("Failed to save the Screenshots/" + str(i+1) + ".png.")
        break

# 关闭浏览器
webDriver.close()
