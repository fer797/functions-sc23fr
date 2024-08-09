import logging
import azure.functions as func
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient
import psycopg2

# Azure Blob Storage configuration
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=functionssc23fjrl24;AccountKey=pkxxP0yGFTe0RIpc83jFkjmMBPifvC7CHxSpaH+8SdWaUBlAiz/AsNxkO0xcmD0Q8mdYU81PXh1Y+ASt4eSwuQ==;EndpointSuffix=core.windows.net'
AZURE_CONTAINER_NAME = 'datasets'
AZURE_BLOB_NAME = 'dataset.csv'

# PostgreSQL configuration
POSTGRES_HOST = 'sc23fjrl.postgres.database.azure.com'
POSTGRES_DB = 'postgres'
POSTGRES_USER = 'sc23fjrl'
POSTGRES_PASSWORD = 'Recordar$1'
POSTGRES_TABLE = 'Medications'

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="fun")
def fun(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Read CSV file from Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=AZURE_BLOB_NAME)
        blob_data = blob_client.download_blob().readall()
        csv_data = blob_data.decode('utf-8')
        
        # Load CSV data into a pandas DataFrame
        df = pd.read_csv(StringIO(csv_data))

        # Data Cleaning

        # 1. Standardizing text data: Convert all text to lowercase and strip whitespace
        df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)

        # 2. Handling missing data
        critical_columns = ['name', 'Chemical Class', 'Therapeutic Class', 'Action Class']
        df.dropna(subset=critical_columns, inplace=True)

        df.fillna({
            'substitute0': 'na', 'substitute1': 'na', 'substitute2': 'na',
            'substitute3': 'na', 'substitute4': 'na',
            'sideEffect0': 'na', 'sideEffect1': 'na', 'sideEffect2': 'na', 'sideEffect3': 'na',
            'sideEffect4': 'na', 'sideEffect5': 'na', 'sideEffect6': 'na', 'sideEffect7': 'na',
            'sideEffect8': 'na', 'sideEffect9': 'na', 'sideEffect10': 'na', 'sideEffect11': 'na',
            'sideEffect12': 'na', 'sideEffect13': 'na',
            'use0': 'na', 'use1': 'na', 'use2': 'na', 'use3': 'na', 'use4': 'na',
            'Chemical Class': 'unknown', 'Habit Forming': 'unknown', 
            'Therapeutic Class': 'unknown', 'Action Class': 'unknown'
        }, inplace=True)

        df.drop_duplicates(inplace=True)

        df['Habit Forming'] = df['Habit Forming'].apply(lambda x: 'yes' if x in ['yes', 'y'] else ('no' if x in ['no', 'n'] else 'unknown'))

        valid_habit_forming_values = ['yes', 'no', 'unknown']
        df = df[df['Habit Forming'].isin(valid_habit_forming_values)]

        df['Action Class'] = df['Action Class'].apply(lambda x: x if len(str(x)) <= 50 else 'other')

        first_5_records = df.head(5).to_dict(orient='records')

        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO Medications (
            name, substitute0, substitute1, substitute2, substitute3, substitute4,
            sideEffect0, sideEffect1, sideEffect2, sideEffect3, sideEffect4, sideEffect5,
            sideEffect6, sideEffect7, sideEffect8, sideEffect9, sideEffect10, sideEffect11,
            sideEffect12, sideEffect13, use0, use1, use2, use3, use4, Chemical_Class,
            Habit_Forming, Therapeutic_Class, Action_Class
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row['name'], row['substitute0'], row['substitute1'], row['substitute2'], row['substitute3'], row['substitute4'],
                row['sideEffect0'], row['sideEffect1'], row['sideEffect2'], row['sideEffect3'], row['sideEffect4'], row['sideEffect5'],
                row['sideEffect6'], row['sideEffect7'], row['sideEffect8'], row['sideEffect9'], row['sideEffect10'], row['sideEffect11'],
                row['sideEffect12'], row['sideEffect13'], row['use0'], row['use1'], row['use2'], row['use3'], row['use4'],
                row['Chemical Class'], row['Habit Forming'], row['Therapeutic Class'], row['Action Class']
            ))

        conn.commit()

        cursor.close()
        conn.close()

        response_body = {
            "message": "Data loaded successfully",
            "first_5_records": first_5_records
        }
        status_code = 200
    except Exception as e:
        response_body = {"error": str(e)}
        status_code = 500

    return func.HttpResponse(
        body=str(response_body),
        status_code=status_code,
        mimetype="application/json"
    )
