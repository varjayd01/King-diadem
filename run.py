import locale
from deep_translator import GoogleTranslator
from ENGINE.decision_engine import generate_choices

def translate(text, target):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except:
        return text

def ask(question, target_lang):
    q = translate(question, target_lang)
    return input(q + " ")

# Detect system language
sys_lang = locale.getdefaultlocale()[0] or "en"
user_lang = "th" if sys_lang.startswith("th") else "en"

print(translate("KING DIADEM Decision System", user_lang))

# Ask user preferred language
pref = input(translate("If you want another language, type it (ex: th, en, ja, zh) or press Enter:", user_lang) + " ")

if pref.strip() != "":
    user_lang = pref.strip()

location = ask("Where are you located?", user_lang)
food = ask("What food do you currently have?", user_lang)
money = ask("How much money do you have?", user_lang)
risk = ask("What risk are you facing now?", user_lang)

choices = generate_choices(location, food, money, risk)

print("\n" + translate("Recommended Actions:", user_lang) + "\n")

for i, c in enumerate(choices):
    print(f"{i+1}. {translate(c, user_lang)}")
