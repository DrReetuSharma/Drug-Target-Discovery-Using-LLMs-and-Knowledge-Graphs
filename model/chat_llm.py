import openai
import time

openai.api_key = " "

def chat_with_gpt(prompt):
"""
To create chatconversation with LLM Model(gpt-3.5-turbo) with ChatCompletion method. 
Add pip install openai==0.28.0 in the requirements.txt. Reason: The new openai version does not this method
Limited attempts allowed

Try except for error handling. The code works when directly called only

Return: conversation with LLM Model
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Please wait before making more requests.")
        time.sleep(60)  # Wait for 60 seconds before retrying
        return None

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gpt(user_input)
        if response:
            print("Chatbot: ", response)
