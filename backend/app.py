import re
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from document_processor import process_documents, get_suggested_facts, extract_date_from_document_name
from database import save_documents, get_facts_by_date, update_facts, clear_question_and_answers, get_question, approve_fact, reject_fact
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/document_processor"
mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_question_and_documents", methods=["POST"])
def submit_question_and_documents():
    data = request.get_json()
    question = data.get("question")
    document_urls = data.get("documents")
    auto_approve = data.get("autoApprove", False)

    clear_question_and_answers(question)

    document_contents = []
    for url in document_urls:
        if "github.com" in url:
            # Extract the file content from GitHub URL
            url_parts = url.split("/")
            if len(url_parts) >= 7 and url_parts[5] == "blob":
                repo_owner = url_parts[3]
                repo_name = url_parts[4]
                branch = url_parts[6]
                file_path = "/".join(url_parts[7:])
                raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"
                response = requests.get(raw_url)
            else:
                return jsonify({"status": "error", "message": f"Invalid GitHub URL format: {url}"}), 400
        else:
            response = requests.get(url)

        if response.status_code == 200:
            document_contents.append((extract_date_from_document_name(url), response.text))
        else:
            return jsonify({"status": "error", "message": f"Failed to retrieve document from {url}"}), 400

    try:
        suggested_facts = process_documents(document_contents, question, auto_approve)
        save_documents(suggested_facts, question)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get_question_and_facts", methods=["GET"])
def get_question_and_facts():
    question = get_question()
    facts_by_day = get_facts_by_date(question)

    if facts_by_day:
        return jsonify({"question": question, "factsByDay": facts_by_day, "status": "done"})
    elif facts_by_day == {}:
        return jsonify({"question": question, "factsByDay": {}, "status": "no_facts"})
    else:
        return jsonify({"question": question, "status": "processing"})

@app.route("/get_suggested_facts", methods=["GET"])
def get_suggested_facts_route():
    question = get_question()
    suggested_facts = get_suggested_facts(question)
    return jsonify({"suggestedFacts": suggested_facts})

@app.route("/approve_fact", methods=["POST"])
def approve_fact_route():
    fact = request.get_json()
    approve_fact(fact)
    return jsonify({"status": "success"})

@app.route("/reject_fact", methods=["POST"])
def reject_fact_route():
    fact = request.get_json()
    reject_fact(fact)
    return jsonify({"status": "success"})

@app.route("/clear_question_and_answers", methods=["POST"])
def clear_question_and_answers_route():
    data = request.get_json()
    question = data.get("question")
    clear_question_and_answers(question)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, port=5002)