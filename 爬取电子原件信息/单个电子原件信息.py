import re

import pymysql
from lxml import etree
import requests




# url：https://www.tme.eu/cn/zh
# 爬取一类电子原件信息
def get_json_context(id):
    url = 'https://www.tme.eu/category-drawer/tree/'
    headers = {
        'cookie': 'hc=cn; hl=zh; catalogue_products=20; _gcl_au=1.1.1151550619.1651375262; gtmCookie_referrer=direct; _gid=GA1.2.870437385.1651375264; gtmCookie_GAUserId=1046944651.1651375264; cookiebar-confirmed=true; currency=USD; gross_prices=false; hide_catalogue_parameters=false; tme_csrf_https-marketplace=bjoam0ItLprr-7k2P6WdfGL1vxNyns5j1-ELt2TDRbM; tme_csrf_https-newsletter=AcnA5evpIPJok7BqPZfDuCZLe7wT3GxkY_G2eIVpXuc; Hm_lvt_ebbcce60d74d66655cd6746b67652d57=1651375619,1651452563; Hm_lpvt_ebbcce60d74d66655cd6746b67652d57=1651452563; _dc_gtm_UA-262098-4=1; _dc_gtm_UA-71669254-1=1; _dc_gtm_UA-262098-23=1; trfk_ctr=27; _ga_78FNPQNVYC=GS1.1.1651452565.5.1.1651452578.0; _ga=GA1.1.1046944651.1651375264',
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://www.tme.eu/cn/zh/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers)
    return res.json()['category_counter'][f'{id}']
def get_pages_url():
    page_num=get_json_context(112791)
    url_list=[]
    for i in range(1,page_num//100+2):
        print(i)
        url = f'https://www.tme.eu/cn/zh/katalog/smd-tong-yong-er-ji-guan_112791/?s_field=1000012&s_order=asc&limit=100&currency=USD&page={i}'
        print(url)
        url_list.append(url)
    return url_list

def get_html_context(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    }
    # url='https://www.tme.eu/cn/zh/katalog/smd-tong-yong-er-ji-guan_112791/?s_field=1000012&s_order=asc&limit=100&currency=USD&page=11'
    print(url)
    res=requests.get(url,headers=headers)

    return res.text

def analysis_content(text):
    html=etree.HTML(text)
    div=html.xpath('//div[@class="c-product-row__cell c-product-row__cell--description"]')
    # model_list=[]
    # all_info=[]
    model_list = {0, }
    all_info = {0, }
    for d in div:
        model=d.xpath('./span[@class="c-product-row__symbol-row"]/a/@data-gtm-prod-id')
        describe=d.xpath('./div[@class="c-product-row__name-cell-sub-row"]/span/text()')
        producer=d.xpath('.//div[@class="manufacturer c-product-row__name-cell-sub-row"]/a/b[@class="c-product-row__producer-link"]/text()')

        all_info.add(tuple(model+describe+producer))
        # print(model+describe+producer)
        model_list.add(model[0])
    all_info.pop()
    model_list.pop()
    print(len(model_list))
    return all_info,model_list

def post_info(model_list):
    url = 'https://www.tme.eu/_ajax/Catalogue/get-stocks-catalogue.js'
    paramdata = {
        # 'symbols[]': ['1N4448W-E3-08',
        #               '1N4448W-HE3-08',
        #               '1N4448W-TP',
        #               '1N4448WQ-7-F',
        #               '1N4448WS',
        #               '1N4448WS-7-F',
        #               '1N4448WS-DC',
        #               '1N4448WS-DIO',
        #               '1N4448WS-E3-08',
        #               '1N4448WS-HE3-08',
        #               '1N4448WS-YAN',
        #               '1N4448WSF-7',
        #               '1N4448WT',
        #               '1N4448WX-TP',
        #               '1N6481-E3/96',
        #               '1N6483-E3/96',
        #               '1N6484-E3/96',
        #               '1N914BWS',
        #               '1N914BWT',
        #               '1N914WS-DC'],
        'symbols[]':model_list,

        'onlyStocks': '0'

    }
    headers = {
        'authority': 'www.tme.eu',
        'method': 'POST',
        'path': '/_ajax/Catalogue/get-stocks-catalogue.js',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '543',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'catalogue_products=20; _gcl_au=1.1.1992645900.1651375230; hc=cn; hl=zh; cookiebar-confirmed=true; gtmCookie_referrer=http%3A//localhost%3A63342/; gtmCookie_GAUserId=1410370444.1651475141; Hm_lvt_ebbcce60d74d66655cd6746b67652d57=1651501240,1651537044,1651583396,1651754656; _ga=GA1.2.1410370444.1651475141; _ga_78FNPQNVYC=GS1.1.1651760605.7.0.1651760605.0; currency=USD; gross_prices=false; hide_catalogue_parameters=false; catalogue_sort_by=1000012; catalogue_sort_dir=asc; tme_csrf_https-marketplace=XEul98nTT7Vke1I0jp_tRoHBxzSoXw-JB9bVHpDnDOU; tme_csrf_https-newsletter=Z_HoOsu9W2uBG1x4xEgITBu9vT09KvA9YFl-Ajng6Kw; trfk_ctr=39',
        'origin': 'https://www.tme.eu',
        'referer': 'https://www.tme.eu/cn/zh/katalog/smd-tong-yong-er-ji-guan_112791/?s_field=1000012&s_order=asc&limit=20&currency=USD&page=3',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    res = requests.post(url=url, headers=headers, data=paramdata)
    text = res.text
    new_html = re.findall("new_html =.*</div>';", text)
    one_list = []
    for index,i in enumerate(new_html):
        nums = re.findall('\\" >(.*?\\+)', i)
        new_num = []

        for num in nums:
            new_num.append(num.strip('\\n'))
        yuan = re.findall('(\d\.\d*)', i)
        one_list.append((model_list[index],new_num,yuan))

        # print(model_list[index])
        # print(new_num)
        # print(yuan)
    return one_list

def connect_mysql():

    LocalMysql={
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'',
            'db':'tme',
            'charset':'utf8'
        }
    conn = pymysql.Connection(**LocalMysql)
    cur = conn.cursor()
    return cur,conn

def witer_all_info(all_info):
    cur, conn = connect_mysql()
    for info in all_info:
        sql=f"INSERT into all_info(model,descr,manufacturer) VALUES {info}"
        print(sql)
        cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

def updata_data(one_list):
    cur, conn = connect_mysql()
    for i in one_list:
        if i[1]==[]:
            # print(i[0],'产品为特殊订货')
            sql=f"UPDATE all_info SET number='产品为特殊订货',usd='产品为特殊订货'  where model='{i[0]}'"
            cur.execute(sql)

            print(sql)
        else:
            num=",".join(i[1])
            usd=",".join(i[2])
            # print(i[0],",".join(i[1]),",".join(i[2]))
            sql=f"UPDATE all_info SET number='{num}',usd='{usd}' where model='{i[0]}'"
            cur.execute(sql)
            print(sql)
    cur.close()
    conn.commit()
    conn.close()





if __name__ == '__main__':
    url_list=get_pages_url()
    for url in url_list:
        text=get_html_context(url)
        all_info,model_list=analysis_content(text)
        print(all_info)
        print(model_list)
        one_list=post_info(list(model_list))
        print(one_list)
        # 写入数据库
        # witer_all_info(all_info)
        # updata_data(one_list)




