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
import item_profile_order
from generate_backfill_parameters_template import write_a_empty_new_item_py

new_item_file = '../Input/backfill/parameters.py'  
wip_image_dir = '../Input/backfill/Pictures'  # Only jpg images
product_database_file = '../Data/item_DB.csv'
profile_dir = '../Data/Profiles'

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
    'item_id',
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

#
if additional_cost == '':
    additional_cost = 0


new_product = {
    'Item ID':item_id,  # not-null
    
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

    'Item Cost':float(item_cost),  # non-null
    'Additional Cost':float(additional_cost), # 0 if empty string
    'Total Cost':float(item_cost)+float(additional_cost),
    'Pricing':float(pricing),  # non-null
    'Sold Price':None,
    'Status':'In Stock',  # ['in stock', 'sold', 'on hold', 'display only']
    'Status Date':datetime.datetime.now().strftime('%Y-%m-%d'),
    'Creation Date':datetime.datetime.now().strftime('%Y-%m-%d'),

}


if db.shape[0] == 0:
    new_index = 0
else:
    new_index = int(db.index.max()) + 1
db = db.append(pd.Series(new_product, name=new_index))

# +
# move image to image folder. Folder name is item_code. Image name is the order.
image_names = os.listdir(wip_image_dir)
image_names.sort()

os.mkdir(os.path.join(profile_dir, str(new_product['Item ID'])))
os.mkdir(os.path.join(profile_dir, str(new_product['Item ID']), 'Pictures'))

for i, image_name in enumerate(image_names):
    i += 1
    if i < 10:
        i = f'0{i}'
    os.rename(
        os.path.join(wip_image_dir, image_name),
        os.path.join(profile_dir, str(new_product['Item ID']), 'Pictures', new_product['Item ID']+f'_{i}.jpg')
    )


# +
item_profile_txt_file = os.path.join(
    profile_dir,
    str(new_product['Item ID']),
    'item_profile.txt'
)
with open(item_profile_txt_file, 'w') as file:
    last_row_of_DB = db.iloc[-1].to_dict()
    for key in item_profile_order.item_profile_order:
        if key == 'newline':
            line = '\n\n'
            file.write(line)
        else:
            value = last_row_of_DB[key]
            if value == None:
                value = ''
            number_of_space = 18 - len(key)
            line = f'{key}' + ' '*number_of_space + f'{value}\n'
            file.write(line)
            file.write('-'*35+'\n')

            
os.mkdir(os.path.join(profile_dir, str(new_product['Item ID']), 'Misc'))
os.rename(
    os.path.join(new_item_file),
    os.path.join(profile_dir, str(new_product['Item ID']), 'Misc','backfill_parameters.py')
)
write_a_empty_new_item_py(new_item_file)
db.to_csv(product_database_file)
