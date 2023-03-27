import pika
import speech_recognition as sr

# create a timer to measeue the timet between two speech recognition events
timer = 0

# initialize speech recognizer
r = sr.Recognizer()

# connect to RabbitMQ message broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create message queue
channel.queue_declare(queue='recognized_text')

# increase the volume of the microphone
r.energy_threshold = 4000

# increase the sensitivity of the microphone
r.dynamic_energy_threshold = True

# set stream chunk size
r.chunk_size = 1024 * 8


# function to recognize speech and publish recognized text to message queue
def recognize_and_publish():
    # listen for speech input
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            # recognize speech using Google Speech Recognition
            recognized_text = r.recognize_google(audio)

            # publish recognized text to message queue
            channel.basic_publish(exchange='',
                                  routing_key='recognized_text',
                                  body=recognized_text)
            print(f"Published recognized text: {recognized_text}")
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    # call this function recursively to keep recognizing speech and publishing recognized text to message queue
    recognize_and_publish()


# start recognizing speech and publishing recognized text to message queue
recognize_and_publish()
