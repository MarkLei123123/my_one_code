# -*- coding: UTF-8 -*-

import json
import time
import requests
from playsound import playsound
from prettytable import PrettyTable

# 监控总开关
monitor_switch = False


# 监控核心代码块
def getIphoneInfo():
    result = requests.get('https://www.apple.com.cn/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&parts.0=MU2P3CH/A&location=%E6%B5%99%E6%B1%9F%20%E6%9D%AD%E5%B7%9E%20%E4%B8%8A%E5%9F%8E%E5%8C%BA')
    status_code = result.status_code  # 取result状态码
    if status_code == 200:
        if check_json_format(result.text):
            # 取result的json数据
            result_json = json.loads(result.text)
            # 进行2次循环，分别取出杭州西湖店和杭州万象城店的相关数据
            table = PrettyTable(['门店名称', '库存状态', '监控机型'])
            for i in range(2):
                # 取门店名称
                storeName = result_json['body']['content']['pickupMessage']['stores'][i]['storeName']
                # 取库存状态
                storeStatus = result_json['body']['content']['pickupMessage']['stores'][i]['partsAvailability']['MU2P3CH/A']['messageTypes']['regular']['storePickupQuote']
                # 取监控机型
                storeModel = result_json['body']['content']['pickupMessage']['stores'][i]['partsAvailability']['MU2P3CH/A']['messageTypes']['regular']['storePickupProductTitle']
                # print(storeName, storeStatus,storeModel)
                if storeStatus.find('不可取货') != -1:
                    storeStatus = '\033[91m%s\033[0m' % storeStatus  # 输出红色1
                else:
                    global monitor_switch  # 更改全局变量
                    monitor_switch = False  # 关闭监控
                    playsound('./Music.mp3', True)  # 播放提示音
                    storeStatus = '\033[92m%s\033[0m' % storeStatus  # 输出绿色
                table.add_row([storeName, storeStatus, storeModel])
            # 设置table左对齐
            table.align = 'l'
            return table.get_string()
        return 'JSON格式错误'


# 计算秒数
def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec


# 检查JSON格式
def check_json_format(raw_msg):
    if isinstance(raw_msg, str) == True:
        try:
            json.loads(raw_msg)
        except ValueError:
            return False
        return True
    else:
        return False


if __name__ == '__main__':
    interval = sleeptime(0, 0, 20)  # 设置刷新间隔时间。。
    while monitor_switch == True:
        print(getIphoneInfo())
        refreshTime = '============================= ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 刷新============================='  # 刷新时间
        print(refreshTime)
        time.sleep(interval)
