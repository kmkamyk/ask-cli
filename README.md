# Ask CLI
**Ask CLI** tool is a command-line application designed to assist Linux system administrators with their daily tasks by leveraging the power of Large Language Models (LLMs). It connects to local and internet-accessible LLMs using APIs compatible with Openai API standards, allowing users to send queries and receive responses directly in the terminal.

<img width="908" alt="image" src="https://github.com/user-attachments/assets/6d2d783e-0211-4a5f-8da9-01070f0ca1c8" />

## Example Usage
You can ask for specific command-line tasks:

```bash
ask How can I compress a directory into a tar.gz file?
```

**Output**:
```bash
tar -czvf archive.tar.gz /path/to/directory
```

## Features

- Communicates with local LLM servers (e.g., [Ollama](https://ollama.ai/) or [Llama.cpp](https://github.com/ggerganov/llama.cpp)).
- Supports public LLM APIs (e.g., OpenAI's GPT models).
- Customizable configuration via YAML.
- Streamed responses for real-time interaction.
- Lightweight and easy to use.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kmkamyk/ask-cli.git
   cd ask-cli
   ```

2. Copy the script to `/usr/bin` and make it executable:
   ```bash
   sudo cp ask.py /usr/bin/ask
   sudo chmod +x /usr/bin/ask
   ```

3. Place the configuration file in `/etc/ask/config.yml`.

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
