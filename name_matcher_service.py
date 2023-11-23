from fastapi import FastAPI, HTTPException, UploadFile, File
import pandas as pd
from name_matching.name_matcher import NameMatcher

matching_table = pd.DataFrame()
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

    matching_table = combined
    #add id column
    matching_table.insert(0, 'id', range(1, 1 + len(matching_table)))

    return {"message": "Data matched with etalons", "data": data_json}
def get_matching_table():
    # Convert the matching table DataFrame to JSON
    table_json = matching_table.to_json(orient='records')
    return {"message": "Matching table retrieved", "table": table_json}

def update_matching_table(file: UploadFile):
    # Read the CSV file containing updates into a DataFrame
    updates_df = pd.read_csv(file.file)
    global matching_table
    matching_table = pd.concat([matching_table, updates_df])
    return {"message": "Matching table updated", "table": matching_table.to_json(orient='records')}



# Assuming 'etalon_df' is a global variable for the etalon DataFrame
etalon_df = pd.DataFrame()

def add_new_etalon(file: UploadFile):
    # Read the CSV file containing the new etalon into a DataFrame
    new_etalon_df = pd.read_csv(file.file)
    global etalon_df
    etalon_df = pd.concat([etalon_df, new_etalon_df], ignore_index=True)
    updated_etalon_json = etalon_df.to_json(orient='records')
    return {"message": "New etalon added", "etalon": updated_etalon_json}

# Assuming 'matches_df' is a global variable for the matches DataFrame
matches_df = pd.DataFrame()

def add_new_match(file: UploadFile):
    # Read the CSV file containing new match data into a DataFrame
    new_match_data = pd.read_csv(file.file)
    global matches_df
    matches_df = pd.concat([matches_df, new_match_data], ignore_index=True)
    updated_matches_json = matches_df.to_json(orient='records')
    return {"message": "New match added to etalon", "match_data": updated_matches_json}


def change_specific_etalon(etalon_id: int, new_values: dict):
    # Assuming 'etalon_df' is a global variable for the etalon DataFrame
    global matching_table
    matching_table.loc[matching_table['id'] == etalon_id, new_values.keys()] = new_values.values()
    return {"message": "Specific etalon updated", "etalon": matching_table.loc[matching_table['id'] == etalon_id].to_json(orient='records')}


def change_specific_match(match_id: int, new_values: dict):
    global matching_table
    matching_table.loc[matching_table['id'] == match_id, new_values.keys()] = new_values.values()
    return {"message": "Specific match updated", "match": matching_table.loc[matching_table['id'] == match_id].to_json(orient='records')}

