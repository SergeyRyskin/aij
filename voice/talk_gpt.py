
import time
import pika
import os
import openai
import pyttsx3

from gtts import gTTS
from io import BytesIO

import simpleaudio as sa

class AIAssistant:
    """
    AI Assistant class that uses OpenAI's GPT-3 API to generate responses.
    """
    def __init__(self, api_key):
        """
        Initializes the AI Assistant.
        :param api_key: The OpenAI API key.
        """
        self.api_key = api_key
        self.start_sequence = "\nAIJ:"
        self.restart_sequence = "\nHuman: "
        self.model = "text-davinci-003"
        self.temperature = 1
        self.max_tokens = 4000
        self.top_p = 1
        self.frequency_penalty = 0.62
        self.presence_penalty = 0.6
        self.stop = [" Human:", " AI:"]

        openai.api_key = self.api_key

    def generate_response(self, prompt):
        """
        Generates a response using OpenAI's GPT-3 API.
        :param prompt: The prompt to use for the AI to generate a response.
        :return: The generated response.
        """
        return openai.Completion.create(
            model=self.model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stop=self.stop
        )

assistant = AIAssistant(os.environ.get('OPENAI_API_KEY'))

response = assistant.generate_response(
    "Act as a journalist and write a news article about the following topic:\n"
    "The United States has been hit hard by the coronavirus pandemic. "
)


print(
    response.choices[0].text
)

speech = gTTS(text=response.choices[0].text, lang='en', slow=False)
speech.save("speech.mp3")


filename = "speech.mp3"
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing