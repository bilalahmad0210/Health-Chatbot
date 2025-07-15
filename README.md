# 🏥 AI Healthcare Chatbot

An intelligent, LLM-powered **clinical triage assistant** built using Nebius API + Qwen3-14B. It analyzes **symptoms, age, gender, and medical history** and returns a structured medical triage assessment in real-time.

---

## 🔧 Project Architecture & Flow

```
User Inputs (via Gradio UI)
      ↓
Prompt Construction with Clinical Triage Template
      ↓
Qwen3-14B via Nebius API (OpenAI-compatible)
      ↓
Structured JSON Output (urgency, condition, next steps)
      ↓
Formatted Markdown Diagnosis Report
```

- `app.py`: Main script containing logic, Nebius API call, prompt formatting, and Gradio interface.
- `.env`: Stores your Nebius API Key.
- `requirements.txt`: All Python dependencies.

---

## 📁 Folder Structure

```
ai-healthcare-chatbot/
├── app.py
├── .env
├── requirements.txt
└── README.md
```

---

## ✨ Key Features

- ✅ Clinical triage using **LLM reasoning**
- ✅ Works with **Nebius Qwen3-14B** (OpenAI-compatible)
- ✅ Outputs structured **JSON** with:
  - Urgency level
  - Possible condition
  - Recommended action
  - Suggested medications
- ✅ Clean, user-friendly **Gradio UI**
- ✅ Handles edge cases and API errors gracefully

---

## ▶️ How to Run Locally

### 1. Clone & Setup Environment

```bash
git clone https://github.com/your-username/ai-healthcare-chatbot.git
cd ai-healthcare-chatbot
python -m venv env
env\Scripts\activate  # or source env/bin/activate on Linux/macOS
pip install -r requirements.txt
```

### 2. Setup Nebius API Key

Create a `.env` file like this:

```
NEBIUS_API_KEY=your_nebius_api_key
```

Get your key from: [https://console.cloud.yandex.com/folders](https://console.cloud.yandex.com/folders)

---

## 💻 Launch the App

```bash
python app.py
```

The Gradio interface will open in your browser:
```
http://127.0.0.1:7860
```

---

## 💡 Prompt Design

| Input Fields        | Used in Prompt       |
|---------------------|----------------------|
| Gender              | Yes                  |
| Age                 | Yes                  |
| Pre-existing Conditions | Yes              |
| Symptom Description | Yes                  |

Prompt is designed to enforce structured JSON output with fields:
- `urgency_level`: [Low, Moderate, High, Emergency]
- `possible_condition`
- `recommended_action`
- `suggested_medication`

---

## 🧪 Sample Output

```json
{
  "urgency_level": "High",
  "possible_condition": "Angina or mild cardiac event",
  "recommended_action": "Seek emergency care immediately",
  "suggested_medication": "Aspirin (if not allergic), avoid exertion"
}
```

Formatted as:

> 🔴 **Urgency Level:** High  
> 🩺 **Possible Condition:** Angina or mild cardiac event  
> 📋 **Recommended Action:** Seek emergency care immediately  
> 💊 **Suggested Medication:** Aspirin (if not allergic), avoid exertion

---

## ⚠️ Limitations & Considerations

- **🚫 Not a diagnostic tool**: Meant for educational/demonstration purposes only.
- **API Usage**: Requires a valid Nebius API key. Qwen3-14B may incur usage charges beyond free tier.
- **Structured JSON parsing**: LLM hallucination may cause missing fields or malformed output.
- **No Offline Inference**: Running this model locally requires significant compute (≥ 24 GB GPU) and is not supported in this repo.

---

## 🌐 Future Ideas

- Add **language support** (e.g., Hindi)
- Export triage results as **PDF**
- Integrate with **calendar APIs** to auto-schedule doctor visits
- Add **chat-based symptom follow-up**

---

## 👨‍⚕️ Author

Developed by **Bilal Ahmad**  
📬 [LinkedIn](https://linkedin.com/in/bilalahmad0210)  
🐙 GitHub: [@bilalahmad0210](https://github.com/bilalahmad0210)

---