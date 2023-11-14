from fastapi import FastAPI
import pandas as pd
from name_matching.name_matcher import NameMatcher

app = FastAPI()

# Load your data here (outside of endpoint functions for efficiency)
etalon = pd.read_excel('data/Эталонная номенклатура.xlsx')
train = pd.read_excel('data/Соответствия.xlsx')
N = 10
train = train.iloc[:N]
etalon = etalon.iloc[:N]


@app.post("/match_names/")
async def match_names():
    etalon_column_name = 'Номенклатура'
    matcher = NameMatcher(number_of_matches=1, legal_suffixes=True,
                          common_words=False, top_n=50, verbose=True)
    matcher.set_distance_metrics(['bag', 'typo', 'refined_soundex'])
    matcher.load_and_process_master_data(column=etalon_column_name,
                                         df_matching_data=etalon,
                                         transform=True)
    matches = matcher.match_names(to_be_matched=train,
                                  column_matching='Описание')

    combined = pd.merge(train, matches, how='left', left_index=True,
                        right_on='match_index')
    selected_columns = ['Описание', 'Эталонная номенклатура', 'score']
    combined = combined[selected_columns]
    sorted_combined = combined.sort_values(by='score', ascending=False).head(
        10)

    return sorted_combined.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
