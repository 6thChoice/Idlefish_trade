from time import time
from selenium.webdriver.support.wait import WebDriverWait

"""
实现对屏幕的操作
"""

def getSize(driver): # private
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return x,y

def roll(driver):
    driver.implicitly_wait(300)
    size = getSize(driver)
    x = size[0] * 0.3
    y_down = size[1] * 0.8
    y_up = size[1] * 0.25
    driver.swipe(x,y_down,x,y_up,1000)

def roll_to_up(driver):
    driver.implicitly_wait(300)
    size = getSize(driver)
    x = size[0] * 0.3
    y_down = size[1] * 0.8
    y_up = size[1] * 0.25
    driver.swipe(x,y_up,x,y_down,100)

def roll_right(driver):
    driver.implicitly_wait(100)
    x_left = 170
    y = 1295
    x_right = 900
    driver.swipe(x_left,y,x_right,y,1000)

def isElementExist(driver,element = "baxia-punish"):
    source = driver.page_source
    if element in source:
        return True
    else:
        return False
    
def tiktok(interval):
    start = time()
    while time() - start < interval:
        pass
    return True

def refreshJustNow(driver):
    roll_to_up(driver)
    clickButton(driver,'最新发布')
    try:
        WebDriverWait(driver,10).until(lambda x: x.find_element("xpath","//*[contains(@content-desc,'¥')]"))
    except:
        roll(driver)
    driver.implicitly_wait(300)
    clickButton(driver,'最新发布')

def clickButton(driver,keyword):
    driver.implicitly_wait(300)
    #WebDriverWait(driver,10).until(lambda x: x.find_element("xpath","//*[contains(@content-desc,'最新发布')]"))
    ele = driver.find_elements("xpath","//android.widget.Button[@content-desc='最​新​发​布​']")
    
    for i in ele:
        if i.get_attribute('class') == 'android.widget.Button':
            i.click()
            return
        
def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False