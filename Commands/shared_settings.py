import os
import pandas
import sys
import math
import shutil

path_to_home = ".."
imagebase_dir = os.path.join(path_to_home, "Data", "Images")
backup_dir = os.path.join(path_to_home, "Data", "Backup")
database_file = os.path.join(path_to_home, "Data", "database.csv")

literal_input_item_id = "item_id"
literal_input_catalogue_number = "catalogue_number"
literal_input_item_name = "item_name"
literal_input_period = "period"
literal_input_age_class = "age_class"
literal_input_condition = "condition"
literal_input_collection_class = "collection_class"
literal_input_item_cost = "item_cost"
literal_input_pricing = "pricing"

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
