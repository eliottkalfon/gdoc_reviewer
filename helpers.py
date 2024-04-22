import pickle
import os
import re
import tiktoken
import logging
from openai import OpenAI
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


# Define the scope of the application
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# Path to save the credentials
CREDENTIALS_PATH = 'google_credentials/token.pickle'
CLIENT_SECRET_FILE = 'google_credentials/credentials.json'

def load_credentials():
    """Loads or create new credentials"""
    creds = None
    # Check if the file with the saved credentials exists
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH, 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials are available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CREDENTIALS_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def extract_doc_id(url: str) -> str:
    """Extracts the document ID from the document URL"""
    pattern = r'/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None
    

def count_tokens(input_text: str) -> int:
    """Counts the GPT-4 tokens in a string"""
    encoding = tiktoken.encoding_for_model("gpt-4-turbo")
    return len(encoding.encode(input_text))

def extract_text(doc_object) -> str:
    """Extracts the text from a gdoc API document object"""
    text_content = ""
    for element in doc_object['body']['content']:
        if 'paragraph' in element:
            for para_element in element['paragraph']['elements']:
                if 'textRun' in para_element:
                    text_content += para_element['textRun']['content']
    return text_content

def send_gpt_request(document_text, openai_api_key, pre_prompt="", post_prompt=""):
    """Sends a string surrounded by prompt prefix and suffix."""
    client = OpenAI(api_key=openai_api_key)
    prompt = (
        f"{pre_prompt}"
        f"{document_text}\n\n"
        f"{post_prompt}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "Failed to get feedback from GPT-4."