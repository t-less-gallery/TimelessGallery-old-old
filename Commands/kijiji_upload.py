# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: post-kijiji
#     language: python
#     name: post-kijiji
# ---

import os
import pandas
import yaml
import subprocess


# +
# shared_settings_file = "./shared_settings.py"
# with open(shared_settings_file) as file:
#     exec(file.read())
    
# operation_name = "kijiji-upload"
# template_dir = os.path.join(path_to_home, "Template")
# template_kijiji_yaml_file = os.path.join(template_dir, f"item.yaml")
# temporary_yaml_file = os.path.join(path_to_home, 'Input', 'Temp', f"item.yaml")

# literal_yaml_title = "postAdForm.title"
# literal_yaml_pricing = "postAdForm.priceAmount"
# literal_yaml_images = "image_paths"
# -

def operation():
    assert len(sys.argv) == 2, f"incorrect number of arguments: need 1, actual {len(sys.argv) - 1}"
    access_key = sys.argv[1]
    db = pandas.read_csv(database_file, index_col=literal_db_index, keep_default_na=False)
    access_column = literal_db_item_id
    assert (db[access_column]==access_key).sum(), f"entry doesn't exist: {access_column} -> {access_key}"
    db_item = db[db[access_column] == access_key].squeeze().to_dict()
    
    # Put your yaml entry here
    image_path_list = add_image(access_key)
    yaml_fulfillment = {
        literal_yaml_title: f'{db_item[literal_db_item_name]} - {db_item[literal_db_manufacturer]}',
        literal_yaml_pricing: f'{db_item[literal_db_pricing]}',
        literal_yaml_images: image_path_list
    }

    with open(template_kijiji_yaml_file) as file:
        item_yaml = yaml.load(file, Loader=yaml.FullLoader)
        
    for key, value in yaml_fulfillment.items():
        item_yaml[key] = value
        
    item_yaml_file = os.path.join(path_to_home, 'Data', 'Profiles', access_key, 'Misc', f"item.yaml")
    with open(item_yaml_file, 'w') as file:
        yaml.dump(item_yaml, file)
        
    command_object = subprocess.run(
        ['python','kijiji_repost_headless','-s', 'ssid.txt', 'post', item_yaml_file],
        capture_output=True
    )
    print(command_object.stderr)
    print(command_object.stdout)


# +
def add_image(access_key):
    '''
    Input: Item ID
    Ouput: [relative path to image_1, relative path to image_2, ...]
    '''
    valid_image_extensions = (".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG")
    item_image_dir = os.path.join(path_to_home, "Data", "Profiles", access_key, 'Pictures')
    output = []
    for image_name in os.listdir(item_image_dir):
        if image_name.endswith(valid_image_extensions):
            output.append(os.path.join('..', 'Pictures', image_name))
    assert len(output) > 0, f'No image file in {item_image_dir}'
    return output
    
    
    
# -

if __name__== '__main__':
    shared_settings_file = "./shared_settings.py"
    with open(shared_settings_file) as file:
        exec(file.read())

    operation_name = "kijiji-upload"
    template_dir = os.path.join(path_to_home, "Template")
    template_kijiji_yaml_file = os.path.join(template_dir, f"item.yaml")

    literal_yaml_title = "postAdForm.title"
    literal_yaml_pricing = "postAdForm.priceAmount"
    literal_yaml_images = "image_paths"
    
    operation()


