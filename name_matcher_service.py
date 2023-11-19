from fastapi import FastAPI, HTTPException, UploadFile, File
import pandas as pd
from name_matching.name_matcher import NameMatcher
def match_with_etalon(file: UploadFile):
    # Read the CSV file into a DataFrame
    train = pd.read_csv(file.file)
    matcher = NameMatcher(number_of_matches=1,
                          legal_suffixes=True,
                          common_words=True,
                          top_n=50,
                          verbose=True)

    # adjust the distance metrics to use
    matcher.set_distance_metrics(['bag', 'typo', 'refined_soundex'])
    etalon_column_name = 'Эталонная номенклатура'

    # load the data to which the names should be matched
    matcher.load_and_process_master_data(column=etalon_column_name,
                                         df_matching_data=train,
                                         transform=True)

    # perform the name matching on the data you want matched
    matches = matcher.match_names(to_be_matched=train,
                                  column_matching='Описание')

    # Convert DataFrame to JSON
    # data_json = data.to_json(orient='records')

    combined = pd.merge(train, matches, how='left', left_index=True,
                        right_on='match_index')
    selected_columns = ['Описание', 'Эталонная номенклатура', 'score']
    combined = combined[selected_columns]

    data_json = combined.to_json(orient='records')


    return {"message": "Data matched with etalons", "data": data_json}
def get_matching_table():
    # Placeholder logic to retrieve the matching table
    # Replace with actual retrieval logic
    return {"message": "Matching table retrieved", "table": []}  # Empty table as placeholder

def update_matching_table(updates):
    # Placeholder logic for updating the matching table
    # Replace with actual update logic
    return {"message": "Matching table updated", "updates": updates}

def add_new_etalon(etalon):
    # Placeholder logic for adding a new etalon nomenclature
    # Replace with actual adding logic
    return {"message": "New etalon added", "etalon": etalon}

def add_new_match(match_data):
    # Placeholder logic for adding new matches to etalons
    # Replace with actual matching logic
    return {"message": "New match added to etalon", "match_data": match_data}
