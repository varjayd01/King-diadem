import locale
from deep_translator import GoogleTranslator
from ENGINE.decision_engine import generate_choices


def translate(text, target):
    try:
        return GoogleTranslator(source="auto", target=target).translate(text)
    except:
        return text


def ask(question, lang):
    q = translate(question, lang)
    return input(q + " ")


# detect system language
sys_lang = locale.getdefaultlocale()[0] or "en"

if sys_lang.startswith("th"):
    user_lang = "th"
else:
    user_lang = "en"

print(translate("KING DIADEM Decision System", user_lang))

location = ask("Where are you located?", user_lang)
food = ask("Food available:", user_lang)
money = ask("Money available:", user_lang)
risk = ask("Current risk:", user_lang)

choices = generate_choices(location, food, money, risk)

print("\n" + translate("Recommended actions:", user_lang))

for i, c in enumerate(choices):
    print(f"{i+1}. {c}")
