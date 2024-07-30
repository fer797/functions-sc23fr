from flask import Flask, request, jsonify
from medication_service import MedicationService
from medication_transformation import MedicationTransformation
from data_ingestion import DataIngestion
import os


# Database connection and service initialization
medication_service = MedicationService()
data_ingestion = None

@app.before_first_request
def initialize():
    medication_service.initialize_db(
        dbname='postgres',
        user='sc23fjrl',
        password='Recordar$1',
        host='sc23fjrl.postgres.database.azure.com',
        port='5432'
    )
    global data_ingestion
    data_ingestion = DataIngestion(medication_service.db)

@app.teardown_appcontext
def close_connection(exception):
    medication_service.close_db()

@app.route('/ingest_and_process', methods=['GET'])
def ingest_and_process_data():
    medications = data_ingestion.fetch_medications()
    transformed_data = []
    for data in medications:
        medication = MedicationTransformation.validate_and_create_medication(dict(data))
        if medication:
            medication_service.insert_medication(medication)
            transformed_data.append(medication.dict())
    return jsonify({"status": "Data ingested and processed successfully", "data"}), 200

