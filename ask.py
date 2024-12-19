"""
ask.py - CLI Assistant for querying an LLM using OpenAI API.

This script provides a command-line interface to interact with an
LLM (Language Model) via a configuration file.
"""

import os
import sys
import openai
import yaml

# Constants
CONFIG_PATH = "/etc/ask/config.yml"
VERSION = "1.1.0"

def load_config(config_path):
    """
    Load and validate the YAML configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration dictionary.

    Raises:
        SystemExit: If the configuration file does not exist or is invalid.
    """
    if not os.path.exists(config_path):
        print(f"The configuration file {config_path} does not exist!")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    validate_config(config)
    return config

def validate_config(config):
    """
    Validate the structure of the configuration file.

    Args:
        config (dict): Configuration dictionary to validate.

    Raises:
        SystemExit: If the configuration is missing required sections or keys.
    """
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
    except KeyError as error:
        print(f"Configuration error: {error}")
        sys.exit(1)

def display_help():
    """
    Display the help message for the CLI tool.
    """
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

def query_llm(prompt, config):
    """
    Send a query to the LLM and display the response.

    Args:
        prompt (str): User's input query.
        config (dict): Configuration dictionary for API and model.
    """
    client = openai.OpenAI(
        base_url=config["api"]["base_url"],
        api_key=config["api"]["api_key"],
    )
    try:
        completion = client.chat.completions.create(
            model=config["model"]["name"],
            messages=[
                {"role": "system", "content": config["model"]["system_prompt"]},
                {"role": "user", "content": prompt}
            ],
            temperature=config["model"].get("temperature", 0.7),
            stream=True,
        )
        for chunk in completion:
            text_chunk = chunk.choices[0].delta.content
            if text_chunk:
                print(text_chunk, end="", flush=True)
        print()  # Add a new line after the response
    except openai.OpenAIError as error:
        print(f"Error: {error}")

def main():
    """
    Main function to handle CLI arguments and run the tool.
    """
    if len(sys.argv) == 2:
        if sys.argv[1] in ("--version", "-v"):
            print(f"ask version {VERSION}")
            sys.exit(0)
        if sys.argv[1] in ("--help", "-h"):
            display_help()
            sys.exit(0)

    try:
        config = load_config(CONFIG_PATH)
    except FileNotFoundError:
        print(f"Configuration file not found at {CONFIG_PATH}.")
        sys.exit(1)
    except yaml.YAMLError as error:
        print(f"Error parsing configuration file: {error}")
        sys.exit(1)
    except openai.OpenAIError as error:
        print(f"Error communicating with OpenAI API: {error}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(0)
    except OSError as error:
        print(f"System error: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: ask <query>")
        print("Use --help or -h for more information.")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    query_llm(user_input, config)

if __name__ == "__main__":
    main()
