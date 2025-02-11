# Oaksol-OCR
# OCR Data Extraction & MySQL Integration

This project extracts text from **patient assessment forms** using **OCR (Tesseract + EasyOCR)** and stores the structured data in **MySQL**.

---

##  Features

- **Extracts text from printed & handwritten forms** using OCR.
- **Converts text into structured JSON format**.
- **Stores extracted data in MySQL** for easy retrieval.
- **Uses Docker for MySQL setup** (or allows manual installation).
- **Processes images extracted from a PDF**.

---

##  **Setup Instructions**

### Clone the Repository

```sh
git clone https://github.com/DatteshSukhadia/ocr_project.git
cd ocr_project
```
## Set Up a Virtual Environment
- **Create and activate a virtual environment to manage dependencies.
- **python3 -m venv venv
- **source venv/bin/activate  

## Requirement Installation
- pip install -r requirements.txt

- Set Up MySQL Database
- You can use Docker 
- Make sure Docker is installed and running.
- Start the MySQL container:
- docker compose up -d

- Verify MySQL is running:
- docker ps

- Extract Images from the PDF
- Run the script to extract images from the provided PDF.
- python3 extract_images.py

- Run the OCR Script to Extract and Store Data
- python3 ocr_extraction.py

- Verify Stored Data in MySQL
- mysql -u myuser -p
- Then run:
- USE ocr_data;
- SELECT * FROM patients;
- SELECT * FROM forms_data;

## Project Structure:
- ocr_project/
- │── extracted_images/       # Folder for extracted images from the PDF
- │── mysql_data/             # MySQL data (if using Docker)
- │── venv/                   # Virtual environment (not uploaded to GitHub)
- │── ocr_extraction.py       # Main OCR script
- │── extract_images.py       # Script to extract images from PDF
- │── docker-compose.yml      # Docker setup for MySQL
- │── schema.sql              # MySQL table creation script
- │── sample_output.json      # Example JSON output
- │── README.md               # Documentation & setup instructions
- │── requirements.txt        # List of dependencies
- │── .gitignore              # To exclude unnecessary files

## Sample JSON Output
- {
  - "patient_name": "John Doe",
  - "dob": "01/05/1988",
  - "injection": "Yes",
  - "exercise_therapy": "No",
  - "difficulty_ratings": {
    - "bending": 3,
    - "putting_on_shoes": 1,
    - "sleeping": 2
  - },
  - "pain_symptoms": {
    - "pain": 2,
    - "numbness": 5,
    - "tingling": 6
  - }
- }


