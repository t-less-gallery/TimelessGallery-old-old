import random
import datetime

shared_code_file = "./shared_code.py"
with open(shared_code_file) as file:
    exec(file.read())
operation_name = "mark_sold_in_db"

input_parameters_file = os.path.join(path_to_home, "Input", operation_name, "parameters.py")
template_input_parameters_file = os.path.join(template_dir, f"{operation_name}_parameters.py")



def execute_operation():
    load_db_entry_to_global(item_id)





def add_db_record():
    db = pandas.read_csv(database_file, index_col=literal_db_index)
    if literal_item_id in globals():
        item_id = globals()[literal_item_id]
    else:
        existing_ids = [] if (db.shape[0] == 0) else (db[literal_db_item_id].str.split('-', expand=True)[1].values)
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

    execute_operation()
