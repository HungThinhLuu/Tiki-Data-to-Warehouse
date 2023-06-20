import requests
import os
from concurrent.futures import ThreadPoolExecutor

url = 'https://tiki.vn/api/v2/products/{}'
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
id_path = './data/productID'

def crawl_data(root):
    path = root.replace('/data/productID/', '/data/product/')
    if not os.path.exists(path):
        os.makedirs(path)
    with open(root + '/ids.txt', 'r') as f:
        id_list = f.readlines()
        for id in id_list:
            file = open(path + '/' + str(id) + '.txt', 'w')
            response = requests.get(url.format(id), headers=headers)
            if (response.status_code == 200):
                file.write(response.text)
    print('Save detail file of ' + path )
        

with ThreadPoolExecutor(max_workers=5) as executor:
    for root, dirs, files in os.walk(id_path):
        if len(files) != 0:
            executor.submit(crawl_data, root)