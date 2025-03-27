from django.core.files.uploadedfile import UploadedFile
import pymupdf
import openai
import os
import io
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")  # Ensure API key is loaded

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Check your .env file.")

openai_client = openai.OpenAI(api_key=api_key)  # Explicitly pass API key


openai_client = openai.OpenAI(api_key=api_key)

def read_uploaded_file(file_object: UploadedFile, file_extension: str) -> str: 
    try:
        file_stream = io.BytesIO(file_object.read())  # Preserve file stream
        with pymupdf.open(stream=file_stream, filetype=file_extension) as document:
            text = "\n".join([page.get_text() for page in document])
        return text
    except Exception as e:
        return f"Error reading file: {str(e)}"

def extract_info(text: str) -> dict:
    """
    Extracts structured resume information using OpenAI API.
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[
                {"role": "system", "content": """You are an AI bot that extracts structured information from resumes.
                Extract the following fields:
                - applicant_name
                - highest_level_of_study
                - institution
                - course_of_study
                - introduction
                - skills (as a list)
                - experiences (list of {employer_name, role, duration})
                Respond in pure JSON format.
                """},
                {"role": "user", "content": text},
            ],
            max_tokens=512,
            temperature=0.5,
        )
        
        extracted_data = response.choices[0].message.content  # Extract content
        return json.loads(extracted_data)  # Convert JSON string to dict
    except Exception as e:
        return {"error": str(e)}
