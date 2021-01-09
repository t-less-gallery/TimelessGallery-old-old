import os
import shutil
import pandas as pd
import random
import datetime
import item_profile_order
import shopify_upload
from shutil import copy


operation_name = "add_to_db"
path_to_home = ".."
input_parameters_file = os.path.join(path_to_home, "Input", operation_name, "parameters.py")
input_images_dir = os.path.join(path_to_home, "Input", operation_name, "Pictures")
database_file = os.path.join(path_to_home, "Data", "database.csv")
profiles_dir = os.path.join(path_to_home, "Data", "Profiles")
template_dir = os.path.join(path_to_home, "Template")
template_input_parameters_file = os.path.join(template_dir, f"{operation_name}_parameters.py")

literal_input_item_id = "item_id"
literal_input_catalogue_number = "catalogue_number"
literal_input_item_name = "item_name"
literal_input_period = "period"
literal_input_age_class = "age_class"
literal_input_condition = "condition"
literal_input_collection_class = "collection_class"
literal_input_item_cost = "item_cost"
literal_input_pricing = "pricing"
literal_database_index = "Table Index"
literal_database_item_id = "Item ID"

new_id_prefix = "F"
manufacturer_brand = "Royal Doulton"
required_db_columns = [literal_input_catalogue_number, literal_input_item_name, literal_input_period, literal_input_age_class, literal_input_condition, literal_input_collection_class, literal_input_item_cost, literal_input_pricing]
valid_image_extensions = (".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG")
date_today = datetime.datetime.now().strftime("%Y-%m-%d")

with open(input_parameters_file) as file:
    exec(file.read())
db = pd.read_csv(database_file, index_col=literal_database_index)

image_names = os.listdir(input_images_dir)
image_names.sort()
for name in image_names:
    assert name.endswith(valid_image_extensions), f'invalid image extension: {name}'
for column in required_db_columns:
    assert globals()[column] != '', f'column should not be empty: {column}'

if literal_input_item_id in globals():
    item_id = globals()[literal_input_item_id]
else:
    existing_ids = [] if (db.shape[0] == 0) else (db[literal_database_item_id].str.split('-', expand=True)[1].values)
    item_id = new_id_prefix + '-' + str(random.choice([x for x in range(1,10_000) if x not in existing_ids]))
additional_cost = 0.0 if (additional_cost == '') else float(additional_cost)
acquisition_date = acquisition_date.strftime("%Y-%m")
length = None if (length == '') else float(length)
width = None if (width == '') else float(width)

new_item = {
    'Item ID':item_id,
    'Status':'In Stock',  # ['in stock', 'sold', 'on hold', 'display only']
    'Catalogue Number':catalogue_number,
    'Item Name':item_name,
    'Period':period,
    'Condition':condition, # perfect, great, good, fair, and customized
    'Pricing':float(pricing),
    'Sold Price':None,
    'Rareness':rareness,
    'Short Highlight':short_highlight,
    'Collection Class':collection_class,
    'Manufacturer':manufacturer_brand,
    'Artist':artist,
    'Series':series,
    'Model Start Year':model_start_year,
    'Model End Year':model_end_year,
    'Age Class':age_class,
    'Height':float(height),
    'Length':length,
    'Width':width,
    'Market Average':float(market_average),
    'Creation Date':date_today,
    'Status Date':date_today,
    'Provenance':provenance,
    'Acquisition Date':acquisition_date,
    'Item Cost':float(item_cost),
    'Additional Cost':additional_cost,
    'Total Cost':float(item_cost) + additional_cost
}
new_db_index = 0 if (db.shape[0] == 0) else (int(db.index.max()) + 1)
db = db.append(pd.Series(new_item, name=new_db_index))

item_profile_dir = os.path.join(profiles_dir, item_id)
item_profile_pictures_dir = os.path.join(item_profile_dir, "Pictures")
operation_backup_dir = os.path.join(item_profile_dir, "Misc", "Backup")
item_profile_file = os.path.join(item_profile_dir, 'profile.txt')
input_backup_file = os.path.join(operation_backup_dir, f'{operation_name}_parameters.py')
os.mkdir(item_profile_dir)
os.mkdir(item_profile_pictures_dir)
os.makedirs(operation_backup_dir)

for i, name in enumerate(image_names):
    new_name = item_id + '_' + str(i + 1).zfill(2) + '.jpg'
    os.rename(os.path.join(input_images_dir, name), os.path.join(item_profile_dir, 'Pictures', new_name))
os.rmdir(input_images_dir)

with open(item_profile_file, 'w') as file:
    last_row_of_DB = db.iloc[-1].to_dict()
    file.write('-'*35+'\n')
    for key in item_profile_order.item_profile_order:
        if key == 'newline':
            line = '\n\n'
            file.write(line)
        else:
            value = last_row_of_DB[key]
            if value == None:
                value = ''
            number_of_space = 19 - len(key)
            line = f'{key}' + ' '*number_of_space + f'{value}\n'
            file.write(line)
            file.write('-'*35+'\n')

os.rename(input_parameters_file, input_backup_file)
shutil.copy(template_input_parameters_file, input_parameters_file)
db.to_csv(database_file)
