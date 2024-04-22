import argparse
import logging
import os
import sys
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Assuming helpers.py contains the necessary functions
from helpers import (
    load_credentials, 
    extract_doc_id, 
    extract_text, 
    count_tokens,
    send_gpt_request
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv("local.env")

def main():
    # Load or create new credentials
    creds = load_credentials()
    # Use the credentials to create an API service object
    service = build('docs', 'v1', credentials=creds)
    openai_api_key = os.getenv("OPEN_AI_API_KEY")

    if not openai_api_key:
        logging.error("OPEN_AI_API_KEY environment variable not set.")
        sys.exit(1)

    # Instantiate arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", help="Document URL", required=True)
    parser.add_argument("-pre", help="Prompt prefix", default="")
    parser.add_argument("-post", help="Prompt suffix", default="")

    args = parser.parse_args()

    # Extract document ID from URL
    document_id = extract_doc_id(args.url)
    if not document_id:
        logging.error("Failed to extract document ID from the URL.")
        sys.exit(1)

    try:
        # Load document and extract text content
        doc = service.documents().get(documentId=document_id).execute()
        text_content = extract_text(doc)
        token_count = count_tokens(text_content)
        logging.info(f"Extracted text content with {token_count} tokens.")

        # Send request to GPT model
        doc_review = send_gpt_request(
            document_text=text_content, 
            openai_api_key=openai_api_key, 
            pre_prompt=args.pre, 
            post_prompt=args.post
        )

        print(doc_review)
    except HttpError as e:
        logging.error(f"An HTTP error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
