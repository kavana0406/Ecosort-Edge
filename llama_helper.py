import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


def generate_ewaste_guidance(item, working, damage, battery, assessment):
    prompt = f"""
You are EcoSort Edge, an electronic waste recycling assistant.

Provide simple, safe and practical guidance.

Item: {item}
Working condition: {working}
Visible damage: {damage}
Battery condition: {battery}
Assessment result: {assessment}

Instructions:
1. Explain whether the item may be reused, repaired or recycled.
2. Give safe handling instructions.
3. Never suggest opening, puncturing, burning or dismantling batteries.
4. If a battery is swollen, leaking or uncertain, give safety guidance first.
5. Recommend authorised e-waste recycling for unusable electronics.
6. Do not invent recycling centre addresses.
7. Use simple English.

Keep the answer concise and organised under:
- Recommendation
- Safety precautions
- Next steps
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json().get(
            "response",
            "No guidance was generated."
        )

    except requests.RequestException as error:
        return (
            "Llama is currently unavailable. "
            "Please use the Python safety assessment. "
            f"Connection details: {error}"
        )