# Document-Processor-Web-Application


## Overview
```
The Document Processor is a web application designed to extract and process information from call logs. Users can input a question and upload call log documents, from which the application will extract relevant facts. It offers features like time navigation, auto-approval of facts, and handling contradictions in the extracted information.
```

## Features
```
- **Question and Answer Screen:** Users can view the extracted facts related to their question. The screen includes a time navigation slider to explore the extracted facts over different days. Changes in facts (added, removed, or modified) are highlighted.
- **Document Addition Screen:** This screen allows for the addition of new call logs via URLs. Users can also set a question for the application to answer based on the uploaded documents.
- **Automatic Fact Processing:** Upon document upload, the application processes the content to extract relevant facts. It handles contradictions and suggests facts to be added, removed, or modified.
- **API Endpoints:** Provides REST API endpoints for submitting questions and documents (`POST /submit_question_and_documents`) and for retrieving the processed facts (`GET /get_question_and_facts`).
```

## Technologies Used
```
- **Flask:** A Python web framework used for building the web application.
- **PyMongo:** A Python tool for interacting with MongoDB, used for data storage and retrieval.
- **OpenAI's GPT:** Utilized for processing documents and extracting relevant facts based on the question provided.
```

## Setup and Installation
```
1. Ensure Python and MongoDB are installed on your system.
2. Install required Python packages using `pip install -r requirements.txt`.
3. Run the application with `python app.py`.
```

## Usage
```
1. Navigate to the Document Addition Screen to add call log documents and set the question.
2. Submit the documents. If auto-approve is checked, all suggestions are automatically approved.
3. Switch to the Question and Answer Screen to view the extracted facts. Use the time slider to navigate through different days.
```

## API Guide
```
- **Submit Question and Documents:**
  - Endpoint: `POST /submit_question_and_documents`
  - Payload:
    ```json
    {
      "question": "Your question here",
      "documents": ["URL1", "URL2"],
      "autoApprove": true
    }
    ```
- **Get Question and Facts:**
  - Endpoint: `GET /get_question_and_facts`
```

## Development Notes
```
- Bring your own LLM API key for document processing.
- The application optimizes for accuracy and handles data consistency across different time points.
```

## Contributing
```
Contributions to the project are welcome. Ensure that any pull requests or issues follow the project's standards and provide sufficient information.
```
