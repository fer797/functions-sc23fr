from flask import Flask, jsonify
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient
import psycopg2

app = Flask(__name__)

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



def main(context):
    """
    The main function is the entry point for the function.
    It takes a context object that includes the request.
    """

    try:
        # Read CSV file from Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=AZURE_BLOB_NAME)
        blob_data = blob_client.download_blob().readall()
        csv_data = blob_data.decode('utf-8')
        
        # Load CSV data into a pandas DataFrame
        df = pd.read_csv(StringIO(csv_data))

        first_5_records = df.head(5).to_dict(orient='records')
        
        # Data cleaning: Replace empty cells with "na"
        df.fillna('na', inplace=True)


        # Establish PostgreSQL connection
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()

        # Insert data into Medications table
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
        
        # Close the connection
        cursor.close()
        conn.close()
        
        body = jsonify({"message": "Data loaded successfully",
                        "first_5_records": first_5_records})
    except Exception as e:
        body = jsonify({"error": str(e)})

    headers = {
        "Content-Type": "application/json"
    }
    return body, 200, headers
