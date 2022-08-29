# coding=utf-8
import re
import time
import os.path
import grequests
import requests
from dataclasses import dataclass

if (os.path.exists("license.txt")):
    license_txt = "license.txt"
else:
    license_txt = "/sdcard/license.txt"

province_encode = '苏'.encode('utf-8')

# license struct
@dataclass
class LicenseInfo:
    Region: str
    LpNumber: str
    Index: int
    Luck: float = 0
    IsValid: bool = True
    Comment: str = ""

license_list = []
sessions = []

def query_luck_g1():
    ts = time.time()
    req_list = []
    for i,item in enumerate(license_list):
        data = {'chepai1': province_encode, 'chepai2': item.Region, 'chepai': item.LpNumber, 'submit': '开始测试'.encode('utf-8')}
        req_list.append(grequests.post('https://chepai.xuenb.com/', data = data, session = sessions[i]))
    res_list = grequests.map(req_list)
    te = time.time()
    print("1号服务器查询用时:", str(te-ts) + "s")

    page_list = []
    for i, res in enumerate(res_list):
        if (res is not None and res.status_code == 200):
            page_list.append(re.sub('<[^<]+?>', '', res.text).replace('\n', '').strip())
        else:
            page_list.append("")
            license_list[i].IsValid = False
    if (len(page_list) < len(license_list)):
        print("Warning: 部分号码查询出错")
    
    for i, page in enumerate(page_list):
        if (len(page) == 0):
            continue
        start = page.find("【")
        if (start == -1):
            print("Error: Site1 invalid response [start]")
            license_list[i].IsValid = False
            continue
        end = page.find("。", start)
        if (end == -1):
            print("Error: Site1 invalid response [end]")
            license_list[i].IsValid = False
            continue
        license_list[i].Comment += "  结果1 -> " + page[start: end] + "\n"
        num_list = re.findall(r"\d+", page[start: end])
        if (len(num_list) > 0 and int(num_list[0]) > 0 and int(num_list[0]) <= 100):
            license_list[i].Luck += int(num_list[0])
        elif (page[start: end].find("凶") != -1):
            license_list[i].Luck += 40
        else:
            license_list[i].Luck += 60

def query_luck_g2():
    ts = time.time()
    req_list = []
    for i,item in enumerate(license_list):
        data = {'sheng': province_encode, 'shi': item.Region, 'czsm': item.LpNumber, 'action': 'test'}
        req_list.append(grequests.post('https://www.xingming.com/haoma/chepai.php', data = data, session = sessions[i]))
    res_list = grequests.map(req_list)
    te = time.time()
    print("2号服务器查询用时:", str(te-ts) + "s")

    page_list = []
    for i, res in enumerate(res_list):
        if (res is not None and res.status_code == 200):
            page_list.append(re.sub('<[^<]+?>', '', res.text).replace('\n', '').strip())
        else:
            page_list.append("")
            license_list[i].IsValid = False
    if (len(page_list) < len(license_list)):
        print("Warning: 部分号码查询出错")
    
    for i, page in enumerate(page_list):
        if (len(page) == 0):
            continue
        start = page.find("『数理』：") + 5
        if (start == -1):
            print("Error: Site2 invalid response [start]")
            license_list[i].IsValid = False
            continue
        end = page.find("『签语』", start)
        if (end == -1):
            print("Error: Site2 invalid response [end]")
            license_list[i].IsValid = False
            continue
        license_list[i].Comment += "  结果2 -> " + page[start: end] + "\n"

        if (page[start: end].find("大凶") != -1):
            license_list[i].Luck += 20
        elif (page[start: end].find("凶") != -1):
            license_list[i].Luck += 40
        elif (page[start: end].find("大吉") != -1):
            license_list[i].Luck += 100
        elif (page[start: end].find("半吉") != -1 or 
              page[start: end].find("沉浮") != -1):
            license_list[i].Luck += 70
        elif (page[start: end].find("吉") != -1):
            license_list[i].Luck += 90
        else:
            license_list[i].Luck += 60

def query_luck_g3():
    ts = time.time()
    req_list = []
    for i,item in enumerate(license_list):
        data = {'province': province_encode, 'let': item.Region, 'num': item.LpNumber}
        req_list.append(grequests.post('https://sm.xingzuo360.cn/sm/chepaijixiong/', data = data, session = sessions[i]))
    res_list = grequests.map(req_list)
    te = time.time()
    print("3号服务器查询用时:", str(te-ts) + "s")

    page_list = []
    for i, res in enumerate(res_list):
        if (res is not None and res.status_code == 200):
            page_list.append(re.sub('<[^<]+?>', '', res.text).replace('\n', '').strip())
        else:
            page_list.append("")
            license_list[i].IsValid = False
    if (len(page_list) < len(license_list)):
        print("Warning: 部分号码查询出错")
    
    for i, page in enumerate(page_list):
        if (len(page) == 0):
            continue
        start = page.find("吉凶分析:") + 5
        if (start == -1):
            print("Error: Site3 invalid response [start]")
            license_list[i].IsValid = False
            continue
        end = page.find("）", start) + 1
        if (end == -1):
            print("Error: Site3 invalid response [end]")
            license_list[i].IsValid = False
            continue
        license_list[i].Comment += "  结果3 -> " + page[start: end] + "\n"

        if (page[start: end].find("凶带吉") != -1):
            license_list[i].Luck += 50
        elif (page[start: end].find("吉带凶") != -1):
            license_list[i].Luck += 70
        elif (page[start: end].find("吉") != -1):
            license_list[i].Luck += 90
        elif (page[start: end].find("凶") != -1):
            license_list[i].Luck += 40
        else:
            license_list[i].Luck += 60

def query_luck_g4():
    ts = time.time()
    req_list = []
    for i,item in enumerate(license_list):
        data = {'province': province_encode, 'city': item.Region, 'chepai': item.LpNumber}
        req_list.append(grequests.post('https://www.qiyuange.com/chepai/', data = data, session = sessions[i]))
    res_list = grequests.map(req_list)
    te = time.time()
    print("4号服务器查询用时:", str(te-ts) + "s")

    page_list = []
    for i, res in enumerate(res_list):
        if (res is not None and res.status_code == 200):
            page_list.append(re.sub('<[^<]+?>', '', res.text).replace('\n', '').strip())
        else:
            page_list.append("")
            license_list[i].IsValid = False
    if (len(page_list) < len(license_list)):
        print("Warning: 部分号码查询出错")
    
    for i, page in enumerate(page_list):
        if (len(page) == 0):
            continue
        start = page.find("总论：") + 3
        if (start == -1):
            print("Error: Site4 invalid response [start]")
            license_list[i].IsValid = False
            continue
        end = page.find(")", start) + 1
        if (end == -1):
            print("Error: Site4 invalid response [end]")
            license_list[i].IsValid = False
            continue
        license_list[i].Comment += "  结果4 -> " + page[start: end] + "\n"

        if (page[start: end].find("大凶") != -1):
            license_list[i].Luck += 20
        elif (page[start: end].find("凶") != -1):
            license_list[i].Luck += 40
        elif (page[start: end].find("大吉") != -1):
            license_list[i].Luck += 100
        elif (page[start: end].find("半吉") != -1):
            license_list[i].Luck += 70
        elif (page[start: end].find("吉") != -1):
            license_list[i].Luck += 90
        else:
            license_list[i].Luck += 60

def query_luck_g5():
    ts = time.time()
    req_list = []
    for i,item in enumerate(license_list):
        data = {'sheng': province_encode, 'shi': item.Region, 'paihao': item.LpNumber}
        req_list.append(grequests.post('http://www.name321.net/cesuan/chepai/', data = data, session = sessions[i]))
    res_list = grequests.map(req_list)
    te = time.time()
    print("5号服务器查询用时:", str(te-ts) + "s")

    page_list = []
    for i, res in enumerate(res_list):
        if (res is not None and res.status_code == 200):
            page_list.append(re.sub('<[^<]+?>', '', res.text).replace('\n', '').strip())
        else:
            page_list.append("")
            license_list[i].IsValid = False
    if (len(page_list) < len(license_list)):
        print("Warning: 部分号码查询出错")
    
    for i, page in enumerate(page_list):
        if (len(page) == 0):
            continue
        start = page.find("【吉凶】：") + 5
        if (start == -1):
            print("Error: Site5 invalid response [start]")
            license_list[i].IsValid = False
            continue
        end = page.find("〗", start) + 1
        if (end == -1):
            print("Error: Site5 invalid response [end]")
            license_list[i].IsValid = False
            continue
        license_list[i].Comment += "  结果5 -> " + page[start: end] + "\n"

        num_list = re.findall(r"\d+", page[start: end])
        if (len(num_list) > 0 and int(num_list[0]) > 0 and int(num_list[0]) <= 100):
            license_list[i].Luck += int(num_list[0])
        elif (page[start: end].find("下") != -1):
            license_list[i].Luck += 40
        else:
            license_list[i].Luck += 60

def check_license_format(licenses):
    for i, item in enumerate(licenses):
        item_formatted = item.upper().strip()
        if (item_formatted[0] != 'U' and item_formatted[0] != 'E'):
            print("Error: 参数[" + item_formatted + "]无效，只能以 U 或 E 开头")
            continue
        if (len(item_formatted) != 6 or str.isalnum(item_formatted) != 1):
            print("Error: 参数[" + item_formatted + "]无效，只能是六位数或字母")
            continue
        region = item_formatted[0]
        license = item_formatted[1:]
        license_list.append(LicenseInfo(region, license, i + 1))
    if (len(license_list) != len(licenses)):
        print("Warning: 部分参数无效")
        return 0
    return 1

def luck_sort(e):
    return e.Luck

if __name__ == '__main__':
    print("=======================================")
    print("=========== 车牌吉凶聚合查询 ==========")
    print("===========      2.0        ===========")
    print("=======================================")

    time_start = time.time()

    print("\n读取", license_txt, "...")
    with open(license_txt, 'r') as f:
        license_list_raw = f.readlines()
    check_license_format(license_list_raw)

    if (len(license_list) > 0):
        print("有效输入(共" + str(len(license_list)) + "个):")
        for i, lic in enumerate(license_list):
            print(lic.Region + lic.LpNumber, end="; ")
            if ((i + 1) % 6 == 0):
                print()
        print("\n")

        sessions = [requests.Session() for i in range(len(license_list))]
        print("查询中, 请稍等...")
        query_luck_g1()
        query_luck_g2()
        query_luck_g3()
        query_luck_g4()
        query_luck_g5()
        print("查询完毕 ^ ^")

        license_list.sort(key = luck_sort, reverse = True)
        print("\n以吉值排序:")
        for i, lic in enumerate(license_list):
            print(lic.Region + lic.LpNumber + "@" + str(lic.Index).rjust(2) + ":" + str(lic.Luck / 5).rjust(5) + "%", end="; ")
            if ((i + 1) % 2 == 0):
                print()
        print("\n详情如下:")
        for i, lic in enumerate(license_list):
            print("吉值(" + str(lic.Luck / 5) + "%) -> 苏" + lic.Region + "·" + lic.LpNumber)
            print(lic.Comment)

        time_end = time.time()
        print("总用时: " + str(time_end - time_start) + "s")

    else:
        print("帮助: 需要在", license_txt, "中列举需要查询的号码，每行一个，示例: U/E12345")
