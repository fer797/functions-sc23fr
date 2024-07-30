from fhir.resources.medication import Medication, MedicationBatch
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.extension import Extension
from pydantic import ValidationError
from datetime import date
import json

def validate_and_create_medication(data):
    try:
        # Create a FHIR Medication resource
        medication = Medication(
            id=str(data["id"]),
            code=CodeableConcept(
                coding=[Coding(system="http://hl7.org/fhir/sid/ndc", code="12345-6789", display=data["name"])],
                text=data["name"]
            ),
            batch=MedicationBatch(
                lotNumber="12345",  # Placeholder lot number
                expirationDate=date(2025, 12, 31)  # Placeholder expiration date
            )
        )

        # Add chemical class, habit forming, therapeutic class, and action class as extensions
        extensions = [
            Extension(url="http://example.com/StructureDefinition/chemicalClass", valueString=data["Chemical_Class"]),
            Extension(url="http://example.com/StructureDefinition/habitForming", valueString=data["Habit_Forming"]),
            Extension(url="http://example.com/StructureDefinition/therapeuticClass", valueString=data["Therapeutic_Class"]),
            Extension(url="http://example.com/StructureDefinition/actionClass", valueString=data["Action_Class"]),
        ]

        # Add side effects as an extension
        side_effects = [data[f"sideEffect{i}"] for i in range(14) if f"sideEffect{i}" in data]
        extensions.append(Extension(url="http://example.com/StructureDefinition/sideEffects", valueString=", ".join(side_effects)))

        # Add uses as an extension
        uses = [data[f"use{i}"] for i in range(5) if f"use{i}" in data]
        extensions.append(Extension(url="http://example.com/StructureDefinition/uses", valueString=", ".join(uses)))

        # Add substitutes as extensions
        for i in range(5):
            if f"substitute{i}" in data:
                extensions.append(Extension(url=f"http://example.com/StructureDefinition/substitute{i}", valueString=data[f"substitute{i}"]))

        # Assign extensions to the medication resource
        medication.extension = extensions

        return medication.dict()

    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

def custom_json_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {obj} not serializable")

# Sample data entries
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
    },
    # Add more data entries as needed
]

# Process and validate multiple data entries
fhir_medications = [validate_and_create_medication(data) for data in data_entries]

# Filter out None values and print the valid FHIR resources
valid_fhir_medications = [med for med in fhir_medications if med is not None]
print(json.dumps(valid_fhir_medications, indent=2, default=custom_json_serializer))