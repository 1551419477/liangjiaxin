import json
from time import sleep

import pandas
import requests

def post_info():
    url='https://so.quandashi.com/search/search/search-list'
    header={
    'authority': 'so.quandashi.com',
    'method': 'POST',
    'path': '/search/search/search-list',
    'scheme': 'https',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '393',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'user_1885214263=ba0c263a6e061dd0e21da28a4040595f; INGRESSCOOKIE=1654562591.739.11573.841149; PHPSESSID=da4f696409e5638eb61eac6607e8d81d; _csrf=99de5918a4597e60c3d003e8b7f0a873854282624ea6fdf6ffac12bf686c5a13a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Ah-6g0A8Fhtl4PbQG30ZrB0aYPLlVAPs%22%3B%7D; Hm_lvt_df2da21ec003ed3f44bbde6cbef22d1c=1654562592; nTalk_CACHE_DATA={uid:kf_9479_ISME9754_guest24A066B9-7A79-8E,tid:1654562592079404}; NTKF_T2D_CLIENTID=guest24A066B9-7A79-8EDB-3AC2-3B9D954F0986; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221813b9e2e464ec-0ba89f85059d09-26021b51-1049088-1813b9e2e47762%22%2C%22%24device_id%22%3A%221813b9e2e464ec-0ba89f85059d09-26021b51-1049088-1813b9e2e47762%22%2C%22props%22%3A%7B%7D%7D; QDS_COOKIE=FF1F0439-03D3-591B-78B4-614DC1CEEABB; QDS_LOGIN_INFO=%7B%22userName%22%3A%22qds2862384%22%2C%22avtar%22%3A%22%22%7D; QDS_LOGIN_INFO_OFFICE=%7B%22operatorId%22%3A%22732234%22%2C%22operatorName%22%3Anull%2C%22userId%22%3A%22536c2f5a65415659544a536673576b30687a473141513d3d%22%2C%22userName%22%3Anull%2C%22userImg%22%3Anull%2C%22agentOrWriter%22%3A2%7D; QDS_AGENT_ORGAN_INFO=%7B%22agentIde%22%3A%22536c2f5a65415659544a536673576b30687a473141513d3d%22%2C%22account%22%3A%2213148642857%22%2C%22agentName%22%3Anull%2C%22agentOrganId%22%3Anull%2C%22agentOrganName%22%3Anull%2C%22agentOrganConName%22%3A%22%5Cu533f%5Cu540d%22%7D; Hm_lpvt_df2da21ec003ed3f44bbde6cbef22d1c=1654564408',
    'origin': 'https://so.quandashi.com',
    'referer': 'https://so.quandashi.com/index/search?key=%E9%98%BF%E9%87%8C&param=2',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    }
    form_data={
    'key': '阿里',
    'searchKey': '',
    'param': '2',
    'page': '463',
    'pageSize': '9280',
    #     all,jingzhun,high_low_similar,bufen,jiazi,jianzi,bianzi,huanxu,pinyin,teshuzi,xingjinzi
    'styles': 'all,jingzhun,high_low_similar,bufen,jiazi,jianzi,bianzi,huanxu,pinyin,teshuzi,xingjinzi',
    'typeCode': '',
    'statusName': '',
    'createYear': '',
    'groupFilter': '',
    'serviceGoods': '',
    'advanceFilter': '',
    'appkey': '',
    'host': 'so.quandashi.com',
    'sort': '',
    'brandSource': '0',
    'reviewWrit': '0',
    'isReload': '0',
    'graphcode': '',
    'similar_code': '',
    'standard_code': '',
    'applicant': '',
    'address': '',
    'agency': '',
    }
    html=requests.post(url=url,headers=header,data=form_data)
    print(html.text)
    # req=text.encode('utf-8').decode('unicode_escape')
    text=html.text.encode('utf-8').decode('unicode_escape')
    # json1 = json.loads(text, strict=False)

    with open('463_9280.txt','w',encoding='utf-8') as f:
        f.write(text)


def wirtr_to_excle():
    with open('463_9280.txt', encoding='utf-8') as f:
        text = f.read()

    dir_text = json.loads(text)

    item = dir_text.get('data').get('items')
    tmName_list = []
    year_list = []
    regNo_list = []
    detailId_list = []
    appDate_list = []
    statusName_list = []
    statusZh_list = []
    address_list = []
    addressEn_list = []
    announcementDate_list = []
    agency_list = []
    applicantCn_list = []
    enApplicant_list = []
    for i in range(len(item)):
        regNo = item[i].get('regNo')
        regNo_list.append(regNo)

        year = item[i].get('year')
        year_list.append(year)

        detailId = item[i].get('detailId')
        detailId_list.append(detailId)

        appDate = item[i].get('appDate')
        appDate_list.append(appDate)

        statusName = item[i].get('statusName')
        statusName_list.append(statusName)

        statusZh = item[i].get('statusZh')
        statusZh_list.append(statusZh)

        address = item[i].get('address')
        address_list.append(address)

        addressEn = item[i].get('addressEn')
        addressEn_list.append(addressEn)

        announcementDate = item[i].get('announcementDate')
        announcementDate_list.append(announcementDate)

        agency = item[i].get('agency')
        agency_list.append(agency)

        applicantCn = item[i].get('applicantCn')
        applicantCn_list.append(applicantCn)

        enApplicant = item[i].get('enApplicant')
        enApplicant_list.append(enApplicant)

        tmName = item[i].get('tmName')
        tmName_list.append(tmName)

        print('商标名称:', tmName)
        print('申请号:', regNo)
        print('year:', year)
        print('详情页地址:', detailId)
        print('申请日期:', appDate)
        print('状态:', statusName)
        print('法律状态:', statusZh)
        print('申请人地址:', address)
        print('申请人地址En:', addressEn)
        print('初审公告日期:', announcementDate)
        print('代理人名称:', agency)
        print('申请人名称:', applicantCn)
        print('申请人名称En:', enApplicant)
        print("=====================================")

    pd = pandas.DataFrame()

    pd['商标名称'] = tmName_list
    pd['申请号'] = regNo_list
    pd['year'] = year_list
    pd['detailId'] = detailId_list
    pd['申请日期'] = appDate_list
    pd['状态'] = statusName_list
    pd['法律状态'] = statusZh_list
    pd['申请人地址'] = address_list
    pd['申请人地址En'] = addressEn_list
    pd['初审公告日期'] = announcementDate_list
    pd['代理人名称'] = agency_list
    pd['申请人名称'] = applicantCn_list
    pd['申请人名称En'] = enApplicant_list
    pd.to_excel('463_9280.xlsx',index=False)


if __name__=='__main__':
    post_info()
    sleep(5)
    wirtr_to_excle()








