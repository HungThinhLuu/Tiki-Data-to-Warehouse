import requests
from concurrent.futures import ThreadPoolExecutor
import json
import os
import time

url_category_info = "https://tiki.vn/api/v2/categories?parent_id={}"
url_product_info = "https://tiki.vn/api/v2/products?limit=100&category={}&page={}&price={},{}"
url_product_info_without_price = "https://tiki.vn/api/v2/products?limit=100&category={}&page={}"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
path = './data-v2/product/'
price_step = 75000
sleep_time = 10

def crawl_ids_with_price(id):
    print('Start crawl for category ' + str(id) + ' with price')
    id_list = []
    detail_list = []
    l_price = 0
    r_price = price_step
    count = 0
    while True:
        page = 1
        while True:
            response = requests.get(url_product_info.format(id, page, l_price, r_price), headers=headers)
            
            if (response.status_code != 200):
                print('At {} sleep {} sec'.format(id, sleep_time))
                time.sleep(sleep_time)
                continue

            try:
                # data = json.loads(response.text.strip("'<>() ").replace('\'', '\"'))
                data = json.loads(response.text)
            except Exception as e:
                print('At {} sleep {} sec'.format(id, sleep_time))
                time.sleep(sleep_time)
                continue
            products = data["data"]

            if len(products) == 0:
                count += 1
                break
            for product in products:
                product_id = str(product["id"])
                if product_id not in id_list:
                    id_list.append(product_id)
                    product['id_category'] = id
                    detail_list.append(product)
            if page == data['paging']["last_page"]:
                count = 0
                break
            page += 1
        if count == 15:
            break
        l_price += price_step
        r_price += price_step

    return id_list, detail_list

def crawl_ids_without_price(id):
    print('Start crawl for category ' + str(id) + ' without price')
    id_list = []
    detail_list = []
    page = 1
    while True:
        response = requests.get(url_product_info_without_price.format(id, page), headers=headers)
            
        if (response.status_code != 200):
            print('At {} sleep {} sec'.format(id, sleep_time))
            time.sleep(sleep_time)
            continue

        try:
            # data = json.loads(response.text.strip("'<>() ").replace('\'', '\"'))
            data = json.loads(response.text)
        except Exception as e:
            print('At {} sleep {} sec'.format(id, sleep_time))
            time.sleep(sleep_time)
            continue
        products = data["data"]
        for product in products:
            product_id = str(product["id"])
            if product_id not in id_list:
                id_list.append(product_id)
                product['id_category'] = id
                detail_list.append(product)
        if page == data['paging']["last_page"]:
            break
        page += 1
    return id_list, detail_list


def crawl_ids(id, count, cur_sub_path):
    ids = []
    if count <= 2000:
        ids, details =  crawl_ids_without_price(id)
    else:
        ids, details = crawl_ids_with_price(id)
    if not os.path.exists(path + cur_sub_path):
        os.makedirs(path + cur_sub_path)
    f = open(path + cur_sub_path + '/ids.txt', 'w+')
    f.write("\n".join(ids))
    f.close()
    for item in details:
        f = open(path + cur_sub_path + '/' + str(item['id']) + '.txt', 'w+')
        json.dump(item, f)
        f.close()
    print('Save file for ' + cur_sub_path)
    

# def callback(cur_sub_path):
#     def temp_call(res):
#         ids = res.result()
#         if not os.path.exists(path + cur_sub_path):
#             os.makedirs(path + cur_sub_path)
#         print('Save file for ' + cur_sub_path)
#         f = open(path + cur_sub_path + '/ids.txt', 'w+')
#         f.write("\n".join(ids))
#         f.close()
#     return temp_call

def process(id, root):
    id_list = [(id, root, 0)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        while len(id_list) != 0:
            cur_id, cur_sub_path, cur_count = id_list.pop()
            response = requests.get(url_category_info.format(cur_id), headers = headers)
            
            if (response.status_code != 200):
                break
            data = json.loads(response.text)['data']

            child_id = list(map(lambda item: (item['id'], cur_sub_path + '/' + item['name'], item['product_count']), data))

            if len(child_id) != 0:
                id_list = id_list + child_id
            else:
                executor.submit(crawl_ids, cur_id, cur_count, cur_sub_path)
                # future.add_done_callback(callback(cur_sub_path=cur_sub_path))

with open('root-category.json', 'r') as f:
    root_category = json.load(f)
    val = "8322"
    process(val, root_category[val])
