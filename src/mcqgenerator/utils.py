import os
import json
import traceback
import PyPDF2

def read_file(file):
    """
    Reads a PDF or TXT file uploaded via Streamlit and returns the text content.
    Supports .pdf and .txt files only.
    """
    try:
        if file.name.lower().endswith(".pdf"):
            # Use PdfReader from PyPDF2 (compatible with BytesIO)
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            if not text.strip():
                raise Exception("PDF file is empty or could not extract text.")
            return text

        elif file.name.lower().endswith(".txt"):
            # Read text file
            return file.read().decode("utf-8")

        else:
            raise Exception("File format not supported. Only PDF and TXT files are supported.")

    except Exception as e:
        raise Exception(f"Error reading the file: {e}") from e


def get_table_data(quiz_str):
    """
    Converts quiz JSON string into a list of dictionaries for displaying in a table.
    """
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "")
            options = " || ".join(
                [f"{option} -> {option_value}" for option, option_value in value.get("options", {}).items()]
            )
            correct = value.get("correct", "")
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
