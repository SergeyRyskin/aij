import os

import pika
import speech_recognition as sr
import deepl


def get_deepl():
    return deepl.Translator(os.environ.get("DEEPL_AUTH_KEY"))


# create a timer to measure the time between two speech recognition events
timer = 0

# initialize speech recognizer
r = sr.Recognizer()

# connect to RabbitMQ message broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create message queue
channel.queue_declare(queue='recognized_text')

# create another message queue for translated text
channel.queue_declare(queue='translated_text')

# increase the volume of the microphone
r.energy_threshold = 3000

# increase the sensitivity of the microphone
r.dynamic_energy_threshold = True

# set stream chunk size
r.chunk_size = 1024 * 8

# improve recognition accuracy
r.pause_threshold = 0.5

# improve the response time
r.non_speaking_duration = 0.1


# function to recognize speech and publish recognized text to message queue
def recognize_and_publish(source_lang="en-US"):
    # listen for speech input
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            # recognize speech using Google Speech Recognition
            recognized_text = r.recognize_google(audio_data=audio, language=source_lang)

            # publish recognized text to message queue
            channel.basic_publish(exchange='', routing_key='recognized_text', body=recognized_text)
            print(f"Published recognized text: {recognized_text}")

        except sr.UnknownValueError:
            # close the connection to RabbitMQ
            if connection.is_open:
                connection.close()
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            if connection.is_open:
                connection.close()

    # call this function recursively to keep recognizing speech and publishing recognized text to message queue
    recognize_and_publish()


def translate_and_publish(source_lang="EN", target_lang="NL"):
    # listen for speech input
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            # recognize speech using Google Speech Recognition
            recognized_text = r.recognize_google(audio)
            translated_text = get_deepl().translate_text(recognized_text, source_lang=source_lang,
                                                         target_lang=target_lang).text

            # publish recognized text to message queue
            channel.basic_publish(exchange='',
                                  routing_key='translated_text',
                                  body=translated_text.encode('utf-8'))

            print(f"Published translated text: {translated_text}")
        except sr.UnknownValueError:
            # close the connection to RabbitMQ
            if connection.is_open:
                connection.close()
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            if connection.is_open:
                connection.close()

    # call this function recursively to keep recognizing speech and publishing recognized text to message queue
    translate_and_publish()


# start recognizing speech and publishing recognized text to message queue
recognize_and_publish()
translate_and_publish()
