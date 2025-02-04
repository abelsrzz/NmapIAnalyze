# Nmap Scan Analyzer

This project is a cybersecurity assistant specialized in analyzing Nmap scan files. It extracts and analyzes relevant information from the scan results, identifies potential security vulnerabilities, and provides actionable insights for offensive security analysts.

## Features

- Extracts detailed information from Nmap scan results.
- Identifies open ports, services, service versions, and operating system details.
- Cross-references identified services and versions with publicly known CVEs.
- Highlights misconfigurations, outdated software, and weak security protocols.
- Provides clear and concise summaries of findings.
- Suggests actionable next steps for further reconnaissance and exploitation.

## Requirements

- Python 3.6+
- Required Python packages (listed in `requirements.txt`):
  - openai
  - pwntools
  - termcolor
  - rich
  - InquirerPy
  - python-dotenv

```sh
pip install -r requirements.txt
```

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/nmap-scan-analyzer.git
    cd nmap-scan-analyzer
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file with your OpenRouter API key:
    ```env
    OPENROUTER_API_KEY="your-api-key-here"
    ```

4. Ensure that the [.env](http://_vscodecontentref_/0) file is listed in [.gitignore](http://_vscodecontentref_/1) to avoid exposing your API key.

## Usage

1. Run the main script:
    ```sh
    python NmapIAnalize.py
    ```

2. Follow the prompts to select an Nmap output file to analyze.

3. The assistant will analyze the file and provide a detailed report of the findings.

4. You can ask further questions based on the analysis results.

## Example

An example Nmap output file (`nmap_sample.txt`) is provided in the repository. You can use this file to test the functionality of the assistant.
