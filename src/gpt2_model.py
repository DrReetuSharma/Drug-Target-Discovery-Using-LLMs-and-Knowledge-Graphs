from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set the padding token to the EOS token
tokenizer.pad_token = tokenizer.eos_token

# Define your input text
input_text = input("Enter your prompt:")

# Tokenize input text
inputs = tokenizer(input_text, return_tensors='pt', padding=True)

# Generate text
output = model.generate(
    inputs.input_ids,
    attention_mask=inputs.attention_mask,  # Set the attention mask
    max_length=1000,
    pad_token_id=tokenizer.eos_token_id,    # Set the pad token ID to the EOS token ID
    do_sample=False,
    temperature=0.2,                       # Adjusted temperature for a balance between randomness and focus
    #top_k=50,                             # Use top 50 tokens
    #top_p=0.9,                            # Cumulative probability for nucleus sampling
    repetition_penalty=1.5,               # Add repetition penalty to reduce repetitive text
    num_return_sequences=1                # Number of variations to return
)

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
print(generated_text)
