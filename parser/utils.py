from django.core.files.uploadedfile import UploadedFile
import pymupdf
import groq
import os
import io
import json
from dotenv import load_dotenv
import re

# Load environment variables from .env
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")  # Ensure API key is loaded

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set. Check your .env file.")

# Initialize Groq client
groq_client = groq.Client(api_key=groq_api_key)

def read_uploaded_file(file_object: UploadedFile, file_extension: str) -> str:
    """
    Reads the uploaded file and extracts text from it.
    """
    try:
        file_stream = io.BytesIO(file_object.read())  # Preserve file stream
        with pymupdf.open(stream=file_stream, filetype=file_extension) as document:
            text = "\n".join([page.get_text() for page in document])
        return text
    except Exception as e:
        return f"Error reading file: {str(e)}"

def extract_info(text: str) -> str:
    """
    Extracts structured resume information using Groq API and returns a formatted JSON string.
    """
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": """
                You are an AI bot that extracts structured information from resumes.
                Extract the following fields and return a valid JSON object:
                - applicant_name (string)
                - highest_level_of_study (string)
                - institution (string)
                - course_of_study (string)
                - introduction (string)
                - skills (list of strings)
                - experiences (list of objects with employer_name, role, and duration)
                
                Ensure the response is a **valid** JSON object **without markdown formatting**.
                """},
                {"role": "user", "content": text},
            ],
            max_tokens=512,
            temperature=0.5,
        )

        extracted_data = response.choices[0].message.content.strip()

        # Remove Markdown-style JSON formatting
        extracted_data = re.sub(r"```json\s*|\s*```", "", extracted_data)

        parsed_data = json.loads(extracted_data)  # Convert JSON string to dictionary
        
        # Return formatted JSON string
        return json.loads(extracted_data)
    except json.JSONDecodeError as e:
        return json.dumps({"error": "Invalid JSON response", "details": extracted_data}, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)
