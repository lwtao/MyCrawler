# -*- coding: utf-8 -*-
import urllib
import urllib2
import json


def getHtml(url):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
               'Cookie':
                   'jkzl_channelid=1000000; jkzl_uuid=64CFEBC1-E321-4331-95F6-F4400898DF4D; _365groups_ClientID=c4d43280-deab-43ee-99fe-5dd61df80da9; PHPSESSID=63ia6nr219019gec8g6edgjt84; YIHU_webNotic=%3F; jkzl_sid=6BCEBF6F-FD5A-4025-921F-2A4DDB9E5591; YIHU_userInfo=hbaL2q-cjJmvurPdgZWpzIm5hsuYZbrYmn-D2H7OpJmG3IPbsYZ43q_Qxc-ApYCnkbqCzIqgutePpovcfs6kmYXMd9qvrHyarqqrl4G1f9aBzo7bkIqurYh8fpl-z45jhtyApbB2eJauqsnegaaIqYbMfZaEd7HdhKSOlYPed3KFt4uUsIeRq6rP2c-IqW_Rmbltq5B1rZl_o3qUhKh6YIame5evnIyVqs_Zz4ipb9GZuW2Rm4qmz3-jpNuBp3-Gm5SM3Laffdm7uaucfc6ulIe2nM2FiNyUhJB624_NfqOBzoTPx3WAm67P2c-JlIzNjZWK2n-c08yDo37agt6GqJGUhM-vdpHRr9Onl4KUg5SGz4LJhXal3IWAg8-Du4pjhcx3zMiDdKI; tmpUserInfo=%7B%22AccountSn%22%3A%2273190267%22%2C%22Info%22%3A%22%E9%9F%A9%E5%A8%9F%22%2C%22UnreadMsgCount%22%3A0%7D; YIHU_Peizhen_Type=; Hm_lvt_50a96b999b752ef15792867dfda15c2a=1486628404,1487033294; Hm_lpvt_50a96b999b752ef15792867dfda15c2a=1487034161; CNZZDATA1256251240=1763306378-1486626946-null%7C1487032202; CNZZDATA1256278949=1042136016-1486624216-null%7C1487032088; jkzl_previsit=1487034161100; YIHU_verifyCookieValue=1; YIHU_UserArea=19%7C200%7C%E5%B9%BF%E5%B7%9E%7C%E5%B9%BF%E4%B8%9C%7CSINGLE_CITY'}

    postdata = urllib.urlencode({
        'NumberSN': '77038324',
        'Store': '665357ac-6819-4d49-a069-57f5a0e79049',
        'SerialNo': '0',
        'CommendTime': '08:00-09:00',
        'ArrangeID': '77038324',
        'ModeID': '1',
        'Remark': '',
        'HintType': '3',
        'CommendScope': '08:00-09:00 4',
        'DoctorSN': '',
        'AccountType': '',
        'member_sn': 'sKZ0r6-oo6eCdXmphqV7l4ObjGmvqrNo',
        'dept_id': '7152377',  # 科室
        'doc_sn': '710724576',  #
        'hosp_id': '965',  # 医院
        'arrangeId': '77038324',
        'province_id': '19',
    })
    req = urllib2.Request(
        url=url,
        data=postdata,
        headers=headers
    )

    result = urllib2.urlopen(req)
    html_bytes = result.read()
    html_string = html_bytes.decode('utf-8')
    return html_string


# url = http://zst.aicai.com/ssq/openInfo/
# 最终输出结果格式如：2015075期开奖号码：6,11,13,19,21,32, 蓝球：4
html = getHtml("http://www.yihu.com/RegAndArrange/doAddOrder")
# html = '{"Code":10000,"Message":"\u6210\u529f","Data":{"Orderid":"87270559711628"}}'
print html
data = json.loads(html)
order_id = data['Data']['Orderid']

#http://www.yihu.com/GuahaoPay/order?order_id=32631798290275&time_id=1
html = getHtml("http://www.yihu.com/GuahaoPay/order?time_id=1&order_id="+order_id)
print html
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
