from datetime import date
from fhir.resources.medication import Medication, MedicationBatch
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.extension import Extension
from pydantic import ValidationError

class MedicationTransformation:
    @staticmethod
    def validate_and_create_medication(data):
        try:
            medication = Medication(
                id=str(data.get("id")),
                code=CodeableConcept(
                    coding=[Coding(system="http://hl7.org/fhir/sid/ndc", code="12345-6789", display=data.get("name"))],
                    text=data.get("name")
                ),
                batch=MedicationBatch(
                    lotNumber="12345",  # Placeholder lot number
                    expirationDate=date(2025, 12, 31)  # Placeholder expiration date
                )
            )

            extensions = []

            chemical_class = data.get("Chemical_Class")
            if chemical_class:
                extensions.append(Extension(url="http://example.com/StructureDefinition/chemicalClass", valueString=chemical_class))

            habit_forming = data.get("Habit_Forming")
            if habit_forming:
                extensions.append(Extension(url="http://example.com/StructureDefinition/habitForming", valueString=habit_forming))

            therapeutic_class = data.get("Therapeutic_Class")
            if therapeutic_class:
                extensions.append(Extension(url="http://example.com/StructureDefinition/therapeuticClass", valueString=therapeutic_class))

            action_class = data.get("Action_Class")
            if action_class:
                extensions.append(Extension(url="http://example.com/StructureDefinition/actionClass", valueString=action_class))

            side_effects = [data.get(f"sideEffect{i}") for i in range(14) if data.get(f"sideEffect{i}")]
            if side_effects:
                extensions.append(Extension(url="http://example.com/StructureDefinition/sideEffects", valueString=", ".join(side_effects)))

            uses = [data.get(f"use{i}") for i in range(5) if data.get(f"use{i}")]
            if uses:
                extensions.append(Extension(url="http://example.com/StructureDefinition/uses", valueString=", ".join(uses)))

            substitutes = [data.get(f"substitute{i}") for i in range(5) if data.get(f"substitute{i}")]
            if substitutes:
                extensions.append(Extension(url="http://example.com/StructureDefinition/substitutes", valueString=", ".join(substitutes)))

            medication.extension = extensions

            return medication

        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
