# Ask CLI

**Ask CLI** is a command-line tool for interacting with a local LLM (Large Language Model) server. It allows you to send queries and receive concise command-line responses.

## Features
- Sends user input to a local LLM server.
- Displays only the command-line output without additional text.
- Reads configuration from `/etc/ask/config.yml`.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kmkamyk/ask-cli.git
   cd ask-cli
   ```

2. Copy the script to `/usr/bin` and make it executable:
   ```bash
   sudo cp ask /usr/bin/
   sudo chmod +x /usr/bin/ask
   ```

3. Place the configuration file in `/etc/ask/config.yml`.

## Example Usage
```bash
ask "How to find the oldest files in the current directory?"
```

Expected output:
```bash
find . -type f -print -exec stat -c "%Y %n" {} \; | sort -rn | head
```

## Configuration
The tool reads its configuration from `/etc/ask/config.yml`. Example:
```yaml
api:
  base_url: "http://localhost:8080/v1"
  api_key: "sk-no-key-required"

model:
  name: "Meta-Llama-3.1"
  system_prompt: "You are a helpful CLI assistant in BASH. Display only the command on the screen and nothing else."
  temperature: 0.7
```
