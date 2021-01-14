import pandas as pd
import os
import datetime
from shared_settings import *


db = pd.read_csv(database_file, index_col='Table Index')


def change_fields(item_id, new_fields: dict, db):
    '''
    Input: new_fields should be a dictionary with fields you want to change
                {
                    literal_db_period:'1999',
                    literal_db_pricing: 200,
                    ...
                }
    output: 1 - error, 0 - success
    '''
    if item_id not in db[literal_db_item_id].unique():
        print(f'{item_id} is not in DB')
        return 1
    for field, value in new_fields.items():
#         db[db[literal_db_item_id] == item_id][field] = value
        db.loc[(db[literal_db_item_id]==item_id), field] = value
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
#     db[db[literal_db_item_id] == item_id][literal_db_status_date] = date_today
    db.loc[(db[literal_db_item_id]==item_id),literal_db_status_date] = date_today
    db.to_csv(database_file)
    print('finished')
    return 0

