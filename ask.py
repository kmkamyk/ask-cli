#!/usr/bin/python3

import openai
import yaml
import sys
import os

# Path to the configuration file
CONFIG_PATH = "/etc/ask/config.yml"

# Function to load the configuration
def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"The configuration file {config_path} does not exist!")
        sys.exit(1)
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

# Function to communicate with the LLM
def query_llm(prompt, config):
    client = openai.OpenAI(
        base_url=config["api"]["base_url"],
        api_key=config["api"]["api_key"],
    )
    
    try:
        # Sending the query to the LLM
        completion = client.chat.completions.create(
            model=config["model"]["name"],
            messages=[
                {"role": "system", "content": config["model"]["system_prompt"]},
                {"role": "user", "content": prompt}
            ],
            temperature=config["model"].get("temperature", 0.7),
            stream=True,
        )
        # Returning the response
        for chunk in completion:
            text_chunk = chunk.choices[0].delta.content
            if text_chunk:  # Skip if `text_chunk` is None or empty
                print(text_chunk, end="", flush=True)
        
        # Add a new line after the response
        print()
    except Exception as e:
        print(f"Error: {e}")

# Main function
def main():
    # Load the configuration
    config = load_config(CONFIG_PATH)

    # Get arguments from the CLI
    if len(sys.argv) < 2:
        print("Usage: ask <query>")
        sys.exit(1)
    
    # Build the prompt from arguments
    user_input = " ".join(sys.argv[1:])
    
    # Send the query to the LLM
    query_llm(user_input, config)
    
if __name__ == "__main__":
    main()
