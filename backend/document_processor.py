import re
import openai
import json
from database import get_suggested_facts

openai.api_key = "sk-"

def process_documents(document_contents, question, auto_approve):
    suggested_facts = []

    for date, content in document_contents:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that extracts facts from documents based on a given question. Respond with the extracted facts in the specified JSON format without any additional text."
                },
                {
                    "role": "user",
                    "content": f"Extract facts from the following document that are relevant to answering the question: {question}\n\nDocument: {content}\n\nRespond with the extracted facts in the following JSON format:\n{{\"facts\": [{{\"fact\": \"fact 1\", \"approved\": true}}, {{\"fact\": \"fact 2\", \"approved\": true}}, ...]}}"
                }
            ]
        )

        try:
            extracted_facts = json.loads(response.choices[0].message['content'])["facts"]
        except (json.JSONDecodeError, KeyError):
            extracted_facts = []

        suggested_facts_for_date = []
        for fact in extracted_facts:
            fact["date"] = date
            fact["question"] = question
            if auto_approve:
                fact["approved"] = True
            else:
                fact["approved"] = False
            suggested_facts_for_date.append(fact)

        suggested_facts.extend(suggested_facts_for_date)

    return handle_contradictions(suggested_facts, question)

def handle_contradictions(suggested_facts, question):
    existing_facts = get_suggested_facts(question)

    for new_fact in suggested_facts:
        for existing_fact in existing_facts:
            if new_fact["fact"] != existing_fact["fact"] and new_fact["date"] == existing_fact["date"]:
                # Handle contradiction by suggesting modification or removal of the existing fact
                if is_more_accurate(new_fact["fact"], existing_fact["fact"]):
                    existing_fact["newFact"] = new_fact["fact"]
                else:
                    new_fact["approved"] = False
                    break

    suggested_facts.extend(existing_facts)
    return suggested_facts

def is_more_accurate(fact1, fact2):
    # Implement logic to determine which fact is more accurate
    # Return True if fact1 is more accurate than fact2, False otherwise
    return True

def extract_date_from_document_name(document_name):
    date_match = re.search(r"(\d{8})", document_name)
    if date_match:
        date_string = date_match.group(1)
        year = date_string[:4]
        month = date_string[4:6]
        day = date_string[6:]
        return f"{year}-{month}-{day}"
    else:
        return ""