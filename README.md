```python?code_reference&code_event_index=1
# Content for the README.md file in Greek
readme_content = """# Leonardo: Expressive Robot Assistant (Emo UI)

Το Leonardo είναι ένα ψηφιακό ρομπότ-βοηθός με γραφικά εμπνευσμένα από το Emo AI, ελληνική σύνθεση φωνής και δυνατότητα πλοήγησης στους Χάρτες Google.

## 🚀 Ξεκινώντας

Το Leonardo μπορεί να τρέξει σε **Raspberry Pi 4 (Linux)** και σε **Windows**.

---

## 🐧 Ρύθμιση σε Linux (Raspberry Pi 4)

### 1. Προαπαιτούμενα
Ενημερώστε το σύστημά σας και εγκαταστήστε τον handler ήχου:
```bash
sudo apt update
sudo apt install mpg123 fonts-freefont-ttf
```

### 2. Περιβάλλον & Εγκατάσταση
Συνιστάται η χρήση εικονικού περιβάλλοντος (venv):
```bash
# Δημιουργία και ενεργοποίηση περιβάλλοντος
python -m venv myenv
source myenv/bin/activate

# Εγκατάσταση βιβλιοθηκών
pip install gTTS SpeechRecognition
```

### 3. Ρύθμιση Ήχου
Αν χρησιμοποιείτε ηχείο Bluetooth (όπως το JBL Go 4), βεβαιωθείτε ότι είναι συνδεδεμένο και ορισμένο ως η προεπιλεγμένη έξοδος στο PulseAudio.

---

## 🪟 Ρύθμιση σε Windows

### 1. Προαπαιτούμενα
* [Python 3.10+](https://www.python.org/downloads/) (Βεβαιωθείτε ότι έχετε επιλέξει το "Add Python to PATH").
* Ένα λειτουργικό μικρόφωνο (εσωτερικό ή USB).

### 2. Περιβάλλον & Εγκατάσταση
Χρησιμοποιώντας **Git Bash** ή **Command Prompt**:
```bash
# Δημιουργία και ενεργοποίηση περιβάλλοντος
python -m venv myenv
source myenv/Scripts/activate  # Για Git Bash
# Ή
myenv\\Scripts\\activate         # Για CMD

# Εγκατάσταση βιβλιοθηκών
pip install gTTS SpeechRecognition pygame pyaudio
```

*Σημείωση: Αν η εγκατάσταση του `pyaudio` αποτύχει, δοκιμάστε:* `pip install pipwin && pipwin install pyaudio`

---

## 🛠️ Ρυθμίσεις Κώδικα

Πριν την εκτέλεση, ελέγξτε τα εξής:

### **Αριθμός Μικροφώνου (Device Index)**
Στο αρχείο `gui.py`, βρείτε τη γραμμή της αναγνώρισης. Αν το ρομπότ δεν σας ακούει, βρείτε το index του μικροφώνου σας και ενημερώστε το:
```python
with sr.Microphone(device_index=1) as source:
```

### **Χειρισμός Φωνής (Speech)**
* **Linux:** Χρησιμοποιήστε την εντολή `os.system("mpg123 -q -a pulse voice.mp3")` στο `speech.py`.
* **Windows:** Χρησιμοποιήστε την έκδοση με την `pygame.mixer` για να αποφύγετε σφάλματα εντολών.

---

## 🎮 Τρόπος Χρήσης

1. Ενεργοποιήστε το περιβάλλον σας (`source myenv/bin/activate` ή `myenv\\Scripts\\activate`).
2. Τρέξτε το κύριο αρχείο:
```bash
python main.py
```

### **Φωνητικές Εντολές (Ελληνικά)**
* **Χαιρετισμός:** Το ρομπότ θα σας χαιρετήσει αυτόματα κατά την εκκίνηση.
* **Πλοήγηση:** Πείτε **"Πήγαινε στο [Τοποθεσία]"** (π.χ. "Πήγαινε στο Παρίσι").
  * Το ρομπότ θα απαντήσει φωνητικά.
  * Οι Χάρτες Google θα ανοίξουν αυτόματα στον browser σας.

---

## 🎨 Επεξήγηση GUI
* **Πλήκτρο Escape:** Έξοδος από την εφαρμογή.
* **Χρώματα:** * 💎 **Γαλάζιο:** Αναμονή (Idle) / Σκέψη
  * 🌿 **Πράσινο:** Ακρόαση (Listening)
  * 🛑 **Κόκκινο:** Σφάλμα (Error - Ελέγξτε το μικρόφωνο ή το ίντερνετ)
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)


```
Το αρχείο **README.md** είναι έτοιμο για λήψη. Περιέχει όλες τις οδηγίες εγκατάστασης και χρήσης για Windows και Linux στα Ελληνικά.

Το αρχείο Markdown (MD) είναι έτοιμο
[file-tag: code-generated-file-0-1776724994067339922]

### Πώς να το χρησιμοποιήσεις:
1. Κατέβασε το αρχείο από το παραπάνω link.
2. Αντέγραψέ το στον κεντρικό φάκελο του project σου (`Leonardo-main`).
3. Όταν το ανεβάσεις στο GitHub, θα εμφανιστεί αυτόματα ως η αρχική σελίδα του project σου.