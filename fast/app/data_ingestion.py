import logging

class DataIngestion:
    def __init__(self, db):
        self.db = db

    def fetch_medications(self):
        logging.info("Fetching medications from the database")
        query = "SELECT * FROM medications"
        medications = self.db.fetch_all(query)
        logging.info(f"Fetched {len(medications)} medications")
        return medications
