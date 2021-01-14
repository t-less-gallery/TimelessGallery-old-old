shared_code_file = "./shared_code.py"
with open(shared_code_file) as file:
    exec(file.read())
operation_name = "view"

empty_line = "\n"
line_separator = "-"*35
max_padding = 19

profile_content = [
    literal_db_item_id,
    literal_db_status,
    literal_db_catalogue_number,
    literal_db_item_name,
    literal_db_period,
    literal_db_condition,
    literal_db_pricing,
    literal_db_sold_price,
    literal_db_finalization,
    empty_line,
    literal_db_rareness,
    literal_db_short_highlight,
    literal_db_collection_class,
    empty_line,
    literal_db_manufacturer,
    literal_db_artist,
    literal_db_series,
    literal_db_model_start_year,
    literal_db_model_end_year,
    literal_db_age_class,
    literal_db_height,
    literal_db_length,
    literal_db_width,
    literal_db_market_average,
    literal_db_creation_date,
    literal_db_status_date,
    empty_line,
    literal_db_provenance,
    literal_db_acquisition_date,
    literal_db_item_cost,
    literal_db_additional_cost,
    literal_db_total_cost
]


def execute_operation():
    item_id = sys.argv[1]
    db_entry = read_db_entry_by_item_id(item_id)
    print_profile(db_entry)


def print_profile(db_entry):
    print(line_separator)
    for key in profile_content:
        if key == empty_line:
            print(empty_line)
        else:
            value = list(db_entry[key].values())[0]
            padding = max_padding - len(key)
            print(f"{key}" + " "*padding + f"{value}")
            print(line_separator)


if __name__ == "__main__":
    assert len(sys.argv) == 2, f"incorrect number of arguments: need 1, actual {len(sys.argv) - 1}"
    execute_operation()
