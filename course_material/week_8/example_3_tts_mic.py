
import speech_recognition as sr

#initalize speech recognition
r = sr.Recognizer()
#Initalize microphone
mic = sr.Microphone()
#List all the microphone hardware
for i, item in enumerate(sr.Microphone.list_microphone_names()):
    print( i, item)

#TODO need to change the device_index to select the microphone you want to use
mic = sr.Microphone(device_index=11)
#Listen to microphone input
with mic as source:
    audio = r.listen(source)
try:
    #recognitze with goole api
    print("Input " + r.recognize_google(audio))
except LookupError:
    #return error 
    print("Could not understand audio")
