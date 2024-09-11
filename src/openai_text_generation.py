import openai
from time import sleep

# Set up your OpenAI API key
openai.api_key = 'your-api-key'

# Define the prompt input from the user
input_text = input("Enter your prompt: ").strip()

if not input_text:
    print("No prompt provided.")
else:
    try:
        # Call the OpenAI API to generate the response using GPT-3.5
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # GPT-3.5 model
            prompt=input_text,
            max_tokens=500,  # Maximum number of tokens to generate
            temperature=0.7,  # Adjust temperature for creativity (higher = more creative)
            top_p=0.9,  # Nucleus sampling
            frequency_penalty=0,  # Control repetition
            presence_penalty=0,  # Encourage new topics
            n=1,  # Number of outputs (1 for single output)
            stop=None  # No stop sequence (can define if needed)
        )

        # Extract the generated text from the response
        generated_text = response.choices[0].text.strip()

        # Print the generated text
        print("\nGenerated Text:\n", generated_text)
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Please try again later.")
        sleep(60)  # Wait for a minute before retrying
