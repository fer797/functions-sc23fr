from fastapi import FastAPI, BackgroundTasks
from medication_service import MedicationService
from medication_transformation import MedicationTransformation
from data_ingestion import DataIngestion
import time
import logging
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Initialize the database connection and service
medication_service = MedicationService()
medication_service.initialize_db(
        dbname='postgres',
        user='sc23fjrl',
        password='Recordar$1',
        host='sc23fjrl.postgres.database.azure.com',
        port='5432'
    )
global data_ingestion
data_ingestion = DataIngestion(medication_service.db)

def background_print_task():
    for i in range(5):
        time.sleep(1)
        print(f"Background task running...{i}")

def background_fhir_task():
    logging.info("Starting data ingestion and processing")
    try:
        medications = data_ingestion.fetch_medications()
        logging.info(f"Fetched {len(medications)} medications")
        transformed_data = []
        for data in medications:
            medication = MedicationTransformation.validate_and_create_medication(dict(data))
            if medication:
                medication_service.insert_medication(medication)
                transformed_data.append(medication.dict())
        logging.info("Data ingestion and processing completed")
    except Exception as e:
            logging.error(f"Exception during data ingestion and processing: {e}")


@app.get("/")
def read_root():
    return {"Hello": "World yy877 feer7"}

@app.get("/background")
def run_background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_print_task)
    return {"message": "Background task started"}

@app.get("/background-data")
def run_background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_fhir_task)
    return {"message": "ACK"}

@app.get('/ingest_and_process')
def ingest_and_process_data():
    logging.info("Starting data ingestion and processing")
    try:
        medications = data_ingestion.fetch_medications()
        logging.info(f"Fetched {len(medications)} medications")
        transformed_data = []
        for data in medications:
            medication = MedicationTransformation.validate_and_create_medication(dict(data))
            if medication:
                medication_service.insert_medication(medication)
                transformed_data.append(medication.dict())
        logging.info("Data ingestion and processing completed")
        return {"status": "Data ingested and processed successfully"}
    except Exception as e:
            logging.error(f"Exception during data ingestion and processing: {e}")
            return {"status": "error", "message": str(e)}
