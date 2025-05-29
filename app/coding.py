# coding.py

def map_to_icd10(reasoning_text):
    if "trigeminal neuralgia" in reasoning_text.lower():
        return {"code": "G50.0", "description": "Trigeminal neuralgia"}
    elif "dental" in reasoning_text.lower():
        return {"code": "K08.8", "description": "Other specified disorders of teeth and supporting structures"}
    return {"code": "R51", "description": "Headache"}

def map_to_snomed(reasoning_text):
    if "trigeminal neuralgia" in reasoning_text.lower():
        return {"code": "428361000124100", "description": "Trigeminal neuralgia (disorder)"}
    elif "dental" in reasoning_text.lower():
        return {"code": "232347008", "description": "Disorder of tooth (disorder)"}
    return {"code": "25064002", "description": "Pain (finding)"}
