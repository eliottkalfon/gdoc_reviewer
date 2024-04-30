# GDoc Reviewer

## Overview
The GDoc Reviewer is a Python script designed to facilitate the review of Google Docs content by leveraging the capabilities of OpenAI's GPT models. It extracts text from a specified Google Docs URL, optionally prepends and appends custom text prompts, and submits the combined text to a GPT model for processing. The script is ideal for automating content review, summarization, or any other text-based analysis.

## Getting Started

### Prerequisites
- Python 3.8+
- Google API OAuth credentials (follow [this guide](https://developers.google.com/workspace/guides/create-credentials) to create credentials)
- OpenAI API key

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/eliottkalfon/gdoc_reviewer
   cd gdoc_reviewer
   ```

2. **Setup a Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Place your `credentials.json` file in the `google_credentials` directory (see `credentials_example.json`)
   - Ensure you have a `.env` file in your project directory (you can rename the provided `local.env.example` to `.env`).
   - Add your `OPEN_AI_API_KEY` to the `.env` file:
     ```
     OPEN_AI_API_KEY='your_openai_api_key_here'
     ```

## Usage

Run the script by providing the Google Docs URL and optionally, pre and post prompts (both are optional):

```bash
python gdoc_reviewer.py -url "https://docs.google.com/document/d/your_document_id_here/edit" -pre "Please review the following text:" -post "End of analysis."
```


## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or improvements.

## License
Distributed under the [Apache 2.0 License](LICENSE). See `LICENSE` for more information.