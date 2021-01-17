import datetime

shared_code_file = "./shared_code.py"
with open(shared_code_file) as file:
    exec(file.read())
operation_name = "mark_sold_in_db"

input_parameters_file = os.path.join(path_to_home, "Input", operation_name, "parameters.py")
template_input_parameters_file = os.path.join(template_dir, f"{operation_name}_parameters.py")
date_today = datetime.datetime.now().strftime("%Y-%m-%d")

def execute_operation():
    parameter_additional_cost = additional_cost
    parameter_sold_price = sold_price

    load_db_entry_to_global(item_id)
    db = pandas.read_csv(database_file, index_col=literal_db_index, keep_default_na=False)

    assert status == 'In Stock', f"item {item_id} status is not In Stock"

    new_additional_cost = additional_cost + parameter_additional_cost
    total_cost = item_cost + new_additional_cost
    finalization = parameter_sold_price - total_cost
    
    db.loc[(db[literal_db_item_id]==item_id), literal_db_additional_cost] = new_additional_cost
    db.loc[(db[literal_db_item_id]==item_id), literal_db_sold_price] = parameter_sold_price
    db.loc[(db[literal_db_item_id]==item_id), literal_db_status] = "Sold"
    db.loc[(db[literal_db_item_id]==item_id), literal_db_total_cost] = total_cost
    db.loc[(db[literal_db_item_id]==item_id), literal_db_status_date] = date_today
    db.loc[(db[literal_db_item_id]==item_id), literal_db_finalization] = finalization
    db.to_csv(database_file)

    backup_input_parameters()
    reset_input_parameters()


def backup_input_parameters():
    item_backup_dir = os.path.join(backup_dir, item_id)
    item_backup_file = os.path.join(item_backup_dir, f'{operation_name}_parameters.py')
    shutil.move(input_parameters_file, item_backup_file)


def reset_input_parameters():
    shutil.copy(template_input_parameters_file, input_parameters_file)


if __name__ == "__main__":
    with open(input_parameters_file) as file:
        exec(file.read())

    additional_cost = 0.0 if (additional_cost == '') else float(additional_cost)
    sold_price = float(sold_price)

    execute_operation()
    os.system('python view.py ' + item_id)
