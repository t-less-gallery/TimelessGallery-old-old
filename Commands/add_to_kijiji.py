import os
import pandas
import yaml
import subprocess
import math

shared_code_file = "./shared_code.py"
with open(shared_code_file) as file:
    exec(file.read())
operation_name = "add_to_kijiji"


template_yaml_file = os.path.join(template_dir, "kijiji_item.yaml")
literal_yaml_title = "postAdForm.title"
literal_yaml_pricing = "postAdForm.priceAmount"
literal_yaml_images = "image_paths"
literal_yaml_description = "postAdForm.description"


def execute_operation(item_id):
    command_backup_dir = os.path.join(backup_dir, item_id)
    item_yaml_file = os.path.join(imagebase_dir, item_id, f"add_to_kijiji.yaml")

    load_db_entry_to_global(item_id)

    description = f"Details:\nhttps://timelessgallery.ca/products/{item_id}\n \n \n \nI have hundreds of other Royal Doulton figurines.\nPlease visit:\n \n \nhttps://timelessgallery.ca/collections/royal-doulton-figurines"
    yaml_parameters = {
        literal_yaml_title: f'{catalogue_number} {item_name} - {age_class} {manufacturer} figurine',
        literal_yaml_pricing: f'{math.ceil(pricing * 1.1 / 5.0) * 5}',
        literal_yaml_images: fetch_images(item_id),
        literal_yaml_description: description
    }
    with open(template_yaml_file) as file:
        item_yaml = yaml.load(file, Loader=yaml.FullLoader)
    for key, value in yaml_parameters.items():
        item_yaml[key] = value
    with open(item_yaml_file, 'w') as file:
        yaml.dump(item_yaml, file)

    os.system('python kijiji_repost_headless -s ssid.txt post ' + item_yaml_file)

    backup_yaml()


def fetch_images(item_id):
    item_image_dir = os.path.join(imagebase_dir, item_id)
    images = []
    for name in os.listdir(item_image_dir):
        if not name.startswith("."):
            images.append(name)
    assert len(images) > 0, f'No image file in {item_image_dir}'
    return images


def backup_yaml():
    item_yaml_file = os.path.join(imagebase_dir, item_id, f"{operation_name}.yaml")
    item_backup_dir = os.path.join(backup_dir, item_id)
    item_backup_file = os.path.join(item_backup_dir, f'{operation_name}.yaml')
    shutil.move(item_yaml_file, item_backup_file)


if __name__== '__main__':
    assert len(sys.argv) == 2, f"incorrect number of arguments: need 1, actual {len(sys.argv) - 1}"
    item_id = sys.argv[1]

    execute_operation(item_id)
