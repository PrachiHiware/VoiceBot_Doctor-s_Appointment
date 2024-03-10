import speech_recognition as sr
import pyttsx3

class Doctor:
    def __init__(self):
        self.available_slots = []

    def add_available_slot(self, slot):
        self.available_slots.append(slot)

    def remove_available_slot(self, slot):
        if slot in self.available_slots:
            self.available_slots.remove(slot)

class VoiceBot:
    def __init__(self, doctor):
        self.doctor = doctor
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.speak("Listening...")
            audio = self.recognizer.listen(source)
        
        try:
            user_input = self.recognizer.recognize_google(audio)
            print("User:", user_input)
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

    def greet(self):
        self.speak("Hello, thanks for calling Dr. Archer’s office. How may I assist you today?")

    def schedule_appointment(self, user_input):
        available_slots = self.doctor.available_slots
        response = "Sure, just give me a second.\n"
        if available_slots:
            response += "I have the following availability: {}\n".format(", ".join(available_slots))
            response += "When would you like to come in?"
        else:
            response += "I'm sorry, there are no available time slots at the moment."
        self.speak(response)

    def book_appointment(self, user_input):
        self.speak("Okay great! Can I get your phone number and Name?")

    def finalize_appointment(self, user_input):
        self.speak("Awesome. I have you set up for that time. To cancel or reschedule please call us again. See you soon.")

# Example usage
doctor = Doctor()
doctor.add_available_slot("10 am")
doctor.add_available_slot("2 pm")
doctor.add_available_slot("4 pm")

voice_bot = VoiceBot(doctor)
voice_bot.greet()

user_input = voice_bot.listen()
if "book" in user_input or "appointment" in user_input:
    voice_bot.schedule_appointment(user_input)

user_input = voice_bot.listen()
voice_bot.book_appointment(user_input)

user_input = voice_bot.listen()
voice_bot.finalize_appointment(user_input)
