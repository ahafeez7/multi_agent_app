# agents.py
from reasoning import reason_about_patient
from validators import validate_reasoning

class PatientAgent:
    def __init__(self, name, history):
        self.name = name
        self.history = history

    def schedule_with(self, *doctors):
        return "Tuesday 2 PM"

    def get_history(self):
        return self.history

    def suggest_investigations(self, assessments):
        investigations = []
        for assessment in assessments:
            if "refer to neurologist" in assessment.lower():
                investigations.append("MRI Brain with trigeminal protocol")
            if "neuropathic" in assessment.lower():
                investigations.append("Detailed neurological exam")
            if "dental workup" in assessment.lower():
                investigations.append("Dental panoramic X-ray")
        return list(set(investigations))

class DoctorDentist:
    def evaluate(self, history):
        reasoning = reason_about_patient("dentist", history)
        warnings = validate_reasoning(reasoning, history)
        if warnings:
            reasoning += "\n\n" + "\n".join(warnings)
        return reasoning

class DoctorNeurologist:
    def evaluate(self, history):
        reasoning = reason_about_patient("neurologist", history)
        warnings = validate_reasoning(reasoning, history)
        if warnings:
            reasoning += "\n\n" + "\n".join(warnings)
        return reasoning
