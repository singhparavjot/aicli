import os
import openai
from openai import OpenAI



# Get the OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)




def interpret_command(user_input):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant that translates natural language to kubectl commands. Provide only the kubectl command as output."},
        {"role": "user", "content": f"Translate this to a kubectl command: {user_input}"}
    ])
    command = response.choices[0].message.content.strip()
    return command

def get_gpt_solution(command, error):
    prompt = (
        f"The following kubectl command encountered an error:\n\n"
        f"Command: {command}\n"
        f"Error: {error}\n\n"
        f"Please provide a potential solution or steps to troubleshoot this issue."
    )
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Kubernetes expert."},
        {"role": "user", "content": prompt}
    ])
    solution = response.choices[0].message.content.strip()
    return solution

def explain_output(output):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant that explains kubectl command outputs in a user-friendly manner."},
        {"role": "user", "content": f"Explain this kubectl command output: {output}"}
    ])
    explanation = response.choices[0].message.content.strip()
    return explanation

