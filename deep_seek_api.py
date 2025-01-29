# import aiohttp
# import asyncio

# async def query_ollama(prompt, model="deepseek-r1"):
#     url = "http://localhost:11434/api/generate"
#     payload = {
#         "model": model,
#         "prompt": prompt,
#         "stream": False
#     }

#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, json=payload) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     return data["response"]
#                 else:
#                     raise Exception(f"Error: {response.status}, {await response.text()}")
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Example usage
# async def main():
#     prompt = "What is Javascript?"
#     response = await query_ollama(prompt)
#     print(response)

# # Run the async function
# asyncio.run(main())


import requests
import json
import pyttsx3
import time
engine = pyttsx3.init()




def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_to_ai(prompt, model="deepseek-r1"):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True  # Enable streaming
    }

    try:
        response = requests.post(url, json=payload, stream=True)
        
        if response.status_code == 200:
            buffer = ""  # Store small chunks before speaking
            interval = 0.5  # Adjust this for faster/slower intervals now interval is 0.5 seconds
            last_spoken = time.time()
            # Iterate over the response stream line by line (chunk by chunk)
            for line in response.iter_lines():
                if line:
                    # Decode the line and parse the JSON chunk
                    chunk = json.loads(line.decode("utf-8")).get("response", "")
                    buffer += chunk
                    print(chunk, end="", flush=True)  # Print response in real-time

                    # Speak after accumulating enough text or after time passes
                    # if len(buffer) > 20 or (time.time() - last_spoken) > interval:
                    if "." in buffer or "?" in buffer or "!" in buffer:
                        speak(buffer)
                        buffer = ""  # Clear buffer after speaking
                        last_spoken = time.time()

            # Speak remaining text if any
            if buffer:
                speak(buffer)
    
    except Exception as e:
        speak(f"An error occurred: {e}")

# Example usage
prompt = "What is Javascript?"
# ask_to_ai(prompt)