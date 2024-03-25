from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
from TouchScreen import roll,roll_right,isElementExist,tiktok,refreshJustNow,is_number
from read import readGood
import hashlib
import sys
#from CatchAndLearn import storeData,showData

count = 0 # 标记商品数量
want = -1 # 对每次翻页的首件商品与上一页的末尾商品进行去重
goods_li = []
good = ''
uniqueGoods = [] # 哈希去重

def GetGoods(driver,goodsli = None):
    """
    函数功能：操作搜索栏，进行商品搜索
    """
    global good
    if goodsli == None:
        goods = input("请输入商品名：")
    else:
        goods = goodsli

    good = goods

    tiktok(3)
    element = WebDriverWait(driver,10).until(lambda x: x.find_element('id','com.taobao.idlefish:id/search_bar_layout'))
    element.click()
    driver.find_element('class name','android.widget.EditText').send_keys(goods)
    driver.implicitly_wait(500)
    driver.find_element('accessibility id',"搜索").click()
    driver.implicitly_wait(5000)

    return driver

def GetInfo(driver,kind,ehco = 5,keyword_good = None,coword_good = None,noword_good = None): # public
    """
    函数功能：先获取该页所有商品信息，展示，随后翻页，持续这个循环，不断抓取商品信息

    ehco 为翻页次数，若 ehco 设置为 -1， 则取消翻页次数限制，不断下翻
    keyword、coword 为 getinfo 调用的 processInfo 使用的参数，具体含义见该函数
    """
    global goods_li, uniqueGoods

    goods_li = []

    tiktok(5)

    if ehco != -1:
        i = 0

        while i < ehco:
            goodli = getinfo(driver,kind,keyword_good,coword_good,noword_good)

            f = False
            
            c = 0
            for item in goodli:
                if item['hash'] in uniqueGoods:
                    #f = True
                    goodli.remove(item)
                    #return
                else:
                    goods_li.append(item)
                    print(item)
                    readGood(driver,item)
                    if c == 0:
                        c += 1
                        if len(uniqueGoods) > 20:
                            while len(uniqueGoods) > 15:
                                print(uniqueGoods.pop(i))
                    uniqueGoods.append(item['hash'])

            if c == 0:
                return
            
            if f == True:
                return goods_li
            
            roll(driver)
            
            i += 1
            """if ehco > 12 and i % 10 == 0 and i != 0:
                storeData(good,goods_li)
                showData(good)
                goods_li = []
            else:
                if i == ehco:
                    storeData(good,goods_li)
                    goods_li = []"""
        return goods_li

    else:
        i = 0
        while True:
            goodli = getinfo(driver,kind,keyword_good,coword_good,noword_good)
            goods_li.extend(goodli)
            roll(driver)
            i += 1
            """if i % 10 == 0 and i != 0:
                storeData(good,goods_li)
                showData(good)
                goods_li = []"""

def getinfo(driver,kind,keyword_good = None,coword_good = None,noword_good = None): # private
    """
    函数功能：获取该页面上的所有商品信息，并依次调用 processInfo 将各条信息规范化后打印在屏幕上

    keyword、coword 为传入 processInfo 函数的参数，具体含义见该函数
    """
    global want,uniqueGoods
    
    text = driver.find_elements('xpath',"//*[contains(@content-desc,'¥')]")

    goods_li = []
    for t in range(len(text)):
        txt = text[t].get_attribute("content-desc")
        good = txt.split('\n')
        good = processInfo(good,kind,keyword_good,coword_good,noword_good)
        #print('good: ',good)
        if good == False:
            continue

        if good['价格'] == sys.maxsize:
            continue
        
        """if '想要' in good:
            if want == good["想要"] and t == 0:
                continue"""
        
        #if good['hash'] not in uniqueGoods:
        goods_li.append(good)
        
        
        """global count
        count += 1
        print("第 " ,count," 件商品")

        if "成色" in good:
            print("成色：",good["成色"])

        if "价格" in good:
            print("价格：",good["价格"])
        if "可选加分" in good:
            print("可选加分：",good["可选加分"])

        print("#############################")"""
        
        
        """try:
            if '想要' in good:
                if good["想要"] != 0:
                    want = good["想要"]
        except Exception as e:
            print('Something happened in getinfo, ',e)"""


        """for i in range(len(good)):
            print(good[i],"  -------------  ",i)
        
        print(' ')
        print("###############")
        print(' ')"""
    return goods_li
        

def processInfo(good, kind ,keyword_good = None,coword_good = None,noword_good = None,): # private
    """
    函数功能：以 good 接收单件商品信息，随后将价格、参数、成色等信息分类储存于字典 info 中，并返回该字典

    keyword 为核心关键字，描述里必须出现
    coword 为可选关键字，描述里可以不出现。若出现，则为该商品加分（暂定）
    """
    """print('good:')
    print(good)
    print('')"""

    info = {}

    # 关键字、否定字、加分项判断
    if good[0] != '':
        if noword_good != None and noword_good != []:
            f = True
            for i in noword_good:
                if i in good[0]:
                    f = False
                    return f
        if keyword_good != None and keyword_good != []:
            f = False
            for i in keyword_good: 
                if i in good[0]:
                    f = True
            if f == False:
                return f
        else:
            if coword_good != None and coword_good != []:
                f = []
                for i in coword_good:
                    if i in good[0]:
                        f.append(i)
                info["可选加分"] = f
    else:
        return False
    
    if kind != None:
        for i in range(len(kind)):
            sort = kind[i]['sort']
            para = kind[i]['depend']
            keyword = kind[i]['keyword'] # 列表

            for line in range(len(good)):
                if para not in info:
                    for k in range(len(keyword)):
                        if keyword[k] in good[line]:
                            info[para] = keyword[k]
                            break

                if "¥" in good[line]:

                    for i in range(len(good[line])):
                        if is_number(good[line][i]):
                            head = i
                            f = True
                            while is_number(good[line][i]):
                                i += 1
                                if i >= len(good[line]):
                                    break
                            tail = i
                        if f == True:
                            info['价格'] = good[line][head:tail]
                        break

                    if '价格' not in info:
                        if line + 1 < len(good):
                            if "想要" in good[line+1]:
                                if is_number(good[line][1:]):
                                    info["价格"] = good[line][1:]
                            else:
                                if is_number(good[line+1]):
                                    info["价格"] = good[line+1]
                        else:
                            info['价格'] = sys.maxsize

                if '想要' in good[line]:
                    info['想要'] = good[line]

                """if "全新" in good[line]  or "几乎全新" in good[line] or "未拆封" in good[line] or "维修" in good[line]:
                    info['成色'] = good[line]
                if "大陆" in good[line] or "香港" in good[line] or "海外" in good[line]:
                    info['版本'] = good[line]
                if "¥" in good[line]:
                    if line + 1 < len(good):
                        if "想要" in good[line+1]:
                            info["价格"] = good[line][1:]
                        else:
                            info["价格"] = good[line+1]
                if "想要" in good[line]:
                    info["想要"] = good[line]"""
                 
    good = joinli(good)
    if good != None:
        hash = encode(good)
    else:
        hash = 0
    info['hash'] = hash
    return info
    """
    0 line: description (maybe not existing)
    1 line: Empty Line
    2 line: info
    3 line: info
    4 line: info
    5 line: sign of money (¥)
    6 line: amount
    7 line: Empty Line
    8 line: how many want it
    """

def encode(string):
    hash_password = hashlib.sha256(string.encode("utf-8")).hexdigest()
    return hash_password

def joinli(li):
    st = ''
    for i in li:
        st += i
    return st

def behuman(driver):
    tiktok(5)
    if isElementExist(driver):
        roll_right(driver)
    driver.implicitly_wait(5000)
    while isElementExist(driver):
        tiktok(5)
        roll_right(driver)
        tiktok(5)