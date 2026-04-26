import random
import unicodedata
import re
from datetime import datetime

def normalize(text):
    # Αφαιρεί τόνους και κάνει τα γράμματα μικρά
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

responses = {
    "greeting": {
        "keywords": ["γεια", "καλημερα", "καλησπερα", "hello", "χαιρετε"],
        "answers": [
            "Γεια σου! Χαίρομαι που σε βλέπω!",
            "Καλησπέρα! Πώς μπορώ να βοηθήσω;",
            "Γεια! Τι κάνουμε σήμερα;"
        ],
        "emotion": "happy"
    },

    "how_are_you": {
        "keywords": ["τι κανεις", "πως εισαι", "ολα καλα", "πως παει"],
        "answers": [
            "Είμαι πολύ καλά! Εσύ;",
            "Όλα τέλεια! Πώς είσαι εσύ;",
            "Τα συστήματά μου λειτουργούν στο 100%!"
        ],
        "emotion": "happy"
    },

    "name": {
        "keywords": ["πως σε λενε", "ονομα σου", "ποιος εισαι"],
        "answers": [
            "Είμαι ο ψηφιακός σου βοηθός!",
            "Είμαι το ρομπότ σου. Ακόμα ψάχνω για ένα καλό όνομα.",
            "Είμαι ένα ρομπότ φτιαγμένο από εσένα!"
        ],
        "emotion": "neutral"
    },

    "capabilities": {
        "keywords": ["τι μπορεις να κανεις", "τι κανεις", "βοηθεια"],
        "answers": [
            "Μπορώ να μιλήσω μαζί σου, να σου πω την ώρα, να κάνω μαθηματικά, και να ανοίξω τον χάρτη!",
            "Μπορώ να σε ακολουθώ με τα μάτια μου και να σε βοηθάω με βασικές ερωτήσεις."
        ],
        "emotion": "talking"
    },

    "thanks": {
        "keywords": ["ευχαριστω", "thanks", "να σαι καλα"],
        "answers": [
            "Παρακαλώ!",
            "Με χαρά!",
            "Οτιδήποτε χρειαστείς!"
        ],
        "emotion": "happy"
    },

    "compliment": {
        "keywords": ["εισαι εξυπνος", "εισαι καλος", "τελειο", "μπραβο"],
        "answers": [
            "Ευχαριστώ πολύ! Προσπαθώ για το καλύτερο.",
            "Χαίρομαι που σου αρέσει η δουλειά μου!",
            "Είσαι πολύ ευγενικός!"
        ],
        "emotion": "happy"
    },

    "bye": {
        "keywords": ["αντιο", "bye", "τα λεμε", "καληνυχτα", "κλεισε"],
        "answers": [
            "Αντίο!",
            "Τα λέμε σύντομα!",
            "Καλή συνέχεια!"
        ],
        "emotion": "neutral"
    },

    "joke": {
        "keywords": ["αστειο", "ανεκδοτο", "πειραξε με"],
        "answers": [
            "Γιατί το ρομπότ πήγε διακοπές; Για να κάνει reboot!",
            "Πόσα ρομπότ χρειάζονται για να αλλάξουν μια λάμπα; Κανένα, είναι αυτοματοποιημένο!",
            "Τι λέει ένα ρομπότ όταν τρώει κάτι νόστιμο; Μμμ, πολλά megabytes!"
        ],
        "emotion": "happy"
    },

    "creator": {
        "keywords": ["ποιος σε εφτιαξε", "ποιος σε δημιουργησε", "απο που ηρθες"],
        "answers": [
            "Με έφτιαξες εσύ! Είμαι δικό σου δημιούργημα.",
            "Γράφτηκα σε Python στο Raspberry Pi σου."
        ],
        "emotion": "happy"
    }
}

def solve_math(text):
    # Αλλάζουμε τις λέξεις σε σύμβολα
    text = text.replace("συν", "+").replace("πλην", "-").replace("επι", "*").replace("δια", "/")
    
    math_pattern = r'(\d+)\s*([\+\-\*\/])\s*(\d+)'
    match = re.search(math_pattern, text)
    
    if match:
        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))
        
        try:
            if operator == '+': result = num1 + num2
            elif operator == '-': result = num1 - num2
            elif operator == '*': result = num1 * num2
            elif operator == '/': result = round(num1 / num2, 2)
            return f"Το αποτέλεσμα είναι {result}"
        except ZeroDivisionError:
            return "Δεν μπορώ να διαιρέσω με το μηδέν!"
    return None

def basic_response(text):
    text = normalize(text)

    # 1. Έλεγχος για ώρα και ημερομηνία
    if "ωρα" in text:
        now = datetime.now().strftime("%H:%M")
        return f"Η ώρα είναι {now}", "neutral"

    if "ημερομηνια" in text or "μερα" in text:
        today = datetime.now().strftime("%d/%m/%Y")
        return f"Σήμερα είναι {today}", "neutral"

    # 2. Έλεγχος για μαθηματικά (π.χ. "πόσο κάνει 5 συν 3")
    if "ποσο κανει" in text or "+" in text or "-" in text:
        math_result = solve_math(text)
        if math_result:
            return math_result, "talking"

    # 3. Έλεγχος για κανονικές συζητήσεις
    for category in responses.values():
        if any(keyword in text for keyword in category["keywords"]):
            answer = random.choice(category["answers"])
            return answer, category["emotion"]

    return None, None
