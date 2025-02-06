#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script analyzes Nmap scan files using an AI model to identify potential security vulnerabilities and known CVEs.
# It provides detailed information on open ports, services, service versions, and operating system details.
# The script highlights misconfigurations, outdated software, and weak security protocols, and suggests actionable next steps for further reconnaissance or exploitation.

# Usage:
# Run the script and follow the prompts to select an Nmap output file for analysis. The script will communicate with the AI model to analyze the file and provide detailed findings. Users can ask further questions based on the analysis.

# Credits:
# - Developed by @abelsrzz

# Import necessary libraries
import os
from dotenv import load_dotenv
from InquirerPy import prompt
from openai import OpenAI
from pwn import *
from rich.console import Console
from rich.markdown import Markdown
from termcolor import colored

# Load environment variables
load_dotenv()
APIKEY = os.getenv("OPENROUTER_API_KEY")
if not APIKEY:
    log.critical("No API key was provided")
    exit(1)

# Define the AI model to use
# IA_MODEL = "deepseek/deepseek-r1:free"
# IA_MODEL = "deepseek/deepseek-r1-distill-llama-70b:free"
# IA_MODEL = "google/gemini-2.0-flash-thinking-exp:free"
IA_MODEL = "nvidia/llama-3.1-nemotron-70b-instruct:free"
# IA_MODEL = "meta-llama/llama-3.2-3b-instruct:free"

# Initialize console for rich text output
console = Console()
client = OpenAI(api_key=APIKEY, base_url="https://openrouter.ai/api/v1")

# Context for AI model
conversation_history = [
    {"role": "system", "content": "You are a cybersecurity assistant specialized in analyzing Nmap scan files with a focus on identifying potential security vulnerabilities and known CVEs (Common Vulnerabilities and Exposures). Your primary task is to extract detailed information from scan results, including open ports, services running on those ports, service versions, and operating system details. Cross-reference identified services and versions with publicly known CVEs to detect possible vulnerabilities. Highlight any misconfigurations, outdated software, or weak security protocols. Provide a clear, concise summary of findings tailored for offensive security analysts, emphasizing exploitable weaknesses and known vulnerabilities. Suggest actionable next steps for further reconnaissance, exploitation techniques, or tools that may be effective based on the scan data."},
]

# Warn the user if a paid model is being used
def not_free_warn():
    if "free" not in IA_MODEL:
        log.warning("You are using a paid model, be careful with the usage of the API key")
        questions = [
            {
                "type": "confirm",
                "name": "user_choice",
                "message": "Do you want to continue?",
                "default": False
            }
        ]
        try:
            answers = prompt(questions)
        except Exception:
            log.error(f"Error while asking for file")
            exit(1)
            
        user_choice = answers["user_choice"]
        if not user_choice:
            log.info("Ending the session.")
            exit(0)

# Send a message to the AI model and get the response
def send_message(message):
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": message})

    # Send message to model
    chat = client.chat.completions.create(
        model=IA_MODEL,
        messages=conversation_history
    )
    try:
        response = chat.choices[0].message.content
        
        if response == "":
            raise TypeError
             
    except Exception:
        log.failure("Error while talking with model. Try again later")
        exit(1)


    # Add model response to conversation history
    conversation_history.append({"role": "assistant", "content": response})

    return response

# Print markdown message to terminal
def markdown_to_terminal(message):
    markdown_message = Markdown(message)
    console.print(markdown_message)

# Ask the user to select a file from the current directory
def ask_for_file():
    posible_answers = os.listdir()
    posible_answers.append("[!] Exit")
    questions = [
        {
            "type": "list",
            "name": "user_input",
            "message": f"Select a file to analyze with {IA_MODEL}",
            "choices": posible_answers
        }
    ]
    try:
        answers = prompt(questions)
        
    except Exception:
        log.error(f"Error while asking for file")
        exit(1)
        
    user_input = answers["user_input"]
    if user_input == "[!] Exit":
        log.info("Ending the session.")
        exit(0)
    return user_input


# Communicate with the AI model
def talk_with_model(user_input):
    try: 
        response = send_message(user_input)
        
        if response == "":
            raise TypeError
             
    except Exception:
        log.failure("Error while talking with model. Try again later")
        exit(1)

    return response

# Ask the user if they want to ask further questions
def ask_for_further_questions():
    questions = [
            {
                "type": "confirm",
                "name": "user_choice",
                "message": "Do you want to ask further questions?",
                "default": False
            }
        ]
    try:
        answers = prompt(questions)
        
    except Exception:
        log.error(f"Error while asking for file.")
        exit(1)
        
    user_choice = answers["user_choice"]
    if not user_choice:
        log.info("Ending the session.")
        exit(0)
        
    return user_choice

# Keep the conversation going with the user
def keep_talking():
    keep_talking_progress = log.progress("Further questions")
    while True:
            user_choice = ask_for_further_questions()
            
            if not user_choice:
                break
            
            keep_talking_progress.status("Asking user to input a question")
            user_input = input("Ask a question: ")
            
            keep_talking_progress.status("Waiting for model response")
            response = talk_with_model(user_input)
            
            keep_talking_progress.status("Output received")
            log.info(f"{IA_MODEL}:")
            markdown_to_terminal(response)
            keep_talking_progress.success("Output printed")

# Main function to run the script
def main():
    
    # Display ASCII art for IA analysis
    ascii_art = """
 _   _                      ___    _                _ _         
| \ | |_ __ ___   __ _ _ __|_ _|  / \   _ __   __ _| (_)_______ 
|  \| | '_ ` _ \ / _` | '_ \| |  / _ \ | '_ \ / _` | | |_  / _ \\
| |\  | | | | | | (_| | |_) | | / ___ \| | | | (_| | | |/ /  __/
|_| \_|_| |_| |_|\__,_| .__/___/_/   \_\_| |_|\__,_|_|_/___\___|
                      |_|                                       
    """
    console.print(ascii_art)
    
    # Warn the user if a paid model is being used
    not_free_warn()
    
    log.info(f"Welcome to NmapIAnalize! --- An AI-powered Nmap analysis tool by {colored('@abelsrzz', 'blue')}")
    log.info("Press Ctrl+C for exit.")
    print("\n")

    # Verbose information about the AI model being used
    log.indented = True
    log.info(f"You are using {IA_MODEL}")
    log.indented = False
    
    # Initialize a progress log for the analysis process
    talk_progress = log.progress(f"Analysis in progress")
    
    # Prompt the user to select an Nmap output file to analyze
    user_input = ask_for_file()
    
    # Read the content of the selected file
    talk_progress.status("Sending file content to model")
    with open(user_input, 'r') as file:
        file_content = file.read()
    
    # Send the file content to the AI model for analysis
    talk_progress.status("Waiting for model response")
    response = talk_with_model(file_content)

    # Log the received response and print it to the terminal
    talk_progress.status("Output received")
    log.info(f"{IA_MODEL}:")
    markdown_to_terminal(response)
    talk_progress.success("Output printed")
    
    # Continue the interaction with the user
    keep_talking()

# Entry point of the script
if __name__ == "__main__":
    try:
        main()

    except TypeError:
        log.error("TypeError: Please check the input file and try again.")
        exit(1)
        
    except KeyboardInterrupt:
        log.info(colored("Ctrl+C detected. Exiting gracefully...", "red"))
        exit(1)
