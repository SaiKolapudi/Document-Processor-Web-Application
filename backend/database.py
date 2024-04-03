from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["document_processor"]

def save_documents(documents, question):
    for document in documents:
        document["question"] = question
        document["approved"] = False
    db.documents.insert_many(documents)

    db.questions.update_one({"question": question}, {"$set": {"question": question}}, upsert=True)

def get_facts_by_date(question):
    facts_by_day = {}

    for document in db.documents.find({"question": question, "approved": True}):
        date = document["date"]
        if date not in facts_by_day:
            facts_by_day[date] = []
        facts_by_day[date].extend(document["facts"])

    current_date = datetime.now().strftime("%Y-%m-%d")
    previous_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    for date, facts in facts_by_day.items():
        for fact in facts:
            if date == current_date and fact not in facts_by_day.get(previous_date, []):
                fact["added"] = True
            elif date == previous_date and fact not in facts_by_day.get(current_date, []):
                fact["removed"] = True
            else:
                fact["modified"] = True

    return facts_by_day

def update_facts(facts_to_update):
    for fact in facts_to_update:
        db.documents.update_one(
            {"question": fact["question"], "date": fact["date"], "facts.fact": fact["fact"]},
            {"$set": {"facts.$.fact": fact["newFact"]}}
        )

def approve_fact(fact):
    db.documents.update_one(
        {"question": fact["question"], "date": fact["date"], "facts.fact": fact["fact"]},
        {"$set": {"facts.$.approved": True}}
    )

def reject_fact(fact):
    db.documents.delete_one(
        {"question": fact["question"], "date": fact["date"], "facts.fact": fact["fact"]}
    )

def clear_question_and_answers(question):
    db.documents.delete_many({"question": question})
    db.questions.delete_one({"question": question})

def get_suggested_facts(question):
    suggested_facts = []
    for document in db.documents.find({"question": question, "approved": False}):
        suggested_facts.extend(document["facts"])
    return suggested_facts

def get_question():
    question_doc = db.questions.find_one()
    if question_doc:
        return question_doc["question"]
    else:
        return ""