# fhir.py
import uuid
import datetime

def create_fhir_service_request(patient_id, investigation_name):
    return {
        "resourceType": "ServiceRequest",
        "id": str(uuid.uuid4()),
        "status": "draft",
        "intent": "order",
        "subject": {"reference": f"Patient/{patient_id}"},
        "code": {"text": investigation_name},
        "authoredOn": datetime.date.today().isoformat(),
        "requester": {"display": "Smart Order Assistant"},
        "note": [
            {"text": f"Suggested investigation: {investigation_name}"}
        ]
    }
