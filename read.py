from Message.chat import send
from selenium.webdriver.support.wait import WebDriverWait
from TouchScreen import isElementExist,is_number
from time import time

"""
提供判断行为，判断是否为目标商品，并提供报价
"""


sharebutton = (880,163)
linkbutton = (312,1895)

def target(good):
    price = 0

    if '款式' in good:
        kind = str(good['款式'])
        kind = kind.upper()
        if kind == "SL2" or kind == "TCR SL2":
            pass
        else:
            return False
        
    else:
        return False

    if '品牌' in good:
        kind = str(good['品牌'])
        kind = kind.upper()
        print("品牌:",kind)
        price = 4400

    if '可选加分' in good:
        plus = good['可选加分']
        if plus != []:
            for item in plus:
                if item == '很新':
                    price += 100

    return price
        
def tickCom(driver,max_look):
    try:
        ele = driver.find_element('xpath',"//*[contains(@content-desc,'浏览')]")
    except:
        return False
    txt = ele.get_attribute("content-desc")
    t = txt.split('\n')

    looked = []
    for i in range(len(t)):
        if '浏' in t[i]:
            for j in range(len(t[i])):
                if '浏' == t[i][j]:
                    j -= 1
                    while is_number(t[i][j]):
                        looked.insert(0,t[i][j])
                        j -= 1
    look = ''
    for i in looked:
        look += i
    if is_number(look):
        look = int(look)
        if look > max_look:
            return False
        else:
            return True
    else:
        return True

        

def readGood(driver,good):

    print('readGood...')
    price = good['价格']
    price = float(price)
    price = round(price)

    """if '版本' not in good:
        return False
"""

    tprice = target(good)
    
    if tprice == False:
        print("关键词缺失")
        return False
    
    print(" ")
    print("比价: ",price," , ",tprice)
    print(" ")
    if int(price) <= tprice:
        alert(driver,good,10000)

def alert(driver,good,max_look):
    print("=======")
    print('alert')
    print("=======")
    path = "//*[contains(@content-desc,{})]".format(good['价格'])

    driver.implicitly_wait(500)

    if isElementExist(driver,"点击屏幕，重新加载"):
        print("back early1")
        driver.back()
        return

    if isElementExist(driver,good['价格']):
        try:
            driver.find_element("xpath",path).click()
        except:
            if isElementExist(driver,'宝贝被卖掉了'):
                driver.back()
                print("卖掉了")
                return
            if isElementExist(driver,'宝贝正在审核中'):
                driver.back()
                print("审核中")
                return
            else:
                print("back early2")
                driver.back()
                return
    
    if isElementExist(driver,'宝贝被卖掉了'):
        driver.back()
        print("卖掉了")
        return
    if isElementExist(driver,'宝贝正在审核中'):
        driver.back()
        print("审核中")
        return

    if tickCom(driver,max_look) == False:
        print("贩子")
        driver.back()
        return

    try:
        WebDriverWait(driver,5).until(lambda x: x.find_element("xpath","//*[contains(@content-desc,'分享')]"))
        driver.find_element("xpath","//*[contains(@content-desc,'分享')]").click()
    except:
        print("分享按键查找失败")
        if isElementExist(driver,'宝贝被卖掉了'):
            driver.back()
            print("卖掉了")
            return
        if isElementExist(driver,'宝贝正在审核中'):
            driver.back()
            print("审核中")
            return
        driver.tap([sharebutton],100)
    print('share')

    driver.implicitly_wait(500)

    i = 0
    while isElementExist(driver,"复制链接") == False:
        i += 1
        if i % 11 == 10:
            driver.tap([sharebutton],100)
            driver.implicitly_wait(1000)
            print('share again1')

        """if now - start >= 10:
            driver.tap([(881,140)],100)
            driver.implicitly_wait(1000)
            print('share again1')"""
        
        if isElementExist(driver,"复制链接"):
            break
            
        if isElementExist(driver,'分享'):
            driver.tap([sharebutton],100)
            driver.implicitly_wait(500)
            print('share again2')
            
        if isElementExist(driver,'宝贝被卖掉了'):
            driver.back()
            print('卖掉了')
            return
        if isElementExist(driver,'宝贝正在审核中'):
            driver.back()
            print('审核中')
            return
        
        driver.implicitly_wait(400)
        pass
    #WebDriverWait(driver,10).until(lambda x: x.find_element('xpath','//*[contains(@content-desc,"复制链接")]'))
    #WebDriverWait(driver,10).until(lambda x: x.find_element('xpath','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.HorizontalScrollView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]'))
    #driver.find_element('xpath','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.HorizontalScrollView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[3]').click()
    driver.implicitly_wait(500)
    if isElementExist(driver,'复制链接'):
        driver.tap([linkbutton],100)
        driver.implicitly_wait(500)
    print('url')

    driver.implicitly_wait(300)
    
    i = 1
    while isElementExist(driver,"复制链接"):
        if i > 0:
            print('timing')
            i -= 1

        driver.implicitly_wait(1000)
        if isElementExist(driver,'淘口令已复制'):
            break

        driver.tap([linkbutton],100)
        print("url again")
        
        if isElementExist(driver,'淘口令已复制') == False:
            continue
        else:
            break

    print('getting code')
    WebDriverWait(driver,10).until(lambda x: x.find_element('xpath','//*[contains(@content-desc,"淘口令已复制")]'))
    
    driver.back()
    driver.back()
    print('2 back')
    
    ss = driver.get_clipboard_text()
    print('copyboard',ss)

    if '价格' not in good:
        return
    
    price = good['价格']
    txt = ''
    for key,value in good.items():
        if key == '价格':
            continue
        if key == '可选加分':
            if good[key] == []:
                continue
        if key == 'hash':
            continue

        txt += key
        txt += ': '
        txt += str(value)
        txt += '\n'
    msg = {
    "msgtype": "link", 
    "link": {
        "text": txt, 
        "title": price, 
        "messageUrl": ss
    }
}
    send(msg)
