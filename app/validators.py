# validators.py

def validate_reasoning(reasoning_text, history):
    warnings = []
    if "trigeminal neuralgia" in reasoning_text.lower():
        if "bilateral" in history.get("location", "").lower():
            warnings.append("⚠️ Trigeminal neuralgia is typically unilateral.")
        if "numbness" in history.get("other_symptoms", "").lower():
            warnings.append("⚠️ Numbness is atypical for trigeminal neuralgia and may suggest another etiology.")
    return warnings


# Example enforcement of structured prompt expectations
from langchain.prompts import PromptTemplate

def get_clinical_prompt(role):
    return PromptTemplate(
        input_variables=["history"],
        template="""
You are a {role} evaluating a patient for trigeminal neuralgia.
Patient history:
{history}

Format your response as:
- Condition suspected: <diagnosis>
- Reasoning: <justification>
- Recommend: <investigate / refer / treat>
"""
    )