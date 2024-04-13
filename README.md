# Document Processor Web Application

## Overview

The Document Processor is a web application designed to extract and process information from call logs. Users can input a question and upload call log documents, from which the application will extract relevant facts. It offers features like time navigation, auto-approval of facts, and handling contradictions in the extracted information.

## Demo
![Demo Image](Images/Document Processor_1.png)

## Features

- **Question and Answer Screen:** Displays a question and its corresponding answers, extracted from the documents, with a time navigation feature.
- **Document Addition Screen:** Allows adding new call logs and setting a question for processing.
- **Automatic Fact Processing:** Processes uploaded documents to extract relevant facts and handles contradictions.
- **API Endpoints:** Offers REST API for submitting questions/documents and retrieving processed facts.

## Technologies Used

- Flask (Python web framework)
- PyMongo (MongoDB interaction tool)
- OpenAI's GPT (for document processing)

## Setup and Installation

1. Install Python and MongoDB.
2. Use `pip install -r requirements.txt` to install Python packages.
3. Run the application: `python app.py`.

## Usage

1. Navigate to the Document Addition Screen to add call logs and set the question.
2. Submit the documents for processing.
3. View the extracted facts on the Question and Answer Screen.

## API Guide

- `POST /submit_question_and_documents`: Submits a question and document URLs for processing.
- `GET /get_question_and_facts`: Retrieves processed facts related to the submitted question.

## Development Notes

- An LLM API key is required for document processing.
- The application prioritizes accuracy and handles temporal data consistency.

## Contributing

Contributors are encouraged to submit pull requests or issues following project standards.
