from flask import Flask, request, jsonify
from medication_service import MedicationService
from medication_transformation import MedicationTransformation
from data_ingestion import DataIngestion
import logging
import os

def create_app():
    app = Flask(__name__)

    # Configure logging
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

    @app.teardown_appcontext
    def close_connection(exception):
        medication_service.close_db()

    @app.route('/ingest_and_process', methods=['GET'])
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
            return jsonify({"status": "Data ingested and processed successfully"}), 200
        except Exception as e:
            logging.error(f"Exception during data ingestion and processing: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))