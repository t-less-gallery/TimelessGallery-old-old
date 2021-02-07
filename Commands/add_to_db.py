import random
import datetime

shared_code_file = "./shared_code.py"
with open(shared_code_file) as file:
    exec(file.read())
operation_name = "add_to_db"

input_parameters_file = os.path.join(path_to_home, "Input", operation_name, "parameters.py")
input_images_dir = os.path.join(path_to_home, "Input", operation_name, "Pictures")
template_input_parameters_file = os.path.join(template_dir, f"{operation_name}_parameters.py")

new_id_prefix = "F"
manufacturer_brand = "Royal Doulton"
valid_image_extensions = (".jpg", ".JPG", ".jpeg", ".JPEG")
date_today = datetime.datetime.now().strftime("%Y-%m-%d")
required_input = [
    literal_catalogue_number,
    literal_item_name,
    literal_period,
    literal_age_class,
    literal_condition,
    literal_collection_class,
    literal_item_cost,
    literal_pricing
]


def execute_operation():
    input_validation()
    add_db_record()
    add_imagebase_record()
    backup_input_parameters()
    reset_input_parameters()


def input_validation():
    image_names = os.listdir(input_images_dir)
    for name in image_names:
        assert name.endswith(valid_image_extensions), f'invalid image extension: {name}'
    for input in required_input:
        assert globals()[input] != '', f'column should not be empty: {input}'


def add_db_record():
    db = pandas.read_csv(database_file, index_col=literal_db_index)
    if globals()[literal_item_id] != '':
        item_id = globals()[literal_item_id]
    else:
        existing_ids = [] if (db.shape[0] == 0) else (db[literal_db_item_id].str.split('-', expand=True)[1].values)
        existing_ids = list(map(int,existing_ids))
        item_id = new_id_prefix + '-' + str(random.choice([x for x in range(1,10_000) if x not in existing_ids]))

    new_item = {
        literal_db_item_id:item_id,
        literal_db_status:'In Stock',  # ['in stock', 'sold', 'on hold', 'display only']
        literal_db_catalogue_number:catalogue_number,
        literal_db_item_name:item_name,
        literal_db_period:period,
        literal_db_condition:condition, # perfect, great, good, fair, and customized
        literal_db_pricing:float(pricing),
        literal_db_sold_price:None,
        literal_db_finalization:None,
        literal_db_rareness:rareness,
        literal_db_short_highlight:short_highlight,
        literal_db_collection_class:collection_class,
        literal_db_manufacturer:manufacturer_brand,
        literal_db_artist:artist,
        literal_db_series:series,
        literal_db_model_start_year:model_start_year,
        literal_db_model_end_year:model_end_year,
        literal_db_age_class:age_class,
        literal_db_height:float(height),
        literal_db_length:length,
        literal_db_width:width,
        literal_db_market_average:market_average,
        literal_db_creation_date:date_today,
        literal_db_status_date:date_today,
        literal_db_provenance:provenance,
        literal_db_acquisition_date:acquisition_date,
        literal_db_item_cost:float(item_cost),
        literal_db_additional_cost:additional_cost,
        literal_db_total_cost:float(item_cost) + additional_cost
    }
    new_db_index = 0 if (db.shape[0] == 0) else (int(db.index.max()) + 1)
    db = db.append(pandas.Series(new_item, name=new_db_index))
    db.to_csv(database_file)


def add_imagebase_record():
    image_names = os.listdir(input_images_dir)
    image_names.sort()
    for i, name in enumerate(image_names):
        new_name = item_id + '_' + str(i + 1).zfill(2) + '.jpg'
        os.rename(os.path.join(input_images_dir, name), os.path.join(input_images_dir, new_name))
    item_image_dir = os.path.join(imagebase_dir, item_id)
    shutil.move(input_images_dir, item_image_dir)


def backup_input_parameters():
    item_backup_dir = os.path.join(backup_dir, item_id)
    os.mkdir(item_backup_dir)
    item_backup_file = os.path.join(item_backup_dir, f'{operation_name}_parameters.py')
    shutil.move(input_parameters_file, item_backup_file)


def reset_input_parameters():
    shutil.copy(template_input_parameters_file, input_parameters_file)


if __name__ == "__main__":
    with open(input_parameters_file) as file:
        exec(file.read())

    additional_cost = 0.0 if (additional_cost == '') else float(additional_cost)
    acquisition_date = acquisition_date.strftime("%Y-%m")
    length = None if (length == '') else float(length)
    width = None if (width == '') else float(width)
    market_average = None if (market_average == '') else float(market_average)

    execute_operation()
