\# Automated Document Verification and Information Inconsistency Detection System



\## Project Overview

The Automated Document Verification System is a Python-based application designed to extract information from documents, verify document details, and identify inconsistencies between two documents.



\## Features

\- \*\*OCR Processing:\*\* Extracts text from scanned documents and images using Tesseract OCR.

\- \*\*Information Extraction:\*\* Identifies fields such as name, date of birth, document ID, phone number, and email.

\- \*\*Document Comparison:\*\* Compares extracted information from two documents.

\- \*\*Inconsistency Detection:\*\* Identifies matching, mismatching, and missing information.

\- \*\*Verification History:\*\* Stores previous comparisons using SQLite.

\- \*\*PDF Reports:\*\* Generates verification reports.



\## Technologies Used

\- Python

\- Streamlit

\- Tesseract OCR

\- PyMuPDF

\- OpenCV

\- SQLite

\- Pandas

\- ReportLab



\## Project Structure

```text

Document-Verification-System/

│

├── app.py

├── database.py

├── requirements.txt

├── modules/

│   ├── \_\_init\_\_.py

│   ├── ocr\_engine.py

│   ├── information\_extraction.py

│   ├── document\_comparison.py

│   └── report\_generator.py

│

├── database/

├── uploads/

└── reports/

```



\## Installation



1\. Clone the repository:

```bash

git clone https://github.com/emanikumar54-spec/Automated-Document-Verification-System.git

```



2\. Navigate into the project:

```bash

cd Automated-Document-Verification-System

```



3\. Create a virtual environment:

```bash

python -m venv .venv

```



4\. Activate it on Windows:

```bash

.venv\\Scripts\\activate

```



5\. Install dependencies:

```bash

pip install -r requirements.txt

```



6\. Install Tesseract OCR and configure its executable path in `modules/ocr\_engine.py`.



\## Run the Application

```bash

streamlit run app.py

```



\## Application Workflow

1\. Upload two documents.

2\. Extract text using OCR.

3\. Identify important information.

4\. Compare extracted details.

5\. Review inconsistencies and verification results.

6\. View comparison history and generate reports.



\## Project Purpose

This project demonstrates how OCR, Python-based information extraction, and automated comparison can support document verification workflows.



\## Author

\*\*E. Manikumar\*\*



\---



\*Developed as an academic Python project.\*

