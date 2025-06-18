# reasoning.py
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from validators import get_clinical_prompt
from guideline_retriever import retrieve_guideline_snippet
import openai
from openai.error import APIError
import streamlit as st
import time

load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY must be set in .streamlit/secrets.toml")

openai.api_key = api_key

#retry 3 times with a delay of 2 seconds
def reason_about_patient(role, history, retries=3, delay=2):
    history_text = "\n".join([f"{k}: {v}" for k, v in history.items()])
    guideline_snippet = retrieve_guideline_snippet(history_text)[0]

    prompt_template = get_clinical_prompt(role)
    formatted_prompt = prompt_template.format(history=history_text, role=role)

    full_prompt = f"""
Relevant clinical guideline excerpt:
{guideline_snippet}

{formatted_prompt}
"""

    st.write("🔍 Reasoning input:", full_prompt)  # Debug log

    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a specialist clinician."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.5
            )
            reply = response.choices[0].message.content.strip()
            st.write("✅ LLM output:", reply)  # Debug log
            return reply

        except APIError as e:
            st.warning(f"⚠️ Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            break

    return "Error in LLM reasoning: Failed after multiple attempts."