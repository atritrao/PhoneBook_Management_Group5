# Installation / Running Guide
Language: Python 3.9 (high 3.13 recommend)

Libraries: pytest, pytest-html, hashlib, json, datetime

Containerization: Docker

Design Tools: Draw.io / StarUML (DFD, Use Case, Class Diagram)

Project Management: GitHub, Excel

## Git code
```bash
git clone https://github.com/atritrao/PhoneBook_Management_Group5.git
```

# Installation & Usage
## Step 1: Run with Docker

# 1. Build the Image: Open Terminal at the project root folder:
```
Bash

docker build -t phonebook-app -f Docker/Dockerfile .
```

## 2. Run the Application:
```
Bash

docker run --rm -it --name my-phonebook phonebook-app
```
(Note: You must use the -it flag to interact with the command-line menu)

# Step 2: Run Locally
## 1. Install Dependencies:
```
Bash

cd SourceCode
pip install -r requirements.txt
```
# 2. Run the App:
```
Bash

python main.py
```

# Testing
The team has implemented 64 Unit Test Cases covering all major functions: Authentication, CRUD, Search, and Group Management.

## Run Automated Tests
To run all test cases using Docker:
```
Bash

docker run --rm phonebook-app pytest
```

ProgAndTest_Group05/
│
├── SourceCode/
│   ├── main.py
│   ├── models.py
│   ├── data.py
│   ├── test_auth_admin.py
│   ├── test_contact_crud.py
│   ├── test_group.py
│   ├── test_search_history.py
│   └── requirements.txt
│
├── Docker/
│   └── Dockerfile
│
├── Docs/
│   ├── Testing_Document.docx
│   ├── TestCases_BugReport.xlsx
│   ├── Task_Assignment_Evidence.xlsx
│   └── Testing_Report.html
│
└── README.md
