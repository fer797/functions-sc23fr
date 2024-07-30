from db_adapter import PostgresDB
from medication_transformation import MedicationTransformation
from medication_service import MedicationService

# Example data
data_entries = [
    {
        "id": 479,
        "name": "Aspirin",
        "substitute0": "Paracetamol",
        "substitute1": "Ibuprofen",
        "substitute2": "Acetaminophen",
        "substitute3": "Naproxen",
        "substitute4": "Diclofenac",
        "sideEffect0": "Nausea",
        "sideEffect1": "Vomiting",
        "sideEffect2": "Stomach Pain",
        "sideEffect3": "Heartburn",
        "sideEffect4": "Constipation",
        "sideEffect5": "Drowsiness",
        "sideEffect6": "Dizziness",
        "sideEffect7": "Rash",
        "sideEffect8": "Itching",
        "sideEffect9": "Swelling",
        "sideEffect10": "Shortness of Breath",
        "sideEffect11": "Liver Damage",
        "sideEffect12": "Kidney Damage",
        "sideEffect13": "Ulcers",
        "use0": "Pain Relief",
        "use1": "Fever Reduction",
        "use2": "Inflammation Reduction",
        "use3": "Blood Thinning",
        "use4": "Heart Attack Prevention",
        "Chemical_Class": "Salicylates",
        "Habit_Forming": "No",
        "Therapeutic_Class": "Analgesic",
        "Action_Class": "NSAID"
    }
]

# Initialize database connection
db = PostgresDB(dbname='postgres', user='sc23fjrl', password='Recordar$1', host='sc23fjrl.postgres.database.azure.com', port='5432')
db.connect()

# Initialize services
medication_service = MedicationService(db)

# Process and insert data
for data in data_entries:
    medication = MedicationTransformation.validate_and_create_medication(data)
    if medication:
        medication_service.insert_medication(medication)

# Close the database connection
db.close()
