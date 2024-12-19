#!/usr/bin/python3

import openai
import yaml
import sys
import os

# Constants
CONFIG_PATH = "/etc/ask/config.yml"
VERSION = "1.1.0"

# Function to load the configuration
def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"The configuration file {config_path} does not exist!")
        sys.exit(1)
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Validate the config structure
    validate_config(config)
    return config

# Function to validate configuration
def validate_config(config):
    required_keys = {
        "api": ["base_url", "api_key"],
        "model": ["name", "system_prompt", "temperature"]
    }
    try:
        for section, keys in required_keys.items():
            if section not in config:
                raise KeyError(f"Missing section '{section}' in configuration.")
            for key in keys:
                if key not in config[section]:
                    raise KeyError(f"Missing key '{key}' in section '{section}' in configuration.")
    except KeyError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

# Function to display help
def display_help():
    help_text = f"""
ask CLI Assistant - Version {VERSION}

Usage:
  ask <query>           Send a query to the LLM and get a response.
  ask --version, -v     Display the version of the CLI tool.
  ask --help, -h        Display this help message.

Configuration:
  The tool uses a configuration file located at {CONFIG_PATH}.
  The configuration file should include the following keys:

  api:
    base_url: "http://<HOSTNAME_IP_ADDRESS>:<PORT_NR>/v1"
    api_key: "your_api_key_here"

  model:
    name: "model_name_here"
    system_prompt: "system_prompt_here"
    temperature: 0.0
"""
    print(help_text)

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
    # Check if version or help flag is used
    if len(sys.argv) == 2:
        if sys.argv[1] in ("--version", "-v"):
            print(f"ask version {VERSION}")
            sys.exit(0)
        elif sys.argv[1] in ("--help", "-h"):
            display_help()
            sys.exit(0)

    # Load the configuration
    try:
        config = load_config(CONFIG_PATH)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

    # Get arguments from the CLI
    if len(sys.argv) < 2:
        print("Usage: ask <query>")
        print("Use --help or -h for more information.")
        sys.exit(1)
    
    # Build the prompt from arguments
    user_input = " ".join(sys.argv[1:])
    
    # Send the query to the LLM
    query_llm(user_input, config)
    
if __name__ == "__main__":
    main()
