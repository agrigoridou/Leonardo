def extract_place(text):
    words = ["πήγαινε", "με", "στο", "στη", "στον", "σε"]

    for w in words:
        text = text.replace(w, "")

    return text.strip()
