# ================================
# KING DIADEM ENGINE (FULL MINIMAL RUNTIME)
# ================================

import os
import requests
from typing import Dict, Any

# ================================
# CONFIG
# ================================

GEMINI_API_KEY = (
    os.getenv("GEMINI_API_KEY") or
    os.getenv("GEMINI_API_KEY2")
)

# (optional search API เช่น SerpAPI หรือ Bing)
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")


# ================================
# SEARCH ENGINE (fallback external data)
# ================================

def search_web(query: str) -> str:
    if not SEARCH_API_KEY:
        return "No external search available."

    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SEARCH_API_KEY,
        "num": 3
    }

    try:
        res = requests.get(url, params=params).json()
        results = []
        for r in res.get("organic_results", [])[:3]:
            results.append(f"{r.get('title')} - {r.get('snippet')}")
        return "\n".join(results) if results else "No results."
    except:
        return "Search failed."


# ================================
# LLM (Gemini API)
# ================================

def call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "LLM not configured."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        res = requests.post(url, json=body).json()
        return res["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"LLM error: {e}"


# ================================
# KING DIADEM KERNEL (Truth Filter)
# ================================

def truth_filter(answer: str) -> str:
    # Core rules:
    # 1. must preserve choice
    # 2. must not create irreversible damage
    # 3. must be actionable

    if not answer:
        return "No valid output."

    # very simple enforcement (can expand later)
    banned = ["kill", "violence", "no choice"]

    for b in banned:
        if b in answer.lower():
            return "Filtered: violates system rules."

    return answer.strip()


# ================================
# DECISION ENGINE
# ================================

def decision_engine(input_data: Dict[str, Any]) -> Dict[str, Any]:
    location = input_data.get("location", "")
    food = input_data.get("food", "")
    money = input_data.get("money", "")
    risk = input_data.get("risk", "")

    query = f"""
    Situation:
    Location: {location}
    Food: {food}
    Money: {money}
    Risk: {risk}

    Task:
    Give 3-4 survival options.
    Must:
    - preserve future choices
    - avoid irreversible damage
    - be realistic

    Keep answer short and actionable.
    """

    # Step 1: LLM reasoning
    llm_output = call_gemini(query)

    # Step 2: If uncertain → search
    if "not sure" in llm_output.lower() or len(llm_output) < 20:
        external = search_web(query)
        llm_output += f"\n\nExternal Data:\n{external}"

    # Step 3: Truth filter (Kernel)
    final = truth_filter(llm_output)

    return {
        "input": input_data,
        "raw": llm_output,
        "final": final
    }


# ================================
# LOOP (REAL-TIME SYSTEM)
# ================================

def run_loop():
    print("KING DIADEM ENGINE STARTED")

    while True:
        try:
            location = input("location: ")
            food = input("food: ")
            money = input("money: ")
            risk = input("risk: ")

            data = {
                "location": location,
                "food": food,
                "money": money,
                "risk": risk
            }

            result = decision_engine(data)

            print("\n=== RESULT ===")
            print(result["final"])
            print("================\n")

        except KeyboardInterrupt:
            print("\nStopped.")
            break


# ================================
# ENTRY
# ================================

if __name__ == "__main__":
    run_loop()
