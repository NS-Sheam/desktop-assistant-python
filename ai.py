import openai
from config import openai_api_key

openai.api_key = openai_api_key

def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message["content"].strip()
        return answer
    except openai.error.RateLimitError:
        return "I'm sorry, I've hit my usage limit. Please try again later."
    