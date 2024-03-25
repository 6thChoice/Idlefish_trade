from appium import webdriver
from Message.chat import send
#from appium.webdriver.extensions.android.nativekey import AndroidKey
from GetGoodsAndSee import GetGoods, GetInfo, behuman
from TouchScreen import refreshJustNow, clickButton
from selenium.webdriver.support.wait import WebDriverWait
from read import readGood
import traceback
import os
import time

desired_caps = {
  'platformName': 'Android',  # 连接设备为安卓系统
  'platformVersion': '10',  # 手机安卓版本,必须与设备匹配
  'appPackage': 'com.taobao.idlefish',  # 启动APP Package名称
  'appActivity': '.maincontainer.activity.MainActivity',  # 启动Activity名称
  'noReset': True,       # 不要重置App
  'automationName': 'UiAutomator2',	# 获取toast信息弹出框需添加，但需要先配置UiAutomator2
  'enforceXPath1': True,
}

targetApp = 'com.taobao.idlefish'

goodname = '捷安特sl2' # 爬取的商品名

kind = [
        {
            'depend' : '品牌', # 分类依据，作为内部字典的 key， 不参与匹配
            'keyword' : ['giant',"捷安特"], # 抓取数据字段后匹配文字的关键字
            'sort' : [], # 若不想直接复制文字，则可使用sort提供内置选项，选填
        },
        {
            'depend' : '码数',
            'keyword' : ['M','175','180'],
            'sort' : []
        },
        {
            'depend' : '想要', # 分类依据，作为内部字典的 key， 不参与匹配
            'keyword' : ["想要"], # 抓取数据字段后匹配文字的关键字
            'sort' : [], # 若不想直接复制文字，则可使用sort提供内置选项，选填
        },
        {
            'depend' : '款式', # 分类依据，作为内部字典的 key， 不参与匹配
            'keyword' : ['TCR SL2','TCR sl2','tcr sl2','tcr SL2',"sl2","SL2"], # 抓取数据字段后匹配文字的关键字
            'sort' : [], # 若不想直接复制文字，则可使用sort提供内置选项，选填
        },
    ]

keyword = [] 
# 必须关键字，若商品详情中缺少该类型关键字，则跳过该商品

coword = ['很新'] 
# 可选关键字，该类型关键字不影响商品筛选，只在获得目标价格时生效。
# 若要修改该类型关键字，需要在 read.py 中的 target 里同时修改匹配规则才能顺利起效

noword = ['高价收',"收！","收!","收收收","高价回收","注意是收",'山地车','平把','fastroad','escape','一字把'] 
# 否定关键字，若商品详情中包含该类型关键字，则跳过该商品


i = 0
round = 0
f = True
while f == True:
    round += 1
    print("========================")
    print("第 ",round," 次执行循环")
    print("========================")

    if round > 1:
        msg = {
                "msgtype": "text",
                "text": {
                    "content": "程序再启动"
                }
            }
        send(msg)
    
    try:
        driver = webdriver.Remote('http://127.0.0.1:4723', desired_caps)

        driver.implicitly_wait(300)

        if driver.current_package != targetApp:
            driver.launch_app()
        driver.implicitly_wait(300)

        print("begin search")
        driver = GetGoods(driver, goodsli = goodname)

        driver.implicitly_wait(300)
        print("HHII")
        driver.implicitly_wait(300)
        behuman(driver)
        print("I am human")

        clickButton(driver,'最新发布')

        
        while i < 10000:
            i += 1
            info = GetInfo(driver,ehco = 5,coword_good=coword,noword_good=noword,kind=kind)
            
            refreshJustNow(driver)
            
            if int(i % 100) == 1:
                t = time.asctime()
                print("========================")
                print("已成功运行 ", i ," 次",', 当前时间：',t)
                print("========================")

        #print(goodsli)
        
        print("================ +++ ================")
        input("Main program is finished, type any key to finish the last part...")
        print("================ +++ ================")
        driver.close_app()
        driver.terminate_app('com.taobao.idlefish')
        driver.quit()

        msg = {
            "msgtype": "text",
            "text": {
                "content": "程序抵达循环极限，继续执行...\n该信息仅供提示，不需要进行任何操作"
            }
        }
        send(msg)
        print("The program is finished totally...")

    except Exception as e:
        print("something happened: ",e)
        traceback.print_exc()
        msg = {
            "msgtype": "text",
            "text": {
                "content": "程序终止"
            }
        }
        send(msg)
        print("========================")
        print('已成功运行 ',i,' 次程序')
        print("========================")
        try:
            os.system("adb shell am force-stop com.taobao.idlefish")
        except:
            driver.close_app()
            driver.terminate_app('com.taobao.idlefish')
            driver.quit()
        
