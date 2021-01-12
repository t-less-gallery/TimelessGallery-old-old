import os
import pandas
import sys
import math
import shutil

path_to_home = ".."
imagebase_dir = os.path.join(path_to_home, "Data", "Images")
backup_dir = os.path.join(path_to_home, "Data", "Backup")
database_file = os.path.join(path_to_home, "Data", "database.csv")
template_dir = os.path.join(path_to_home, "Template")

literal_item_id = "item_id"
literal_catalogue_number = "catalogue_number"
literal_item_name = "item_name"
literal_period = "period"
literal_age_class = "age_class"
literal_condition = "condition"
literal_collection_class = "collection_class"
literal_item_cost = "item_cost"
literal_pricing = "pricing"
literal_short_highlight = "short_highlight"
literal_artist = "artist"
literal_series = "series"
literal_model_start_year = "model_start_year"
literal_model_end_year = "model_end_year"
literal_height = "height"
literal_length = "length"
literal_width = "width"
literal_provenance = "provenance"
literal_acquisition_date = "acquisition_date"
literal_market_average = "market_average"
literal_additional_cost = "additional_cost"
literal_rareness = "rareness"
literal_status = "status"
literal_sold_price = "sold_price"
literal_finalization = "finalization"
literal_manufacturer = "manufacturer"
literal_creation_date = "creation_date"
literal_status_date = "status_date"
literal_total_cost = "total_cost"

literal_db_index = "Table Index"
literal_db_item_id = "Item ID"
literal_db_status = "Status"
literal_db_catalogue_number = "Catalogue Number"
literal_db_item_name = "Item Name"
literal_db_period = "Period"
literal_db_condition = "Condition"
literal_db_pricing = "Pricing"
literal_db_sold_price = "Sold Price"
literal_db_rareness = "Rareness"
literal_db_short_highlight = "Short Highlight"
literal_db_collection_class = "Collection Class"
literal_db_manufacturer = "Manufacturer"
literal_db_artist = "Artist"
literal_db_series = "Series"
literal_db_model_start_year = "Model Start Year"
literal_db_model_end_year = "Model End Year"
literal_db_age_class = "Age Class"
literal_db_height = "Height"
literal_db_length = "Length"
literal_db_width = "Width"
literal_db_market_average = "Market Average"
literal_db_creation_date = "Creation Date"
literal_db_status_date = "Status Date"
literal_db_provenance = "Provenance"
literal_db_acquisition_date = "Acquisition Date"
literal_db_item_cost = "Item Cost"
literal_db_additional_cost = "Additional Cost"
literal_db_total_cost = "Total Cost"
literal_db_finalization = "Finalization"

def read_db_entry_by_item_id(item_id):
    access_column = literal_db_item_id
    db = pandas.read_csv(database_file, index_col=literal_db_index, keep_default_na=False)
    assert db[access_column].str.contains(item_id).any(), f"entry doesn't exist: {access_column} -> {item_id}"
    return db.loc[db[access_column] == item_id].to_dict()


def load_db_entry_to_global(id):
    db_entry = read_db_entry_by_item_id(id)
    globals()[literal_item_id] = list(db_entry[literal_db_item_id].values())[0]
    globals()[literal_status] = list(db_entry[literal_db_status].values())[0]
    globals()[literal_catalogue_number] = list(db_entry[literal_db_catalogue_number].values())[0]
    globals()[literal_item_name] = list(db_entry[literal_db_item_name].values())[0]
    globals()[literal_period] = list(db_entry[literal_db_period].values())[0]
    globals()[literal_condition] = list(db_entry[literal_db_condition].values())[0]
    globals()[literal_pricing] = list(db_entry[literal_db_pricing].values())[0]
    globals()[literal_sold_price] = list(db_entry[literal_db_sold_price].values())[0]
    globals()[literal_rareness] = list(db_entry[literal_db_rareness].values())[0]
    globals()[literal_short_highlight] = list(db_entry[literal_db_short_highlight].values())[0]
    globals()[literal_collection_class] = list(db_entry[literal_db_collection_class].values())[0]
    globals()[literal_manufacturer] = list(db_entry[literal_db_manufacturer].values())[0]
    globals()[literal_artist] = list(db_entry[literal_db_artist].values())[0]
    globals()[literal_series] = list(db_entry[literal_db_series].values())[0]
    globals()[literal_model_start_year] = list(db_entry[literal_db_model_start_year].values())[0]
    globals()[literal_model_end_year] = list(db_entry[literal_db_model_end_year].values())[0]
    globals()[literal_age_class] = list(db_entry[literal_db_age_class].values())[0]
    globals()[literal_height] = list(db_entry[literal_db_height].values())[0]
    globals()[literal_length] = list(db_entry[literal_db_length].values())[0]
    globals()[literal_width] = list(db_entry[literal_db_width].values())[0]
    globals()[literal_market_average] = list(db_entry[literal_db_market_average].values())[0]
    globals()[literal_creation_date] = list(db_entry[literal_db_creation_date].values())[0]
    globals()[literal_status_date] = list(db_entry[literal_db_status_date].values())[0]
    globals()[literal_provenance] = list(db_entry[literal_db_provenance].values())[0]
    globals()[literal_acquisition_date] = list(db_entry[literal_db_acquisition_date].values())[0]
    globals()[literal_item_cost] = list(db_entry[literal_db_item_cost].values())[0]
    globals()[literal_additional_cost] = list(db_entry[literal_db_additional_cost].values())[0]
    globals()[literal_total_cost] = list(db_entry[literal_db_total_cost].values())[0]
    globals()[literal_finalization] = list(db_entry[literal_db_finalization].values())[0]
