# multi_agent_app.py

import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"   #ensures env var set before protobuf

import sys
sys.path.append(os.path.dirname(__file__)) #ensures that the current folder is importable

import streamlit as st
from agents import PatientAgent, DoctorDentist, DoctorNeurologist
from coding import map_to_icd10, map_to_snomed
from fhir import create_fhir_service_request
from populate_guidelines import populate_guideline_chroma
from clinical_notes_store import initialize_embeddings, retrieve_similar_patients
import json

st.set_page_config(page_title="Multi-Agent Diagnostic Assistant")
st.title("🤖 Multi-Agent AI for Trigeminal Neuralgia Workup")

st.write("Running Python version:", sys.version)

collection = initialize_embeddings()

# Optional: Button to refresh guideline embeddings
if st.sidebar.button("🔄 Refresh Guidelines DB"):
    populate_guideline_chroma()
    st.sidebar.success("Guideline snippets re-embedded.")

# Select patient
st.sidebar.header("👥 Select Patient")

file_path = os.path.join(os.path.dirname(__file__), "patients.json")
st.sidebar.subheader("📁 Upload Patients JSON (optional)")
uploaded_file = st.sidebar.file_uploader("Choose patients.json", type="json")

if uploaded_file:
    patient_options = json.load(uploaded_file)
    st.sidebar.success("✔️ Patients loaded from uploaded file.")
else:
    with open(file_path, "r") as f:
        patient_options = json.load(f)

selected_patient = st.sidebar.selectbox("Patient", list(patient_options.keys()))

# Step 1: Appointment Scheduling
st.header("📅 Step 1: Schedule Appointment")

patient = PatientAgent(name=selected_patient, history=patient_options[selected_patient])
dentist = DoctorDentist()
neurologist = DoctorNeurologist()

appointment_time = patient.schedule_with(dentist, neurologist)
st.success(f"✅ Common appointment time found: {appointment_time}")

# Step 2: Intake History
st.header("📝 Step 2: Patient History and Complaints")
history = patient.get_history()
st.json(history)

# Similar Case Retrieval BEFORE Reasoning
st.header("🔁 Step 2.5: Similar Cases Based on ClinicalBERT")
history_text = "\n".join([f"{k}: {v}" for k, v in history.items()])
similar_cases = retrieve_similar_patients(collection, history_text, top_k=3)

for case in similar_cases:
    st.markdown(f"**Similar Patient ID:** {case['patient_id']}")
    st.markdown(f"**Similarity Score:** {case['score']}")
    st.markdown(f"**Matched Note:**\n{case['matched_note']}")
    st.markdown("---")

# Step 3: Agents Reason and Recommend Investigations
st.header("🧠 Step 3: Reasoning by Doctors")

dentist_result = dentist.evaluate(history)
neurologist_result = neurologist.evaluate(history)

st.subheader("🦷 Dentist Assessment")
st.markdown(dentist_result)

st.subheader("🧠 Neurologist Assessment")
st.markdown(neurologist_result)

# Similar Case Retrieval AFTER Reasoning
st.header("🔁 Step 3.5: Similar Cases (Post-Reasoning Context)")
for case in similar_cases:
    st.markdown(f"**Similar Patient ID:** {case['patient_id']}")
    st.markdown(f"**Similarity Score:** {case['score']}")
    st.markdown(f"**Matched Note:**\n{case['matched_note']}")
    st.markdown("---")

# Step 4: Suggested Investigations and Mappings
st.header("🔬 Step 4: Suggested Investigations")
investigations = patient.suggest_investigations([dentist_result, neurologist_result])

for item in investigations:
    st.markdown(f"- **{item}**")
    fhir_request = create_fhir_service_request(patient_id=selected_patient.replace(" ", "_"), investigation_name=item)
    st.code(fhir_request, language="json")

# Step 5: Diagnosis Coding
st.header("🧾 Step 5: Diagnosis Coding")
icd = map_to_icd10(neurologist_result + dentist_result)
snomed = map_to_snomed(neurologist_result + dentist_result)

st.markdown(f"**ICD-10:** {icd['code']} - {icd['description']}")
st.markdown(f"**SNOMED CT:** {snomed['code']} - {snomed['description']}")