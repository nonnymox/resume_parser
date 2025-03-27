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
    try:
        file_stream = io.BytesIO(file_object.read())  # Preserve file stream
        with pymupdf.open(stream=file_stream, filetype=file_extension) as document:
            text = "\n".join([page.get_text() for page in document])
        return text
    except Exception as e:
        return f"Error reading file: {str(e)}"


def extract_info(text: str) -> dict:
    """
    Extracts structured resume information using Groq API.
    """
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": """You are an AI bot that extracts structured information from resumes.
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
            temperature=0.3,
        )

        extracted_data = response.choices[0].message.content.strip()

        # Remove Markdown-style JSON formatting
        extracted_data = re.sub(r"```json\s*|\s*```", "", extracted_data)

        return json.loads(extracted_data)  # Convert JSON string to dictionary
    except json.JSONDecodeError as e:
        return {"error": "Invalid JSON response", "details": extracted_data}
    except Exception as e:
        return {"error": str(e)}
