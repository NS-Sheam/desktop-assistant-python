

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import requests
import re
import random
from config import weather_api_key, currency_api_key, news_api_key

from deep_seek_api import ask_to_ai


engine = pyttsx3.init()


rate = engine.getProperty('rate')


engine.setProperty('rate', rate - 10) 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    speak("Hello Avengers!")
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you today?")


def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}")
        except Exception as e:
            print("Sorry, I didn't catch that. Could you repeat?")
            return "None"
        return query.lower()

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except Exception as e:
        return "Sorry, I couldn't find any results on Wikipedia."

def fetch_weather(city):
    api_key = weather_api_key  
    base_url = "http://api.weatherapi.com/v1/current.json?"  
    complete_url = f"{base_url}key={api_key}&q={city}&aqi=no" 
    
    try:
        response = requests.get(complete_url)
        data = response.json()
        
        if "error" not in data:
          
            location = data['location']['name']
            region = data['location']['region']
            country = data['location']['country']
            temperature = data['current']['temp_c']
            condition = data['current']['condition']['text']
            feels_like = data['current']['feelslike_c']
            
            weather_info = f"The temperature in {location}, {region}, {country} is {temperature}°C with {condition}. " \
                            f"It feels like {feels_like}°C."
            return weather_info
        else:
            return "Sorry, I couldn't find the weather for that location."
    except Exception as e:
        return "There was a problem fetching the weather."

def calculate_expression(expression):

    expression = expression.replace("x", "*").replace("times", "*").replace("divided by", "/").replace("plus", "+").replace("minus", "-")
    

    if not re.match(r'^[0-9+\-*/.() ]+$', expression):
        return "Sorry, I couldn't compute that. Please check the expression."

    try:
        result = eval(expression) 
        return f"The result is {result}"
    except Exception as e:
        return "Sorry, I couldn't compute that. Please check the expression."


def fetch_latest_news():
    api_key = news_api_key  
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        news_data = response.json()
        if news_data["status"] == "ok":
            articles = news_data["articles"]
            headlines = [article["title"] for article in articles[:5]]
            return "Here are the latest headlines: " + " | ".join(headlines)
        else:
            return "Sorry, I couldn't fetch the latest news."
    except Exception as e:
        return "There was an issue fetching the news."


def tell_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "I asked the librarian if the library had any books on suicide. She said they're on the top shelf."
    ]
    return random.choice(jokes)
def convert_currency(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{currency_api_key}/latest/{from_currency}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
       
        if data["result"] == "success":
          
            conversion_rate = data["conversion_rates"].get(to_currency)
            if conversion_rate:
                converted_amount = round(amount * conversion_rate, 2)
                return f"{amount} {from_currency} is equal to {converted_amount} {to_currency}."
            else:
                return f"Sorry, I couldn't find the exchange rate for {to_currency}."
        else:
            return "Sorry, I couldn't fetch the currency conversion data."
    except Exception as e:
        return f"There was an issue fetching the currency conversion data: {str(e)}"


def set_reminder():
    speak("What would you like to be reminded about?")
    task = listen_to_user()
    if task != "None":
        speak(f"Reminder set for: {task}")

def main():
    greet_user()
    while True:
        query = listen_to_user()

        if "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "open google" in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")
        elif "open youtube" in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
        elif "open github" in query:
            speak("Opening GitHub...")
            webbrowser.open("https://github.com/NS-Sheam")
        elif "play music" in query:
            music_dir = "D:\\Python\\desktop-assistance\\songs"  
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found in your music directory.")

        elif "wikipedia" in query:
            speak("What do you want to know from Wikipedia?")
            topic = listen_to_user()
            if topic != "None":
                summary = search_wikipedia(topic)
                speak(summary)

        elif "weather" in query:
            speak("Which city's weather would you like to know?")
            city = listen_to_user()
            if city != "None":
                weather_info = fetch_weather(city)
                speak(weather_info)

        elif "calculate" in query:
            speak("Please tell me the calculation.")
            expression = listen_to_user()
            if expression != "None":
                result = calculate_expression(expression)
                speak(result)

        elif "news" in query:
            speak("Fetching the latest news for you...")
            news_info = fetch_latest_news()
            speak(news_info)

        elif "tell me a joke" in query:
            joke = tell_joke()
            speak(joke)

        elif "convert currency" in query:
            speak("Please tell me the amount and the currencies to convert from and to.")
            conversion_info = listen_to_user()
            if conversion_info != "None":
         
                match = re.match(r"(\d+) (\w+) to (\w+)", conversion_info)
                if match:
                    amount, from_currency, to_currency = match.groups()
                    result = convert_currency(float(amount), from_currency, to_currency)
                    speak(result)

        elif "set reminder" in query:
            set_reminder()

        elif "exit" in query or "quit" in query:
            speak("Goodbye! Have a great day!")
            break

        else:
            # speak("What would you like to ask?")
            # prompt = listen_to_user()
            prompt = query
            
            if prompt != "None":
                speak("Thinking...")
                response_stream = ask_to_ai(prompt)

                # Speak responses as they arrive
                full_response = ""
                for chunk in response_stream:
                    print(chunk, end="", flush=True)  # Show response in terminal
                    full_response += chunk  # Accumulate full response
                    speak(chunk)  # Speak the chunk in real-time

                print("\n")  # Add a new line for better formatting

if __name__ == "__main__":
    main()
