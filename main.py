import requests
import json
import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the speech rate (optional)
engine.setProperty('volume', 1.20)  # Adjust the volume (optional)

voices = engine.getProperty('voices')  # Select the first available voice (you can change this if you have multiple voices)
engine.setProperty('voice', voices[1].id)

if __name__ == "__main__":
    print("Welcome to the Weather App!")
    
place = input("Enter a place: ")
url =f"http://api.weatherapi.com/v1/current.json?key=60e6aec7046343f291a61832260906&q={place}&aqi=no"


response = requests.get(url)
wd=json.loads(response.text)
print(wd)

temp = wd['current']['temp_c']
print(temp)
engine.say(f" {place} is currently {temp} degrees Celsius.\n  ")
engine.runAndWait()
engine.stop()
