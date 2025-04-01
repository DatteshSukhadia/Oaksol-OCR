import pymysql  #Replacing mysql.connector with pymysql
import json
import cv2
import pytesseract
import easyocr
import os
import re

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "myuser",
    "password": "mypassword",
    "database": "ocr_data",
    "port": 3306
}

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def preprocess_image(image_path):
    """Convert image to grayscale and apply thresholding."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: Image file '{image_path}' not found or cannot be opened.")

    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Error: Unable to read image file '{image_path}'. Check the format and path.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image_path):
    """Extract text using OCR."""
    processed_img = preprocess_image(image_path)

    # Use Tesseract for printed text
    text_tesseract = pytesseract.image_to_string(processed_img)

    # Use EasyOCR for handwritten text
    text_easyocr = " ".join(reader.readtext(image_path, detail=0))

    # Combine both results
    full_text = text_tesseract + "\n" + text_easyocr
    return full_text

def extract_data(text):
    """Extract structured data using regex."""
    data = {}

    # Extract patient details
    name_match = re.search(r"Patient Name\s*:\s*(.+)", text)
    dob_match = re.search(r"DOB\s*:\s*(\d{2}/\d{2}/\d{4})", text)
    
    data["patient_name"] = name_match.group(1).strip() if name_match else "Unknown"
    data["dob"] = dob_match.group(1) if dob_match else "Unknown"

    # Extract injection and therapy details
    data["injection"] = "Yes" if "INJECTION : YES" in text else "No"
    data["exercise_therapy"] = "Yes" if "Exercise Therapy : YES" in text else "No"

    # Extract difficulty ratings
    difficulty_keywords = [
        "Bending", "Putting on shoes", "Sleeping", "Standing for an hour",
        "Going up or down a flight of stairs", "Walking through a store",
        "Driving for an hour", "Preparing a meal", "Yard work", "Picking up items off the floor"
    ]
    
    difficulty_ratings = {}
    for keyword in difficulty_keywords:
        match = re.search(fr"{keyword}:\s*(\d)", text)
        difficulty_ratings[keyword.lower().replace(" ", "_")] = int(match.group(1)) if match else None

    data["difficulty_ratings"] = difficulty_ratings

    # Extract pain symptoms
    pain_keywords = ["Pain", "Numbness", "Tingling", "Burning", "Tightness"]
    pain_symptoms = {}
    for keyword in pain_keywords:
        match = re.search(fr"{keyword}:\s*(\d+)", text)
        pain_symptoms[keyword.lower()] = int(match.group(1)) if match else None

    data["pain_symptoms"] = pain_symptoms

    return data

def insert_into_db(data):
    """Insert extracted OCR JSON data into MySQL."""
    try:
        conn = pymysql.connect(**db_config)  
        cursor = conn.cursor()

        # Insert Patient Data
        cursor.execute(
            "INSERT INTO patients (name, dob) VALUES (%s, %s)", 
            (data["patient_name"], data["dob"])
        )
        patient_id = cursor.lastrowid  # Get the newly inserted patient ID

        # Insert JSON Data
        cursor.execute(
            "INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s)",
            (patient_id, json.dumps(data))
        )

        conn.commit()
        cursor.close()
        conn.close()
        print(" Data successfully stored in MySQL!")

    except pymysql.MySQLError as err:
        print(f" MySQL Error: {err}")

if __name__ == "__main__":
    # Set image path (update as needed)
    image_path = "/Users/kishansukhadia/ocr_project/extracted_images/sample_form_1.jpg"

    try:
        # Step 1: Extract text from the image
        ocr_text = extract_text(image_path)

        # Step 2: Convert extracted text into structured JSON format
        structured_data = extract_data(ocr_text)

        # Step 3: Print structured data
        print("Extracted JSON Data:", json.dumps(structured_data, indent=4))

        # Step 4: Store in MySQL
        insert_into_db(structured_data)

    except Exception as e:
        print(f" Error: {e}")
