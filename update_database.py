#delete mongodb
#
from pymongo import MongoClient
from config import CONNECTION_STRING
import requests
import pandas as pd
from io import BytesIO

GOOGLE_SHEETS_SOURCE = 'https://docs.google.com/spreadsheet/ccc?key=1Eqi7FPpZVEH2Zml3lw1Dp8DSu7Kk7k2RTP5U2CdApSo&output=csv'
if __name__ == "__main__":
    response = requests.get(GOOGLE_SHEETS_SOURCE)
    assert response.status_code == 200, 'Wrong status code '+ str(response.status_code)
    print("Google Sheets Response",response.status_code)
    data = response.content
    df = pd.read_csv(BytesIO(data), index_col=0)
    print(df.head(10))
    client = MongoClient(CONNECTION_STRING)
    client.drop_database('data')
    print('Database deleted')
    db = client['data']
    collection = db['data']
    state = collection.insert_many(df.to_dict('records'))
    print(state)
    if state:
        print('Database created successfully')
    else:
        print('Database not created state ',state)

