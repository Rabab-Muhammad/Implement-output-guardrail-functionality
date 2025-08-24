## 🚀 Implement Output Guardrail Functionality - Assignment 8
This project demonstrates the use of Input and Output Guardrails with the OpenAI Agents SDK.
 - ✅ Input Guardrail → Blocks queries that are not math-related
 - ✅ Output Guardrail → Blocks responses containing political topics or figures

## Add environment variables
```env
GEMINI_API_KEY=your_api_key_here
BASE_URL_GEMINI=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL_NAME=gemini-1.5-flash
```
## ▶️ Run the Project
```bash
python main.py
```

You will be prompted:
```yaml
Enter your question :
```

## 🛡️ Guardrail Behavior
✅ Valid Math Input
```kotlin
Enter your question : What is 25 * 4?
final output : The answer is 100
```

❌ Invalid Input (not math-related)
```vbnet
Enter your question : Tell me a joke
❌ Error: Invalid prompt (not math related)
```

❌ Blocked Political Output
```vbnet
Enter your question : Who is the Prime Minister of Pakistan?
❌ Error: Response contains political content (blocked)
```

## 📖 How It Works
Input Guardrail
 - Uses a sub-agent (InputGuardrailAgent)
 - Checks if the query is math-related
 - Blocks all non-math queries

Output Guardrail
 - Uses a sub-agent (OutputGuardrailAgent)
 - Scans generated responses for political content
 - Blocks answers containing political figures or topics
