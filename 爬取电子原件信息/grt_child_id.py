import re

import pymysql

import requests
def get_json_context():
    url = 'https://www.tme.eu/category-drawer/tree/'
    headers = {
        'cookie': 'hc=cn; hl=zh; catalogue_products=20; _gcl_au=1.1.1151550619.1651375262; gtmCookie_referrer=direct; _gid=GA1.2.870437385.1651375264; gtmCookie_GAUserId=1046944651.1651375264; cookiebar-confirmed=true; currency=USD; gross_prices=false; hide_catalogue_parameters=false; tme_csrf_https-marketplace=bjoam0ItLprr-7k2P6WdfGL1vxNyns5j1-ELt2TDRbM; tme_csrf_https-newsletter=AcnA5evpIPJok7BqPZfDuCZLe7wT3GxkY_G2eIVpXuc; Hm_lvt_ebbcce60d74d66655cd6746b67652d57=1651375619,1651452563; Hm_lpvt_ebbcce60d74d66655cd6746b67652d57=1651452563; _dc_gtm_UA-262098-4=1; _dc_gtm_UA-71669254-1=1; _dc_gtm_UA-262098-23=1; trfk_ctr=27; _ga_78FNPQNVYC=GS1.1.1651452565.5.1.1651452578.0; _ga=GA1.1.1046944651.1651375264',
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://www.tme.eu/cn/zh/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers)
    return res.json()

def get_semiconductor_id(json_context):

    # print(len(json_context['category_tree'][0]['children']))
    # print(len(json_context['category_tree'][0]['children'][0]['children']))
    semiconductor_lists=json_context['category_tree'][0]['children'][0]['children']
    id_list=[]
    for semiconductor in semiconductor_lists:
        semiconductor_id=semiconductor['id']
        id_list.append(semiconductor_id)
    return id_list
def get_id_name(id_list,json_context):
    for id in id_list:
        print(json_context['category_list'][f'{id}'].get('name'),id)
    pass
def get_sub_id(json_context):
    print(len(json_context['category_tree'][0]['children'][0]['children']))
    sub_id=json_context['category_tree'][0]['children'][0]['children']
    for id in sub_id[0:1]:
        ids=id['children']
        for id in ids:
            # print(id)
            if 'children' in id:
                ids=id['children']
                for id in ids:
                    print(id)
json_context=get_json_context()
# id_list=get_semiconductor_id(json_context)
# get_id_name(id_list,json_context)
# get_sub_id(json_context)
# print()
# json_context['category_tree'][0]['children'][0]['children'[0]]
def get_all_name(json_context):
    id_list=re.findall(r"'id': '(.*?)'",str(json_context['category_tree']))
    print(len(id_list))
    ids_lt={0,}
    for id in id_list:
        ids_lt.add(id)
    for id in ids_lt:
        if id !=0:
            name = json_context['category_list'][f'{id}'].get('name')
            print(id,name)

def get_all_ids(json_context):
    id_list = re.findall(r"'id': '(.*?)'", str(json_context['category_tree']))
    print(len(id_list))
    ids_lt = {0, }
    for id in id_list:
        ids_lt.add(id)
    # for id in ids_lt:
    #     if id != 0:
    #         name = json_context['category_list'][f'{id}'].get('name')
    #         print(id, name)
    ids_lt.pop()
    return ids_lt

def get_all_info(json_context,id):
    id=json_context['category_list'][f'{id}'].get('id')
    name=json_context['category_list'][f'{id}'].get('name')
    href=json_context['category_list'][f'{id}'].get('href')
    if  json_context['category_list'][f'{id}'].get('parent_ids') ==[]:
        return (id, name, 'https://www.tme.eu'+href,'主目录')
    else:
        parent_ids = json_context['category_list'][f'{id}'].get('parent_ids')
        return (id, name, 'https://www.tme.eu'+href, str(parent_ids[0]))

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

def wr_mysql(cur,conn,all_info):
    for info in all_info:
        print(info)
        sql = f'insert into catalog_name values{info}'
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()

def get_all_info_list(ids):

    all_info=[]
    for id in ids:
        if id !=0:
            all_info.append(get_all_info(json_context, id))
    return all_info


# 获取目录信息
if __name__=='__main__':
    ids=get_all_ids(json_context)
    print(ids)
    all_info=get_all_info_list(ids)
    # cur,conn=connect_mysql()
    print(all_info)
    # 保存数据库
    # wr_mysql(cur,conn,all_info)
    # cur.close()








