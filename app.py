import gradio as gr 
import os
import json
import re
from openai import OpenAI 
from dotenv import load_dotenv 
load_dotenv()
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
QWEN_MODEL_ID = "Qwen/Qwen3-14B"

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=NEBIUS_API_KEY
) if NEBIUS_API_KEY else None


PROMPT_TEMPLATE = """
You are a smart AI healthcare consultant. A patient has provided the following information:

Gender: {gender}
Age: {age}
Pre-existing Conditions: {pre_existing}
Symptoms: "{symptoms}"

Based on clinical protocols and triage logic, respond in VALID JSON with only these fields:
1. urgency_level: One of [Low, Moderate, High, Emergency]
2. possible_condition: A short, likely diagnosis
3. recommended_action: What steps should the patient take next?
4. suggested_medication: Any general advice or OTC meds (if applicable)

Respond only in raw JSON. Do not include text explanations or markdown formatting.
"""

def build_prompt(gender: str, age: str, pre_existing: str, symptoms: str) -> str:
    return PROMPT_TEMPLATE.format(
        gender=gender, age=age, pre_existing=pre_existing.strip(), symptoms=symptoms.strip()
    )

def extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text.strip()

def triage_response(gender: str, age: str, pre_existing: str, symptoms: str) -> dict:
    if not client:
        return {"error": "NEBIUS_API_KEY environment variable not set."}
    
    if not symptoms.strip():
        return {"error": "Please provide a symptom description."}

    prompt = build_prompt(gender, age, pre_existing, symptoms)

    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a helpful healthcare assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600
        )
        raw_output = response.choices[0].message.content
        cleaned_output = extract_json(raw_output)

        try:
            result = json.loads(cleaned_output)
            required_fields = ["urgency_level", "possible_condition", "recommended_action", "suggested_medication"]
            if all(field in result for field in required_fields):
                return result
            else:
                return {
                    "error": "Missing fields in response",
                    "raw_output": raw_output,
                    "parsed_result": result
                }
        except json.JSONDecodeError as e:
            return {
                "error": "Invalid JSON format",
                "raw_output": raw_output,
                "exception": str(e)
            }

    except Exception as e:
        return {"error": f"Nebius API Error: {str(e)}"}

def format_triage_output(result: dict) -> str:
    if "error" in result:
        return f"❌ Error: {result['error']}"

    urgency_icons = {
        "Low": "🟢", "Moderate": "🟡", "High": "🟠", "Emergency": "🔴"
    }

    urgency = result.get("urgency_level", "Unknown")
    icon = urgency_icons.get(urgency, "⚪")

    return f"""
{icon} **Urgency Level:** {urgency}
🩺 **Possible Condition:** {result.get("possible_condition", "Not specified")}
📋 **Recommended Action:** {result.get("recommended_action", "Not specified")}
💊 **Suggested Medication:** {result.get("suggested_medication", "Not specified")}

---
*This tool is for educational use only. Always consult a medical professional.*
""".strip()

def gradio_triage_wrapper(gender, age, pre_existing, symptoms):
    result = triage_response(gender, age, pre_existing, symptoms)
    return format_triage_output(result)

# Gradio UI
demo = gr.Interface(
    fn=gradio_triage_wrapper,
    inputs=[
        gr.Dropdown(["Male", "Female", "Other"], label="Gender", value="Male"),
        gr.Textbox(label="Age", placeholder="Enter age (e.g., 45)"),
        gr.Textbox(label="Pre-existing Conditions", placeholder="e.g., BP, diabetes, asthma..."),
        gr.Textbox(lines=4, label="Describe Symptoms", placeholder="e.g., chest pain, dizziness...")
    ],
    outputs=gr.Markdown(label="Smart Diagnosis Report"),
    title="AI Healthcare Chatbot",
    description="""
AI-powered clinical triage assistant that evaluates symptoms, age, gender, and medical history to provide urgent care guidance.

⚠️ Not for emergency use. Always consult licensed professionals.
""",
    theme=gr.themes.Soft(),
    examples=[
        ["Female", "55", "High BP", "Chest tightness and breathlessness"],
        ["Male", "18", "None", "High fever, severe body pain, sore throat"],
    ]
)

if __name__ == "__main__":
    demo.launch()
