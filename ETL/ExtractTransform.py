import os
import json
import csv

path = './data-v2/product/'

fields = ['id', 'name', "price", "original_price", "discount", "discount_rate", "rating_average", "review_count", "primary_category_name", "id_category", "category_path"]

output = open('product.csv',mode='w')
writer = csv.writer(output)
writer.writerow(fields)

for root, dirs, files in os.walk(path):
    if len(files) != 0:
        category_path = root.replace(path, '')
        for file in files:
            if file == 'ids.txt':
                continue
            with open(root + '/' + file, 'r') as f:
                data = json.load(f)
                data["category_path"] = category_path
                data["primary_category_name"] = category_path.split('/')[-1]
                writer.writerow([data[field] for field in fields])
output.close()