import os

import deepl
import speech_recognition as sr

auth_key = os.environ.get("DEEPL_AUTH_KEY")
translator = deepl.Translator(os.environ.get("DEEPL_AUTH_KEY"))

def capture_voice():
    """
    It takes microphone input from the user
    @return: string output from the user's voice
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Started listening ...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing your speech ...")
        query = r.recognize_google(
            audio, language="en-be"
        )
    except Exception as e:
        print("Say that again please ...")
        return "None"

    return query


if __name__ == "__main__":

    speech = capture_voice()

    print(
        "You said: {}".format(speech) + "\n" +
        "Translated: {}".format(translator.translate_text(speech, target_lang="NL"))
    )
