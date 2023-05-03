import os
import time
from langchain.llms import OpenAI
from gtts import gTTS
from io import BytesIO
from playsound import playsound


llm = OpenAI(model_name="text-ada-001", n=2, best_of=2)
answer = llm("Tell me a joke")

# remove empty lines
answer = "\n".join([line for line in answer.split("\n") if line.strip() != ""])

print(
    answer
)

tts = gTTS(answer, lang="en")
# save to file
tts.save("chat/speech.mp3")

# play the file
playsound("chat/speech.mp3")