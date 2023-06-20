import requests
import json

url = "https://api.tiki.vn/raiden/v2/menu-config?platform=desktop"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

response = requests.get(url, headers = headers)

root_category_info = json.loads(response.text)["menu_block"]['items']

root_category_info = filter(lambda item: item['text'] != "NGON", root_category_info)

dict_root_category = {}
for category in root_category_info:
    dict_root_category[int(category['link'].split('/')[-1][1:])] = category['text']

with open('./root-category.json', "w") as f:
    json.dump(dict_root_category, f)
