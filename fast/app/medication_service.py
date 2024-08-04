from db_adapter import PostgresDB
import logging

class MedicationService:
    def __init__(self):
        self.db = None
    
    def initialize_db(self, dbname, user, password, host, port):
        self.db = PostgresDB(dbname=dbname, user=user, password=password, host=host, port=port)
        self.db.connect()
        logging.info("Database connection initialized")

    def close_db(self):
        if self.db:
            self.db.close()
            logging.info("Database connection closed")

    def insert_medication(self, medication):
        try:
            query = """
            INSERT INTO Medication_FHIR (
                medication_id, name, chemical_class, habit_forming, therapeutic_class, action_class, side_effects, uses, substitutes, lot_number, expiration_date
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            # Ensure the extensions list is properly handled
            extensions = {ext.url: ext.valueString for ext in medication.extension}
            
            data = (
                medication.id,
                medication.code.text,
                extensions.get("http://example.com/StructureDefinition/chemicalClass", None),
                extensions.get("http://example.com/StructureDefinition/habitForming", None),
                extensions.get("http://example.com/StructureDefinition/therapeuticClass", None),
                extensions.get("http://example.com/StructureDefinition/actionClass", None),
                extensions.get("http://example.com/StructureDefinition/sideEffects", None),
                extensions.get("http://example.com/StructureDefinition/uses", None),
                extensions.get("http://example.com/StructureDefinition/substitutes", None),
                medication.batch.lotNumber,
                medication.batch.expirationDate
            )
            
            self.db.execute_query(query, [data])
            logging.info(f"Inserted medication with ID {medication.id}")
        except Exception as e:
            logging.error(f"Error inserting medication: {e}")