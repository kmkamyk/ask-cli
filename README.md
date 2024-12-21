# Ask CLI
**Ask CLI** is a Linux shell LLM assistant designed to assist system administrators with their daily tasks. It connects to local or internet-accessible Large Language Models (LLMs) using APIs compatible with Openai api standards, allowing users to send queries and receive concise, actionable responses directly in the terminal.

It works seamlessly with tools like [llama.cpp](https://github.com/ggerganov/llama.cpp) and [Ollama](https://github.com/ollama/ollama), which enable running all the most popular open LLMs, such as LLaMA 3, Gemma, and Mistral, providing flexibility and enhanced privacy.


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

#### Option 1: Using the Installation Script (Recommended)

To install **Ask CLI** with the provided script, run the following command:

```bash
curl -sfL https://github.com/kmkamyk/ask-cli/raw/main/install.sh | sh -
```

This will automatically download and install `ask.py` to `/usr/bin/ask` and `config.yml` to `/etc/ask/config.yml`.

To uninstall, run:

```bash
curl -sfL https://github.com/kmkamyk/ask-cli/raw/main/install.sh | sh -s uninstall
```

#### Option 2: Manual Installation (Using Git)

1. Clone the repository:

   ```bash
   git clone https://github.com/kmkamyk/ask-cli.git
   cd ask-cli
   ```
2. Install requirements for Python.

   ```bash
   python3 -m pip install -r requirements.txt
   ```
4. Copy the `ask.py` script to `/usr/bin/` and make it executable:

   ```bash
   sudo cp ask.py /usr/bin/ask
   sudo chmod +x /usr/bin/ask
   ```

5. Place the `config.yml` configuration file in `/etc/ask/`:

   ```bash
   sudo mkdir -p /etc/ask
   sudo cp config.yml /etc/ask/config.yml
   ```

6. Place the configuration file in `/etc/ask/config.yml`.

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
