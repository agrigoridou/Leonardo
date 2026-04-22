import random
import unicodedata

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

responses = {
    "greeting": {
        "keywords": ["γεια", "καλημερα", "καλησπερα", "hello"],
        "answers": [
            "Γεια σου! Χαίρομαι που σε βλέπω!",
            "Καλησπέρα! Πώς μπορώ να βοηθήσω;",
            "Γεια! Τι κάνουμε σήμερα;"
        ],
        "emotion": "happy"
    },

    "how_are_you": {
        "keywords": ["τι κανεις", "πως εισαι", "ολα καλα"],
        "answers": [
            "Είμαι πολύ καλά! Εσύ;",
            "Όλα τέλεια! Πώς είσαι εσύ;",
            "Δουλεύω κανονικά!"
        ],
        "emotion": "happy"
    },

    "name": {
        "keywords": ["πως σε λενε", "ονομα σου"],
        "answers": [
            "Είμαι το ρομπότ σου!",
            "Δεν έχω όνομα ακόμα, θέλεις να μου δώσεις ένα;",
            "Μπορείς να με φωνάζεις όπως θέλεις!"
        ],
        "emotion": "neutral"
    },

    "thanks": {
        "keywords": ["ευχαριστω", "thanks"],
        "answers": [
            "Παρακαλώ!",
            "Με χαρά!",
            "Οτιδήποτε χρειαστείς!"
        ],
        "emotion": "happy"
    },

    "bye": {
        "keywords": ["αντιο", "bye"],
        "answers": [
            "Αντίο!",
            "Τα λέμε!",
            "Καλή συνέχεια!"
        ],
        "emotion": "neutral"
    },

    "joke": {
        "keywords": ["αστειο"],
        "answers": [
            "Γιατί το ρομπότ πήγε διακοπές; Για να κάνει reboot!",
            "Πόσα ρομπότ χρειάζονται για να αλλάξουν μια λάμπα; Κανένα, είναι αυτοματοποιημένο!"
        ],
        "emotion": "happy"
    },

    "time": {
        "keywords": ["τι ωρα", "ωρα"],
        "answers": [],
        "emotion": "neutral"
    },

    "date": {
        "keywords": ["τι μερα", "ημερομηνια"],
        "answers": [],
        "emotion": "neutral"
    }
}

def basic_response(text):
    text = normalize(text)

    for category in responses.values():
        if any(keyword in text for keyword in category["keywords"]):

            # δυναμικά για ώρα
            if "ωρα" in text:
                from datetime import datetime
                now = datetime.now().strftime("%H:%M")
                return f"Η ώρα είναι {now}", "neutral"

            # δυναμικά για ημερομηνία
            if "ημερομηνια" in text or "μερα" in text:
                from datetime import datetime
                today = datetime.now().strftime("%d/%m/%Y")
                return f"Σήμερα είναι {today}", "neutral"

            answer = random.choice(category["answers"])
            return answer, category["emotion"]

    return None, None
