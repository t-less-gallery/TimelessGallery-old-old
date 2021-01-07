# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import os
import pandas as pd
import base64
import requests
import json

# +
# product_database_file = '../Data/item_DB.csv'
# profile_dir = '../Data/Profiles'

# +
api_key='6ae5f1a8049eb87f1a430722b37bbc35'
api_password = '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'
hostname = 'timeless-gallery-antique.myshopify.com'
version = '2021-01'

auth = f'{api_key}:{api_password}'
b64_auth = base64.b64encode(auth.encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "application/json" 
}


# +
# db = pd.read_csv(product_database_file,index_col='Table Index')
# item_dict = db[db['Item ID'] == target_id].squeeze().to_dict()

# +
# '12332'.replace("2", "0")

# +
# item_dict['Item Name']
# title = \
# item_dict['Catalogue Number'] + \
# " " + \
# item_dict['Item Name'] + \
# " - " + \
# item_dict['Age Class'] + \
# " Porcelain Figurine by " + \
# item_dict['Manufacturer'] + \
# ", " + \
# item_dict['Period'] + \
# " " + \
# "(Item# " + \
# item_dict['Item ID'] + \
# ")"
# -

def shopify_list_new_item(
    item_name,
    catalogue_number,
    age_class,
    manufacturer,
    period,
    item_id,
    product_type,
    tags,
    profile_dir,
    product_database_file
):
    images_list = []
    pictures_folder = os.path.join(profile_dir, item_id, 'Pictures')
    for file in os.listdir(pictures_folder):
        if '.jpg' in file or '.png' in file:
            with open(os.path.join(pictures_folder, file), 'rb') as file:
                pic = file.read()
            base64_image = base64.b64encode(pic).decode()
            image_dict = {
                "attachment": f"{base64_image}\n",
                "filename": "??"
            }
            images_list.append(image_dict)
    
    title = f"{catalogue_number} {item_name} - {age_class} Porcelain Figurine by {manufacturer}, {period} (Item# {item_id})"
    # https://shopify.dev/docs/admin-api/rest/reference/products/product
    new_item_json = {
      "product": {
        "title": title,
        "body_html": "<strong>Good snowboard!</strong>",
        "vendor": "Timeless Gallery",
        "product_type": product_type,
        "tags": [
          "Barnes & Noble",
          "John's Fav",
          "Big Air"
        ],
        "images": images_list
      }
    }
    response = requests.post(
        url=f"https://{hostname}/admin/api/{version}/products.json",
        headers=headers,
        data=json.dumps(new_item_json)
    )
    print(response)


