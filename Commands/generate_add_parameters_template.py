import os

new_item_file = '../Input/add/parameters.py'  

def write_a_empty_new_item_py(new_item_file):
    with open(new_item_file,'w') as file:
        for variable in [
            'catalogue_number',
            'item_name',
            'artist',
            'series',
            'model_start_year',
            'model_end_year',
            'period',
            'age_class',
            'height',
            'length',
            'width',
            'market_average',
            'rareness',
            'condition',
            'short_highlight',
            'collection_class',
            'item_cost',
            'additional_cost',
            'pricing'
        ]:
            file.write(f"{variable}=''\n")

if __name__ == '__main__':
    write_a_empty_new_item_py(new_item_file)
