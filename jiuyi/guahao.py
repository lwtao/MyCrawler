# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import time
import datetime
from bs4 import BeautifulSoup

url_list = ['http://www.yihu.com/doctor/gd/D3AEA17BD4774615B4D1B0624BD4F9CB.shtml'
    , 'http://www.yihu.com/doctor/gd/6F66B8BF69A34235BFDFD5CEFA134D53.shtml'
    , 'http://www.yihu.com/doctor/gd/576E193C444A4DE1816A8682270C962B.shtml'
    , 'http://www.yihu.com/doctor/gd/743C5A3BDEDE42D1A298FB64DCF5AE36.shtml'
    , 'http://www.yihu.com/doctor/gd/2E01DC937A5A4DE79CF8A1EE07EA2696.shtml'
    , 'http://www.yihu.com/doctor/gd/ABFD0299B4944045816B207299281A86.shtml'
    , 'http://www.yihu.com/doctor/gd/55289DFB029C4851B59F9C4660334091.shtml'
    , 'http://www.yihu.com/doctor/gd/E85BF278D81640EC9310B0C0270453E5.shtml'
            ]


def getHtmlAndHeaders(url, postdata):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
               'Cookie':
                   'jkzl_channelid=1000000; jkzl_uuid=64CFEBC1-E321-4331-95F6-F4400898DF4D; _365groups_ClientID=c4d43280-deab-43ee-99fe-5dd61df80da9; PHPSESSID=63ia6nr219019gec8g6edgjt84; YIHU_webNotic=%3F; jkzl_sid=6BCEBF6F-FD5A-4025-921F-2A4DDB9E5591; YIHU_userInfo=hbaL2q-cjJmvurPdgZWpzIm5hsuYZbrYmn-D2H7OpJmG3IPbsYZ43q_Qxc-ApYCnkbqCzIqgutePpovcfs6kmYXMd9qvrHyarqqrl4G1f9aBzo7bkIqurYh8fpl-z45jhtyApbB2eJauqsnegaaIqYbMfZaEd7HdhKSOlYPed3KFt4uUsIeRq6rP2c-IqW_Rmbltq5B1rZl_o3qUhKh6YIame5evnIyVqs_Zz4ipb9GZuW2Rm4qmz3-jpNuBp3-Gm5SM3Laffdm7uaucfc6ulIe2nM2FiNyUhJB624_NfqOBzoTPx3WAm67P2c-JlIzNjZWK2n-c08yDo37agt6GqJGUhM-vdpHRr9Onl4KUg5SGz4LJhXal3IWAg8-Du4pjhcx3zMiDdKI; tmpUserInfo=%7B%22AccountSn%22%3A%2273190267%22%2C%22Info%22%3A%22%E9%9F%A9%E5%A8%9F%22%2C%22UnreadMsgCount%22%3A0%7D; YIHU_Peizhen_Type=; Hm_lvt_50a96b999b752ef15792867dfda15c2a=1486628404,1487033294; Hm_lpvt_50a96b999b752ef15792867dfda15c2a=1487034161; CNZZDATA1256251240=1763306378-1486626946-null%7C1487032202; CNZZDATA1256278949=1042136016-1486624216-null%7C1487032088; jkzl_previsit=1487034161100; YIHU_verifyCookieValue=1; YIHU_UserArea=19%7C200%7C%E5%B9%BF%E5%B7%9E%7C%E5%B9%BF%E4%B8%9C%7CSINGLE_CITY'}

    req = urllib2.Request(
        url=url,
        data=postdata,
        headers=headers
    )
    result = urllib2.urlopen(req)
    result.info()
    html_bytes = result.read()
    html_string = html_bytes.decode('utf-8')
    return html_string, result.info()


def getHtml(url, postdata):
    html_result, headers_result = getHtmlAndHeaders(url, postdata)
    return html_result


def getServerDate(index):
    html_result, headers_result = getHtmlAndHeaders(url_list[index / (len(url_list) - 1)], urllib.urlencode({}))
    server_date_result = datetime.datetime.strptime(headers_result['Date'], '%a, %d %b %Y %H:%M:%S GMT')
    print server_date_result
    return server_date_result


hosp_id = '1255'
dept_id = '7001008'
# 获取排班信息列表
doc_sn = '23682'  # 需配置  张建平=23682   张睿=23683 遗传=710230347
page = '3'  # 需配置
postdata = urllib.urlencode({
    'page': page,
    'doctor_sn': doc_sn,
    'hospital_id': hosp_id
})
yuyue_url = ''
count = 0
# 现在是北京时间6:30放号  服务器时间是22:30
server_date = getServerDate(count)
second = (30 - server_date.minute) * 60 - server_date.second - 1
print '现在时间：', server_date, '等待：', second
# time.sleep(second)

while count < 20:
    count += 1
    html = getHtml("http://www.yihu.com/DoctorArrange/doGetListByPage", postdata)
    soup = BeautifulSoup(html)
    # print soup.prettify()
    element_a = soup.select(".btn-gh")
    if len(element_a) > 0:
        # 获取预约的详细url
        yuyue_url = element_a[0].get('href')
        print '找到可以预约的了,预约url:', yuyue_url
        break
        # time.sleep(0.3)
    else:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ',未找到可以预约的'
        time.sleep(4)

if yuyue_url != '':
    # 获取排班详细信息
    html = getHtml(yuyue_url, urllib.urlencode({}))

    # 解析页面
    # {"NumberSN":"76656477","Store":"cc6341dd-0bf1-4356-914c-b398118dfade","SerialNo":"0","CommendTime":"08:00-09:00","ArrangeID":null,"ModeID":"1","Remark":null,"HintType":"3","CommendScope":"08:00-09:00 \u5269\u4f59\uff1a5","DoctorSN":null,"AccountType":null}
    soup = BeautifulSoup(html)
    # print (soup.prettify())
    element_t = soup.select('.sr-sou li a span')
    print 'element_t size:', len(element_t)
    paiban = element_t[0].get_text()
    print ('paiban:' + paiban)
    paiban_json = json.loads(paiban)

    number_sn = paiban_json['NumberSN']
    store = paiban_json['Store']
    serial_no = paiban_json['SerialNo']
    print 'number_sn:', number_sn, ',store:' + store + ',serial_no:' + serial_no
    postdata = urllib.urlencode({
        'NumberSN': number_sn,
        'Store': store,
        'SerialNo': serial_no,  # 1
        # 'CommendTime': '14:30-15:30',
        'ArrangeID': number_sn,
        'ModeID': '1',  # 1
        'Remark': '',  # 1
        'HintType': '3',  # 1
        # 'CommendScope': '08:00-09:00 4',
        'DoctorSN': '',  # 1
        'AccountType': '',  # 1
        'member_sn': 'sKZ0r6-oo6eCdXmphqV7l4ObjGmvqrNo',  # 1
        # 可固定 医生个人页 var newOtherParams = {"hosid":"1255","deptid":"7001008","doctorid":"710016853"}
        'dept_id': dept_id,  # 科室
        # 可固定 医生个人页 <input type="text" name='doctor_sn' value='710015943' style="display:none;">
        'doc_sn': doc_sn,  # 医生编号
        'hosp_id': hosp_id,  # 医院 1255
        'arrangeId': number_sn,  # 排班id  需求放号时获取
        'province_id': '19',  # 省 19
    })

    html = getHtml("http://www.yihu.com/RegAndArrange/doAddOrder", postdata)
    # html = '{"Code":10000,"Message":"\u6210\u529f","Data":{"Orderid":"87270559711628"}}'
    print html
# data = json.loads(html)
# order_id = data['Data']['Orderid']
# print order_id
# http://www.yihu.com/GuahaoPay/order?order_id=32631798290275&time_id=1
# html = getHtml("http://www.yihu.com/GuahaoPay/order?time_id=1&order_id="+order_id)
# print html
# <table class="fzTab nbt"> </table>

#
# table = html[html.find('<table class="fzTab nbt">') : html.find('</table>')]
# #print (table)
# #<tr onmouseout="this.style.background=''" onmouseover="this.style.background='#fff7d8'">
# #<tr \r\n\t\t                  onmouseout=
# tmp = table.split('<tr \r\n\t\t                  onmouseout=',1)
# #print(tmp)
# #print(len(tmp))
# trs = tmp[1]
# tr = trs[: trs.find('</tr>')]
# #print(tr)
# number = tr.split('<td   >')[1].split('</td>')[0]
# print(number + '期开奖号码：',end='')
# redtmp = tr.split('<td  class="redColor sz12" >')
# reds = redtmp[1:len(redtmp)-1]#去掉第一个和最后一个没用的元素
# #print(reds)
# for redstr in reds:
#     print(redstr.split('</td>')[0] + ",",end='')
#     print('蓝球：',end='')
#     blue = tr.split('<td  class="blueColor sz12" >')[1].split('</td>')[0]
#     print(blue)
