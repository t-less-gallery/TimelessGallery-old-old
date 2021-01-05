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
import random
import datetime
from generate_add_parameters_template import write_a_empty_new_item_py

# +
# product_database_file = '../data/item_DB.csv'  #

# db = pd.DataFrame(
#         columns=[
#             'Table Index',
#             'Item ID',
#             'Catalogue Number',
#             'Item Name',
#             'Total Cost',
#             'Status',
#             'Pricing',
#             'Sold Price',
            
#             'Artist',
#             'Manufacturer',
#             'Series',
#             'Model Start Year',
#             'Model End Year',
#             'Period',
#             'Age Class',
#             'Height',
#             'Length',
#             'Width',
    
#             'Market Average',
#             'Rareness',
#             'Condition',
#             'Short Highlight',
#             'Collection Class',

#             'Item Cost',
#             'Additional Cost',

#             'Status Date',
#             'Creation Date',
#         ]
#     ).set_index('Table Index')

# db.to_csv(product_database_file)

# -

new_item_file = '../Input/add/parameters.py'  
wip_image_dir = '../Input/add/Pictures'  # Only jpg images
product_database_file = '../Data/item_DB.csv'
image_dir = '../Data/Profiles'

# +
image_names = os.listdir(wip_image_dir)
image_names.sort()

for i, image_name in enumerate(image_names):
    assert '.jpg' in image_name, f'WIP image folder has a non-JPG file: {image_name}'
    
# Import variables
with open(new_item_file) as file:
    tmp = file.read()
    exec(tmp)
    
# Check if there is empty string in the non-null columns
for column in [
    'catalogue_number',
    'item_name',
    'period',
    'age_class',
    'condition',
    'collection_class',
    'item_cost',
    'pricing',
]:
    assert globals()[column] != '', f'{column} should not be empty'

# +
'''
Read a existing DB, append a new item to database and overwrite DB
Note: It doesn't check duplicates
'''
# Read existing DB
db = pd.read_csv(product_database_file, index_col='Table Index')

# Create unique ID
if db.shape[0] != 0:
    existing_ids = db['Item ID'].str.split('-', expand=True)[1].values
else:
    existing_ids = []
item_id = 'F-' + str(random.choice([x for x in range(1,10_000) if x not in existing_ids]))

#
if additional_cost == '':
    additional_cost = 0


new_product = {
    'Item ID':item_id,
    
    'Catalogue Number':catalogue_number,  # non-null
    'Item Name':item_name,  # non-null
    'Artist':artist,
    'Manufacturer':'Royal Doulton',
    'Series':series,
    'Model Start Year':model_start_year,
    'Model End Year':model_end_year,
    'Period':period, # non-null
    'Age Class':age_class,  # non-null
    'Height':height,
    'Length':length,
    'Width':width,
    
    'Market Average':market_average,
    'Rareness':rareness,
    'Condition': condition, # non-null # perfect, great, good, fair, and customized (from short highlight)
    'Short Highlight':short_highlight,
    'Collection Class':collection_class,  # non-null

    'Item Cost':item_cost,  # non-null
    'Additional Cost':additional_cost, # 0 if empty string
    'Total Cost':float(item_cost)+float(additional_cost),
    'Pricing':pricing,  # non-null
    'Sold Price':None,
    'Status':'In Stock',  # ['in stock', 'sold', 'on hold', 'display only']
    'Status Date':datetime.datetime.now().strftime('%Y-%m-%d'),
    'Creation Date':datetime.datetime.now().strftime('%Y-%m-%d'),

}

# Change empty string to None
for key, value in new_product.items():
    if value == '':
        new_product[key] = None

if db.shape[0] == 0:
    new_index = 0
else:
    new_index = int(db.index.max()) + 1
db = db.append(pd.Series(new_product, name=new_index))

# +
# move image to image folder. Folder name is item_code. Image name is the order.
image_names = os.listdir(wip_image_dir)
image_names.sort()

os.mkdir(os.path.join(image_dir, str(new_product['Item ID'])))
for i, image_name in enumerate(image_names):
    os.rename(
        os.path.join(wip_image_dir, image_name),
        os.path.join(image_dir, str(new_product['Item ID']), new_product['Item ID']+f'_{i}.jpg')
    )
# -

write_a_empty_new_item_py(new_item_file)
db.to_csv(product_database_file)
